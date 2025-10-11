# Filesystem Tool for UGENTIC Agents (MCP Client)

import json
import time
import subprocess

class FilesystemTool:
    def __init__(self, server_command, allowed_paths):
        self.name = "Filesystem Tool (MCP Client)"
        self.description = "Provides secure access to read from and write to the local file system via an MCP server."
        self.server_command = server_command
        self.allowed_paths = allowed_paths
        self.process = None
        self._start_server()

    def _start_server(self):
        """Starts the filesystem MCP server."""
        command_str = ' '.join(self.server_command + self.allowed_paths)
        try:
            # shell=True is added to ensure executables like 'npx' (which is npx.cmd on Windows) are found via the system's shell.
            self.process = subprocess.Popen(command_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            print(f"{self.name} started with command: {command_str}")
            # Allow server to initialize to prevent race condition on startup
            time.sleep(2)
        except FileNotFoundError:
            print(f"Error: The command '{command[0]}' was not found.")
            print(f"Falling back to direct filesystem access...")
            self.process = None
        except Exception as e:
            print(f"Error starting filesystem server: {e}")
            print(f"Falling back to direct filesystem access...")
            self.process = None

    def _send_request(self, method, params):
        """Sends a request to the filesystem MCP server."""
        if not self.process:
            # Fallback to direct filesystem access
            return self._fallback_filesystem_operation(method, params)

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
    
    def _fallback_filesystem_operation(self, method, params):
        """Direct filesystem operations when MCP server is not available."""
        import os
        
        try:
            if method == "read_file":
                file_path = params["path"]
                if not self._is_path_allowed(file_path):
                    return {"status": "error", "message": "Path not allowed"}
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"status": "success", "content": content}
            
            elif method == "write_file":
                file_path = params["path"]
                content = params["content"]
                if not self._is_path_allowed(file_path):
                    return {"status": "error", "message": "Path not allowed"}
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {"status": "success", "content": "File written successfully"}
            
            elif method == "list_directory":
                dir_path = params["path"]
                if not self._is_path_allowed(dir_path):
                    return {"status": "error", "message": "Path not allowed"}
                
                items = os.listdir(dir_path)
                content = "\n".join(items)
                return {"status": "success", "content": content}
            
            else:
                return {"status": "error", "message": f"Unknown method: {method}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _is_path_allowed(self, path):
        """Check if the path is within allowed directories."""
        import os
        abs_path = os.path.abspath(path)
        for allowed_path in self.allowed_paths:
            if abs_path.startswith(os.path.abspath(allowed_path)):
                return True
        return False

    def read_file(self, file_path):
        """Reads the content of a specified file."""
        return self._send_request("read_file", {"path": file_path})

    def write_file(self, file_path, content):
        """Writes content to a specified file."""
        return self._send_request("write_file", {"path": file_path, "content": content})

    def list_directory(self, dir_path='.'):
        """Lists the contents of a specified directory."""
        return self._send_request("list_directory", {"path": dir_path})

    def __del__(self):
        """Stops the filesystem MCP server when the object is deleted."""
        if self.process:
            self.process.terminate()
            print(f"{self.name} stopped.")

