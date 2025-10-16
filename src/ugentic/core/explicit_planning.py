"""
Explicit Planning Engine - Deep Agents Architecture Pillar #1
Structured investigation planning for UGENTIC agents

Based on Deep Agents 2.0 (Phil Schmid, 2024):
- Agents create explicit plans before investigation
- Plans track objectives, steps, status, blockers
- Enables plan referencing during investigation
- Supports plan updates with findings
- Provides progress checking

This completes the Deep Agents architecture requirements.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging


class ExplicitPlanner:
    """
    Deep Agents Pillar #1: Explicit Planning
    
    Creates structured investigation plans that agents can:
    - Create before starting work
    - Reference during investigation  
    - Update with findings
    - Check for completion status
    
    Plans are stored as JSON files in plans/ directory for:
    - Persistence across sessions
    - Easy inspection and debugging
    - Evidence collection for dissertation
    """
    
    def __init__(self, plans_directory: str = "plans/", llm=None):
        """
        Initialize Explicit Planner
        
        Args:
            plans_directory: Directory to store plan files
            llm: Optional LLM for intelligent plan generation
        """
        self.plans_dir = Path(plans_directory)
        self.plans_dir.mkdir(exist_ok=True)
        self.llm = llm
        
        logging.info(f"📋 ExplicitPlanner initialized")
        logging.info(f"   Plans directory: {self.plans_dir.absolute()}")
    
    def create_plan(self, 
                    objective: str, 
                    agent_name: str, 
                    problem_context: Dict[str, Any]) -> str:
        """
        Create structured investigation plan
        
        Args:
            objective: Main investigation objective
            agent_name: Agent creating the plan
            problem_context: Context information about the problem
            
        Returns:
            plan_id: Unique identifier for the plan
        """
        # Generate unique plan ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_id = f"{agent_name.replace(' ', '_')}_{timestamp}"
        
        # Generate investigation steps
        steps = self._generate_initial_steps(objective, problem_context)
        
        # Create plan structure
        plan = {
            "plan_id": plan_id,
            "objective": objective,
            "created_by": agent_name,
            "created_at": datetime.now().isoformat(),
            "problem_context": problem_context,
            "steps": steps,
            "status": "active",
            "blockers": [],
            "findings": {},
            "updated_at": datetime.now().isoformat(),
            "completion_percentage": 0
        }
        
        # Save plan to file
        self._write_plan(plan_id, plan)
        
        logging.info(f"📋 Created investigation plan: {plan_id}")
        logging.info(f"   Objective: {objective}")
        logging.info(f"   Steps: {len(steps)}")
        
        return plan_id
    
    def _generate_initial_steps(self, 
                                objective: str, 
                                context: Dict) -> List[Dict]:
        """
        Generate logical investigation steps
        
        Uses LLM if available, otherwise creates structured steps
        based on problem type heuristics.
        
        Args:
            objective: Investigation objective
            context: Problem context
            
        Returns:
            List of investigation steps
        """
        # If LLM available, use it for intelligent step generation
        if self.llm:
            return self._llm_generate_steps(objective, context)
        
        # Otherwise, use heuristic-based step generation
        return self._heuristic_generate_steps(objective, context)
    
    def _heuristic_generate_steps(self, 
                                  objective: str, 
                                  context: Dict) -> List[Dict]:
        """
        Heuristic-based step generation
        
        Creates logical investigation steps based on:
        - Problem type (connectivity, performance, access, error)
        - Agent role
        - Context clues
        """
        steps = []
        
        # Step 1: Always gather initial information
        steps.append({
            "step_number": 1,
            "description": "Gather initial information about the issue",
            "status": "pending",
            "reasoning": "Need baseline understanding before diagnosis",
            "expected_tools": ["check_system_logs", "gather_user_info"],
            "findings": "",
            "updated_at": None
        })
        
        # Step 2: Identify likely causes based on problem type
        problem_lower = objective.lower()
        
        if any(word in problem_lower for word in ['connect', 'network', 'access']):
            steps.append({
                "step_number": 2,
                "description": "Check connectivity and network status",
                "status": "pending",
                "reasoning": "Connectivity issues require network diagnostics",
                "expected_tools": ["ping_test", "check_network_config"],
                "findings": "",
                "updated_at": None
            })
        elif any(word in problem_lower for word in ['slow', 'performance', 'lag']):
            steps.append({
                "step_number": 2,
                "description": "Analyze system performance metrics",
                "status": "pending",
                "reasoning": "Performance issues require resource analysis",
                "expected_tools": ["check_cpu_usage", "check_memory"],
                "findings": "",
                "updated_at": None
            })
        elif any(word in problem_lower for word in ['error', 'crash', 'fail']):
            steps.append({
                "step_number": 2,
                "description": "Investigate error logs and messages",
                "status": "pending",
                "reasoning": "Errors typically leave traces in logs",
                "expected_tools": ["check_error_logs", "analyze_stack_trace"],
                "findings": "",
                "updated_at": None
            })
        else:
            # Generic diagnostic step
            steps.append({
                "step_number": 2,
                "description": "Perform diagnostic checks",
                "status": "pending",
                "reasoning": "Need to identify root cause",
                "expected_tools": ["run_diagnostics"],
                "findings": "",
                "updated_at": None
            })
        
        # Step 3: Test hypothesis
        steps.append({
            "step_number": 3,
            "description": "Test hypothesis and verify root cause",
            "status": "pending",
            "reasoning": "Confirm diagnosis before applying solution",
            "expected_tools": ["test_hypothesis"],
            "findings": "",
            "updated_at": None
        })
        
        # Step 4: Apply solution
        steps.append({
            "step_number": 4,
            "description": "Apply solution and verify resolution",
            "status": "pending",
            "reasoning": "Fix issue and confirm it's resolved",
            "expected_tools": ["apply_fix", "verify_resolution"],
            "findings": "",
            "updated_at": None
        })
        
        # Step 5: Document
        steps.append({
            "step_number": 5,
            "description": "Document solution and close investigation",
            "status": "pending",
            "reasoning": "Create knowledge for future similar issues",
            "expected_tools": ["document_solution"],
            "findings": "",
            "updated_at": None
        })
        
        return steps
    
    def _llm_generate_steps(self, objective: str, context: Dict) -> List[Dict]:
        """
        LLM-based step generation (placeholder for future enhancement)
        
        Would use LLM to generate more intelligent, context-aware steps
        """
        # TODO: Implement LLM-based step generation
        # For now, fall back to heuristics
        return self._heuristic_generate_steps(objective, context)
    
    def update_step(self, 
                   plan_id: str, 
                   step_number: int, 
                   status: str, 
                   findings: str,
                   tools_used: List[str] = None):
        """
        Update step progress
        
        Args:
            plan_id: Plan identifier
            step_number: Step number to update
            status: New status (pending/in_progress/completed/failed/blocked)
            findings: What was discovered
            tools_used: List of tools actually used (optional)
        """
        plan = self._read_plan(plan_id)
        
        # Find and update step
        for step in plan["steps"]:
            if step["step_number"] == step_number:
                step["status"] = status
                step["findings"] = findings
                step["updated_at"] = datetime.now().isoformat()
                if tools_used:
                    step["actual_tools"] = tools_used
                break
        
        # Update overall plan status
        plan["updated_at"] = datetime.now().isoformat()
        plan["completion_percentage"] = self._calculate_completion(plan)
        
        # If all steps complete, mark plan complete
        all_complete = all(s["status"] == "completed" for s in plan["steps"])
        if all_complete:
            plan["status"] = "completed"
            logging.info(f"✅ Plan {plan_id} COMPLETED")
        
        # Save updated plan
        self._write_plan(plan_id, plan)
        
        logging.debug(f"📝 Updated plan {plan_id} step {step_number}: {status}")
    
    def add_blocker(self, plan_id: str, blocker_description: str):
        """
        Add blocker to plan
        
        Args:
            plan_id: Plan identifier
            blocker_description: Description of the blocker
        """
        plan = self._read_plan(plan_id)
        
        blocker = {
            "description": blocker_description,
            "added_at": datetime.now().isoformat()
        }
        plan["blockers"].append(blocker)
        plan["updated_at"] = datetime.now().isoformat()
        
        self._write_plan(plan_id, plan)
        logging.warning(f"⚠️ Blocker added to plan {plan_id}: {blocker_description}")
    
    def check_progress(self, plan_id: str) -> Dict:
        """
        Get current plan status
        
        Args:
            plan_id: Plan identifier
            
        Returns:
            Dictionary with plan progress information
        """
        plan = self._read_plan(plan_id)
        
        # Calculate progress metrics
        total_steps = len(plan["steps"])
        completed_steps = sum(1 for step in plan["steps"] if step["status"] == "completed")
        in_progress_steps = sum(1 for step in plan["steps"] if step["status"] == "in_progress")
        
        # Get next pending step
        next_step = self._get_next_step(plan)
        
        return {
            "plan_id": plan_id,
            "objective": plan["objective"],
            "status": plan["status"],
            "progress": f"{completed_steps}/{total_steps}",
            "completion_percentage": plan["completion_percentage"],
            "completed_steps": completed_steps,
            "in_progress_steps": in_progress_steps,
            "pending_steps": total_steps - completed_steps - in_progress_steps,
            "next_step": next_step,
            "blockers": plan["blockers"],
            "updated_at": plan["updated_at"]
        }
    
    def _get_next_step(self, plan: Dict) -> Optional[Dict]:
        """Get next pending step"""
        for step in plan["steps"]:
            if step["status"] == "pending":
                return {
                    "step_number": step["step_number"],
                    "description": step["description"],
                    "reasoning": step["reasoning"]
                }
        return None
    
    def _calculate_completion(self, plan: Dict) -> int:
        """Calculate completion percentage"""
        total = len(plan["steps"])
        completed = sum(1 for step in plan["steps"] if step["status"] == "completed")
        return int((completed / total) * 100) if total > 0 else 0
    
    def get_plan(self, plan_id: str) -> Dict:
        """Get complete plan details"""
        return self._read_plan(plan_id)
    
    def list_active_plans(self, agent_name: Optional[str] = None) -> List[Dict]:
        """
        List all active plans
        
        Args:
            agent_name: Optional filter by agent name
            
        Returns:
            List of active plan summaries
        """
        active_plans = []
        
        for plan_file in self.plans_dir.glob("*.json"):
            try:
                plan = self._read_plan(plan_file.stem)
                if plan["status"] == "active":
                    if agent_name is None or plan["created_by"] == agent_name:
                        active_plans.append({
                            "plan_id": plan["plan_id"],
                            "objective": plan["objective"],
                            "created_by": plan["created_by"],
                            "created_at": plan["created_at"],
                            "completion_percentage": plan["completion_percentage"]
                        })
            except Exception as e:
                logging.error(f"Error reading plan {plan_file}: {e}")
        
        return active_plans
    
    # File I/O operations
    
    def _write_plan(self, plan_id: str, plan: Dict):
        """Write plan to JSON file"""
        plan_file = self.plans_dir / f"{plan_id}.json"
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
    
    def _read_plan(self, plan_id: str) -> Dict:
        """Read plan from JSON file"""
        plan_file = self.plans_dir / f"{plan_id}.json"
        
        if not plan_file.exists():
            raise FileNotFoundError(f"Plan {plan_id} not found")
        
        with open(plan_file, 'r') as f:
            return json.load(f)
