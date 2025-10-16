"""
Reflection Engine - Agent Self-Evaluation
Enables agents to assess their own progress and decision quality
Based on 2024-2025 research on agentic reflection patterns
"""

from typing import Dict, List, Any
from datetime import datetime


class ReflectionEngine:
    """
    Implements reflection mechanisms for agent self-evaluation
    
    Key capabilities:
    - Progress assessment (is agent making meaningful progress?)
    - Strategy evaluation (is current approach working?)
    - Information gain measurement (are observations providing new info?)
    - Decision quality scoring (are tool choices optimal?)
    
    Based on research:
    - Reflexion: Learning via Self-Feedback (Shinn et al., 2023)
    - ReAct: Reasoning and Acting (Yao et al., 2022)
    - Self-Evaluation techniques (2024-2025)
    """
    
    def __init__(self):
        self.reflection_history = []
    
    def evaluate_progress(
        self, 
        current_iteration: int,
        current_observation: Dict[str, Any],
        previous_observations: List[Dict[str, Any]],
        current_thought: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate if agent is making meaningful progress
        
        Args:
            current_iteration: Current iteration number
            current_observation: Latest tool observation
            previous_observations: All previous observations
            current_thought: Current reasoning state
            
        Returns:
            Reflection result with progress assessment and recommendations
        """
        # Calculate information gain
        info_gain = self._calculate_information_gain(
            current_observation, 
            previous_observations
        )
        
        # Check for repetitive behavior
        is_repetitive = self._detect_repetitive_pattern(previous_observations)
        
        # Evaluate strategy effectiveness
        strategy_score = self._evaluate_strategy(
            current_thought, 
            current_observation,
            current_iteration
        )
        
        # Determine if stuck
        is_stuck = (
            info_gain < 0.2 or  # Low information gain
            is_repetitive or     # Repetitive observations
            strategy_score < 0.3  # Poor strategy effectiveness
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            is_stuck=is_stuck,
            info_gain=info_gain,
            strategy_score=strategy_score,
            current_iteration=current_iteration
        )
        
        reflection = {
            "iteration": current_iteration,
            "timestamp": datetime.now().isoformat(),
            "progress_score": min(info_gain + strategy_score, 1.0),
            "information_gain": info_gain,
            "strategy_effectiveness": strategy_score,
            "is_stuck": is_stuck,
            "is_repetitive": is_repetitive,
            "recommendation": recommendation,
            "should_change_strategy": is_stuck and current_iteration >= 2
        }
        
        self.reflection_history.append(reflection)
        return reflection
    
    def _calculate_information_gain(
        self,
        current_obs: Dict[str, Any],
        previous_obs: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate how much new information current observation provides
        
        Returns value between 0 (no new info) and 1 (completely new info)
        """
        if not previous_obs:
            return 1.0  # First observation always provides new info
        
        # Convert observations to comparable format
        current_data = str(current_obs.get('data', ''))
        
        # Check similarity with previous observations
        similarities = []
        for prev_obs in previous_obs[-3:]:  # Last 3 observations
            prev_data = str(prev_obs.get('data', ''))
            similarity = self._calculate_similarity(current_data, prev_data)
            similarities.append(similarity)
        
        if not similarities:
            return 1.0
        
        # Information gain is inverse of similarity
        # High similarity = low information gain
        avg_similarity = sum(similarities) / len(similarities)
        info_gain = 1.0 - avg_similarity
        
        return max(0.0, min(1.0, info_gain))
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Simple similarity metric based on common words
        
        Returns value between 0 (completely different) and 1 (identical)
        """
        if not text1 or not text2:
            return 0.0
        
        # Simple word-based similarity (production would use embeddings)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _detect_repetitive_pattern(
        self, 
        observations: List[Dict[str, Any]]
    ) -> bool:
        """
        Detect if observations are repetitive (getting same results)
        """
        if len(observations) < 2:
            return False
        
        # Check last 3 observations
        recent = observations[-3:]
        if len(recent) < 2:
            return False
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(recent) - 1):
            data1 = str(recent[i].get('data', ''))
            data2 = str(recent[i + 1].get('data', ''))
            similarity = self._calculate_similarity(data1, data2)
            similarities.append(similarity)
        
        # If average similarity > 0.8, consider repetitive
        avg_similarity = sum(similarities) / len(similarities)
        return avg_similarity > 0.8
    
    def _evaluate_strategy(
        self,
        thought: Dict[str, Any],
        observation: Dict[str, Any],
        iteration: int
    ) -> float:
        """
        Evaluate effectiveness of current strategy
        
        Returns score between 0 (poor) and 1 (excellent)
        """
        score = 0.5  # Neutral starting score
        
        # Positive indicators
        if observation.get('success'):
            score += 0.3
        
        if observation.get('data'):
            score += 0.2
        
        # Negative indicators
        if observation.get('error'):
            score -= 0.3
        
        if iteration > 5:  # Taking too long
            score -= 0.1 * (iteration - 5)
        
        return max(0.0, min(1.0, score))
    
    def _generate_recommendation(
        self,
        is_stuck: bool,
        info_gain: float,
        strategy_score: float,
        current_iteration: int
    ) -> str:
        """
        Generate actionable recommendation for agent
        """
        if is_stuck:
            if info_gain < 0.2:
                return "LOW_INFO_GAIN: Try different tool or conclude investigation"
            elif strategy_score < 0.3:
                return "POOR_STRATEGY: Change approach or seek collaboration"
            else:
                return "STUCK: Consider alternative hypothesis"
        
        if current_iteration >= 7:
            return "LONG_INVESTIGATION: Consider concluding or escalating"
        
        if info_gain > 0.6 and strategy_score > 0.6:
            return "PROGRESSING_WELL: Continue current approach"
        
        return "MODERATE_PROGRESS: Monitor next iteration closely"
    
    def get_overall_assessment(self) -> Dict[str, Any]:
        """
        Get overall assessment of investigation progress
        """
        if not self.reflection_history:
            return {"status": "NO_DATA", "assessment": "No reflections yet"}
        
        recent_reflections = self.reflection_history[-3:]
        
        avg_progress = sum(r['progress_score'] for r in recent_reflections) / len(recent_reflections)
        stuck_count = sum(1 for r in recent_reflections if r['is_stuck'])
        
        if stuck_count >= 2:
            status = "STUCK"
            assessment = "Agent appears stuck - consider alternative approach"
        elif avg_progress > 0.7:
            status = "EXCELLENT"
            assessment = "Making good progress"
        elif avg_progress > 0.4:
            status = "MODERATE"
            assessment = "Some progress, continue monitoring"
        else:
            status = "POOR"
            assessment = "Limited progress - may need intervention"
        
        return {
            "status": status,
            "assessment": assessment,
            "average_progress": avg_progress,
            "stuck_iterations": stuck_count,
            "total_reflections": len(self.reflection_history)
        }
