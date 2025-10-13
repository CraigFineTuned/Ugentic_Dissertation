# Application Support Playbook

**Purpose:** This playbook provides detailed information about business applications, common issues, troubleshooting procedures, and escalation paths for the Application Support specialist.

**Last Updated:** [Date]  
**Maintained By:** Application Support Team

---

## 1. APPLICATION INVENTORY

### Critical Business Applications

#### [Application Name 1]
- **Type:** [e.g., POS System, CRM, Database, etc.]
- **Vendor:** [Vendor name]
- **Version:** [Current version]
- **Business Owner:** [Department/Person]
- **Technical Owner:** [IT contact]
- **Criticality:** [High/Medium/Low]
- **Users:** [Number and type of users]
- **Uptime Requirement:** [e.g., 99.9%, 24/7, Business hours]
- **Dependencies:** [Other systems, databases, network requirements]

#### [Application Name 2]
- **Type:** 
- **Vendor:** 
- **Version:** 
- **Business Owner:** 
- **Technical Owner:** 
- **Criticality:** 
- **Users:** 
- **Uptime Requirement:** 
- **Dependencies:** 

#### [Application Name 3]
- **Type:** 
- **Vendor:** 
- **Version:** 
- **Business Owner:** 
- **Technical Owner:** 
- **Criticality:** 
- **Users:** 
- **Uptime Requirement:** 
- **Dependencies:** 

---

## 2. COMMON ISSUES AND SOLUTIONS

### [Application Name 1]

#### Issue: [e.g., "Slow Login Performance"]
- **Symptoms:** [How users describe the problem]
- **Frequency:** [How often this occurs]
- **Impact:** [What business processes are affected]
- **Troubleshooting Steps:**
  1. [First diagnostic step]
  2. [Second diagnostic step]
  3. [Third diagnostic step]
- **Common Causes:**
  - [Cause 1 with explanation]
  - [Cause 2 with explanation]
- **Resolution:**
  - [Solution approach]
  - [Expected time to resolve]
- **Escalation Criteria:** [When to escalate to vendor or Infrastructure]
- **Known Workarounds:** [Temporary fixes users can apply]

#### Issue: [e.g., "Cannot Access Reports"]
- **Symptoms:** 
- **Frequency:** 
- **Impact:** 
- **Troubleshooting Steps:**
  1. 
  2. 
  3. 
- **Common Causes:**
  - 
  - 
- **Resolution:**
  - 
  - 
- **Escalation Criteria:** 
- **Known Workarounds:** 

### [Application Name 2]

#### Issue: [Common issue name]
- **Symptoms:** 
- **Frequency:** 
- **Impact:** 
- **Troubleshooting Steps:**
  1. 
  2. 
  3. 
- **Common Causes:**
  - 
  - 
- **Resolution:**
  - 
  - 
- **Escalation Criteria:** 
- **Known Workarounds:** 

---

## 3. DIAGNOSTIC PROCEDURES

### Performance Investigation

**When to Use:** Application is slow or unresponsive

**Step-by-Step Process:**
1. **Verify Scope**
   - [ ] Ask: Is this affecting one user or multiple users?
   - [ ] Ask: When did the slowness start?
   - [ ] Ask: What specific action is slow?

2. **Check Application Health**
   - [ ] Use tool: `check_app_availability` to verify uptime
   - [ ] Use tool: `check_app_response_time` to measure latency
   - [ ] Check application error logs for recent errors

3. **Check Infrastructure**
   - [ ] Collaborate with Infrastructure: Check server CPU/memory/disk
   - [ ] Collaborate with Network: Check network latency to app server
   - [ ] Verify database performance (if applicable)

4. **Identify Root Cause**
   - [ ] Application code issue → Escalate to vendor
   - [ ] Database performance → Optimize queries or add resources
   - [ ] Network latency → Collaborate with Network team
   - [ ] Server resources → Collaborate with Infrastructure team

5. **Document Findings**
   - Log the investigation in the ticketing system
   - Note any patterns or correlations discovered
   - Update this playbook if new issue type identified

### Availability Investigation

**When to Use:** Application is down or users cannot connect

**Step-by-Step Process:**
1. **Confirm Outage**
   - [ ] Verify from multiple locations/users
   - [ ] Check: Is it complete outage or partial?
   - [ ] Check: Does the application respond at all?

2. **Check Basic Connectivity**
   - [ ] Use tool: `check_app_availability`
   - [ ] Ping the application server
   - [ ] Verify DNS resolution

