# Git Tool for UGENTIC Agents (MCP Client)

import json
import subprocess

class GitTool:
    def __init__(self, server_command, repository_path):
        self.name = "Git Tool (MCP Client)"
        self.description = "Provides git functionality via an MCP server."
        self.server_command = server_command
        self.repository_path = repository_path
        self.process = None
        self._start_server()

    def _start_server(self):
        """Starts the git MCP server."""
        command = self.server_command + ["--repository", self.repository_path]
        try:
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"{self.name} started with command: {' '.join(command)}")
        except FileNotFoundError:
            print(f"Error: The command '{command[0]}' was not found.")
            self.process = None
        except Exception as e:
            print(f"Error starting git server: {e}")
            self.process = None

    def _send_request(self, method, params):
        """Sends a request to the git MCP server."""
        if not self.process:
            return {"status": "error", "message": "Git server is not running."}

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": {"repo_path": self.repository_path, **params},
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

    def git_status(self):
        return self._send_request("git_status", {})

    def git_diff_unstaged(self):
        return self._send_request("git_diff_unstaged", {})

    def git_diff_staged(self):
        return self._send_request("git_diff_staged", {})

    def git_diff(self, target):
        return self._send_request("git_diff", {"target": target})

    def git_commit(self, message):
        return self._send_request("git_commit", {"message": message})

    def git_add(self, files):
        return self._send_request("git_add", {"files": files})

    def git_reset(self):
        return self._send_request("git_reset", {})

    def git_log(self, max_count=10):
        return self._send_request("git_log", {"max_count": max_count})

    def git_create_branch(self, branch_name, base_branch=None):
        params = {"branch_name": branch_name}
        if base_branch:
            params["base_branch"] = base_branch
        return self._send_request("git_create_branch", params)

    def git_checkout(self, branch_name):
        return self._send_request("git_checkout", {"branch_name": branch_name})

    def git_show(self, revision):
        return self._send_request("git_show", {"revision": revision})

    def git_init(self):
        return self._send_request("git_init", {})

    def __del__(self):
        """Stops the git MCP server when the object is deleted."""
        if self.process:
            self.process.terminate()
            print(f"{self.name} stopped.")