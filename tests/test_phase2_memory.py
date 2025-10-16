"""
Phase 2: Pure Python Memory System - Test Suite

Tests the AgentMemory implementation with JSON storage.
No external dependencies required.

Author: Claude + Craig Vraagom
Date: October 14, 2025
Version: 2.0 (Pure Python)
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ugentic.core.agent_memory import AgentMemory
from src.ugentic.utils.investigation_logger import InvestigationLogger


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(text)
    print("="*60)


def print_test_result(test_name, passed, message=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {test_name}")
    if message:
        print(f"   {message}")


def test_memory_initialization():
    """Test 1: Memory System Initialization"""
    print_header("TEST 1: AgentMemory Initialization")
    
    try:
        # Create memory instance
        memory = AgentMemory(storage_dir="data/test_memory")
        
        # Verify initialization
        assert memory is not None, "Memory instance not created"
        assert memory.storage_dir.exists(), "Storage directory not created"
        assert isinstance(memory.investigations, list), "Investigations not initialized"
        
        # Start memory (should always succeed for Pure Python)
        started = memory.start()
        assert started, "Memory failed to start"
        
        # Stop memory
        memory.stop()
        
        print_test_result("Memory Initialization", True)
        return True
        
    except Exception as e:
        print_test_result("Memory Initialization", False, str(e))
        return False


def test_investigation_storage():
    """Test 2: Investigation Storage"""
    print_header("TEST 2: Investigation Storage")
    
    try:
        memory = AgentMemory(storage_dir="data/test_memory")
        memory.start()
        
        # Store test investigation
        stored = memory.store_investigation(
            investigation_id="test_inv_001",
            agent_name="Infrastructure",
            problem="Server disk at 90% capacity",
            root_cause="Log files not rotating",
            solution="Configured log rotation",
            actions_taken=["check_disk_space", "analyze_logs", "configure_rotation"],
            ubuntu_collaboration=False,
            success=True,
            iterations=3,
            timestamp="2025-10-14T10:00:00"
        )
        
        assert stored, "Failed to store investigation"
        
        # Verify storage
        assert len(memory.investigations) > 0, "Investigation not in memory"
        
        # Verify investigation content
        inv = memory.investigations[-1]  # Get last added
        assert inv["id"] == "test_inv_001", "Investigation ID mismatch"
        assert inv["agent"] == "Infrastructure", "Agent name mismatch"
        assert inv["success"] == True, "Success status mismatch"
        
        memory.stop()
        
        print_test_result("Investigation Storage", True, f"Stored {len(memory.investigations)} investigation(s)")
        return True
        
    except Exception as e:
        print_test_result("Investigation Storage", False, str(e))
        return False


def test_similar_problem_recall():
    """Test 3: Similar Problem Recall"""
    print_header("TEST 3: Similar Problem Recall")
    
    try:
        memory = AgentMemory(storage_dir="data/test_memory")
        memory.start()
        
        # Store multiple related investigations
        problems = [
            "Server disk space at 90%",
            "Database server running out of disk space",
            "Backup server disk full",
            "Network connectivity issues"  # Different category
        ]
        
        for i, problem in enumerate(problems):
            memory.store_investigation(
                investigation_id=f"test_inv_{i+10}",
                agent_name="Infrastructure",
                problem=problem,
                root_cause="Various causes",
                solution="Various solutions",
                success=True,
                iterations=2 + i
            )
        
        # Query for similar problems
        similar = memory.recall_similar_problem("Server disk space low", limit=3)
        
        assert len(similar) > 0, "No similar problems found"
        assert len(similar) <= 3, "Too many results returned"
        
        # Verify similarity scores exist
        for inv in similar:
            assert "similarity" in inv, "Similarity score missing"
            assert inv["similarity"] > 0, "Invalid similarity score"
        
        # Verify most similar is disk-related (not network)
        top_match = similar[0]
        assert "disk" in top_match["problem"].lower(), "Top match not relevant"
        
        memory.stop()
        
        print_test_result("Similar Problem Recall", True, f"Found {len(similar)} similar investigation(s)")
        return True
        
    except Exception as e:
        print_test_result("Similar Problem Recall", False, str(e))
        return False


def test_ubuntu_collaboration_tracking():
    """Test 4: Ubuntu Collaboration Tracking"""
    print_header("TEST 4: Ubuntu Collaboration Tracking")
    
    try:
        memory = AgentMemory(storage_dir="data/test_memory")
        memory.start()
        
        # Store Ubuntu collaboration investigation
        memory.store_investigation(
            investigation_id="test_ubuntu_001",
            agent_name="Infrastructure",
            problem="Complex application performance issue",
            root_cause="Database and network bottleneck",
            solution="Optimized both layers",
            ubuntu_collaboration=True,
            collaborating_agents=["App Support", "Network Support"],
            success=True,
            iterations=5
        )
        
        # Store solo investigation
        memory.store_investigation(
            investigation_id="test_solo_001",
            agent_name="Infrastructure",
            problem="Simple server restart needed",
            root_cause="Service crashed",
            solution="Restarted service",
            ubuntu_collaboration=False,
            success=True,
            iterations=2
        )
        
        # Get Ubuntu stats
        stats = memory.get_ubuntu_collaboration_stats()
        
        assert stats is not None, "Stats not returned"
        assert "ubuntu_investigations" in stats, "Ubuntu count missing"
        assert "solo_investigations" in stats, "Solo count missing"
        assert "ubuntu_success_rate" in stats, "Ubuntu success rate missing"
        assert "solo_success_rate" in stats, "Solo success rate missing"
        
        # Verify counts
        assert stats["ubuntu_investigations"] > 0, "No Ubuntu investigations tracked"
        assert stats["solo_investigations"] > 0, "No solo investigations tracked"
        
        memory.stop()
        
        print_test_result("Ubuntu Collaboration Tracking", True, 
                         f"Ubuntu: {stats['ubuntu_investigations']}, Solo: {stats['solo_investigations']}")
        return True
        
    except Exception as e:
        print_test_result("Ubuntu Collaboration Tracking", False, str(e))
        return False


def test_agent_learning_metrics():
    """Test 5: Agent Learning Metrics"""
    print_header("TEST 5: Agent Learning Metrics")
    
    try:
        memory = AgentMemory(storage_dir="data/test_memory")
        memory.start()
        
        # Simulate learning over time (iterations should decrease)
        iterations_sequence = [10, 9, 7, 6, 5, 4]  # Improving over time
        
        for i, iterations in enumerate(iterations_sequence):
            memory.store_investigation(
                investigation_id=f"test_learning_{i}",
                agent_name="Infrastructure",
                problem=f"Similar problem #{i}",
                root_cause="Root cause",
                solution="Solution",
                success=True,
                iterations=iterations,
                timestamp=f"2025-10-14T{10+i}:00:00"
            )
        
        # Get learning metrics
        metrics = memory.get_agent_learning_metrics("Infrastructure")
        
        assert metrics is not None, "Metrics not returned"
        assert "agent" in metrics, "Agent name missing"
        assert "total_investigations" in metrics, "Total count missing"
        assert "average_iterations" in metrics, "Average iterations missing"
        assert "improvement_over_time" in metrics, "Improvement metric missing"
        
        # Verify learning improvement
        assert metrics["total_investigations"] >= 6, "Not enough investigations tracked"
        assert metrics["improvement_over_time"] > 0, "No improvement detected"
        
        memory.stop()
        
        print_test_result("Agent Learning Metrics", True, 
                         f"Improvement: {metrics['improvement_over_time']:.1f}%")
        return True
        
    except Exception as e:
        print_test_result("Agent Learning Metrics", False, str(e))
        return False


def test_logger_integration():
    """Test 6: InvestigationLogger + AgentMemory Integration"""
    print_header("TEST 6: InvestigationLogger Integration")
    
    try:
        # Initialize memory
        memory = AgentMemory(storage_dir="data/test_memory")
        memory.start()
        
        # Initialize logger with memory
        logger = InvestigationLogger(base_dir="logs/test_phase2", memory=memory)
        
        # Start investigation
        inv_id = logger.start_investigation(
            query="Cannot access email",
            agent="Infrastructure"
        )
        
        assert inv_id is not None, "Investigation ID not created"
        
        # End investigation (should auto-store in memory)
        investigation_count_before = len(memory.investigations)
        
        logger.end_investigation(
            inv_id=inv_id,
            outcome="success",
            final_response="Email server was down. Restarted email server."
        )
        
        investigation_count_after = len(memory.investigations)
        
        # Verify investigation was stored in memory
        assert investigation_count_after > investigation_count_before, \
            "Investigation not stored in memory"
        
        # Verify we can recall it
        stats = memory.get_memory_stats() if hasattr(memory, 'get_memory_stats') else \
                logger.get_memory_stats() if hasattr(logger, 'get_memory_stats') else \
                memory.get_ubuntu_collaboration_stats()
        
        assert stats is not None, "Could not retrieve memory stats"
        
        memory.stop()
        
        print_test_result("Logger Integration", True, "Investigation auto-stored in memory")
        return True
        
    except Exception as e:
        print_test_result("Logger Integration", False, str(e))
        return False


def cleanup_test_data():
    """Clean up test data"""
    import shutil
    test_dir = Path("data/test_memory")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("\n[Cleanup] Test data removed")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PHASE 2: PURE PYTHON MEMORY SYSTEM - TEST SUITE")
    print("="*60)
    print("Testing AgentMemory with JSON storage")
    print("No external dependencies required")
    print("="*60)
    
    input("\nPress Enter to start tests... ")
    
    # Run tests
    tests = [
        ("Memory Initialization", test_memory_initialization),
        ("Investigation Storage", test_investigation_storage),
        ("Similar Problem Recall", test_similar_problem_recall),
        ("Ubuntu Collaboration Tracking", test_ubuntu_collaboration_tracking),
        ("Agent Learning Metrics", test_agent_learning_metrics),
        ("Logger Integration", test_logger_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    success_rate = (passed_count / total_count * 100) if total_count > 0 else 0
    
    print(f"Total Tests: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_count - passed_count}")
    print(f"Success Rate: {success_rate:.1f}%")
    print("="*60)
    
    if passed_count == total_count:
        print("\n✅ ALL TESTS PASSED! Memory system ready for use.")
        print("\nNext steps:")
        print("  1. Run: python app.py")
        print("  2. Test live system with real investigations")
        print("  3. Check memory statistics on exit")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Review errors above.")
    
    # Cleanup
    print("\n" + "="*60)
    cleanup_response = input("Clean up test data? (y/n): ")
    if cleanup_response.lower() == 'y':
        cleanup_test_data()
    
    print("\nTest suite complete!")


if __name__ == "__main__":
    main()
