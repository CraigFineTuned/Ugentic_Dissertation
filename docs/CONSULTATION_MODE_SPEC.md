# Consultation Mode - Implementation Specification

**Document Version:** 1.0
**Created:** December 3, 2025
**Status:** DESIGN PHASE - Awaiting Code Unfreeze
**Priority:** HIGH (Creative Innovation #1)
**Complexity:** MEDIUM (Est. 3-5 files modified, 200-300 LOC)

---

## 1. EXECUTIVE SUMMARY

**Problem:**
Currently, IT Support must fully escalate tickets to specialists even for simple questions that could be answered quickly through consultation. This creates unnecessary ticket transfers, context loss, and specialist overhead.

**Proposed Solution:**
Implement "Consultation Mode" - a lightweight mechanism allowing IT Support to request specialist advice without transferring ticket ownership. The Level 1 agent maintains ticket control while gaining expert input.

**Business Value:**
- **Efficiency:** Reduce specialist workload by 30-40% (consultations vs full escalations)
- **User Experience:** Faster resolution (no handoff delays)
- **Knowledge Transfer:** Level 1 agents learn from specialist responses
- **Ticket Ownership:** Maintain single point of contact for users

---

## 2. CURRENT SYSTEM BEHAVIOR

### 2.1 Existing Escalation Flow
```
User Issue → IT Support Investigation
             ↓
        [Needs Expert?]
             ↓
     Full Escalation to Service Desk Manager
             ↓
     Routing to Network/App/Infra Specialist
             ↓
     Specialist Takes Ownership
             ↓
     Specialist Resolves & Closes
```

**Problems with Current Flow:**
1. **All or Nothing:** No middle ground between "handle alone" and "full escalation"
2. **Context Loss:** Ticket changes hands 2-3 times (IT Support → Service Desk → Specialist)
3. **Specialist Bottleneck:** Specialists handle tickets that need 30 seconds of advice
4. **No Learning:** IT Support doesn't see specialist's resolution process

---

## 3. PROPOSED CONSULTATION MODE

### 3.1 New Consultation Flow
```
User Issue → IT Support Investigation
             ↓
        [Needs Expert Input?]
             ↓ (YES - Consultation)
     IT Support Requests Consultation
             ↓
     Specialist Provides Advice (No Ownership Transfer)
             ↓
     IT Support Applies Solution
             ↓
     IT Support Resolves & Closes
             ↓
        [Record for Learning]
```

### 3.2 Key Design Principles
1. **Ownership Retention:** IT Support remains ticket owner throughout consultation
2. **Lightweight:** Consultation requests are faster than full escalations
3. **Transparent:** User sees seamless resolution, not handoffs
4. **Bi-directional Learning:** Both parties learn from interaction
5. **Fallback Ready:** Can still fully escalate if consultation insufficient

---

## 4. ARCHITECTURE & INTEGRATION

### 4.1 Components Affected

**Modified Files:**
1. `src/ugentic/agents/react_agents/itsupport_agent_react.py`
   - Add: `request_consultation()` method
   - Add: `_should_consult_vs_escalate()` decision logic
   - Add: `_apply_consultation_advice()` method

2. `src/ugentic/agents/react_agents/service_desk_manager_react.py`
   - Add: `handle_consultation_request()` method
   - Add: `_route_consultation()` (lightweight routing)

3. `src/ugentic/agents/react_agents/network_support_agent_react.py`
   - Add: `provide_consultation()` method
   - Modify: `handle_issue()` to distinguish consultation vs ownership

4. `src/ugentic/agents/react_agents/application_support_agent_react.py`
   - (Same as Network Support)

5. `src/ugentic/agents/react_agents/infrastructure_agent_react.py`
   - (Same as Network Support)

**New Files:**
- `src/ugentic/tools/consultation_tools.py` (Optional: logging/tracking helpers)

### 4.2 Integration Points

```python
# IT Support Agent - New Methods
class ITSupportAgentReAct:
    def _should_consult_vs_escalate(self, problem: str, investigation: Dict) -> tuple:
        """
        Decide if issue needs:
        - Direct resolution (continue investigating)
        - Consultation (quick expert advice)
        - Full escalation (transfer ownership)

        Returns: (action: str, specialist_type: str|None)
        """
        pass

    def request_consultation(self, specialist_type: str, question: str,
                            context: Dict) -> Dict:
        """
        Request quick advice from specialist without transferring ticket.

        Args:
            specialist_type: 'network'|'application'|'infrastructure'
            question: Specific question for specialist
            context: Investigation findings so far

        Returns:
            {
                'advice': str,
                'confidence': float,
                'recommended_action': str,
                'escalate_if_fails': bool
            }
        """
        pass

    def _apply_consultation_advice(self, advice: Dict) -> Dict:
        """Apply specialist's recommended action and verify results."""
        pass


# Service Desk Manager - New Methods
class ServiceDeskManagerReAct:
    def handle_consultation_request(self, request: Dict) -> Dict:
        """
        Route consultation request to appropriate specialist.
        Lighter-weight than full escalation routing.
        """
        specialist_type = request['specialist_type']
        specialist = self._get_specialist_instance(specialist_type)

        return specialist.provide_consultation(
            question=request['question'],
            context=request['context']
        )


# Specialist Agents - New Methods
class NetworkSupportAgentReAct:
    def provide_consultation(self, question: str, context: Dict) -> Dict:
        """
        Provide expert advice without taking ticket ownership.

        Uses LLM to:
        1. Analyze question in context
        2. Provide specific recommendation
        3. Assess if full escalation needed
        """
        prompt = f"""You are a Network Specialist providing consultation to IT Support.

QUESTION: {question}

CONTEXT FROM IT SUPPORT:
{json.dumps(context, indent=2)}

Provide a concise expert recommendation:
1. What is likely causing this issue?
2. What specific action should IT Support take?
3. Should they escalate if this doesn't work?

Keep your response practical and actionable for Level 1 staff."""

        response = self.llm_client.generate(prompt)

        return {
            'advice': response,
            'confidence': self._assess_confidence(question, context),
            'recommended_action': self._extract_action(response),
            'escalate_if_fails': self._should_escalate_on_failure(question)
        }
```

---

## 5. DECISION LOGIC: CONSULT VS ESCALATE

### 5.1 When to Consult (Instead of Escalate)

**Consultation Triggers:**
- Issue involves specialized domain BUT has clear symptoms
- Single verification/action likely resolves issue
- IT Support has done thorough Level 1 investigation
- Question is specific and bounded (not open-ended troubleshooting)

**Examples:**
- "What firewall rule allows RDP traffic to jump server?"
- "Which config file controls Citrix session timeout?"
- "What's the correct VLAN for Building C printers?"
- "Is it safe to restart the SQL Server service during business hours?"

**Full Escalation Triggers:**
- Issue requires multiple specialist actions
- Needs access to specialist-only tools
- Complex multi-step troubleshooting required
- Regulatory/compliance implications

**Examples:**
- "Firewall blocking all traffic from HQ to Branch Office"
- "SQL Server corruption requiring database recovery"
- "Active Directory replication failure across domains"

### 5.2 Implementation Algorithm

```python
def _should_consult_vs_escalate(self, problem: str, investigation: Dict) -> tuple:
    """
    Returns: ('continue'|'consult'|'escalate', specialist_type|None)
    """
    # If resolved or obvious Level 1 issue, continue investigating
    if investigation.get('status') == 'RESOLVED':
        return ('continue', None)

    if self._is_common_level1_issue(problem):
        return ('continue', None)

    # Check if needs specialist tools (full escalation required)
    if self._needs_specialist_tools(problem, investigation):
        specialist = self._suggest_specialist(problem, investigation)
        return ('escalate', specialist)

    # Check if consultation would help
    if self._would_benefit_from_consultation(problem, investigation):
        specialist = self._suggest_specialist(problem, investigation)
        return ('consult', specialist)

    # Default: continue investigating if under iteration threshold
    iterations = investigation.get('iterations', 0)
    if iterations < 3:
        return ('continue', None)

    # Final fallback: escalate
    specialist = self._suggest_specialist(problem, investigation)
    return ('escalate', specialist)


def _would_benefit_from_consultation(self, problem: str, investigation: Dict) -> bool:
    """Check if quick specialist advice would resolve issue."""
    consultation_indicators = [
        'configuration',
        'settings',
        'permission',
        'which server',
        'what port',
        'safe to restart',
        'correct syntax',
        'recommended setting',
    ]

    problem_lower = problem.lower()

    # Has investigation findings but stuck on specialist knowledge
    has_findings = bool(investigation.get('findings'))
    needs_expert_input = any(ind in problem_lower for ind in consultation_indicators)

    return has_findings and needs_expert_input
```

---

## 6. DATA FLOW & MESSAGE STRUCTURE

### 6.1 Consultation Request Format

```python
consultation_request = {
    'type': 'consultation',
    'ticket_id': 'TKT-12345',
    'requester': 'IT Support Agent',
    'specialist_type': 'network',
    'question': 'What firewall rule allows RDP to jump server 192.168.10.5?',
    'context': {
        'user': 'John Smith',
        'symptoms': 'Cannot RDP to jump server, connection times out',
        'investigation_findings': {
            'network_connectivity': 'Ping succeeds',
            'user_permissions': 'User has RemoteDesktop group membership',
            'attempted_actions': ['Verified credentials', 'Checked server status']
        }
    },
    'timestamp': '2025-12-03T14:30:00Z'
}
```

### 6.2 Consultation Response Format

```python
consultation_response = {
    'type': 'consultation_response',
    'ticket_id': 'TKT-12345',
    'specialist': 'Network Support Agent',
    'advice': '''Based on your findings, the issue is likely firewall policy.

RECOMMENDED ACTION:
1. Check if firewall rule "Allow-RDP-JumpServer" is enabled
2. Verify rule includes source IP range 192.168.0.0/16
3. If rule missing, use template "RDP-Access-Standard" and apply to user's subnet

VERIFICATION:
After applying rule, test RDP connection within 5 minutes (rule propagation time).

ESCALATE IF: Rule exists and connection still fails (possible server-side issue).''',
    'confidence': 0.85,
    'recommended_action': 'check_firewall_rule',
    'escalate_if_fails': True,
    'estimated_resolution_time': '5-10 minutes',
    'timestamp': '2025-12-03T14:31:30Z'
}
```

### 6.3 Consultation Outcome Tracking

```python
consultation_outcome = {
    'ticket_id': 'TKT-12345',
    'consultation_id': 'CONSULT-789',
    'specialist_type': 'network',
    'question': 'Firewall rule for RDP access',
    'advice_followed': True,
    'outcome': 'resolved',  # 'resolved'|'escalated'|'still_investigating'
    'resolution_time_seconds': 420,
    'learning_value': 'high',  # For future training/optimization
    'timestamp': '2025-12-03T14:38:00Z'
}
```

---

## 7. IMPLEMENTATION STEPS

### Phase 1: Core Consultation Mechanism (Priority: HIGH)
**Estimated Effort:** 2-3 hours

1. **IT Support Agent - Consultation Request**
   - [ ] Add `_would_benefit_from_consultation()` method
   - [ ] Modify `_should_escalate()` to return 3-way decision
   - [ ] Implement `request_consultation()` method
   - [ ] Add `_apply_consultation_advice()` method

2. **Service Desk Manager - Consultation Routing**
   - [ ] Add `handle_consultation_request()` method
   - [ ] Implement lightweight specialist selection

3. **Specialist Agents - Consultation Response**
   - [ ] Add `provide_consultation()` to NetworkSupportAgentReAct
   - [ ] Add `provide_consultation()` to ApplicationSupportAgentReAct
   - [ ] Add `provide_consultation()` to InfrastructureAgentReAct

### Phase 2: Logging & Analytics (Priority: MEDIUM)
**Estimated Effort:** 1-2 hours

4. **Consultation Tracking**
   - [ ] Create `logs/consultations/` directory
   - [ ] Log all consultation requests/responses
   - [ ] Track consultation success rate
   - [ ] Measure time savings vs full escalation

### Phase 3: Learning & Optimization (Priority: LOW)
**Estimated Effort:** 2-3 hours

5. **Pattern Recognition**
   - [ ] Identify common consultation patterns
   - [ ] Auto-suggest consultations based on history
   - [ ] Improve consultation → escalation threshold

---

## 8. TESTING STRATEGY

### 8.1 Unit Tests

**Test 1: Consultation Decision Logic**
```python
def test_should_consult_for_firewall_question():
    problem = "User cannot RDP to server, what firewall rule is needed?"
    investigation = {
        'findings': ['Ping succeeds', 'Credentials valid'],
        'iterations': 2
    }

    action, specialist = agent._should_consult_vs_escalate(problem, investigation)

    assert action == 'consult'
    assert specialist == 'network'
```

**Test 2: Consultation Request/Response**
```python
def test_consultation_request_response_cycle():
    request = {
        'specialist_type': 'network',
        'question': 'What port does Citrix use?',
        'context': {'user': 'Test User'}
    }

    response = it_support.request_consultation(**request)

    assert 'advice' in response
    assert 'recommended_action' in response
    assert response['confidence'] > 0.7
```

### 8.2 Integration Tests

**Test 3: End-to-End Consultation Flow**
```
INPUT: "User Sarah Chen cannot access VPN. Connection fails with error 0x800.
       I verified her account is active and password is correct.
       What VPN configuration should I check?"

EXPECTED FLOW:
1. IT Support investigates (2 iterations)
2. Decides to consult Network Specialist (not full escalate)
3. Network Specialist provides advice: "Check VPN client version, update to 10.2.4"
4. IT Support applies advice
5. Issue resolved at Level 1
6. No ticket handoff occurred

SUCCESS CRITERIA:
✅ Consultation triggered instead of escalation
✅ Specialist response contains actionable advice
✅ IT Support maintains ticket ownership
✅ Resolution logged with consultation_id
```

**Test 4: Consultation → Escalation Fallback**
```
INPUT: "User cannot print. I checked printer status (online),
       permissions (has access), and driver (up to date).
       Consultation: What else to check?"

SPECIALIST ADVICE: "Check print spooler service status"

IT SUPPORT APPLIES: Print spooler running normally, still can't print

EXPECTED OUTCOME:
- Consultation advice attempted
- Advice didn't resolve issue
- Automatic escalation triggered with context: "Tried specialist consultation, issue persists"
- Specialist takes ownership for deeper troubleshooting

SUCCESS CRITERIA:
✅ Consultation attempted first
✅ Advice applied and tested
✅ Automatic escalation when advice insufficient
✅ Context preserved in escalation
```

### 8.3 Performance Tests

**Test 5: Consultation Speed vs Escalation**
```
METRIC: Time to resolution for issues solvable with specialist advice

BASELINE (Full Escalation):
- IT Support investigation: 3 minutes
- Escalation to Service Desk: 1 minute
- Routing to Specialist: 1 minute
- Specialist investigation: 5 minutes
- Total: ~10 minutes

TARGET (Consultation Mode):
- IT Support investigation: 3 minutes
- Consultation request: 30 seconds
- Specialist advice: 1 minute
- IT Support applies: 2 minutes
- Total: ~6.5 minutes

SUCCESS CRITERIA:
✅ 30-40% time reduction for consultation-eligible issues
✅ No increase in escalation rate for complex issues
✅ Specialist workload reduced (fewer tickets taking ownership)
```

---

## 9. SUCCESS METRICS

### 9.1 Performance Metrics
- **Consultation Success Rate:** % of consultations that resolve issue without escalation (Target: >70%)
- **Time Savings:** Average time saved per consultation vs full escalation (Target: 3-5 min)
- **Specialist Efficiency:** Reduction in specialist-owned tickets (Target: 30-40%)
- **Level 1 Resolution Rate:** Increase in IT Support resolution rate (Target: 80% → 85%+)

### 9.2 Quality Metrics
- **User Satisfaction:** Faster resolution due to no handoffs
- **Context Preservation:** Single point of contact (IT Support throughout)
- **Knowledge Transfer:** IT Support learns from specialist advice (trackable in logs)

### 9.3 System Health Metrics
- **Consultation → Escalation Rate:** % that need full escalation after consultation (Target: <30%)
- **False Consultation Rate:** % of consultations that should have been direct escalations (Target: <10%)
- **Consultation Response Time:** How fast specialists provide advice (Target: <2 min)

---

## 10. ROLLBACK PLAN

### 10.1 Feature Toggle
```python
# config.json
{
    "features": {
        "consultation_mode": {
            "enabled": true,
            "fallback_to_escalation": true,
            "min_confidence_threshold": 0.7
        }
    }
}
```

### 10.2 Rollback Triggers
- Consultation success rate < 50% for 24 hours
- Specialist response time > 5 minutes average
- User satisfaction decrease
- System errors related to consultation routing

### 10.3 Rollback Procedure
1. Set `features.consultation_mode.enabled = false` in config.json
2. Restart agents (or hot-reload config)
3. All consultation attempts automatically fallback to full escalation
4. Monitor logs for stability
5. Investigate root cause

---

## 11. FUTURE ENHANCEMENTS

### 11.1 Consultation Templates (Phase 2)
```python
# Pre-defined consultation patterns for common scenarios
consultation_templates = {
    'firewall_rule_check': {
        'specialist': 'network',
        'question_template': 'What firewall rule allows {protocol} to {destination}?',
        'expected_response_time': 60  # seconds
    },
    'permission_verification': {
        'specialist': 'infrastructure',
        'question_template': 'Does user {username} have {permission} on {resource}?',
        'expected_response_time': 90
    }
}
```

### 11.2 Multi-Specialist Consultations (Phase 3)
- Consult multiple specialists simultaneously for multi-domain issues
- Aggregate responses and identify consensus
- Example: "Slow application performance" → Consult Network + Application + Infrastructure

### 11.3 Consultation Learning (Phase 4)
- Build consultation knowledge base from successful patterns
- Auto-suggest consultations based on similar past tickets
- Train LLM on consultation outcomes to improve advice quality

---

## 12. DEPENDENCIES & PREREQUISITES

### 12.1 Technical Dependencies
- ✅ Existing specialist agent infrastructure
- ✅ LLM client for generating consultation responses
- ✅ Logging infrastructure for tracking
- ⚠️ May need: Inter-agent communication protocol enhancement

### 12.2 Design Dependencies
- ✅ Current escalation logic (as reference/fallback)
- ✅ Tool registry (no new tools required initially)
- ✅ ReAct engine (consultation uses same reasoning pattern)

### 12.3 Testing Dependencies
- ✅ Manual test prompts (extend TEST_PROMPTS_DEC3.md)
- ⚠️ Automated test framework (pending Windows Unicode fix)

---

## 13. RISK ASSESSMENT

### 13.1 Technical Risks

**RISK: Consultation loops (IT Support → Specialist → IT Support → ...)**
- **Mitigation:** Limit consultations per ticket (max 2), automatic escalation after
- **Severity:** MEDIUM

**RISK: Specialist advice quality varies (LLM hallucination)**
- **Mitigation:** Confidence scoring, validation against knowledge base, escalate if low confidence
- **Severity:** MEDIUM

**RISK: Performance degradation (additional LLM calls)**
- **Mitigation:** Async consultation, caching common responses, parallel specialist queries
- **Severity:** LOW

### 13.2 Operational Risks

**RISK: False consultations (should have escalated directly)**
- **Mitigation:** Track consultation → escalation rate, tune thresholds
- **Severity:** LOW

**RISK: Specialist overload (too many consultation requests)**
- **Mitigation:** Rate limiting, queue management, fallback to escalation
- **Severity:** LOW

---

## 14. APPROVAL CHECKLIST

**Before Implementation:**
- [ ] User approval obtained for code unfreeze
- [ ] Specification reviewed and accepted
- [ ] Test scenarios validated
- [ ] Rollback plan confirmed

**During Implementation:**
- [ ] Follow Ubuntu philosophy (collaborative development)
- [ ] Maintain code quality standards (type hints, logging, error handling)
- [ ] Update AGENTS.md with new methods
- [ ] Update ARCHITECTURE.md with consultation flow diagram
- [ ] Create/update unit tests for new methods

**After Implementation:**
- [ ] Run all existing tests (ensure no regressions)
- [ ] Run consultation-specific tests (8.1, 8.2, 8.3)
- [ ] Update SESSION_ENTRY.md with implementation status
- [ ] Monitor logs for consultation patterns
- [ ] Measure success metrics (9.1, 9.2, 9.3)

---

## 15. REFERENCES

**Related Documents:**
- `docs/SESSION_ENTRY.md` - Project nucleus (line 173-176: Creative Innovations)
- `docs/SESSION_COMPLETE_DEC3.md` - Detailed creative innovation descriptions
- `docs/AGENTS.md` - Current agent architecture (Version 2.0)
- `docs/ARCHITECTURE.md` - System design and escalation flow
- `src/ugentic/agents/react_agents/itsupport_agent_react.py` - IT Support implementation
- `src/ugentic/agents/react_agents/service_desk_manager_react.py` - Service Desk routing

**Key Concepts:**
- **Ubuntu Philosophy:** Collective intelligence ("I am because we are")
- **ReAct Pattern:** Reasoning + Acting for LLM-guided decisions
- **Level 1-2-3 Model:** IT Support → Service Desk → Specialists → IT Manager

---

**Document Status:** ✅ COMPLETE - Ready for Implementation Review
**Next Action:** Await user approval for code unfreeze, then proceed with Phase 1 implementation
**Estimated Total Implementation Time:** 5-8 hours (all phases)

---
*Specification authored by: Claude Sonnet 4.5*
*Project: UGENTIC - Ubuntu-Driven Multi-Agent IT Support System*
*Dissertation: Craig Vraagom (402415017)*
