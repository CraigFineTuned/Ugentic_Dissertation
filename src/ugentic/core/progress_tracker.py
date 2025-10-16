"""
Progress Tracker - Monitor Agent Investigation Progress
Detects when agent is stuck, making progress, or ready to conclude
Based on 2024-2025 research on agent monitoring and evaluation
"""

import math
from typing import Dict, List, Any
from collections import Counter
from datetime import datetime


class ProgressTracker:
    """
    Tracks and analyzes agent progress during investigation
    
    Key capabilities:
    - Tool usage diversity monitoring
    - Progress velocity calculation
    - Stuck state detection
    - Optimal conclusion timing
    
    Based on research:
    - Agent monitoring best practices (2024-2025)
    - Tool selection intelligence (Anthropic, 2024)
    - Error identification mechanisms (2025)
    """
    
    def __init__(self, diversity_threshold: float = 0.5):
        """
        Initialize progress tracker
        
        Args:
            diversity_threshold: Minimum tool diversity score (0-1)
        """
        self.tool_usage: List[str] = []
        self.observation_history: List[Dict] = []
        self.diversity_threshold = diversity_threshold
        self.progress_markers = []
    
    def record_tool_usage(self, tool_name: str, iteration: int):
        """Record tool usage for diversity analysis"""
        self.tool_usage.append(tool_name)
        self.progress_markers.append({
            "iteration": iteration,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat()
        })
    
    def record_observation(self, observation: Dict[str, Any], iteration: int):
        """Record observation for progress analysis"""
        self.observation_history.append({
            "iteration": iteration,
            "observation": observation,
            "timestamp": datetime.now().isoformat()
        })
    
    def calculate_tool_diversity(self) -> float:
        """
        Calculate tool usage diversity score
        
        Returns value between 0 (no diversity, same tool) and 1 (perfect diversity)
        
        Based on Shannon entropy normalized to [0,1]
        """
        if not self.tool_usage:
            return 1.0
        
        # Count tool usage
        tool_counts = Counter(self.tool_usage)
        total_uses = len(self.tool_usage)
        
        # Calculate Shannon entropy (FIXED Session 22: corrected formula)
        entropy = 0.0
        for count in tool_counts.values():
            probability = count / total_uses
            if probability > 0:
                entropy -= probability * math.log2(probability)  # Correct Shannon entropy
        
        # Normalize to [0, 1]
        # Perfect diversity (all tools used equally) = 1.0
        # No diversity (same tool) = 0.0
        unique_tools = len(tool_counts)
        if unique_tools == 1:
            return 0.0
        
        # Maximum entropy: when all tools used equally
        max_entropy = math.log2(unique_tools)
        diversity_score = entropy / max_entropy if max_entropy > 0 else 0.0
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, diversity_score))
    
    def is_tool_diversity_low(self) -> bool:
        """Check if tool diversity is below threshold"""
        if len(self.tool_usage) < 3:
            return False  # Not enough data
        
        diversity = self.calculate_tool_diversity()
        return diversity < self.diversity_threshold
    
    def get_tool_usage_summary(self) -> Dict[str, Any]:
        """Get summary of tool usage patterns"""
        if not self.tool_usage:
            return {
                "total_calls": 0,
                "unique_tools": 0,
                "diversity_score": 1.0,
                "most_used_tool": None,
                "tool_distribution": {}
            }
        
        tool_counts = Counter(self.tool_usage)
        most_common = tool_counts.most_common(1)[0]
        
        return {
            "total_calls": len(self.tool_usage),
            "unique_tools": len(tool_counts),
            "diversity_score": self.calculate_tool_diversity(),
            "most_used_tool": most_common[0],
            "most_used_count": most_common[1],
            "tool_distribution": dict(tool_counts),
            "diversity_assessment": "LOW" if self.is_tool_diversity_low() else "GOOD"
        }
    
    def suggest_alternative_tools(
        self, 
        available_tools: List[str]
    ) -> List[str]:
        """
        Suggest alternative tools to improve diversity
        
        Args:
            available_tools: List of all available tool names
            
        Returns:
            List of suggested tools (least recently used)
        """
        if not available_tools:
            return []
        
        # Count tool usage
        tool_counts = Counter(self.tool_usage)
        
        # Find tools not used or used least
        unused_tools = [t for t in available_tools if t not in tool_counts]
        if unused_tools:
            return unused_tools[:3]  # Top 3 unused
        
        # Return least used tools
        least_used = sorted(
            available_tools,
            key=lambda t: tool_counts.get(t, 0)
        )
        
        return least_used[:3]
    
    def calculate_progress_velocity(self) -> float:
        """
        Calculate how fast agent is making progress
        
        Returns value representing progress rate:
        - > 0.7: Fast progress
        - 0.4 - 0.7: Moderate progress
        - < 0.4: Slow progress
        """
        if len(self.observation_history) < 2:
            return 0.5  # Neutral for insufficient data
        
        # Analyze last 3 observations
        recent_obs = self.observation_history[-3:]
        
        success_count = sum(
            1 for obs in recent_obs 
            if obs['observation'].get('success', False)
        )
        
        error_count = sum(
            1 for obs in recent_obs
            if obs['observation'].get('error', False)
        )
        
        # Calculate velocity score
        velocity = 0.5  # Neutral baseline
        
        # Positive factors
        velocity += (success_count / len(recent_obs)) * 0.5
        
        # Negative factors
        velocity -= (error_count / len(recent_obs)) * 0.3
        
        return max(0.0, min(1.0, velocity))
    
    def is_making_progress(self) -> bool:
        """Determine if agent is making meaningful progress"""
        if len(self.observation_history) < 2:
            return True  # Assume progress early on
        
        velocity = self.calculate_progress_velocity()
        return velocity >= 0.4
    
    def should_conclude_investigation(
        self,
        current_iteration: int,
        max_iterations: int
    ) -> tuple[bool, str]:
        """
        Determine if investigation should conclude
        
        Returns:
            (should_conclude: bool, reason: str)
        """
        # Approaching max iterations
        if current_iteration >= max_iterations - 1:
            return True, "MAX_ITERATIONS_REACHED"
        
        # Low tool diversity and slow progress
        if self.is_tool_diversity_low() and not self.is_making_progress():
            return True, "LOW_DIVERSITY_AND_SLOW_PROGRESS"
        
        # Stuck in pattern
        if (len(self.tool_usage) >= 5 and 
            self.calculate_tool_diversity() < 0.3):
            return True, "STUCK_IN_TOOL_PATTERN"
        
        # Many iterations with poor progress
        if (current_iteration >= max_iterations * 0.7 and 
            self.calculate_progress_velocity() < 0.3):
            return True, "EXTENDED_POOR_PROGRESS"
        
        return False, "CONTINUE"
    
    def get_progress_report(self, current_iteration: int) -> Dict[str, Any]:
        """
        Generate comprehensive progress report
        """
        tool_summary = self.get_tool_usage_summary()
        velocity = self.calculate_progress_velocity()
        making_progress = self.is_making_progress()
        
        # Determine status
        if velocity > 0.7:
            status = "EXCELLENT"
            status_desc = "Making fast progress"
        elif velocity > 0.4:
            status = "MODERATE"
            status_desc = "Making steady progress"
        else:
            status = "SLOW"
            status_desc = "Limited progress detected"
        
        return {
            "iteration": current_iteration,
            "status": status,
            "status_description": status_desc,
            "progress_velocity": velocity,
            "is_making_progress": making_progress,
            "tool_diversity": tool_summary['diversity_score'],
            "tool_diversity_assessment": tool_summary['diversity_assessment'],
            "total_tool_calls": tool_summary['total_calls'],
            "unique_tools_used": tool_summary['unique_tools'],
            "most_used_tool": tool_summary.get('most_used_tool'),
            "observations_recorded": len(self.observation_history),
            "timestamp": datetime.now().isoformat()
        }
    
    def reset(self):
        """Reset tracker for new investigation"""
        self.tool_usage = []
        self.observation_history = []
        self.progress_markers = []
