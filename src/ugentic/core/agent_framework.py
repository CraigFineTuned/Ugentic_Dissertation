"""Main framework for UGENTIC agents"""

import logging
import os
import json
import inspect
from .tool_base import Tool

# Initialize loggers
agent_logger = logging.getLogger("ugentic.agent")
llm_logger = logging.getLogger("ugentic.llm")
tool_logger = logging.getLogger("ugentic.tool")
workflow_logger = logging.getLogger("ugentic.workflow")


from .time_tool import TimeTool
from .rag_core import RAGCore, get_ollama_embeddings, get_text_splitter
from .fetch_tool import FetchTool
from .decision_tool import DecisionTool
from langchain_community.llms import Ollama  # Import Ollama for live LLM interaction





class Agent:
    def __init__(self, name, persona, tools=None, rag_system=None, llm_model=None):
        self.name = name
        self.persona = persona
        self.tools = {tool.name: tool for tool in tools} if tools is not None else {}
        self.rag_system = rag_system
        self.llm_model = llm_model  # Store the LLM model
        self.agent_directory = None # To be populated by the Orchestrator
        agent_logger.info(f"Agent '{self.name}' initialized.", extra={"context": {"agent_name": self.name, "persona": self.persona}})

    def register_peers(self, agent_directory):
        """Registers the directory of all agents for consultation."""
        self.agent_directory = agent_directory

    def consult(self, target_agent_name: str, question: str):
        """Consults a peer agent with a specific question."""
        agent_logger.info(f"Agent '{self.name}' consulting with '{target_agent_name}' about: '{question}'", extra={"context": {"source_agent": self.name, "target_agent": target_agent_name, "question": question}})
        if not self.agent_directory:
            return "Error: Agent directory not registered. Cannot consult peers."
        
        # Prevent an agent from consulting itself
        if target_agent_name == self.name:
            return "Error: An agent cannot consult itself."

        peer_agent = self.agent_directory.get(target_agent_name)
        if not peer_agent:
            return f"Error: Agent '{target_agent_name}' not found in directory."

        print(f"  [{self.name}]: Consulting with {target_agent_name} about: '{question}'")
        # The result of a consultation is the direct result of the peer's task execution
        return peer_agent.execute_task(question)

    def _build_tool_prompt(self):
        """Builds the part of the prompt listing available tools and actions."""
        prompt = "You have the following tools and abilities available:\n"
        
        # Add standard tools
        for tool_name, tool_obj in self.tools.items():
            prompt += f"- {tool_name}: {tool_obj.description}\n"
            # Filter to include only public, callable methods (actions)
            actions = [name for name, method in inspect.getmembers(tool_obj, predicate=inspect.ismethod) if not name.startswith('_')] 
            for action_name in actions:
                # Ensure the method is not an internal attribute like llm_model
                if action_name != "llm_model": # Explicitly exclude llm_model
                    action = getattr(tool_obj, action_name)
                    if callable(action):
                        action_signature = inspect.signature(action)
                        action_params = action_signature.parameters
                        param_details = []
                        for param_name, param in action_params.items():
                            if param_name != 'self':
                                param_details.append(f"{param_name}: {param.annotation if param.annotation != inspect._empty else 'any'}")
                        prompt += f"  - Action: {action_name} (Parameters: {', '.join(param_details)}) (Description: {getattr(tool_obj, action_name).__doc__}) (Returns: dict with status and content/message fields)\n"

        # Add special, built-in abilities
        if self.agent_directory:
            peer_names = [name for name in self.agent_directory.keys() if name != self.name]
            prompt += f"- consult: Ask a peer agent a question to get their expert opinion or data. Use this when you need information from another department. Parameters: target_agent_name: str (must be one of {peer_names}), question: str\n"

        

        # Guidance for FilesystemTool and AnalysisTool
        prompt += "\nIMPORTANT: When using Filesystem Tool or AnalysisTool, only use file paths that are explicitly provided to you, or that you have discovered using list_directory. Do NOT invent file paths. For example, if you need to analyze 'budget.csv', use 'budget.csv' directly if it's listed as available, or first use list_directory to find it. If you need to analyze a CSV, ensure it's a real file you have access to.\n"
        # Dynamically list policy documents using the filesystem tool
        if self.rag_system and hasattr(self.rag_system, 'filesystem_tool'):
            policy_docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'documents', 'policies')
            response = self.rag_system.filesystem_tool.list_directory(policy_docs_path)
            if response["status"] == "success":
                policy_documents = [item[7:] for item in response["contents"] if item.startswith("[FILE]")]
                if policy_documents:
                    prompt += f"\nAvailable Policy Documents (for use with RAG-enabled tools like ResearchTool): {', '.join(policy_documents)}\n"
            else:
                prompt += f"\nCould not list policy documents: {response['message']}\n"
        
        prompt += "\nVERY IMPORTANT: Only use the actions that are explicitly listed for each tool. Do not try to guess action names. For example, the ResearchTool has the action 'perform_web_search', not 'perform_research'. The DecisionTool has the action 'make_choice' which requires the 'options' parameter."

        return prompt

    def _interact_with_llm(self, prompt_text):
        """Interacts with the live LLM to get a response, with robust JSON parsing."""
        if self.llm_model is None:
            return '{"tool": "none", "response": "No LLM configured."}'

        llm_logger.debug(f"Processing prompt: '{prompt_text[:100]}...'", extra={"context": {"agent_name": self.name, "prompt": prompt_text}})

        example_format = {"tool": "tool_name", "action": "action_name", "parameters": {"key": "value"}}
        example_no_tool = {"tool": "none", "response": "Your natural language response here."}

        llm_prompt = f"""YOUR RESPONSE MUST BE ONLY A JSON OBJECT. DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION.\n\nYou are a helpful AI assistant. Your task is to select the best tool and action from the available tools that *most appropriately* fulfills the request: '{prompt_text}'.\n\nWhen using a tool that requires a 'query' parameter, extract the most relevant search query directly from the request: '{prompt_text}'.\n\n{self._build_tool_prompt()}\n\nRespond with ONLY a JSON object in the format: 
{json.dumps(example_format)} 
\nIf no tool is appropriate, respond with: {json.dumps(example_no_tool)}\n"""

        try:
            response = self.llm_model.invoke(llm_prompt)
            llm_logger.debug(f"LLM response: '{response}'", extra={"context": {"agent_name": self.name, "response": response}})
            
            # Use regex to find the JSON block, allowing for surrounding text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                try:
                    # Validate that the extracted string is valid JSON
                    json.loads(json_str)
                    return json_str
                except json.JSONDecodeError as e:
                    llm_logger.error(f"Extracted string is not valid JSON: {json_str}. Error: {e}", extra={"context": {"agent_name": self.name, "error": str(e)}})
                    return f'{{"tool": "none", "response": "LLM returned malformed JSON: {json_str}"}}'
            else:
                llm_logger.warning(f"No JSON object found in LLM response: {response}", extra={"context": {"agent_name": self.name, "response": response}})
                return '{"tool": "none", "response": "No valid action could be determined from the LLM response."}'

        except Exception as e:
            llm_logger.error(f"Error invoking LLM: {e}", extra={"context": {"agent_name": self.name, "error": str(e)}})
            return '{"tool": "none", "response": "Error communicating with LLM."}'

    def retrieve_info_from_rag(self, query, top_k=3):
        """Retrieves information from the RAG system based on a query."""
        agent_logger.info(f"Retrieving info from RAG for query: '{query}'", extra={"context": {"agent_name": self.name, "query": query, "top_k": top_k}})
        if self.rag_system:
            retrieved_chunks = self.rag_system.retrieve(query, top_k=top_k)
            if retrieved_chunks:
                return "\n".join([chunk["chunk_text"] for chunk in retrieved_chunks])
            return "No relevant information found."
        return "RAG system not initialized."

    def execute_task(self, task_description):
        """Executes a given task by reasoning over available tools with an LLM."""
        agent_logger.info(f"Executing task: '{task_description}'", extra={"context": {"agent_name": self.name, "task": task_description}})
        llm_response_str = self._interact_with_llm(task_description)
        
        agent_logger.debug(f"LLM Response String: {llm_response_str}", extra={"context": {"agent_name": self.name, "llm_response": llm_response_str}})
        try:
            decision = json.loads(llm_response_str)
            agent_logger.debug(f"Parsed Decision: {decision}", extra={"context": {"agent_name": self.name, "decision": decision}})
        except json.JSONDecodeError as e:
            error_message = f"Failed to decode LLM response: {llm_response_str}. Error: {e}"
            agent_logger.error(error_message, extra={"context": {"agent_name": self.name, "llm_response": llm_response_str}})
            return f"Error: Invalid JSON response from LLM. The response was: {llm_response_str}"

        tool_name = decision.get("tool")
        agent_logger.debug(f"Tool Name: {tool_name}", extra={"context": {"agent_name": self.name, "tool_name": tool_name}})
        parameters = decision.get("parameters", {})

        if tool_name == "consult":
            tool_logger.info(f"Using tool: {tool_name}", extra={"context": {"agent_name": self.name, "tool_name": tool_name, "parameters": parameters}})
            target_agent = parameters.get("target_agent_name")
            question = parameters.get("question")
            if target_agent and question:
                return self.consult(target_agent, question)
            else:
                return "Error: 'consult' action requires 'target_agent_name' and 'question'."
        
        elif tool_name in self.tools:
            tool_logger.info(f"Using tool: {tool_name}", extra={"context": {"agent_name": self.name, "tool_name": tool_name, "parameters": parameters}})
            tool_to_use = self.tools[tool_name]
            action_name = decision.get("action")

            if action_name is None:
                return f"Error: Tool '{tool_name}' selected, but no action was specified."

            if not hasattr(tool_to_use, action_name) or not callable(getattr(tool_to_use, action_name)):
                available_actions = [method for method in dir(tool_to_use) if callable(getattr(tool_to_use, method)) and not method.startswith("_")]
                return f"Error: Action '{action_name}' not found or not callable on tool '{tool_name}'. Available actions: {', '.join(available_actions)}"

            action = getattr(tool_to_use, action_name)
            expected_params = inspect.signature(action).parameters
            filtered_parameters = {}
            missing_params = []

            for param_name, param_obj in expected_params.items():
                if param_obj.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and param_obj.default == inspect.Parameter.empty:
                    # This is a required parameter
                    if param_name not in parameters:
                        missing_params.append(param_name)
                    else:
                        filtered_parameters[param_name] = parameters[param_name]
                elif param_name in parameters:
                    # This is an optional parameter provided by the LLM
                    filtered_parameters[param_name] = parameters[param_name]

            if missing_params:
                return f"Error: Action '{action_name}' on tool '{tool_name}' is missing required parameters: {', '.join(missing_params)}. Please provide them."
            
            tool_response = action(**filtered_parameters)
            if tool_response["status"] == "success":
                return tool_response["content"]
            else:
                return f"Error executing tool: {tool_response['message']}"
        
        else: # No tool found or tool is 'none'
            agent_logger.info("No tool used.", extra={"context": {"agent_name": self.name}})
            return decision.get("response", "No action taken.")


