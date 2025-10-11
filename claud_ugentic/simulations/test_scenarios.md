# UGENTIC TEST SCENARIOS

**Purpose:** Comprehensive test cases to validate the simulation environment

---

## 🎯 HOW TO USE THESE SCENARIOS

Point Claude to `SIMULATION_MASTER.md` and provide any scenario below. Claude will simulate the complete agent response including delegation, Ubuntu collaboration, and resolution.

**Format:**
```
"Read SIMULATION_MASTER.md and simulate: [scenario from below]"
```

---

## ✅ TIER 1: SIMPLE SCENARIOS (Single Agent)

### S1.1: Password Reset
**Query:** "I forgot my password and cannot log into my computer"

**Expected Flow:**
- IT Manager → Service Desk Manager → IT Support
- IT Support handles independently (standard procedure)
- Quick resolution
- User educated on self-service portal

**Ubuntu Elements:**
- Knowledge base check (someone documented this before)
- User-friendly communication
- Documentation review if any edge cases

---

### S1.2: Software Installation Request
**Query:** "I need Microsoft Teams installed on my laptop"

**Expected Flow:**
- IT Manager → Service Desk Manager → IT Support
- IT Support handles standard installation
- Verifies license availability
- User training on application basics

**Ubuntu Elements:**
- Check knowledge base for installation procedure
- Document any issues encountered
- Share with team if novel aspects arise

---

## 🔧 TIER 2: MODERATE SCENARIOS (Some Collaboration)

### S2.1: Email Sync Issues
**Query:** "My email works on desktop but not on my phone"

**Expected Flow:**
- IT Manager → Service Desk Manager → IT Support
- IT Support initial diagnosis
- Collaborates with Network Support (connectivity) and/or Infrastructure (server settings)
- Collective diagnosis reveals certificate or configuration issue
- Multi-agent resolution

**Ubuntu Elements:**
- Proactive collaboration when root cause unclear
- Cross-domain knowledge sharing
- Documented for future similar cases

---

### S2.2: Slow Application Performance
**Query:** "The CRM application has been really slow for the past hour"

**Expected Flow:**
- IT Manager → App Support
- App Support checks application
- Collaborates with Infrastructure (database/server check)
- May involve Network Support if connectivity-related
- Collective diagnosis and resolution

**Ubuntu Elements:**
- Multi-domain collaboration
- Shared expertise (app + infrastructure + possibly network)
- Knowledge captured about performance bottlenecks

---

### S2.3: VPN Connection Problems
**Query:** "I cannot connect to the company VPN from home"

**Expected Flow:**
- IT Manager → Network Support
- Network Support diagnoses VPN infrastructure
- Coordinates with IT Support for user-specific settings
- May involve Infrastructure if VPN server issues

**Ubuntu Elements:**
- Network expertise + user support coordination
- User-friendly communication from IT Support
- Technical resolution from Network Support

---

## 🔥 TIER 3: COMPLEX SCENARIOS (Heavy Collaboration)

### S3.1: System-Wide Slowness
**Query:** "Multiple users across departments are reporting that everything is running slow"

**Expected Flow:**
- IT Manager → Initiates Ubuntu multi-agent collaboration
- Infrastructure: Checks server resources and capacity
- Network Support: Analyzes network traffic and connectivity
- App Support: Reviews application performance metrics
- IT Support: Gathers user reports for pattern identification
- Collective diagnosis reveals root cause
- Coordinated resolution across teams

**Ubuntu Elements:**
- Full multi-agent collaboration
- Collective problem-solving
- Knowledge sharing across all domains
- Comprehensive documentation

**Possible Root Causes (for simulation variety):**
- Network configuration change
- Server capacity issue
- Database query optimization needed
- Network bandwidth saturation
- Combination of factors

---

### S3.2: Application Deployment Issue
**Query:** "We need to deploy a major update to the accounting software this weekend"

**Expected Flow:**
- IT Manager → Strategic initiative, involves all relevant teams
- App Support: Leads deployment planning and testing
- Infrastructure: Prepares servers, ensures capacity
- Network Support: Ensures network can handle load
- Service Desk Manager + IT Support: Plans user communication and support
- Consensus building on timing, approach, rollback plans
- Coordinated execution

**Ubuntu Elements:**
- Strategic consensus building
- All teams contribute their expertise
- Shared ownership of success
- Comprehensive planning
- Risk mitigation through collaboration

---

### S3.3: Security Incident Response
**Query:** "We detected unusual network traffic that might indicate a security breach"

**Expected Flow:**
- IT Manager → URGENT all-hands collaboration
- Network Support: Analyzes traffic patterns, identifies source
- Infrastructure: Checks server logs, isolates affected systems
- App Support: Reviews application access logs
- IT Support: Prepares user communications, monitors for user impact
- Rapid collective response
- Post-incident collaborative analysis

**Ubuntu Elements:**
- Crisis management collaboration
- Rapid knowledge sharing
- Collective security response
- Comprehensive post-mortem
- Lessons learned documented

---

## 💡 TIER 4: STRATEGIC SCENARIOS (Planning & Consensus)

### S4.1: Infrastructure Upgrade Planning
**Query:** "We need to plan a major server upgrade for next quarter"

**Expected Flow:**
- IT Manager → Leads strategic planning with all teams
- Infrastructure: Technical requirements, capacity planning
- App Support: Application compatibility, testing needs
- Network Support: Network requirements, connectivity implications
- Service Desk Manager: User impact assessment, communication planning
- Consensus building on approach, timing, budget
- Collaborative implementation plan

