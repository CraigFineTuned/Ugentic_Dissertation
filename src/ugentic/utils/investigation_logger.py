"""
Investigation Logger - Persistent evidence collection system
Logs all investigations, orchestration events, and system metrics
Session 12 - Component 0 (Critical First Priority)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


class InvestigationLogger:
    """
    Comprehensive logging system for UGENTIC investigations
    
    Creates persistent logs for:
    - Individual investigations (JSON + Markdown)
    - Ubuntu orchestration events
    - Session summaries and metrics
    - Agent performance data
    """
    
    def __init__(self, base_dir: str = "logs"):
        """
        Initialize investigation logger
        
        Args:
            base_dir: Base directory for all logs (default: "logs")
        """
        self.base_dir = Path(base_dir)
        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
        
        # Session-level tracking
        self.investigations = []
        self.orchestrations = []
        self.metrics = {
            'total_investigations': 0,
            'successful_investigations': 0,
            'orchestration_count': 0,
            'agent_usage': {},
            'tool_usage': {},
            'avg_response_time': 0,
            'total_response_time': 0
        }
        
        # Create directory structure
        self._create_directories()
        
        print(f"Investigation Logger initialized: {self.base_dir}")
        print(f"Session ID: {self.session_id}")
    
    def _create_directories(self):
        """Create logs directory structure"""
        dirs = [
            self.base_dir / "investigations",
            self.base_dir / "orchestration",
            self.base_dir / "metrics",
            self.base_dir / "sessions"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _sanitize_filename(self, text: str, max_length: int = 50) -> str:
        """
        Convert text to safe filename
        
        Args:
            text: Original text
            max_length: Maximum filename length
            
        Returns:
            Safe filename string
        """
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace spaces with underscores
        text = re.sub(r'[-\s]+', '_', text)
        # Lowercase
        text = text.lower()
        # Truncate
        text = text[:max_length]
        # Remove trailing underscores
        text = text.rstrip('_')
        
        return text if text else "query"
    
    def start_investigation(self, query: str, agent: str) -> str:
        """
        Start logging a new investigation
        
        Args:
            query: User query
            agent: Assigned agent name
            
        Returns:
            Investigation ID
        """
        timestamp = datetime.now()
        inv_id = f"inv_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        investigation = {
            'investigation_id': inv_id,
            'timestamp_start': timestamp.isoformat(),
            'query': query,
            'agent': agent,
            'iterations': [],
            'collaboration': None,
            'outcome': None,
            'duration_seconds': None,
            'timestamp_end': None
        }
        
        self.investigations.append(investigation)
        self.metrics['total_investigations'] += 1
        self.metrics['agent_usage'][agent] = self.metrics['agent_usage'].get(agent, 0) + 1
        
        return inv_id
    
    def log_iteration(self, inv_id: str, iteration_num: int, 
                     thought: str, action: str, parameters: Dict,
                     observation: Dict, reflection: str):
        """
        Log a ReAct iteration
        
        Args:
            inv_id: Investigation ID
            iteration_num: Iteration number (1-10)
            thought: Agent's thought process
            action: Tool/action selected
            parameters: Action parameters
            observation: Tool execution result
            reflection: Agent's reflection on result
        """
        investigation = self._get_investigation(inv_id)
        if not investigation:
            return
        
        iteration = {
            'iteration': iteration_num,
            'thought': thought,
            'action': action,
            'parameters': parameters,
            'observation': observation,
            'reflection': reflection,
            'timestamp': datetime.now().isoformat()
        }
        
        investigation['iterations'].append(iteration)
        
        # Track tool usage
        if action:
            self.metrics['tool_usage'][action] = self.metrics['tool_usage'].get(action, 0) + 1
    
    def log_collaboration_decision(self, inv_id: str, triggered: bool, 
                                   confidence: float = None, reason: str = None):
        """
        Log collaboration detection decision
        
        Args:
            inv_id: Investigation ID
            triggered: Whether collaboration was triggered
            confidence: Confidence score (0-1)
            reason: Reason for decision
        """
        investigation = self._get_investigation(inv_id)
        if not investigation:
            return
        
        investigation['collaboration'] = {
            'triggered': triggered,
            'confidence': confidence,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
        
        if triggered:
            self.metrics['orchestration_count'] += 1
    
    def log_orchestration(self, collab_id: str, participating_agents: List[str],
                         root_cause: str, solution: str, ubuntu_value: str,
                         knowledge_articles: List[Dict] = None):
        """
        Log Ubuntu orchestration event
        
        Args:
            collab_id: Collaboration ID
            participating_agents: List of participating agent names
            root_cause: Identified root cause
            solution: Proposed solution
            ubuntu_value: Ubuntu philosophy value statement
            knowledge_articles: Retrieved knowledge base articles
        """
        orchestration = {
            'collaboration_id': collab_id,
            'timestamp': datetime.now().isoformat(),
            'participating_agents': participating_agents,
            'root_cause': root_cause,
            'solution': solution,
            'ubuntu_value': ubuntu_value,
            'knowledge_articles': knowledge_articles or []
        }
        
        self.orchestrations.append(orchestration)
        
        # Save orchestration log immediately
        self._save_orchestration(orchestration)
    
    def end_investigation(self, inv_id: str, outcome: str, final_response: str = None):
        """
        Complete an investigation and save logs
        
        Args:
            inv_id: Investigation ID
            outcome: Investigation outcome (e.g., 'success', 'needs_collaboration', 'error')
            final_response: Final response to user
        """
        investigation = self._get_investigation(inv_id)
        if not investigation:
            return
        
        # Calculate duration
        start_time = datetime.fromisoformat(investigation['timestamp_start'])
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        investigation['timestamp_end'] = end_time.isoformat()
        investigation['duration_seconds'] = round(duration, 2)
        investigation['outcome'] = outcome
        investigation['final_response'] = final_response
        
        # Update metrics
        if outcome == 'success':
            self.metrics['successful_investigations'] += 1
        
        self.metrics['total_response_time'] += duration
        if self.metrics['total_investigations'] > 0:
            self.metrics['avg_response_time'] = round(
                self.metrics['total_response_time'] / self.metrics['total_investigations'], 2
            )
        
        # Save investigation logs immediately
        self._save_investigation(investigation)
    
    def _get_investigation(self, inv_id: str) -> Optional[Dict]:
        """Get investigation by ID"""
        for inv in self.investigations:
            if inv['investigation_id'] == inv_id:
                return inv
        print(f"Warning: Investigation {inv_id} not found")
        return None
    
    def _save_investigation(self, investigation: Dict):
        """Save investigation to JSON and Markdown"""
        inv_id = investigation['investigation_id']
        query_slug = self._sanitize_filename(investigation['query'])
        base_filename = f"{inv_id}_{query_slug}"
        
        # Save JSON
        json_path = self.base_dir / "investigations" / f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(investigation, f, indent=2, ensure_ascii=False)
        
        # Save Markdown
        md_path = self.base_dir / "investigations" / f"{base_filename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self._format_investigation_markdown(investigation))
        
        print(f"Investigation saved: {base_filename}")
    
    def _format_investigation_markdown(self, investigation: Dict) -> str:
        """Format investigation as readable Markdown"""
        md = f"# Investigation Report\n\n"
        md += f"**ID:** {investigation['investigation_id']}\n"
        md += f"**Query:** {investigation['query']}\n"
        md += f"**Agent:** {investigation['agent']}\n"
        md += f"**Started:** {investigation['timestamp_start']}\n"
        md += f"**Duration:** {investigation['duration_seconds']} seconds\n"
        md += f"**Outcome:** {investigation['outcome']}\n\n"
        
        # Investigation Process
        md += f"## Investigation Process\n\n"
        for iteration in investigation['iterations']:
            md += f"### Iteration {iteration['iteration']}\n\n"
            md += f"**Thought:** {iteration['thought']}\n\n"
            md += f"**Action:** {iteration['action']}\n"
            md += f"**Parameters:** {json.dumps(iteration['parameters'], indent=2)}\n\n"
            
            if iteration['observation'].get('success'):
                md += f"**Result:** ✅ Success\n"
                if 'data' in iteration['observation']:
                    md += f"```json\n{json.dumps(iteration['observation']['data'], indent=2)}\n```\n\n"
            else:
                md += f"**Result:** ❌ Failed\n"
                md += f"**Error:** {iteration['observation'].get('error', 'Unknown')}\n\n"
            
            md += f"**Reflection:** {iteration['reflection']}\n\n"
        
        # Collaboration
        if investigation.get('collaboration'):
            collab = investigation['collaboration']
            md += f"## Collaboration Decision\n\n"
            md += f"**Triggered:** {'Yes' if collab['triggered'] else 'No'}\n"
            if collab.get('confidence'):
                md += f"**Confidence:** {collab['confidence']:.2f}\n"
            if collab.get('reason'):
                md += f"**Reason:** {collab['reason']}\n"
            md += f"\n"
        
        # Final Response
        if investigation.get('final_response'):
            md += f"## Final Response\n\n"
            md += f"{investigation['final_response']}\n\n"
        
        md += f"---\n"
        md += f"*Generated by UGENTIC Investigation Logger*\n"
        
        return md
    
    def _save_orchestration(self, orchestration: Dict):
        """Save orchestration event to JSON and Markdown"""
        collab_id = orchestration['collaboration_id']
        
        # Save JSON
        json_path = self.base_dir / "orchestration" / f"{collab_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(orchestration, f, indent=2, ensure_ascii=False)
        
        # Save Markdown
        md_path = self.base_dir / "orchestration" / f"{collab_id}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self._format_orchestration_markdown(orchestration))
        
        print(f"Orchestration saved: {collab_id}")
    
    def _format_orchestration_markdown(self, orchestration: Dict) -> str:
        """Format orchestration as readable Markdown"""
        md = f"# Ubuntu Orchestration Event\n\n"
        md += f"**Collaboration ID:** {orchestration['collaboration_id']}\n"
        md += f"**Timestamp:** {orchestration['timestamp']}\n\n"
        
        md += f"## Participating Agents\n\n"
        for agent in orchestration['participating_agents']:
            md += f"- {agent}\n"
        md += f"\n"
        
        md += f"## Root Cause\n\n"
        md += f"{orchestration['root_cause']}\n\n"
        
        md += f"## Solution\n\n"
        md += f"{orchestration['solution']}\n\n"
        
        md += f"## Ubuntu Value\n\n"
        md += f"{orchestration['ubuntu_value']}\n\n"
        
        if orchestration.get('knowledge_articles'):
            md += f"## Knowledge Base Articles\n\n"
            for article in orchestration['knowledge_articles']:
                relevance = article.get('relevance', 0)
                content = article.get('content', 'N/A')
                md += f"- **Relevance:** {relevance:.2f}\n"
                md += f"  {content[:200]}...\n\n"
        
        md += f"---\n"
        md += f"*Generated by UGENTIC Investigation Logger*\n"
        
        return md
    
    def save_session_summary(self):
        """Save complete session summary"""
        session_summary = {
            'session_id': self.session_id,
            'session_start': self.session_start.isoformat(),
            'session_end': datetime.now().isoformat(),
            'metrics': self.metrics,
            'investigation_count': len(self.investigations),
            'orchestration_count': len(self.orchestrations),
            'investigations': [
                {
                    'id': inv['investigation_id'],
                    'query': inv['query'],
                    'agent': inv['agent'],
                    'outcome': inv['outcome'],
                    'duration': inv['duration_seconds']
                }
                for inv in self.investigations
            ]
        }
        
        # Save session JSON
        json_path = self.base_dir / "sessions" / f"session_{self.session_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(session_summary, f, indent=2, ensure_ascii=False)
        
        # Save daily metrics
        date_str = self.session_start.strftime("%Y%m%d")
        metrics_path = self.base_dir / "metrics" / f"daily_summary_{date_str}.json"
        
        # Load existing metrics if available
        if metrics_path.exists():
            with open(metrics_path, 'r', encoding='utf-8') as f:
                daily_metrics = json.load(f)
        else:
            daily_metrics = {
                'date': date_str,
                'sessions': [],
                'total_investigations': 0,
                'total_orchestrations': 0
            }
        
        # Add this session
        daily_metrics['sessions'].append(self.session_id)
        daily_metrics['total_investigations'] += self.metrics['total_investigations']
        daily_metrics['total_orchestrations'] += self.metrics['orchestration_count']
        
        # Save updated metrics
        with open(metrics_path, 'w', encoding='utf-8') as f:
            json.dump(daily_metrics, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"SESSION SUMMARY")
        print(f"{'='*60}")
        print(f"Session ID: {self.session_id}")
        print(f"Total Investigations: {self.metrics['total_investigations']}")
        print(f"Successful: {self.metrics['successful_investigations']}")
        print(f"Orchestrations: {self.metrics['orchestration_count']}")
        print(f"Avg Response Time: {self.metrics['avg_response_time']}s")
        print(f"Logs saved to: {self.base_dir.absolute()}")
        print(f"{'='*60}\n")
    
    def __repr__(self) -> str:
        return f"InvestigationLogger(session={self.session_id}, investigations={len(self.investigations)})"
