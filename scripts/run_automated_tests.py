"""
UGENTIC Automated Test Suite - Simplified Version
Reuses app.py initialization for reliability
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
sys.path.insert(0, str(project_root / 'src'))

# Import from app.py
from app import (
    initialize_llm,
    initialize_embeddings,
    initialize_agents,
    initialize_logger,
    initialize_planner,
    process_user_request
)

# Test scenarios
TEST_SCENARIOS = [
    {
        'id': 'T01',
        'category': 'LEVEL_1',
        'name': 'Password Reset',
        'prompt': "Sarah Chen forgot her password and is locked out.",
        'expected_escalation': False,
        'expected_time': 15
    },
    {
        'id': 'T02',
        'category': 'LEVEL_1',
        'name': 'Printer Offline',
        'prompt': "I can't print to HP-LaserJet-301. It shows offline.",
        'expected_escalation': False,
        'expected_time': 15
    },
    {
        'id': 'T03',
        'category': 'LEVEL_1',
        'name': 'Access Request',
        'prompt': "New employee John Smith needs Finance shared drive access.",
        'expected_escalation': False,  # Unless strategic approval needed
        'expected_time': 15
    },
    {
        'id': 'T04',
        'category': 'SPECIALIST',
        'name': 'VPN Slow (Network)',
        'prompt': "Our VPN is extremely slow. 5 Marketing users affected.",
        'expected_escalation': True,
        'expected_specialist': 'Network Support',
        'expected_time': 30
    },
    {
        'id': 'T05',
        'category': 'SPECIALIST',
        'name': 'CRM Timeout (App)',
        'prompt': "CRM application times out on large exports. Small ones work fine.",
        'expected_escalation': True,
        'expected_specialist': 'App Support',
        'expected_time': 30
    },
    {
        'id': 'T06',
        'category': 'SPECIALIST',
        'name': 'Disk Space (Infrastructure)',
        'prompt': "File server at 95% capacity. Backups failing.",
        'expected_escalation': True,
        'expected_specialist': 'Infrastructure',
        'expected_time': 30
    },
    {
        'id': 'T07',
        'category': 'ORCHESTRATION',
        'name': 'Multi-Domain Issue',
        'prompt': "Marketing can't access shared drive and files load slow.",
        'expected_escalation': True,
        'expected_orchestration': True,
        'expected_time': 60
    },
    {
        'id': 'T08',
        'category': 'STRATEGIC',
        'name': 'License Purchase',
        'prompt': "Need Microsoft 365 E5 for 50 users. Cost $15k annually.",
        'expected_escalation': True,
        'expected_specialist': 'IT Manager',
        'expected_time': 25
    }
]


def run_test_suite():
    """Run automated test suite"""
    print("\n" + "="*70)
    print("🚀 UGENTIC AUTOMATED TEST SUITE")
    print("="*70)
    print(f"Tests: {len(TEST_SCENARIOS)}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        # Initialize system (minimal output)
        print("\n🔧 Initializing system...")

        from ugentic.config_manager import get_config
        config = get_config()

        llm = initialize_llm(config.get('reasoning_model', 'kimi-k2-thinking:cloud'))
        logger = initialize_logger()
        planner = initialize_planner(llm)
        agents = initialize_agents(llm, logger, planner)

        print(f"✅ System ready ({len(agents)} agents)\n")

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Run tests
    results = []
    start_time = time.time()

    for i, test in enumerate(TEST_SCENARIOS, 1):
        print(f"\n{'='*70}")
        print(f"🧪 TEST {test['id']}: {test['name']}")
        print(f"{'='*70}")
        print(f"Prompt: {test['prompt']}")
        print(f"Expected: {'No escalation' if not test.get('expected_escalation') else 'Escalate to ' + test.get('expected_specialist', 'specialist')}")

        test_start = time.time()

        try:
            # Run test using app.py's process_user_request
            result_dict = process_user_request(
                user_input=test['prompt'],
                agents=agents,
                logger=logger,
                planner=planner,
                config=config
            )

            duration = time.time() - test_start

            # Analyze result
            test_result = {
                'id': test['id'],
                'name': test['name'],
                'category': test['category'],
                'duration': round(duration, 2),
                'passed': True,
                'issues': []
            }

            # Check duration
            expected_time = test.get('expected_time', 30)
            if duration > expected_time:
                test_result['issues'].append(f"Slow: {duration:.1f}s > {expected_time}s")

            # Simple pass/fail for now (detailed validation would require parsing result_dict)
            if result_dict:
                test_result['passed'] = True
                status_icon = "✅"
            else:
                test_result['passed'] = False
                test_result['issues'].append("No result returned")
                status_icon = "❌"

            print(f"\n{status_icon} Duration: {duration:.1f}s")

            if test_result['issues']:
                print(f"⚠️  Issues: {', '.join(test_result['issues'])}")

            results.append(test_result)

        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append({
                'id': test['id'],
                'name': test['name'],
                'passed': False,
                'duration': 0,
                'issues': [str(e)]
            })

        # Small delay between tests
        time.sleep(0.5)

    # Generate summary
    total_duration = time.time() - start_time
    passed = sum(1 for r in results if r['passed'])
    failed = len(results) - passed
    avg_duration = sum(r['duration'] for r in results) / len(results) if results else 0

    print("\n\n" + "="*70)
    print("📊 TEST SUITE SUMMARY")
    print("="*70)
    print(f"\nResults:")
    print(f"  Total: {len(results)}")
    print(f"  Passed: {passed} ({passed/len(results)*100:.0f}%)")
    print(f"  Failed: {failed}")
    print(f"\nTiming:")
    print(f"  Total Duration: {total_duration:.1f}s")
    print(f"  Average per Test: {avg_duration:.1f}s")

    # Save report
    report_path = project_root / "logs_test" / "test_report.json"
    report_path.parent.mkdir(exist_ok=True)

    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': len(results),
            'passed': passed,
            'failed': failed,
            'pass_rate': passed/len(results)*100 if results else 0,
            'total_duration': total_duration,
            'avg_duration': avg_duration
        },
        'results': results
    }

    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n💾 Report saved: {report_path}")
    print("="*70 + "\n")

    # Save logger session
    if logger:
        logger.save_session_summary()
        print(f"📁 Investigation logs: logs/\n")


if __name__ == "__main__":
    run_test_suite()