3. **Identify Failure Point**
   - [ ] Application service stopped → Restart service
   - [ ] Server down → Collaborate with Infrastructure
   - [ ] Network issue → Collaborate with Network
   - [ ] Database unavailable → Check database status

4. **Restore Service**
   - [ ] Apply fix based on identified cause
   - [ ] Verify application fully functional
   - [ ] Monitor for stability

5. **Post-Incident Review**
   - Document root cause
   - Identify prevention measures
   - Update disaster recovery procedures if needed

---

## 4. ACCESS AND PERMISSIONS

### [Application Name 1] Access Levels

#### Role: [e.g., "Basic User"]
- **Permissions:** [What they can do]
- **How to Grant:** [Step-by-step process or system used]
- **Approval Required:** [Who must approve]
- **Common Issues:** [Access problems users face]

#### Role: [e.g., "Power User"]
- **Permissions:** 
- **How to Grant:** 
- **Approval Required:** 
- **Common Issues:** 

#### Role: [e.g., "Administrator"]
- **Permissions:** 
- **How to Grant:** 
- **Approval Required:** 
- **Common Issues:** 

### Access Request Process
1. [Step 1 of access request workflow]
2. [Step 2 of access request workflow]
3. [Step 3 of access request workflow]

---

## 5. INTEGRATION POINTS

### [Application Name 1] Integrations

