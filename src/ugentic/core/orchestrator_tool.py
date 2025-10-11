# Orchestrator Tool for UGENTIC Agents (MCP Client)

import json
import subprocess

class OrchestratorTool:
    def __init__(self, server_command):
        self.name = "Orchestrator Tool (MCP Client)"
        self.description = "Provides advanced task orchestration capabilities via an MCP server."
        self.server_command = server_command
        self.process = None
        self._start_server()

    def _start_server(self):
        """Starts the orchestrator MCP server."""
        command = self.server_command
        try:
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"{self.name} started with command: {' '.join(command)}")
        except FileNotFoundError:
            print(f"Error: The command '{command[0]}' was not found.")
            print(f"Falling back to local orchestrator functionality...")
            self.process = None
        except Exception as e:
            print(f"Error starting orchestrator server: {e}")
            print(f"Falling back to local orchestrator functionality...")
            self.process = None
        
        # Initialize local storage for fallback
        self.workflows = {}
        self.tasks = {}
        self.next_workflow_id = 1
        self.next_task_id = 1

    def _send_request(self, method, params):
        """Sends a request to the orchestrator MCP server."""
        if not self.process:
            # Fallback to local orchestrator functionality
            return self._fallback_orchestrator_operation(method, params)

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        try:
            self.process.stdin.write(json.dumps(request) + '\n')
            self.process.stdin.flush()
            response_str = self.process.stdout.readline()
            response = json.loads(response_str)
            if "result" in response:
                return {"status": "success", "content": response["result"]["content"][0]["text"]}
            elif "error" in response:
                return {"status": "error", "message": response["error"]["message"]}
            else:
                return {"status": "error", "message": "Invalid response from server."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _fallback_orchestrator_operation(self, method, params):
        """Local orchestrator operations when MCP server is not available."""
        import json
        
        try:
            if method == "create_workflow":
                workflow_id = str(self.next_workflow_id)
                self.next_workflow_id += 1
                
                workflow = {
                    "id": workflow_id,
                    "name": params["name"],
                    "description": params["description"],
                    "created": True,
                    "tasks": []
                }
                
                self.workflows[workflow_id] = workflow
                return {"status": "success", "content": json.dumps(workflow)}
            
            elif method == "add_task":
                task_id = str(self.next_task_id)
                self.next_task_id += 1
                
                task = {
                    "id": task_id,
                    "workflowId": params["workflowId"],
                    "title": params["title"],
                    "description": params["description"],
                    "priority": params["priority"],
                    "estimatedDuration": params["estimatedDuration"],
                    "dependencies": params["dependencies"],
                    "tags": params["tags"],
                    "assignee": params.get("assignee"),
                    "status": "created"
                }
                
                self.tasks[task_id] = task
                
                # Add task to workflow if it exists
                workflow_id = params["workflowId"]
                if workflow_id in self.workflows:
                    self.workflows[workflow_id]["tasks"].append(task_id)
                
                return {"status": "success", "content": json.dumps(task)}
            
            else:
                return {"status": "error", "message": f"Unknown method: {method}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_workflow(self, name, description):
        return self._send_request("create_workflow", {"name": name, "description": description})

    def add_task(self, workflowId, title, description, priority, estimatedDuration, dependencies, tags, assignee=None):
        params = {"workflowId": workflowId, "title": title, "description": description, "priority": priority, "estimatedDuration": estimatedDuration, "dependencies": dependencies, "tags": tags}
        if assignee:
            params["assignee"] = assignee
        return self._send_request("add_task", params)

    def update_task_status(self, workflowId, taskId, status, actualDuration=None):
        params = {"workflowId": workflowId, "taskId": taskId, "status": status}
        if actualDuration:
            params["actualDuration"] = actualDuration
        return self._send_request("update_task_status", params)

    def get_next_tasks(self, workflowId):
        return self._send_request("get_next_tasks", {"workflowId": workflowId})

    def add_task_note(self, workflowId, taskId, note):
        return self._send_request("add_task_note", {"workflowId": workflowId, "taskId": taskId, "note": note})

    def get_workflow_status(self, workflowId):
        return self._send_request("get_workflow_status", {"workflowId": workflowId})

    def list_workflows(self, status=None):
        params = {}
        if status:
            params["status"] = status
        return self._send_request("list_workflows", params)

    def analyze_workflow(self, workflowId):
        return self._send_request("analyze_workflow", {"workflowId": workflowId})

    def __del__(self):
        """Stops the orchestrator MCP server when the object is deleted."""
        if self.process:
            self.process.terminate()
            print(f"{self.name} stopped.")
