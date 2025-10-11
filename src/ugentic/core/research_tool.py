# Research Tool for UGENTIC Agents (MCP Client)

import json
import subprocess

class ResearchTool:
    def __init__(self, server_command):
        self.name = "Research Tool (MCP Client)"
        self.description = "Provides advanced research capabilities via an MCP server."
        self.server_command = server_command
        self.process = None
        self._start_server()

    def _start_server(self):
        """Starts the research MCP server."""
        command = self.server_command
        try:
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"{self.name} started with command: {' '.join(command)}")
        except FileNotFoundError:
            print(f"Error: The command '{command[0]}' was not found.")
            self.process = None
        except Exception as e:
            print(f"Error starting research server: {e}")
            self.process = None

    def _send_request(self, method, params):
        """Sends a request to the research MCP server."""
        if not self.process:
            return {"status": "error", "message": "Research server is not running."}

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

    def start_research(self, query):
        return self._send_request("start_research", {"query": query})

    def add_source(self, topicId, title, content, type, url=None, credibility=None, relevance=None, tags=None):
        params = {"topicId": topicId, "title": title, "content": content, "type": type}
        if url:
            params["url"] = url
        if credibility:
            params["credibility"] = credibility
        if relevance:
            params["relevance"] = relevance
        if tags:
            params["tags"] = tags
        return self._send_request("add_source", params)

    def synthesize_findings(self, topicId, synthesis, keyFindings):
        return self._send_request("synthesize_findings", {"topicId": topicId, "synthesis": synthesis, "keyFindings": keyFindings})

    def add_research_questions(self, topicId, questions):
        return self._send_request("add_research_questions", {"topicId": topicId, "questions": questions})

    def get_research_topic(self, topicId):
        return self._send_request("get_research_topic", {"topicId": topicId})

    def list_research_topics(self, status=None):
        params = {}
        if status:
            params["status"] = status
        return self._send_request("list_research_topics", params)

    def analyze_source_credibility(self, topicId):
        return self._send_request("analyze_source_credibility", {"topicId": topicId})

    def search_topics(self, query):
        return self._send_request("search_topics", {"query": query})

    def __del__(self):
        """Stops the research MCP server when the object is deleted."""
        if self.process:
            self.process.terminate()
            print(f"{self.name} stopped.")