#### Integration: [e.g., "Data Sync to Data Warehouse"]
- **Direction:** [One-way / Two-way / Real-time / Batch]
- **Schedule:** [When it runs]
- **Dependencies:** [What it relies on]
- **Failure Symptoms:** [How you know it's broken]
- **Troubleshooting:** [How to diagnose/fix]
- **Business Impact:** [What happens if it fails]

#### Integration: [e.g., "SSO with Active Directory"]
- **Direction:** 
- **Schedule:** 
- **Dependencies:** 
- **Failure Symptoms:** 
- **Troubleshooting:** 
- **Business Impact:** 

---

## 6. MAINTENANCE WINDOWS

### Scheduled Maintenance

#### [Application Name 1]
- **Frequency:** [e.g., Monthly, Quarterly]
- **Duration:** [Typical downtime]
- **Day/Time:** [When it happens]
- **Pre-Maintenance Checklist:**
  - [ ] [Task 1]
  - [ ] [Task 2]
  - [ ] [Task 3]
- **Post-Maintenance Verification:**
  - [ ] [Verification 1]
  - [ ] [Verification 2]
  - [ ] [Verification 3]
- **Rollback Plan:** [How to revert if issues occur]

### Patching Schedule

#### [Application Name]
- **Patch Type:** [Security / Feature / Bug Fix]
- **Testing Required:** [Yes/No - where to test]
- **Approval Process:** [Who approves patches]
- **Deployment Window:** [When patches are applied]

---

## 7. DISASTER RECOVERY PROCEDURES

### [Application Name 1] Recovery

#### Recovery Time Objective (RTO)
- **Target:** [e.g., 4 hours]
- **Business Justification:** [Why this target]

#### Recovery Point Objective (RPO)
- **Target:** [e.g., 1 hour - max data loss acceptable]
- **Backup Frequency:** [How often backups occur]

#### Disaster Scenarios

**Scenario: Database Corruption**
1. [Step 1 to recover]
2. [Step 2 to recover]
3. [Step 3 to recover]

**Scenario: Application Server Failure**
1. 
2. 
3. 

**Scenario: Complete Data Center Outage**
1. 
2. 
3. 

---

## 8. MONITORING AND ALERTING

### Key Performance Indicators (KPIs)

#### [Application Name 1]
- **Availability Target:** [e.g., 99.9%]
- **Response Time Target:** [e.g., < 2 seconds]
- **Error Rate Target:** [e.g., < 0.1%]
- **Concurrent Users:** [Expected load]

### Alert Thresholds

#### Critical Alerts (Immediate Action Required)
- Application down for > [X] minutes
- Response time > [Y] seconds
- Error rate > [Z]%
- [Other critical threshold]

#### Warning Alerts (Investigate Soon)
- Response time > [Y] seconds for > [X] minutes
- Error rate trending upward
- [Other warning threshold]

### Monitoring Tools
- **Tool Name:** [What it monitors]
- **Access:** [How to access it]
- **Dashboard:** [Key metrics to watch]

---

## 9. CHANGE MANAGEMENT

### Change Categories

#### Standard Changes (Pre-Approved)
- [Type of change - e.g., Password reset]
- [Type of change - e.g., Add user access]
- [Type of change - e.g., Restart service]

#### Normal Changes (Requires Approval)
- [Type of change - e.g., Version upgrade]
- [Type of change - e.g., Configuration change]
- [Type of change - e.g., New integration]

#### Emergency Changes (Expedited Process)
- [Type of change - e.g., Security patch]
- [Type of change - e.g., Critical bug fix]

### Change Request Process
1. **Document Change**
   - What is changing
   - Why it's needed
   - Risk assessment
   - Rollback plan

2. **Get Approval**
   - [Who approves what types of changes]
   - [Approval timeline]

3. **Implement Change**
   - Schedule during appropriate window
   - Follow documented procedure
   - Have rollback plan ready

4. **Verify and Document**
   - Test functionality
   - Document results
   - Update configuration documentation

---

## 10. COLLABORATION SCENARIOS

### When to Collaborate with Infrastructure Team
- Application server performance issues (CPU, memory, disk)
- Need to restart services on the server
- Server capacity planning
- Virtual machine provisioning or changes
- Storage expansion requirements

### When to Collaborate with Network Team
- Application connectivity issues
- Network latency affecting application performance
- Firewall rule changes needed
- VPN access for remote application access
- Load balancer configuration

### When to Collaborate with Service Desk
- User training needs identified
- Pattern of similar user issues (requires communication)
- Application access process changes
- Major outage communications to users

### When to Collaborate with IT Manager
- Budget needed for licenses or upgrades
- Strategic decisions about application roadmap
- Risk assessment for major changes
- Resource allocation decisions
- Vendor relationship escalations

---

## 11. VENDOR CONTACT INFORMATION

(See separate document: `02-03_Vendor_Escalation_Contacts.md` for detailed vendor information)

### Quick Reference

#### [Application Name 1]
- **Vendor:** [Name]
- **Support Portal:** [URL]
- **Emergency Phone:** [Number]
- **Escalation Process:** [Brief overview]

#### [Application Name 2]
- **Vendor:** 
- **Support Portal:** 
- **Emergency Phone:** 
- **Escalation Process:** 

---

## 12. FREQUENTLY ASKED QUESTIONS (FAQ)

### General Application Support

**Q: How do I know if I should troubleshoot myself or escalate immediately?**
A: [Answer based on your procedures]

**Q: What information should I collect before escalating to a vendor?**
A: [List of information needed]

**Q: How do I determine if an issue requires collaboration with other teams?**
A: [Guidelines for collaboration decision]

### [Application Name 1] Specific

**Q: [Common question about this application]**
A: [Answer]

**Q: [Another common question]**
A: [Answer]

---

## 13. TRAINING AND RESOURCES

### Internal Documentation
- [Link or location of detailed technical documentation]
- [Link to runbook or procedure documents]
- [Link to architecture diagrams]

### Vendor Resources
- [Vendor knowledge base URL]
- [Vendor training portal URL]
- [Vendor community forum URL]

### Team Knowledge Sharing
- [Where to find lessons learned from past incidents]
- [Team wiki or shared documentation location]
- [Regular team meeting schedule for knowledge sharing]

---

## 14. GLOSSARY

### Application-Specific Terms

**[Term 1]:** [Definition]

**[Term 2]:** [Definition]

**[Term 3]:** [Definition]

### IT Industry Terms (Common in Application Support)

**SLA (Service Level Agreement):** Expected uptime and performance standards

**RTO (Recovery Time Objective):** Maximum acceptable time to restore service after an outage

**RPO (Recovery Point Objective):** Maximum acceptable amount of data loss measured in time

**API (Application Programming Interface):** How applications communicate with each other

---

## NOTES FOR USING THIS PLAYBOOK

**For the AI Agent:**
- This playbook is your primary reference for application-specific knowledge
- Always check this document before troubleshooting an application issue
- Use the diagnostic procedures as a guide, but apply ubuntu principles to collaborate when needed
- Update this document with new learnings from incidents

**For Maintenance:**
- Review and update quarterly or after major incidents
- Add new applications as they are deployed
- Remove or archive retired applications
- Keep vendor contact information current
- Document new issues and solutions as they are discovered

**For Populating This Template:**
- Start with your most critical applications
- Add detail incrementally as you handle incidents
- Include real examples from your environment
- Don't worry about completing everything at once - this is a living document

---

**Template Status:** Ready for population  
**Priority:** Start with critical business applications  
**Estimated Time to Complete:** Incremental - add detail over multiple sessions  
**Next Steps:** Begin with Application Name 1 inventory and common issues