class Orchestrator(Agent):
    def __init__(self, name, persona, departmental_agents, rag_system=None, tools=None, llm_model=None):
        super().__init__(name, persona, tools=tools, rag_system=rag_system, llm_model=llm_model)
        self.departmental_agents = departmental_agents
        # After all agents are created, register them with each other
        for agent in self.departmental_agents.values():
            agent.register_peers(self.departmental_agents)
        workflow_logger.info("Orchestrator initialized and all agents registered for consultation.", extra={"context": {"orchestrator_name": self.name}})

    def decompose_goal(self, high_level_goal):
        workflow_logger.info(f"Decomposing goal: '{high_level_goal}'", extra={"context": {"orchestrator_name": self.name, "goal": high_level_goal}})

        # Define the JSON schema for the expected output
        json_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "agent": {
                        "type": "string",
                        "description": "Name of the departmental agent (e.g., Marketing, Finance, HR)",
                    },
                    "task": {
                        "type": "string",
                        "description": "Specific task for the agent to perform",
                    },
                },
                "required": ["agent", "task"],
            },
        }

        # Create the example JSON string outside the f-string to avoid syntax errors
        example_data = [
            {"agent": "Marketing", "task": "Research market trends"},
            {"agent": "Finance", "task": "Analyze budget"},
        ]
        example_json = json.dumps(example_data, indent=2)

        # Construct the prompt for the LLM to decompose the goal
        llm_prompt = f"""YOUR RESPONSE MUST BE ONLY A JSON ARRAY. DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION. NO PREAMBLE, NO EXPLANATION, JUST THE JSON.

You are an expert orchestrator. Your task is to decompose the following high-level goal
into a list of smaller, highly specific, and actionable tasks. Each task must be assigned to
ONE relevant departmental agent from the following EXACT list: {', '.join(self.departmental_agents.keys())}.

High-level goal: '{high_level_goal}'

YOUR RESPONSE MUST BE ONLY A JSON ARRAY, WRAPPED IN A 'json' MARKDOWN BLOCK (e.g., ```json...```). DO NOT INCLUDE ANY OTHER TEXT, CONVERSATION, OR EXPLANATION.
The JSON array must conform to the following JSON schema:
'''{json.dumps(json_schema, indent=2)}'''

Example: ```json
{example_json}
```

IMPORTANT: You MUST use agent names ONLY from the provided list. If you are unsure, or if a task seems to fit multiple agents, choose the most appropriate one. Do NOT invent new agent names or misspell existing ones. For example, use 'Operations' not 'Opereations'."""

        try:
            # FIX: Call the LLM directly, bypassing the flawed Agent._interact_with_llm
            llm_logger.debug(f"Processing prompt: '{llm_prompt[:100]}...'", extra={"context": {"orchestrator_name": self.name, "prompt": llm_prompt}})
            llm_response_str = self.llm_model.invoke(llm_prompt)
            llm_logger.debug(f"Raw LLM response for decomposition: '{llm_response_str}'", extra={"context": {"orchestrator_name": self.name, "response": llm_response_str}})

            # --- Robust JSON Parsing ---
            # Clean the string: remove markdown, leading/trailing whitespace
            cleaned_str = llm_response_str.strip()
            if cleaned_str.startswith("```json"):
                cleaned_str = cleaned_str[7:]
            if cleaned_str.endswith("```"):
                cleaned_str = cleaned_str[:-3]

            # Find the start and end of the JSON content
            json_start = cleaned_str.find("[")
            if json_start == -1:
                json_start = cleaned_str.find("{")

            json_end = cleaned_str.rfind("]")
            if json_end == -1:
                json_end = cleaned_str.rfind("}")

            if json_start == -1 or json_end == -1:
                raise json.JSONDecodeError(
                    "No JSON object or array found in response.", cleaned_str, 0
                )

            json_str = cleaned_str[json_start : json_end + 1]

            # If the response is a single JSON object or multiple objects, wrap it in a list
            if not json_str.startswith("["):
                json_str = f"[{json_str}]"

            decomposed_tasks = json.loads(json_str)

            # If the result is a single dictionary that was parsed into a list, ensure it's correct
            if isinstance(decomposed_tasks, dict):
                decomposed_tasks = [decomposed_tasks]

            # Define common agent name misspellings and their corrections
            agent_name_corrections = {
                "Opereations": "Operations",
                "Operation": "Operations",
                "Finace": "Finance",
                "Markting": "Marketing",
                "Sale": "Sales",
                "Human Resources": "HR" # Example for multi-word agent names
            }

            # Apply corrections to agent names
            for task_item in decomposed_tasks:
                if "agent" in task_item and task_item["agent"] in agent_name_corrections:
                    task_item["agent"] = agent_name_corrections[task_item["agent"]]

            # Basic validation of the decomposed tasks against the schema (can be more robust)
            if not isinstance(decomposed_tasks, list):
                raise ValueError("LLM response is not a list.")

            for task_item in decomposed_tasks:
                if (
                    not isinstance(task_item, dict)
                    or "agent" not in task_item
                    or "task" not in task_item
                ):
                    raise ValueError(
                        "Each task item must be an object with 'agent' and 'task'."
                    )
                workflow_logger.info(f"Decomposed goal into {len(decomposed_tasks)} tasks.", extra={"context": {"orchestrator_name": self.name, "tasks": decomposed_tasks}})
            return [
                task
                for task in decomposed_tasks
                if task["agent"] in self.departmental_agents
            ]  # Filter out invalid agents
        except json.JSONDecodeError as e:
            workflow_logger.error(f"Failed to parse LLM response as JSON: {e}", extra={"context": {"orchestrator_name": self.name, "error": str(e), "llm_response": llm_response_str}})
            return [
                {
                    "agent": "HR",
                    "task": f"Error decomposing goal: {high_level_goal}. The system's planning module failed to generate a valid JSON plan.",
                }
            ]
        except ValueError as e:
            workflow_logger.error(f"LLM response validation failed: {e}", extra={"context": {"orchestrator_name": self.name, "error": str(e), "llm_response": llm_response_str}})
            return [
                {
                    "agent": "HR",
                    "task": f"Error decomposing goal: {high_level_goal}. The system's planning module response was invalid.",
                }
            ]
        except Exception as e:
            workflow_logger.error(f"An unexpected error occurred during goal decomposition: {e}", extra={"context": {"orchestrator_name": self.name, "error": str(e)}})
            return [
                {
                    "agent": "HR",
                    "task": f"Unexpected error decomposing goal: {high_level_goal}.",
                }
            ]

    def orchestrate(self, high_level_goal):
        workflow_logger.info(f"Orchestrator received high-level goal: '{high_level_goal}'", extra={"context": {"orchestrator_name": self.name, "goal": high_level_goal}})
        workflow_steps = self.decompose_goal(high_level_goal)
        for step in workflow_steps:
            agent_name = step.get("agent")
            task = step.get("task")
            if agent_name in self.departmental_agents:
                agent = self.departmental_agents[agent_name]
                workflow_logger.info(f"Delegating task '{task}' to {agent_name}.", extra={"context": {"orchestrator_name": self.name, "agent_name": agent_name, "task": task}})
                result = agent.execute_task(task)
                workflow_logger.info(f"Agent {agent_name} completed task with result: {result}", extra={"context": {"orchestrator_name": self.name, "agent_name": agent_name, "result": result}})
            else:
                workflow_logger.warning(f"Agent '{agent_name}' not found.", extra={"context": {"orchestrator_name": self.name, "agent_name": agent_name}})
        workflow_logger.info(f"Goal '{high_level_goal}' orchestration complete.", extra={"context": {"orchestrator_name": self.name, "goal": high_level_goal}})
