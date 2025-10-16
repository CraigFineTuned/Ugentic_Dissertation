"""
Pure Python Agent Memory System for UGENTIC
JSON-based storage with semantic similarity for cross-session learning

This module provides:
- Investigation storage and retrieval
- Similar problem matching (semantic embeddings or text-based fallback)
- Ubuntu collaboration tracking
- Agent learning metrics

Dependencies: Optional embeddings model for semantic similarity

Author: Claude + Craig Vraagom
Date: October 14, 2025 (Updated: October 15, 2025)
Version: 2.1 (Semantic Similarity Enhancement)
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import shutil


class AgentMemory:
    """
    Pure Python memory system using JSON storage.
    
    Features:
        - Store investigation history
        - Recall similar problems
        - Track Ubuntu collaboration effectiveness
        - Monitor agent learning over time
    
    Storage:
        data/memory/investigations.json - All investigation records
        data/memory/metadata.json - Session metadata
    
    Example Usage:
        memory = AgentMemory()
        
        # Store investigation
        memory.store_investigation(
            investigation_id="inv_20251014_120000",
            agent_name="Infrastructure",
            problem="Cannot access shared drive",
            root_cause="DNS misconfiguration",
            solution="Updated DNS server IP",
            success=True
        )
        
        # Recall similar problems
        similar = memory.recall_similar_problem("Cannot access shared drive")
        
        # Get Ubuntu stats
        stats = memory.get_ubuntu_collaboration_stats()
    """
    
    def __init__(self, storage_dir: str = "data/memory", embeddings_model=None):
        """
        Initialize Agent Memory system.
        
        Args:
            storage_dir: Directory for JSON storage (default: data/memory)
            embeddings_model: Optional embeddings model for semantic similarity
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Store embeddings model for semantic similarity
        self.embeddings = embeddings_model
        
        # Create backups directory
        self.backup_dir = self.storage_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self.investigations_file = self.storage_dir / "investigations.json"
        self.metadata_file = self.storage_dir / "metadata.json"
        
        # Load existing data
        self.investigations = self._load_investigations()
        self.metadata = self._load_metadata()
        
        print(f"[AgentMemory] Initialized with storage: {self.storage_dir}")
        print(f"[AgentMemory] Loaded {len(self.investigations)} investigation(s)")
    
    def _load_investigations(self) -> List[Dict]:
        """Load investigations from JSON file."""
        if self.investigations_file.exists():
            try:
                with open(self.investigations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[AgentMemory] Warning: Could not parse investigations.json, starting fresh")
                return []
        return []
    
    def _save_investigations(self):
        """Save investigations to JSON file with backup."""
        # Create backup first
        if self.investigations_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"investigations_backup_{timestamp}.json"
            shutil.copy2(self.investigations_file, backup_file)
            
            # Keep only last 10 backups
            backups = sorted(self.backup_dir.glob("investigations_backup_*.json"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
        
        # Save current data
        with open(self.investigations_file, 'w', encoding='utf-8') as f:
            json.dump(self.investigations, f, indent=2, ensure_ascii=False)
    
    def _load_metadata(self) -> Dict:
        """Load metadata from JSON file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_metadata(self):
        """Save metadata to JSON file."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
    
    def start(self) -> bool:
        """
        Start memory system (compatibility method).
        
        Pure Python version is always ready, no startup needed.
        Returns True immediately.
        """
        print("[AgentMemory] ✅ Memory system ready (Pure Python)")
        return True
    
    def stop(self):
        """
        Stop memory system (compatibility method).
        
        Pure Python version has no background processes to stop.
        """
        print("[AgentMemory] Memory system stopped")
    
    # ===== HIGH-LEVEL MEMORY METHODS =====
    
    def store_investigation(
        self,
        investigation_id: str,
        agent_name: str,
        problem: str,
        root_cause: Optional[str] = None,
        solution: Optional[str] = None,
        actions_taken: Optional[List[str]] = None,
        ubuntu_collaboration: bool = False,
        collaborating_agents: Optional[List[str]] = None,
        success: bool = True,
        iterations: int = 0,
        timestamp: Optional[str] = None
    ) -> bool:
        """
        Store a complete investigation in memory.
        
        Args:
            investigation_id: Unique investigation identifier
            agent_name: Primary agent conducting investigation
            problem: Problem description
            root_cause: Identified root cause (if found)
            solution: Applied solution (if found)
            actions_taken: List of actions taken during investigation
            ubuntu_collaboration: Whether Ubuntu orchestration was used
            collaborating_agents: Other agents involved
            success: Whether investigation was successful
            iterations: Number of iterations taken
            timestamp: Investigation timestamp
        
        Returns:
            True if stored successfully
        """
        try:
            # Create investigation record
            investigation = {
                "id": investigation_id,
                "timestamp": timestamp or datetime.now().isoformat(),
                "agent": agent_name,
                "problem": problem,
                "root_cause": root_cause,
                "solution": solution,
                "actions_taken": actions_taken or [],
                "ubuntu_collaboration": ubuntu_collaboration,
                "collaborating_agents": collaborating_agents or [],
                "success": success,
                "iterations": iterations,
                "category": self._categorize_problem(problem)
            }
            
            # Add to investigations list
            self.investigations.append(investigation)
            
            # Save to disk
            self._save_investigations()
            
            # Update metadata
            self.metadata["last_updated"] = datetime.now().isoformat()
            self.metadata["total_investigations"] = len(self.investigations)
            self._save_metadata()
            
            print(f"[AgentMemory] ✅ Stored investigation: {investigation_id}")
            return True
            
        except Exception as e:
            print(f"[AgentMemory] Error storing investigation: {e}")
            return False
    
    def recall_similar_problem(self, problem: str, limit: int = 5) -> List[Dict]:
        """
        Find similar past problems using semantic similarity (if embeddings available)
        or text matching (fallback).
        
        Args:
            problem: Current problem description
            limit: Maximum number of similar problems to return
        
        Returns:
            List of similar investigations with solutions
        """
        try:
            if not self.investigations:
                return []
            
            scored_investigations = []
            
            # Use semantic similarity if embeddings available
            if self.embeddings:
                print(f"[AgentMemory] Using semantic similarity (embeddings)")
                for inv in self.investigations:
                    # Calculate semantic similarity
                    similarity = self._calculate_semantic_similarity(
                        problem, 
                        inv["problem"]
                    )
                    
                    # Boost score if same category
                    if inv["category"] == self._categorize_problem(problem):
                        similarity = min(similarity * 1.2, 1.0)  # Cap at 1.0
                    
                    if similarity > 0.3:  # Threshold for semantic match
                        scored_investigations.append({
                            "investigation_id": inv["id"],
                            "problem": inv["problem"],
                            "agent": inv["agent"],
                            "root_cause": inv["root_cause"],
                            "solution": inv["solution"],
                            "success": inv["success"],
                            "iterations": inv["iterations"],
                            "timestamp": inv["timestamp"],
                            "similarity": similarity
                        })
            
            else:
                # Fallback to text matching
                print(f"[AgentMemory] Using text matching (no embeddings)")
                problem_lower = problem.lower()
                problem_words = set(problem_lower.split())
                
                for inv in self.investigations:
                    inv_problem_lower = inv["problem"].lower()
                    inv_words = set(inv_problem_lower.split())
                    
                    # Calculate Jaccard similarity
                    intersection = problem_words & inv_words
                    union = problem_words | inv_words
                    similarity = len(intersection) / len(union) if union else 0
                    
                    # Boost score if same category
                    if inv["category"] == self._categorize_problem(problem):
                        similarity *= 1.5
                    
                    if similarity > 0:
                        scored_investigations.append({
                            "investigation_id": inv["id"],
                            "problem": inv["problem"],
                            "agent": inv["agent"],
                            "root_cause": inv["root_cause"],
                            "solution": inv["solution"],
                            "success": inv["success"],
                            "iterations": inv["iterations"],
                            "timestamp": inv["timestamp"],
                            "similarity": similarity
                        })
            
            # Sort by similarity and return top N
            scored_investigations.sort(key=lambda x: x["similarity"], reverse=True)
            similar = scored_investigations[:limit]
            
            if similar:
                method = "semantic" if self.embeddings else "text"
                print(f"[AgentMemory] Found {len(similar)} similar investigation(s) using {method} matching")
            
            return similar
            
        except Exception as e:
            print(f"[AgentMemory] Error recalling similar problems: {e}")
            return []
    
    def get_investigation_solution(self, investigation_id: str) -> Optional[Dict]:
        """
        Get the solution used in a past investigation.
        
        Args:
            investigation_id: Investigation identifier
        
        Returns:
            Solution details or None
        """
        try:
            for inv in self.investigations:
                if inv["id"] == investigation_id:
                    if inv["solution"]:
                        return {
                            "investigation_id": investigation_id,
                            "solution": inv["solution"],
                            "root_cause": inv["root_cause"],
                            "success": inv["success"]
                        }
            return None
            
        except Exception as e:
            print(f"[AgentMemory] Error getting solution: {e}")
            return None
    
    def get_ubuntu_collaboration_stats(self) -> Dict:
        """
        Get statistics on Ubuntu collaboration effectiveness.
        
        Returns:
            Dict with collaboration metrics
        """
        try:
            if not self.investigations:
                return {
                    "total_investigations": 0,
                    "ubuntu_investigations": 0,
                    "solo_investigations": 0,
                    "ubuntu_success_rate": 0.0,
                    "solo_success_rate": 0.0,
                    "ubuntu_advantage": 0.0
                }
            
            # Count investigations
            total = len(self.investigations)
            ubuntu_invs = [inv for inv in self.investigations if inv["ubuntu_collaboration"]]
            solo_invs = [inv for inv in self.investigations if not inv["ubuntu_collaboration"]]
            
            ubuntu_count = len(ubuntu_invs)
            solo_count = len(solo_invs)
            
            # Calculate success rates
            ubuntu_successes = sum(1 for inv in ubuntu_invs if inv["success"])
            solo_successes = sum(1 for inv in solo_invs if inv["success"])
            
            ubuntu_success_rate = (ubuntu_successes / ubuntu_count * 100) if ubuntu_count > 0 else 0
            solo_success_rate = (solo_successes / solo_count * 100) if solo_count > 0 else 0
            
            return {
                "total_investigations": total,
                "ubuntu_investigations": ubuntu_count,
                "solo_investigations": solo_count,
                "ubuntu_success_rate": ubuntu_success_rate,
                "solo_success_rate": solo_success_rate,
                "ubuntu_advantage": ubuntu_success_rate - solo_success_rate
            }
            
        except Exception as e:
            print(f"[AgentMemory] Error getting Ubuntu stats: {e}")
            return {}
    
    def get_agent_learning_metrics(self, agent_name: str) -> Dict:
        """
        Get learning metrics for a specific agent (improvement over time).
        
        Args:
            agent_name: Agent to analyze
        
        Returns:
            Dict with learning metrics
        """
        try:
            # Filter investigations by agent
            agent_invs = [inv for inv in self.investigations if inv["agent"] == agent_name]
            
            if not agent_invs:
                return {
                    "agent": agent_name,
                    "total_investigations": 0
                }
            
            # Sort by timestamp
            agent_invs.sort(key=lambda x: x["timestamp"])
            
            # Calculate metrics
            total = len(agent_invs)
            total_iterations = sum(inv["iterations"] for inv in agent_invs)
            avg_iterations = total_iterations / total if total > 0 else 0
            
            successes = sum(1 for inv in agent_invs if inv["success"])
            success_rate = (successes / total * 100) if total > 0 else 0
            
            # Learning trend (first half vs second half)
            improvement = 0
            if total >= 4:  # Need at least 4 investigations for meaningful comparison
                mid = total // 2
                first_half = agent_invs[:mid]
                second_half = agent_invs[mid:]
                
                first_avg = sum(inv["iterations"] for inv in first_half) / len(first_half)
                second_avg = sum(inv["iterations"] for inv in second_half) / len(second_half)
                
                improvement = ((first_avg - second_avg) / first_avg * 100) if first_avg > 0 else 0
            
            return {
                "agent": agent_name,
                "total_investigations": total,
                "average_iterations": round(avg_iterations, 2),
                "success_rate": round(success_rate, 1),
                "improvement_over_time": round(improvement, 1)
            }
            
        except Exception as e:
            print(f"[AgentMemory] Error getting learning metrics: {e}")
            return {}
    
    # ===== HELPER METHODS =====
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity using embeddings.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        try:
            if not self.embeddings:
                return 0.0
            
            # Generate embeddings
            emb1 = self.embeddings.embed_query(text1)
            emb2 = self.embeddings.embed_query(text2)
            
            # Calculate cosine similarity
            dot_product = sum(a * b for a, b in zip(emb1, emb2))
            magnitude1 = sum(a * a for a in emb1) ** 0.5
            magnitude2 = sum(b * b for b in emb2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            similarity = dot_product / (magnitude1 * magnitude2)
            # Normalize to 0-1 range (cosine similarity is -1 to 1)
            return (similarity + 1) / 2
            
        except Exception as e:
            print(f"[AgentMemory] Error calculating semantic similarity: {e}")
            return 0.0
    
    def _categorize_problem(self, problem: str) -> str:
        """Categorize problem based on keywords."""
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ["network", "connection", "vpn", "connectivity"]):
            return "Network"
        elif any(word in problem_lower for word in ["server", "disk", "cpu", "memory", "infrastructure"]):
            return "Infrastructure"
        elif any(word in problem_lower for word in ["application", "app", "software", "program"]):
            return "Application"
        elif any(word in problem_lower for word in ["email", "outlook", "mail"]):
            return "Email"
        elif any(word in problem_lower for word in ["printer", "print", "hardware"]):
            return "Hardware"
        else:
            return "General"
    
    def get_all_investigations(self) -> List[Dict]:
        """Get all stored investigations."""
        return self.investigations.copy()
    
    def clear_memory(self):
        """Clear all investigations (use with caution)."""
        self.investigations = []
        self._save_investigations()
        print("[AgentMemory] Memory cleared")
    
    def export_investigations(self, filepath: str):
        """Export investigations to a specific file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.investigations, f, indent=2, ensure_ascii=False)
        print(f"[AgentMemory] Exported {len(self.investigations)} investigations to {filepath}")
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
    
    def __repr__(self):
        return f"AgentMemory(investigations={len(self.investigations)}, storage='{self.storage_dir}')"
