"""
Test Suite for Explicit Planning Integration
Phase 1: Deep Agents Pillar #1 Implementation

Tests:
1. Plan creation
2. Plan updates during investigation
3. Progress tracking
4. Ubuntu collaboration planning
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ugentic.core.explicit_planning import ExplicitPlanner


def test_plan_creation():
    """Test 1: Create investigation plan"""
    print("\n" + "="*60)
    print("TEST 1: Plan Creation")
    print("="*60)
    
    planner = ExplicitPlanner(plans_directory="plans/test/")
    
    plan_id = planner.create_plan(
        objective="User cannot access shared drive on server",
        agent_name="IT Support",
        problem_context={
            "user": "john.doe",
            "department": "finance",
            "server": "FILE_SERVER_01"
        }
    )
    
    print(f"✅ Plan created: {plan_id}")
    
    # Check plan was created
    plan = planner.get_plan(plan_id)
    assert plan["objective"] == "User cannot access shared drive on server"
    assert plan["created_by"] == "IT Support"
    assert len(plan["steps"]) > 0
    assert plan["status"] == "active"
    
    print(f"✅ Plan has {len(plan['steps'])} steps")
    print(f"✅ Plan status: {plan['status']}")
    
    return plan_id


def test_progress_tracking(plan_id):
    """Test 2: Track plan progress"""
    print("\n" + "="*60)
    print("TEST 2: Progress Tracking")
    print("="*60)
    
    planner = ExplicitPlanner(plans_directory="plans/test/")
    
    progress = planner.check_progress(plan_id)
    
    print(f"✅ Progress: {progress['progress']}")
    print(f"✅ Completion: {progress['completion_percentage']}%")
    print(f"✅ Status: {progress['status']}")
    
    if progress['next_step']:
        print(f"✅ Next step: {progress['next_step']['description']}")
    
    assert progress['completion_percentage'] == 0
    assert progress['status'] == 'active'
    assert progress['next_step'] is not None


def test_step_updates(plan_id):
    """Test 3: Update plan steps"""
    print("\n" + "="*60)
    print("TEST 3: Step Updates")
    print("="*60)
    
    planner = ExplicitPlanner(plans_directory="plans/test/")
    
    # Update step 1 as completed
    planner.update_step(
        plan_id=plan_id,
        step_number=1,
        status="completed",
        findings="User confirmed unable to access \\\\FILE_SERVER_01\\finance",
        tools_used=["check_system_logs", "gather_user_info"]
    )
    
    print("✅ Updated step 1 to completed")
    
    # Check progress after update
    progress = planner.check_progress(plan_id)
    print(f"✅ New progress: {progress['progress']}")
    print(f"✅ New completion: {progress['completion_percentage']}%")
    
    assert progress['completed_steps'] == 1
    assert progress['completion_percentage'] > 0
    
    # Update step 2
    planner.update_step(
        plan_id=plan_id,
        step_number=2,
        status="completed",
        findings="Network connectivity OK, issue is permissions-related",
        tools_used=["ping_test", "check_network_config"]
    )
    
    print("✅ Updated step 2 to completed")
    
    progress = planner.check_progress(plan_id)
    print(f"✅ Final progress: {progress['progress']}")
    print(f"✅ Final completion: {progress['completion_percentage']}%")


def test_ubuntu_collaboration_plan():
    """Test 4: Ubuntu collaboration planning"""
    print("\n" + "="*60)
    print("TEST 4: Ubuntu Collaboration Planning")
    print("="*60)
    
    planner = ExplicitPlanner(plans_directory="plans/test/")
    
    collab_plan_id = planner.create_plan(
        objective="Ubuntu Collaboration: Complex cross-departmental issue",
        agent_name="Ubuntu_Orchestrator",
        problem_context={
            "type": "multi_agent_collaboration",
            "lead_agent": "IT Manager",
            "issue": "Application timeout affecting multiple users"
        }
    )
    
    print(f"✅ Ubuntu collaboration plan created: {collab_plan_id}")
    
    plan = planner.get_plan(collab_plan_id)
    assert plan["objective"].startswith("Ubuntu Collaboration:")
    assert plan["created_by"] == "Ubuntu_Orchestrator"
    
    print(f"✅ Plan has {len(plan['steps'])} coordination steps")


def test_list_active_plans():
    """Test 5: List active plans"""
    print("\n" + "="*60)
    print("TEST 5: List Active Plans")
    print("="*60)
    
    planner = ExplicitPlanner(plans_directory="plans/test/")
    
    active_plans = planner.list_active_plans()
    
    print(f"✅ Found {len(active_plans)} active plans")
    
    for plan in active_plans:
        print(f"   - {plan['plan_id']}: {plan['objective'][:50]}...")
    
    assert len(active_plans) > 0


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "#"*60)
    print("EXPLICIT PLANNING - TEST SUITE")
    print("Phase 1: Deep Agents Pillar #1")
    print("#"*60)
    
    try:
        # Test 1: Create plan
        plan_id = test_plan_creation()
        
        # Test 2: Track progress
        test_progress_tracking(plan_id)
        
        # Test 3: Update steps
        test_step_updates(plan_id)
        
        # Test 4: Ubuntu collaboration
        test_ubuntu_collaboration_plan()
        
        # Test 5: List active plans
        test_list_active_plans()
        
        print("\n" + "#"*60)
        print("✅ ALL TESTS PASSED")
        print("#"*60 + "\n")
        
    except Exception as e:
        print("\n" + "#"*60)
        print(f"❌ TEST FAILED: {e}")
        print("#"*60 + "\n")
        raise


if __name__ == "__main__":
    run_all_tests()
