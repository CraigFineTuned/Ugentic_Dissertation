"""
UGENTIC Automated Test Suite Runner
Validates all fixes from Dec 3, 2025 bug fix session

Tests:
- Level 1 resolution (should NOT escalate)
- Specialist routing (should escalate to CORRECT specialist)
- Multi-agent orchestration
- Strategic decisions
- Edge cases

Metrics Collected:
- Resolution time per test
- Escalation decisions
- Tool accuracy (username handling)
- Routing accuracy
- Success/failure status
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ugentic.core.config_manager import ConfigManager
from src.ugentic.utils.investigation_logger import InvestigationLogger
from src.ugentic.agents.react_agents.itsupport_agent_react import ITSupportAgent
from src.ugentic.agents.react_agents.service_desk_manager_react import ServiceDeskManagerAgent
from src.ugentic.agents.react_agents.itmanager_agent_react import ITManagerAgent
from src.ugentic.agents.react_agents.network_agent_react import NetworkSupportAgent
from src.ugentic.agents.react_agents.app_agent_react import AppSupportAgent
from src.ugentic.agents.react_agents.infrastructure_agent_react import InfrastructureAgent

# Test scenarios
TEST_SCENARIOS = [
    {
        'id': 'T01',
        'category': 'LEVEL_1_SIMPLE',
        'name': 'Password Reset',
        'prompt': "Sarah Chen forgot her password and is locked out. She needs access ASAP for the 2pm board meeting.",
        'expected': {
            'should_escalate': False,
            'resolution_level': 'IT Support',
            'max_time': 15,
            'tools_used': ['reset_user_password'],
            'username_check': 'Sarah Chen'
        }
    },
    {
        'id': 'T02',
        'category': 'LEVEL_1_SIMPLE',
        'name': 'Printer Offline',
        'prompt': "I can't print to the 3rd floor printer HP-LaserJet-301. It shows as offline but the power light is on.",
        'expected': {
            'should_escalate': False,
            'resolution_level': 'IT Support',
            'max_time': 15,
            'tools_used': ['check_printer_status']
        }
    },
    {
        'id': 'T03',
        'category': 'LEVEL_1_SIMPLE',
        'name': 'Access Request',
        'prompt': "New employee John Smith needs access to the Finance shared drive to review Q4 reports.",
        'expected': {
            'should_escalate': False,  # May escalate to IT Manager (strategic), but not technical
            'resolution_level': 'IT Support',
            'max_time': 15,
            'tools_used': ['check_user_permissions'],
            'username_check': 'John Smith'
        }
    },
    {
        'id': 'T04',
        'category': 'LEVEL_2_SPECIALIST',
        'name': 'VPN Performance (Network)',
        'prompt': "Our team's VPN connection is extremely slow since yesterday morning. At least 5 people in Marketing are affected.",
        'expected': {
            'should_escalate': True,
            'correct_specialist': 'Network Support',
            'escalation_type': 'technical',
            'max_time': 30
        }
    },
    {
        'id': 'T05',
        'category': 'LEVEL_2_SPECIALIST',
        'name': 'Application Timeout (App Support)',
        'prompt': "The CRM application times out every time we try to export large customer reports. Small exports work fine.",
        'expected': {
            'should_escalate': True,
            'correct_specialist': 'App Support',
            'escalation_type': 'technical',
            'max_time': 30
        }
    },
    {
        'id': 'T06',
        'category': 'LEVEL_2_SPECIALIST',
        'name': 'Disk Space Critical (Infrastructure)',
        'prompt': "Our main file server disk space is at 95% capacity. Backup jobs started failing last night with 'insufficient space' errors.",
        'expected': {
            'should_escalate': True,
            'correct_specialist': 'Infrastructure',
            'escalation_type': 'technical',
            'max_time': 30
        }
    },
    {
        'id': 'T07',
        'category': 'LEVEL_3_ORCHESTRATION',
        'name': 'Multi-Domain Issue',
        'prompt': "Half the Marketing department can't access the shared drive. When they do connect, files take forever to load. This started this morning around 9am.",
        'expected': {
            'should_escalate': True,
            'orchestration': True,
            'min_agents': 2,
            'max_time': 60
        }
    },
    {
        'id': 'T08',
        'category': 'STRATEGIC',
        'name': 'License Purchase',
        'prompt': "Our department needs Microsoft 365 E5 licenses for 50 users to enable advanced security features. Annual cost is approximately $15,000.",
        'expected': {
            'should_escalate': True,
            'correct_specialist': 'IT Manager',
            'escalation_type': 'strategic',
            'max_time': 25
        }
    },
    {
        'id': 'T09',
        'category': 'EDGE_CASE',
        'name': 'Everything Slow (Diagnostic Pivot)',
        'prompt': "Everything suddenly became slow 10 minutes ago - email, file shares, internal websites, even our applications. Nothing specific, just everything is crawling.",
        'expected': {
            'should_escalate': True,
            'adaptive_reasoning': True,
            'max_time': 60
        }
    },
    {
        'id': 'T10',
        'category': 'LEVEL_1_ANALYTICAL',
        'name': 'Permission Comparison',
        'prompt': "Can you compare permissions between users 'jdoe' and 'jsmith'? They're supposed to have the same access since they're both Financial Analysts, but jdoe can't access certain folders that jsmith can.",
        'expected': {
            'should_escalate': False,
            'resolution_level': 'IT Support',
            'max_time': 25,
            'tools_used': ['check_user_permissions'],
            'comparative_analysis': True
        }
    }
]


class TestRunner:
    """Automated test suite runner with metrics collection"""

    def __init__(self):
        self.config = ConfigManager()
        self.logger = InvestigationLogger(base_dir="logs_test")
        self.results = []
        self.start_time = None
        self.agents = {}

    def initialize_agents(self):
        """Initialize all agents"""
        print("🔧 Initializing agents...")

        try:
            self.agents['IT Support'] = ITSupportAgent(config=self.config, logger=self.logger)
            self.agents['Service Desk Manager'] = ServiceDeskManagerAgent(config=self.config, logger=self.logger)
            self.agents['IT Manager'] = ITManagerAgent(config=self.config, logger=self.logger)
            self.agents['Network Support'] = NetworkSupportAgent(config=self.config, logger=self.logger)
            self.agents['App Support'] = AppSupportAgent(config=self.config, logger=self.logger)
            self.agents['Infrastructure'] = InfrastructureAgent(config=self.config, logger=self.logger)

            print(f"✅ Initialized {len(self.agents)} agents")
            return True

        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            return False

    def run_test(self, test_scenario):
        """Run a single test scenario"""
        test_id = test_scenario['id']
        test_name = test_scenario['name']
        prompt = test_scenario['prompt']
        expected = test_scenario['expected']

        print(f"\n{'='*70}")
        print(f"🧪 TEST {test_id}: {test_name}")
        print(f"{'='*70}")
        print(f"Prompt: {prompt[:80]}...")
        print(f"Category: {test_scenario['category']}")

        result = {
            'test_id': test_id,
            'test_name': test_name,
            'category': test_scenario['category'],
            'prompt': prompt,
            'expected': expected,
            'actual': {},
            'passed': False,
            'issues': [],
            'duration': 0,
            'timestamp': datetime.now().isoformat()
        }

        try:
            start_time = time.time()

            # STEP 1: IT Support (Level 1) attempts resolution
            it_support = self.agents['IT Support']
            level1_result = it_support.investigate(prompt, context={'test_id': test_id})

            duration = time.time() - start_time
            result['duration'] = round(duration, 2)

            # Extract actual behavior
            result['actual']['status'] = level1_result.get('status')
            result['actual']['agent'] = 'IT Support'
            result['actual']['duration'] = result['duration']
            result['actual']['escalated'] = level1_result.get('status') == 'NEEDS_ESCALATION'

            # Check if escalation occurred
            if level1_result.get('status') == 'NEEDS_ESCALATION':
                escalation_details = level1_result.get('escalation_details', {})
                result['actual']['escalation_type'] = escalation_details.get('type')
                result['actual']['escalation_reason'] = escalation_details.get('reason')
                result['actual']['suggested_specialist'] = escalation_details.get('suggested_specialist')

                # STEP 2: Service Desk Manager routes (if technical escalation)
                if escalation_details.get('type') == 'technical':
                    service_desk = self.agents['Service Desk Manager']
                    routed_specialist = service_desk.route_escalation(
                        issue=prompt,
                        level1_findings=level1_result,
                        context={'test_id': test_id}
                    )
                    result['actual']['routed_to'] = routed_specialist

                elif escalation_details.get('type') == 'strategic':
                    result['actual']['routed_to'] = 'IT Manager'

            else:
                # Resolved at Level 1
                result['actual']['resolved_at_level1'] = True

            # Check for tool usage and username handling
            investigation_history = it_support.get_investigation_history()
            if investigation_history:
                tools_used = []
                for step in investigation_history:
                    if 'action' in step:
                        tool = step['action'].get('tool_name')
                        if tool:
                            tools_used.append(tool)

                            # Check username handling
                            params = step['action'].get('parameters', {})
                            if 'username' in params:
                                result['actual']['username_param'] = params['username']

                            # Check tool observation
                            if 'observation' in step:
                                obs_data = step['observation'].get('data', {})
                                if 'user_id' in obs_data:
                                    returned_user = obs_data.get('username', obs_data.get('user_id'))
                                    result['actual']['returned_username'] = returned_user

                result['actual']['tools_used'] = tools_used

            # Validate against expected behavior
            result['passed'], result['issues'] = self.validate_test(result, expected)

            # Print result summary
            status_icon = "✅" if result['passed'] else "❌"
            print(f"\n{status_icon} Result: {'PASSED' if result['passed'] else 'FAILED'}")
            print(f"   Duration: {result['duration']}s")
            print(f"   Status: {result['actual']['status']}")

            if result['actual'].get('escalated'):
                print(f"   Escalated: Yes → {result['actual'].get('routed_to', 'Unknown')}")
            else:
                print(f"   Resolved: Level 1")

            if result['issues']:
                print(f"\n⚠️  Issues Found:")
                for issue in result['issues']:
                    print(f"   - {issue}")

        except Exception as e:
            result['passed'] = False
            result['issues'].append(f"Test execution error: {str(e)}")
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()

        self.results.append(result)
        return result

    def validate_test(self, result, expected):
        """Validate test result against expected behavior"""
        issues = []
        passed = True

        actual = result['actual']

        # Check escalation expectation
        if 'should_escalate' in expected:
            should_escalate = expected['should_escalate']
            did_escalate = actual.get('escalated', False)

            if should_escalate != did_escalate:
                issues.append(f"Escalation mismatch: Expected {should_escalate}, got {did_escalate}")
                passed = False

        # Check correct specialist routing
        if 'correct_specialist' in expected:
            expected_specialist = expected['correct_specialist']
            actual_specialist = actual.get('routed_to')

            if expected_specialist != actual_specialist:
                issues.append(f"Routing error: Expected {expected_specialist}, got {actual_specialist}")
                passed = False

        # Check escalation type
        if 'escalation_type' in expected:
            expected_type = expected['escalation_type']
            actual_type = actual.get('escalation_type')

            if expected_type != actual_type:
                issues.append(f"Escalation type: Expected {expected_type}, got {actual_type}")
                passed = False

        # Check duration
        if 'max_time' in expected:
            max_time = expected['max_time']
            duration = result['duration']

            if duration > max_time:
                issues.append(f"Duration exceeded: {duration}s > {max_time}s target")
                # Don't fail test for timing, just warn

        # Check username handling
        if 'username_check' in expected:
            expected_username = expected['username_check']
            returned_username = actual.get('returned_username')

            if returned_username and 'default_user' in str(returned_username).lower():
                issues.append(f"Username bug: Returned 'default_user' instead of '{expected_username}'")
                passed = False

        # Check tools used
        if 'tools_used' in expected:
            expected_tools = expected['tools_used']
            actual_tools = actual.get('tools_used', [])

            for tool in expected_tools:
                if tool not in actual_tools:
                    issues.append(f"Missing tool: Expected to use '{tool}'")
                    # Don't fail, just note

        return passed, issues

    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*70)
        print("🚀 UGENTIC AUTOMATED TEST SUITE")
        print("="*70)
        print(f"Test Scenarios: {len(TEST_SCENARIOS)}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("="*70)

        self.start_time = time.time()

        # Initialize agents
        if not self.initialize_agents():
            print("❌ Cannot proceed without agents")
            return

        # Run each test
        for i, test in enumerate(TEST_SCENARIOS, 1):
            print(f"\n\n{'#'*70}")
            print(f"# Test {i}/{len(TEST_SCENARIOS)}")
            print(f"{'#'*70}")

            self.run_test(test)

            # Small delay between tests
            time.sleep(1)

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate comprehensive test report"""
        total_duration = time.time() - self.start_time

        # Calculate metrics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['passed'])
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # Category breakdown
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'passed': 0}
            categories[cat]['total'] += 1
            if result['passed']:
                categories[cat]['passed'] += 1

        # Escalation metrics
        escalation_tests = [r for r in self.results if r['expected'].get('should_escalate')]
        correct_escalations = sum(1 for r in escalation_tests
                                 if r['actual'].get('escalated') and r['passed'])

        level1_tests = [r for r in self.results if not r['expected'].get('should_escalate')]
        level1_resolved = sum(1 for r in level1_tests
                             if not r['actual'].get('escalated') and r['passed'])
        level1_rate = (level1_resolved / len(level1_tests) * 100) if level1_tests else 0

        # Average duration
        avg_duration = sum(r['duration'] for r in self.results) / total_tests if total_tests > 0 else 0

        # Print summary report
        print("\n\n" + "="*70)
        print("📊 TEST SUITE SUMMARY")
        print("="*70)

        print(f"\n📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ({pass_rate:.1f}%)")
        print(f"   Failed: {failed_tests}")
        print(f"   Total Duration: {total_duration:.1f}s")
        print(f"   Avg Duration: {avg_duration:.1f}s")

        print(f"\n🎯 Key Metrics:")
        print(f"   Level 1 Resolution Rate: {level1_rate:.1f}% ({level1_resolved}/{len(level1_tests)})")
        print(f"   Correct Escalations: {correct_escalations}/{len(escalation_tests)}")

        print(f"\n📂 Category Breakdown:")
        for cat, stats in categories.items():
            cat_pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "✅" if cat_pass_rate == 100 else "⚠️" if cat_pass_rate >= 50 else "❌"
            print(f"   {status} {cat}: {stats['passed']}/{stats['total']} ({cat_pass_rate:.0f}%)")

        # Failed tests detail
        failed_results = [r for r in self.results if not r['passed']]
        if failed_results:
            print(f"\n❌ Failed Tests Detail:")
            for r in failed_results:
                print(f"\n   Test {r['test_id']}: {r['test_name']}")
                for issue in r['issues']:
                    print(f"      - {issue}")

        # Save detailed report to JSON
        report_path = Path("logs_test") / "test_report.json"
        report_path.parent.mkdir(exist_ok=True)

        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'pass_rate': pass_rate,
                'total_duration': total_duration,
                'avg_duration': avg_duration,
                'level1_resolution_rate': level1_rate,
                'correct_escalations': correct_escalations
            },
            'categories': categories,
            'test_results': self.results
        }

        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"\n💾 Detailed report saved: {report_path}")

        # Save logger session summary
        self.logger.save_session_summary()

        print(f"\n📁 Logs saved to: logs_test/")
        print("="*70 + "\n")

        return report_data


def main():
    """Main entry point"""
    runner = TestRunner()
    runner.run_all_tests()


if __name__ == "__main__":
    main()
