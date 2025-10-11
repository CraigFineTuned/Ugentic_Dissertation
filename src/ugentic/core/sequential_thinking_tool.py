# Sequential Thinking Tool for UGENTIC Agents

import json
import re

from langchain_community.llms import Ollama # Import Ollama for live LLM interaction

class SequentialThinkingTool:
    def __init__(self, llm_model=None):
        self.name = "SequentialThinkingTool"
        self.description = "Manages complex, multi-step workflows by decomposing goals into actionable sequences."
        self.llm_model = llm_model

    def _interact_with_llm(self, prompt_text):
        """Interacts with the live LLM to get a response for decomposition."""
        if self.llm_model is None:
            return '{"error": "LLM model not provided."}'

        print(f"  [SequentialThinkingTool LLM]: Processing prompt: '{prompt_text[:100]}...' ")

        try:
            response = self.llm_model.invoke(prompt_text)
            
            # Robust JSON parsing logic (copied from agent_framework.py)
            cleaned_str = response.strip()
            if cleaned_str.startswith("```json"):
                cleaned_str = cleaned_str[7:]
            if cleaned_str.endswith("```"):
                cleaned_str = cleaned_str[:-3]

            json_start = cleaned_str.find("{")
            if json_start == -1:
                json_start = cleaned_str.find("[")

            json_end = cleaned_str.rfind("}")
            if json_end == -1:
                json_end = cleaned_str.rfind("]")

            if json_start == -1 or json_end == -1:
                print(f"  [SequentialThinkingTool LLM]: Could not find JSON object or array in LLM response: {response[:100]}...")
                return "[]"

            json_str = cleaned_str[json_start : json_end + 1]
            json.loads(json_str) # Validate
            return json_str
        except Exception as e:
            print(f"  [SequentialThinkingTool LLM]: Error invoking LLM: {e}")
            return "[]"

    def decompose_goal(self, goal):
        """Decomposes a high-level goal into a sequence of smaller, actionable steps."""
        prompt = f"""
        Decompose the following high-level goal into a sequence of smaller, actionable steps.
        List each step as a numbered item, followed by a concise description of the task and the suggested agent (e.g., Marketing, Finance, HR, Operations, Sales).

        Goal: {goal}

        Example Output:
        1. Step 1: Research market trends (Agent: Marketing)
        2. Step 2: Analyze budget (Agent: Finance)
        """
        response_str = self._interact_with_llm(prompt)
        
        # Parse the natural language response into a structured format
        decomposed_steps = []
        for line in response_str.splitlines():
            line = line.strip()
            if line.startswith(tuple(str(i) + '.' for i in range(1, 100))): # Check for numbered list
                try:
                    # Extract step number, task, and agent
                    parts = line.split(':', 1) # Split only on the first colon
                    step_part = parts[0].strip()
                    task_agent_part = parts[1].strip()

                    step_number = int(step_part.split('.')[0].strip())
                    
                    task_match = re.match(r'(.*?) \(Agent:\s*(.*?)\)', task_agent_part)
                    if task_match:
                        task = task_match.group(1).strip()
                        agent = task_match.group(2).strip()
                        decomposed_steps.append({"step": step_number, "task": task, "agent": agent})
                    else:
                        # Fallback if agent not found in parentheses
                        decomposed_steps.append({"step": step_number, "task": task_agent_part, "agent": "Unknown"})
                except (ValueError, IndexError):
                    # If parsing fails, treat as unstructured text
                    pass
        
        return decomposed_steps

    def execute_sequence(self, sequence_of_tasks):
        """Executes a given sequence of tasks in order."""
        print(f"  [SequentialThinkingTool]: Executing sequence of {len(sequence_of_tasks)} tasks.")
        for task_info in sequence_of_tasks:
            print(f"    - Step {task_info.get('step', '')}: Task '{task_info.get('task', '')}' (Agent: {task_info.get('agent', '')})")
            # In a real system, this would involve delegating to the specified agent/tool
        print(f"  [SequentialThinkingTool]: Sequence execution complete.")
        return {"status": "success", "message": "Sequence executed.", "executed_tasks": len(sequence_of_tasks)}

# Example Usage (for testing)
if __name__ == "__main__":
    seq_tool = SequentialThinkingTool()

    print("\n--- Testing decompose_goal ---")
    goal = "Launch a new product."
    decomposed_steps = seq_tool.decompose_goal(goal)
    print(f"Decomposed Steps: {decomposed_steps}")

    print("\n--- Testing execute_sequence ---")
    if decomposed_steps:
        seq_tool.execute_sequence(decomposed_steps)
    else:
        print("No steps to execute.")