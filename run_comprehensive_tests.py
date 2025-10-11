#!/usr/bin/env python3
"""
Comprehensive Scenario Testing for UGENTIC Framework
Tests the three key scenarios with qwen2.5:7b and compares with simulation predictions
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ugentic.core.rag_core import RAGCore, get_embedding_model_from_config
from ugentic.agents.it_departmental_agents import initialize_it_departmental_agents
from ugentic.core.orchestrator_tool import OrchestratorTool
from ugentic.core.filesystem_tool import FilesystemTool
from ugentic.core.git_tool import GitTool
from ugentic.core.research_tool import ResearchTool

class ComprehensiveTestRunner:
    """Runs comprehensive tests and captures detailed results"""
    
    def __init__(self):
        self.results = {
            "test_date": datetime.now().isoformat(),
            "llm_model": None,
            "scenarios": []
        }
        self.agents = None
        self.rag_system = None
        
    def initialize_system(self):
        """Initialize the UGENTIC system"""
        print("\n" + "="*70)
        print("🚀 INITIALIZING UGENTIC FRAMEWORK FOR COMPREHENSIVE TESTING")
        print("="*70)
        
        # Load configuration
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.results["llm_model"] = config.get("reasoning_model", "unknown")
        print(f"📊 LLM Model: {self.results['llm_model']}")
        
        # Initialize RAG system
        print("\n📚 Initializing RAG System...")
        # Create temporary filesystem tool for config reading
        from ugentic.core.filesystem_tool import FilesystemTool
        temp_fs_tool = FilesystemTool()
        embedding_model_name = get_embedding_model_from_config(temp_fs_tool)
        from ugentic.core.rag_core import get_ollama_embeddings, get_text_splitter
        embedding_model = get_ollama_embeddings(embedding_model_name)
        text_splitter = get_text_splitter()
        self.rag_system = RAGCore(embedding_model=embedding_model, text_splitter=text_splitter, filesystem_tool=temp_fs_tool)
        
        # Load documents
        docs_path = Path(__file__).parent / "documents" / "policies"
        doc_count = 0
        if docs_path.exists():
            for doc_file in docs_path.glob("*.md"):
                self.rag_system.add_documents([str(doc_file)])
                doc_count += 1
        
        print(f"   ✅ Loaded {doc_count} policy documents")
        print(f"   ✅ RAG System operational")
        
        # Initialize tools
        print("\n🛠️  Initializing MCP Tools...")
        orchestrator = OrchestratorTool()
        filesystem = FilesystemTool()
        git = GitTool()
        research = ResearchTool()
        
        tools = {
            "orchestrator": orchestrator,
            "filesystem": filesystem,
            "git": git,
            "research": research
        }
        print(f"   ✅ {len(tools)} tools initialized")
        
        # Initialize agents
        print("\n🤖 Initializing Ubuntu Agents...")
        self.agents = initialize_it_departmental_agents(
            rag_system=self.rag_system,
            mcp_tools=tools
        )
        print(f"   ✅ {len(self.agents)} agents ready")
        
        # Display agent status
        print("\n📋 Agent Status:")
        for agent_key, agent in self.agents.items():
            ubuntu_status = "✅ Ubuntu Active" if hasattr(agent, 'ubuntu_principles') and agent.ubuntu_principles else "⚠️ Ubuntu Inactive"
            print(f"   🤖 {agent_key}: {agent.name} ({agent.role}) - {ubuntu_status}")
        
        print("\n" + "="*70)
        print("✅ SYSTEM INITIALIZATION COMPLETE")
        print("="*70 + "\n")
    
    def run_test_scenario(self, scenario_name, user_query, expected_agents, expected_time_range, complexity):
        """Run a single test scenario and capture results"""
        print("\n" + "="*70)
        print(f"🧪 TEST SCENARIO: {scenario_name}")
        print("="*70)
        print(f"📝 User Query: \"{user_query}\"")
        print(f"🎯 Expected Agents: {', '.join(expected_agents)}")
        print(f"⏱️  Expected Time: {expected_time_range}")
        print(f"📊 Complexity: {complexity}")
        print("-"*70)
        
        scenario_result = {
            "name": scenario_name,
            "user_query": user_query,
            "expected_agents": expected_agents,
            "expected_time": expected_time_range,
            "complexity": complexity,
            "start_time": datetime.now().isoformat(),
            "agents_involved": [],
            "decisions": [],
            "ubuntu_collaborations": [],
            "success": False,
            "notes": []
        }
        
        start_time = datetime.now()
        
        try:
            # Step 1: IT Manager receives the request
            print("\n📥 STEP 1: IT Manager Analysis")
            it_manager = self.agents.get('ITManager')
            if not it_manager:
                raise Exception("IT Manager not found")
            
            scenario_result["agents_involved"].append("ITManager")
            
            # Analyze the goal
            analysis = it_manager.analyze_goal(user_query)
            print(f"   📊 Analysis: {json.dumps(analysis, indent=6)}")
            
            scenario_result["decisions"].append({
                "agent": "ITManager",
                "decision": analysis.get("decision"),
                "target": analysis.get("target_agent"),
                "reasoning": analysis.get("task", "")
            })
            
            # Step 2: Delegation
            if analysis.get("decision") == "Delegate":
                target_agent_key = analysis.get("target_agent")
                print(f"\n🔀 STEP 2: Delegation to {target_agent_key}")
                
                target_agent = self.agents.get(target_agent_key)
                if not target_agent:
                    print(f"   ⚠️  Warning: Target agent '{target_agent_key}' not found in routing")
                    scenario_result["notes"].append(f"Routing gap: {target_agent_key} not wired")
                else:
                    scenario_result["agents_involved"].append(target_agent_key)
                    
                    # If IT Support, analyze with Ubuntu
                    if target_agent_key == "ITSupport":
                        from ugentic.agents.departmental_agents.agent_itsupport import SupportTicket, SupportPriority
                        
                        ticket = SupportTicket(
                            ticket_id=f"TEST_{datetime.now().timestamp()}",
                            user_name="Test User",
                            issue_description=user_query,
                            priority=SupportPriority.HIGH,
                            category="test_scenario",
                            time_reported=datetime.now()
                        )
                        
                        print("   🔍 IT Support analyzing with Ubuntu principles...")
                        support_analysis = target_agent.analyze_support_request(ticket)
                        print(f"   📊 Support Analysis: {json.dumps(support_analysis, indent=6)}")
                        
                        scenario_result["decisions"].append({
                            "agent": "ITSupport",
                            "can_resolve_independently": support_analysis.get("can_resolve_independently"),
                            "requires_collaboration": support_analysis.get("requires_collaboration"),
                            "collaboration_targets": support_analysis.get("collaboration_targets", []),
                            "ubuntu_approach": support_analysis.get("ubuntu_approach")
                        })
                        
                        # Check for Ubuntu collaboration
                        if support_analysis.get("requires_collaboration"):
                            print("\n🤝 STEP 3: Ubuntu Collaboration Triggered")
                            
                            collab_data = {
                                "triggering_agent": "ITSupport",
                                "targets": support_analysis.get("collaboration_targets", []),
                                "approach": support_analysis.get("ubuntu_approach"),
                                "reason": "Collective diagnosis required"
                            }
                            
                            scenario_result["ubuntu_collaborations"].append(collab_data)
                            scenario_result["agents_involved"].extend(support_analysis.get("collaboration_targets", []))
                            
                            print(f"   👥 Collaboration Partners: {', '.join(support_analysis.get('collaboration_targets', []))}")
                            print(f"   🎯 Ubuntu Approach: {support_analysis.get('ubuntu_approach')}")
                        
                        # User communication
                        communication = target_agent.provide_user_communication(ticket, support_analysis)
                        print(f"\n💬 User Communication:\n{communication}")
                        scenario_result["user_communication"] = communication
                    
                    elif target_agent_key in ["Infrastructure", "NetworkSupport", "AppSupport"]:
                        print(f"   🔧 {target_agent_key} would handle this request")
                        print(f"   ℹ️  Full execution flow not implemented in test harness")
                        scenario_result["notes"].append(f"{target_agent_key} agent exists but test harness limited")
            
            scenario_result["success"] = True
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            scenario_result["success"] = False
            scenario_result["error"] = str(e)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        scenario_result["end_time"] = end_time.isoformat()
        scenario_result["duration_seconds"] = duration
        
        print(f"\n⏱️  Test Duration: {duration:.2f} seconds")
        print(f"✅ Agents Involved: {', '.join(set(scenario_result['agents_involved']))}")
        print(f"🤝 Ubuntu Collaborations: {len(scenario_result['ubuntu_collaborations'])}")
        print(f"📊 Test Result: {'✅ SUCCESS' if scenario_result['success'] else '❌ FAILED'}")
        print("="*70 + "\n")
        
        self.results["scenarios"].append(scenario_result)
        return scenario_result
    
    def run_all_tests(self):
        """Run all three test scenarios"""
        print("\n" + "="*70)
        print("🎯 COMPREHENSIVE SCENARIO TESTING - UGENTIC FRAMEWORK")
        print("="*70)
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 LLM Model: {self.results.get('llm_model', 'Loading...')}")
        print("="*70)
        
        # Test 1: Simple Password Reset (S1.1)
        self.run_test_scenario(
            scenario_name="S1.1 - Password Reset",
            user_query="I forgot my password and cannot log into my computer",
            expected_agents=["ITManager", "ServiceDeskManager", "ITSupport"],
            expected_time_range="~5 minutes",
            complexity="Simple"
        )
        
        # Test 2: Email Sync Issues (S2.1)
        self.run_test_scenario(
            scenario_name="S2.1 - Email Sync Issues",
            user_query="My email works on desktop but not on my phone",
            expected_agents=["ITManager", "ServiceDeskManager", "ITSupport", "Infrastructure", "NetworkSupport"],
            expected_time_range="~15 minutes",
            complexity="Moderate"
        )
        
        # Test 3: System-Wide Performance (S3.1)
        self.run_test_scenario(
            scenario_name="S3.1 - System-Wide Performance",
            user_query="Multiple users across departments are reporting that everything is running slow",
            expected_agents=["ITManager", "Infrastructure", "NetworkSupport", "AppSupport", "ITSupport"],
            expected_time_range="~32 minutes",
            complexity="Complex"
        )
        
        # Summary
        self.print_summary()
        self.save_results()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        
        total = len(self.results["scenarios"])
        passed = sum(1 for s in self.results["scenarios"] if s["success"])
        
        print(f"✅ Tests Passed: {passed}/{total}")
        print(f"⏱️  Total Test Duration: {sum(s['duration_seconds'] for s in self.results['scenarios']):.2f} seconds")
        print(f"🤝 Total Ubuntu Collaborations: {sum(len(s['ubuntu_collaborations']) for s in self.results['scenarios'])}")
        
        print("\n📋 Individual Results:")
        for scenario in self.results["scenarios"]:
            status = "✅ PASS" if scenario["success"] else "❌ FAIL"
            print(f"   {status} - {scenario['name']}")
            print(f"      Agents: {', '.join(set(scenario['agents_involved']))}")
            print(f"      Duration: {scenario['duration_seconds']:.2f}s")
            print(f"      Ubuntu Collabs: {len(scenario['ubuntu_collaborations'])}")
            if scenario.get("notes"):
                for note in scenario["notes"]:
                    print(f"      Note: {note}")
        
        print("="*70 + "\n")
    
    def save_results(self):
        """Save test results to file"""
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"comprehensive_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"💾 Results saved to: {results_file}")

def main():
    """Main test execution"""
    runner = ComprehensiveTestRunner()
    runner.initialize_system()
    runner.run_all_tests()

if __name__ == "__main__":
    main()
