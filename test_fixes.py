"""
Simple test runner to validate Dec 3 bug fixes
Runs directly from project root
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import json
import time
from datetime import datetime

from langchain_ollama import ChatOllama
from src.ugentic.config_manager import get_config
from src.ugentic.agents.react_agents import (
    ITSupportAgentReAct,
    ServiceDeskManagerAgentReAct,
    ITManagerAgentReAct,
    NetworkSupportAgentReAct,
    AppSupportAgentReAct,
    InfrastructureAgentReAct
)
from src.ugentic.utils.investigation_logger import InvestigationLogger

# Test prompts
TESTS = [
    {
        'id': 'T01',
        'name': 'Password Reset (Level 1)',
        'prompt': "Sarah Chen forgot her password and is locked out.",
        'expect': 'no_escalation'
    },
    {
        'id': 'T02',
        'name': 'Printer Offline (Level 1)',
        'prompt': "Can't print to HP-LaserJet-301. Shows offline.",
        'expect': 'no_escalation'
    },
    {
        'id': 'T03',
        'name': 'VPN Slow (Network Specialist)',
        'prompt': "VPN extremely slow. 5 users affected in Marketing.",
        'expect': 'escalate_network'
    },
    {
        'id': 'T04',
        'name': 'CRM Timeout (App Specialist)',
        'prompt': "CRM times out on large exports.",
        'expect': 'escalate_app'
    },
    {
        'id': 'T05',
        'name': 'Disk Full (Infrastructure)',
        'prompt': "File server 95% full. Backups failing.",
        'expect': 'escalate_infra'
    }
]


def main():
    print("\n" + "="*70)
    print("UGENTIC BUG FIX VALIDATION - Dec 3, 2025")
    print("="*70)
    print(f"Tests: {len(TESTS)}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")

    # Initialize
    print("Initializing...")
    try:
        config = get_config()
        model = config.get('reasoning_model', 'kimi-k2-thinking:cloud')

        llm = ChatOllama(model=model, temperature=0.1)
        logger = InvestigationLogger(base_dir="logs_test")

        # Create agents (minimal set)
        agents = {
            'IT Support': ITSupportAgentReAct(llm=llm, logger=logger),
            'Service Desk Manager': ServiceDeskManagerAgentReAct(llm=llm, logger=logger),
            'Network Support': NetworkSupportAgentReAct(llm=llm, logger=logger),
            'App Support': AppSupportAgentReAct(llm=llm, logger=logger),
            'Infrastructure': InfrastructureAgentReAct(llm=llm, logger=logger)
        }

        print(f"[OK] Ready ({len(agents)} agents)\n")

    except Exception as e:
        print(f"[ERROR] Init failed: {e}")
        return

    # Run tests
    results = []
    for i, test in enumerate(TESTS, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}/{len(TESTS)}: {test['name']}")
        print(f"{'='*70}")
        print(f"Prompt: {test['prompt']}")

        start = time.time()

        try:
            # Run investigation
            it_support = agents['IT Support']
            result = it_support.investigate(test['prompt'], context={'test_id': test['id']})

            duration = time.time() - start

            # Analyze
            status = result.get('status')
            escalated = (status == 'NEEDS_ESCALATION')

            test_result = {
                'id': test['id'],
                'name': test['name'],
                'duration': round(duration, 1),
                'status': status,
                'escalated': escalated,
                'passed': True
            }

            # Validation
            if test['expect'] == 'no_escalation':
                if escalated:
                    test_result['passed'] = False
                    test_result['issue'] = "Should NOT escalate (Level 1 issue)"
                else:
                    test_result['note'] = " Correctly resolved at Level 1"

            elif test['expect'].startswith('escalate_'):
                if not escalated:
                    test_result['passed'] = False
                    test_result['issue'] = "Should escalate to specialist"
                else:
                    # Check routing
                    escalation = result.get('escalation_details', {})
                    suggested = escalation.get('suggested_specialist', '')

                    if test['expect'] == 'escalate_network':
                        expected_spec = 'Network Support'
                    elif test['expect'] == 'escalate_app':
                        expected_spec = 'App Support'
                    elif test['expect'] == 'escalate_infra':
                        expected_spec = 'Infrastructure'
                    else:
                        expected_spec = ''

                    if expected_spec and expected_spec in suggested:
                        test_result['note'] = f" Correctly routed to {expected_spec}"
                        test_result['specialist'] = suggested
                    else:
                        test_result['passed'] = False
                        test_result['issue'] = f"Wrong specialist: expected {expected_spec}, got {suggested}"
                        test_result['specialist'] = suggested

            # Print result
            icon = "" if test_result['passed'] else ""
            print(f"\n{icon} {test_result.get('note', test_result.get('issue', 'Complete'))}")
            print(f"   Duration: {duration:.1f}s")
            print(f"   Status: {status}")

            if escalated:
                print(f"   Escalated: Yes")
                if 'specialist' in test_result:
                    print(f"   Routed to: {test_result['specialist']}")

            results.append(test_result)

        except Exception as e:
            print(f" Error: {e}")
            results.append({
                'id': test['id'],
                'name': test['name'],
                'passed': False,
                'error': str(e)
            })

    # Summary
    passed = sum(1 for r in results if r.get('passed', False))
    total = len(results)
    avg_time = sum(r.get('duration', 0) for r in results) / total if total > 0 else 0

    print("\n\n" + "="*70)
    print(" SUMMARY")
    print("="*70)
    print(f"\nResults: {passed}/{total} passed ({passed/total*100:.0f}%)")
    print(f"Avg Time: {avg_time:.1f}s")

    # Category breakdown
    level1_tests = [r for r in results if 'Level 1' in r['name']]
    level1_passed = sum(1 for r in level1_tests if r.get('passed', False))
    if level1_tests:
        print(f"\nLevel 1 Resolution: {level1_passed}/{len(level1_tests)} ({level1_passed/len(level1_tests)*100:.0f}%)")

    specialist_tests = [r for r in results if 'Specialist' in r['name'] or any(x in r['name'] for x in ['Network', 'App', 'Infrastructure'])]
    specialist_passed = sum(1 for r in specialist_tests if r.get('passed', False))
    if specialist_tests:
        print(f"Specialist Routing: {specialist_passed}/{len(specialist_tests)} ({specialist_passed/len(specialist_tests)*100:.0f}%)")

    # Failed tests
    failed = [r for r in results if not r.get('passed', False)]
    if failed:
        print(f"\n Failed Tests:")
        for r in failed:
            print(f"   {r['id']}: {r['name']}")
            if 'issue' in r:
                print(f"      Issue: {r['issue']}")
            if 'error' in r:
                print(f"      Error: {r['error']}")

    # Save report
    report_path = Path("logs_test/quick_test_report.json")
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': total,
                'passed': passed,
                'failed': total - passed,
                'pass_rate': passed/total*100 if total > 0 else 0,
                'avg_duration': avg_time
            },
            'results': results
        }, f, indent=2)

    print(f"\n Report: {report_path}")
    print("="*70 + "\n")

    # Save logger session
    logger.save_session_summary()
    print(f" Logs: logs_test/\n")


if __name__ == "__main__":
    main()