**Ubuntu Elements:**
- Full consensus building
- All perspectives valued
- Strategic collective decision-making
- Shared ownership
- Transparent planning process

---

### S4.2: New Technology Evaluation
**Query:** "Should we migrate our email system to the cloud?"

**Expected Flow:**
- IT Manager → Strategic decision requiring collective input
- App Support: Technical feasibility, migration complexity
- Infrastructure: Current infrastructure assessment, cost implications
- Network Support: Bandwidth requirements, security considerations
- IT Support: User training needs, change management
- Collaborative evaluation
- Consensus recommendation to leadership

**Ubuntu Elements:**
- Strategic collaboration
- All expertise contributes
- Collective wisdom shapes decision
- Transparent decision-making
- Documented rationale

---

## 🎓 TIER 5: LEARNING & GROWTH SCENARIOS

### S5.1: Knowledge Transfer Session
**Query:** "Can someone teach me how to troubleshoot database connection issues?"

**Expected Flow:**
- IT Manager → Routes to App Support (database expertise)
- App Support teaches, not just solves
- May involve Infrastructure for server-side perspective
- Documentation created for team benefit
- Knowledge multiplicates

**Ubuntu Elements:**
- Teaching, not just telling
- Knowledge sharing as priority
- Documented for collective benefit
- Multiple perspectives shared

---

### S5.2: Process Improvement Initiative
**Query:** "We're getting too many password reset requests. How can we improve this?"

**Expected Flow:**
- Service Desk Manager → Facilitates team discussion
- IT Support: Shares patterns observed
- App Support: Self-service portal options?
- Collective brainstorming
- Consensus on improvement approach
- Implementation with team buy-in

**Ubuntu Elements:**
- Bottom-up improvement
- Collective problem-solving
- Consensus on solution
- Team ownership of process

---

## 🧪 TIER 6: EDGE CASES & STRESS TESTS

### S6.1: Conflicting Priorities
**Query:** "Both the CRM team and Finance need urgent support simultaneously, but we only have one App Support specialist available"

**Expected Flow:**
- Service Desk Manager → Coordinates prioritization
- Consults affected teams for impact assessment
- May involve IT Manager for strategic priority call
- Transparent communication to both requesters
- Ubuntu mutual support (can other agents help with simpler aspects?)
- Fair resolution with explanation

**Ubuntu Elements:**
- Transparent priority decision
- Fair resource allocation
- Mutual support exploration
- Honest communication

---

### S6.2: Knowledge Gap
**Query:** "We're encountering an error we've never seen before and can't find documentation"

**Expected Flow:**
- Receiving agent → Checks knowledge base (not found)
- Initiates collaboration for collective diagnosis
- Uses Research tool for external knowledge
- Team works together to solve
- **CRITICAL:** Solution thoroughly documented for future
- Team celebrates collective discovery

**Ubuntu Elements:**
- Admit when knowledge is lacking
- Collaborate rather than struggle alone
- External knowledge sought
- Learning captured and shared
- Community grows stronger

---

## 📊 VALIDATION CRITERIA

For each simulation, verify:

### Correct Routing
- [ ] Request went to appropriate agent(s)
- [ ] Delegation followed hierarchy
- [ ] Collaboration triggered when needed

### Ubuntu Principles
- [ ] Collective problem-solving visible
- [ ] Knowledge sharing demonstrated
- [ ] Mutual support evident
- [ ] Consensus building (if applicable)

### Complete Workflow
- [ ] Request received
- [ ] Analysis performed
- [ ] Decision made
- [ ] Collaboration initiated (if needed)
- [ ] Resolution achieved
- [ ] Knowledge captured
- [ ] Documentation updated

### Quality of Output
- [ ] Reasoning is clear
- [ ] Ubuntu principles explained
- [ ] Tools used appropriately
- [ ] Communication professional
- [ ] Learning documented

---

## 🚀 QUICK TEST COMMANDS

### For Quick Testing:
```
"Simulate S1.1" (references this doc)
or
"Simulate: I forgot my password"
```

### For Detailed Analysis:
```
"Mode 2 (Detailed): Simulate S3.1"
```

### For Step-by-Step:
```
"Mode 3: Simulate S4.1 step by step"
```

### For Multiple Scenarios:
```
"Run simulations for S1.1, S2.1, and S3.1 and compare approaches"
```

---

## 📝 NOTES FOR DISSERTATION

These scenarios demonstrate:

1. **Scalability:** From simple to complex
2. **Flexibility:** Different types of requests
3. **Ubuntu Integration:** Visible in all tiers
4. **Real-world Relevance:** Based on actual IT scenarios
5. **Measurable Outcomes:** Clear success criteria

**Use these in:**
- Chapter 4 (Implementation): Show system design
- Chapter 5 (Results): Demonstrate Ubuntu in action
- Defense Presentation: Live simulation examples
- Appendix: Complete test coverage documentation

---

## 🎯 CREATING YOUR OWN SCENARIOS

**Format:**
```
SCENARIO: [Brief title]
QUERY: [Exact user request]
EXPECTED AGENTS: [Who should be involved]
EXPECTED COLLABORATION: [Type of Ubuntu principles]
EXPECTED OUTCOME: [What should happen]
```

Then simulate and validate!

---

**These scenarios provide comprehensive test coverage for the UGENTIC simulation environment. Start with Tier 1 for basics, progress through tiers as confidence grows.**
