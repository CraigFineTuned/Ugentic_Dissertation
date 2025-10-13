# Disaster Recovery Plan

**Purpose:** This document provides comprehensive disaster recovery procedures, business continuity planning, and emergency response protocols for IT infrastructure.

**Last Updated:** [Date]  
**Maintained By:** Infrastructure Support Team  
**Classification:** CONFIDENTIAL - Business Critical Information  
**Last Tested:** [Date]

---

## 1. DOCUMENT OVERVIEW

### Purpose of This Plan

This Disaster Recovery (DR) Plan ensures:
- **Business Continuity:** Critical services restored quickly
- **Data Protection:** Minimize data loss during disasters
- **Clear Procedures:** Step-by-step recovery instructions
- **Defined Roles:** Everyone knows their responsibilities
- **Regular Testing:** Plan is validated and works

### Scope

**In Scope:**
- All production IT infrastructure
- Critical business applications
- Data and databases
- Network connectivity
- Communication systems

**Out of Scope:**
- Facilities management (separate plan)
- Human resources continuity (separate plan)
- Business operations (separate BCP)

### Disaster Definition

**A disaster is any event that:**
- Causes extended IT service outage (> 4 hours)
- Results in data loss or corruption
- Destroys or renders unusable IT equipment
- Makes primary data center inaccessible
- Significantly impacts business operations

**Examples:**
- Fire, flood, natural disaster
- Cyber attack or ransomware
- Hardware failure (multiple systems)
- Power outage (extended)
- Building evacuation
- Critical personnel unavailable

---

## 2. DISASTER RECOVERY OBJECTIVES

### Recovery Time Objective (RTO)

**RTO:** Maximum acceptable time to restore a service after disaster

| System/Service | RTO | Business Impact if Down |
|----------------|-----|------------------------|
| Domain Controllers | 2 hours | Cannot authenticate, all services affected |
| Email System | 4 hours | Communication severely impacted |
| Critical Business App | 4 hours | Revenue generation stops |
| Database Servers | 4 hours | Multiple applications affected |
| File Servers | 8 hours | Productivity impacted |
| Web Servers | 8 hours | External access unavailable |
| Development Systems | 48 hours | Low impact |
| Test Systems | 72 hours | Minimal impact |

### Recovery Point Objective (RPO)

**RPO:** Maximum acceptable data loss measured in time

| System/Service | RPO | Backup Frequency |
|----------------|-----|-----------------|
| Critical Database | 1 hour | Transaction logs every 15 min |
| Business Applications | 4 hours | Every 4 hours |
| File Servers | 24 hours | Daily backups |
| Email System | 24 hours | Daily backups |
| Development Systems | 7 days | Weekly backups |

### Recovery Priorities

**Priority 1 (Critical - Restore First):**
1. Network connectivity
2. Domain Controllers / Authentication
3. Critical Database(s)
4. Critical Application Server(s)

**Priority 2 (Important - Restore Second):**
5. Email system
6. File servers
7. Web servers
8. Secondary application servers

**Priority 3 (Standard - Restore Last):**
9. Development systems
10. Test systems
11. Non-critical applications

---

## 3. DISASTER RESPONSE TEAM

### DR Team Roles and Responsibilities

#### Incident Commander
- **Primary:** [Name - IT Manager]
- **Backup:** [Name - Senior Infrastructure Engineer]
- **Phone:** [Emergency contact number]
- **Email:** [Emergency email]

**Responsibilities:**
- Declare disaster and activate DR plan
- Coordinate all recovery activities
- Make critical decisions
- Communicate with executive management
- Authorize expenditures
- Declare recovery complete

#### Infrastructure Lead
- **Primary:** [Name - Infrastructure Specialist]
- **Backup:** [Name]
- **Phone:** [Number]

**Responsibilities:**
- Restore servers and VMs
- Restore storage systems
- Restore backup systems
- Coordinate with hypervisor vendor if needed

#### Network Lead
- **Primary:** [Name - Network Specialist]
- **Backup:** [Name]
- **Phone:** [Number]

**Responsibilities:**
- Restore network connectivity
- Configure firewalls and routing
- Establish VPN access
- Restore internet connectivity

#### Application Lead
- **Primary:** [Name - Application Support Specialist]
- **Backup:** [Name]
- **Phone:** [Number]

**Responsibilities:**
- Restore business applications
- Verify application functionality
- Coordinate with vendors
- Restore application data

#### Communications Lead
- **Primary:** [Name]
- **Backup:** [Name]
- **Phone:** [Number]

**Responsibilities:**
- Notify stakeholders
- Provide regular status updates
- Coordinate with business units
- Manage user communications

### Contact Information

**Emergency Contact List:**

| Role | Primary Contact | Phone | Alternate | Phone |
|------|----------------|-------|-----------|-------|
| IT Manager | [Name] | [Number] | [Name] | [Number] |
| Infrastructure | [Name] | [Number] | [Name] | [Number] |
| Network | [Name] | [Number] | [Name] | [Number] |
| Application Support | [Name] | [Number] | [Name] | [Number] |

**Vendor Emergency Contacts:**

| Vendor | Service | Emergency Number | Account # |
|--------|---------|-----------------|-----------|
| [ISP Provider] | Internet | [Number] | [Account] |
| [Hypervisor Vendor] | VMware Support | [Number] | [Account] |
| [Hardware Vendor] | Server Support | [Number] | [Account] |
| [Backup Vendor] | Backup Support | [Number] | [Account] |

---

## 4. DISASTER DECLARATION

### Declaration Criteria

**Minor Incident:**
- Single system failure
- Resolved with standard procedures
- RTO/RPO not at risk
- **Action:** Normal incident response

**Major Incident:**
- Multiple system failures
- Extended outage expected
- RTO at risk but not exceeded
- **Action:** Major incident response, DR team on standby

**Disaster:**
- RTO will be or has been exceeded
- Multiple critical systems affected
- Data center unavailable
- Significant business impact
- **Action:** Activate DR plan

### Declaration Process

**Step 1: Assessment (First 30 minutes)**
1. Incident Commander evaluates situation
2. Determine scope and impact
3. Estimate recovery time
4. Decide if disaster criteria met

**Step 2: Declaration (If disaster)**
1. Incident Commander officially declares disaster
2. Notify executive management
3. Activate DR team
4. Initiate DR procedures
5. Begin status log

**Step 3: Documentation**
- Time of disaster
- Type of disaster
- Systems affected
- Decision rationale
- Who was notified

---

## 5. DISASTER RESPONSE PHASES

### Phase 1: Initial Response (First Hour)

**Objectives:**
- Ensure personnel safety
- Assess damage
- Secure remaining assets
- Activate DR team
- Begin communications

**Actions:**

**Incident Commander:**
- [ ] Declare disaster
- [ ] Activate DR team
- [ ] Contact executive management
- [ ] Establish command center
- [ ] Begin incident log

**All Team Members:**
- [ ] Report to command center (physical or virtual)
- [ ] Assess assigned systems
- [ ] Report status to Incident Commander
- [ ] Gather necessary access credentials
- [ ] Prepare for recovery operations

**Communications Lead:**
- [ ] Notify all IT staff
- [ ] Send initial communication to business
- [ ] Set up status update channel
- [ ] Prepare ongoing communications plan

**Initial Assessment Checklist:**
- [ ] What systems are affected?
- [ ] What systems are still functioning?
- [ ] Is data center accessible?
- [ ] Are backups accessible?
- [ ] What caused the disaster?
- [ ] Can primary systems be recovered or need DR site?

### Phase 2: Damage Assessment (Hours 1-2)

**Objectives:**
- Complete damage inventory
- Determine recovery strategy
- Identify needed resources
- Prioritize recovery actions

**Assessment Tasks:**

**Infrastructure Lead:**
- [ ] Assess server hardware status
- [ ] Check hypervisor functionality
- [ ] Verify storage system status
- [ ] Determine backup accessibility
- [ ] List what can be recovered in-place vs. needs restoration

**Network Lead:**
- [ ] Assess network equipment status
- [ ] Check internet connectivity
- [ ] Verify firewall functionality
- [ ] Test VPN accessibility
- [ ] Determine if failover to alternate circuits needed

**Application Lead:**
- [ ] List affected applications
- [ ] Identify application dependencies
- [ ] Verify application data integrity
- [ ] Assess vendor system status
- [ ] Prioritize application recovery order

**Recovery Strategy Decision:**
- [ ] Can recover in primary data center? (Best case)
- [ ] Need to failover to DR site? (If available)
- [ ] Need to rebuild in cloud? (If no DR site)
- [ ] Need to procure new hardware? (Worst case)

### Phase 3: Recovery Operations (Hours 2-24+)

**Objectives:**
- Restore critical systems per RTO
- Minimize data loss per RPO
- Return to operational state

**Recovery Procedures:** (See Section 6 for detailed procedures)

---

## 6. RECOVERY PROCEDURES

### Scenario 1: Complete Data Center Loss

**Assumption:** Primary data center completely unavailable, failover to DR site or rebuild

**Prerequisites:**
- DR site available OR cloud infrastructure ready
- Backups accessible
- Network connectivity to DR site

**Recovery Steps:**

#### Step 1: Establish Network Connectivity (Target: Hour 1)

1. **Activate Backup Internet Circuit**
   - Contact ISP to activate circuit
   - Verify connectivity
   - Configure routing

2. **Establish VPN Access**
   - Configure firewall for VPN
   - Test VPN connectivity
   - Provide VPN access to DR team

3. **Configure Core Networking**
   - Power on network equipment (if DR site)
   - Configure switches
   - Establish VLAN configuration
   - Configure routing to match primary

#### Step 2: Restore Core Infrastructure (Target: Hour 2-4)

1. **Restore Hypervisor Hosts**
   - If DR site exists:
     - Power on DR hypervisor hosts
     - Verify connectivity to storage
     - Join to vCenter/management cluster
   - If rebuilding:
     - Install hypervisor on available hardware
     - Configure networking
     - Connect to storage

2. **Restore Storage Systems**
   - If DR site: Verify storage online
   - If rebuilding: Configure temporary storage
   - Create datastores
   - Verify storage accessible to hosts

3. **Restore Backup Infrastructure**
   - Restore backup server VM
   - Configure access to backup storage
   - Verify backup catalog
   - Test backup repository access

#### Step 3: Restore Priority 1 VMs (Target: Hour 4-8)

**Order of Restoration:**

1. **Domain Controller (VM-DC-01)**
   - Restore from backup
   - Power on VM
   - Verify network connectivity
   - Test authentication
   - Verify time sync
   - **Validation:** Can authenticate users

2. **Primary Database (VM-DB-01)**
   - Restore from backup
   - Power on VM
   - Start database service
   - Verify data integrity
   - Check transaction log status
   - Apply any transaction logs (minimize data loss)
   - **Validation:** Database queries work

3. **Critical Application Server (VM-APP-01)**
   - Restore from backup
   - Power on VM
   - Verify connectivity to database
   - Start application services
   - **Validation:** Application responds

4. **DNS/DHCP Servers**
   - Restore from backup
   - Verify network services
   - Update DNS records if needed
   - **Validation:** Name resolution works

#### Step 4: Restore Priority 2 VMs (Target: Hour 8-16)

5. **Email Server**
   - Restore from backup
   - Verify mail flow
   - Test send/receive
   - **Validation:** Users can send/receive email

6. **File Server**
   - Restore from backup
   - Verify share accessibility
   - Test permissions
   - **Validation:** Users can access files

7. **Web Servers**
   - Restore from backup
   - Verify application pools
   - Test websites
   - Update DNS if needed
   - **Validation:** Websites accessible

#### Step 5: Restore Priority 3 Systems (Target: Hour 16-48)

8. **Development Systems**
9. **Test Systems**
10. **Non-critical applications**

#### Step 6: Verification and Testing (Throughout)

**For Each Restored System:**
- [ ] VM powered on successfully
- [ ] Network connectivity verified
- [ ] Services started
- [ ] Application responding
- [ ] Data integrity confirmed
- [ ] User access tested
- [ ] Dependencies verified
- [ ] Monitoring configured

### Scenario 2: Ransomware Attack

**Assumption:** Systems encrypted, need to restore from backups

**Critical First Steps:**

1. **Isolate Affected Systems (IMMEDIATELY)**
   - Disconnect affected VMs from network
   - Disable VPN access
   - Block external access at firewall
   - Preserve evidence for investigation

2. **Assess Scope**
   - Identify all affected systems
   - Determine when attack occurred
   - Find last clean backup
   - Identify attack vector

3. **Recovery Strategy**
   - Rebuild systems from clean backups
   - Verify backups not encrypted
   - Restore to isolated network initially
   - Scan all systems before reconnecting

**Recovery Steps:**

1. **Create Isolated Recovery Network**
   - Separate VLAN
   - No internet access
   - No connection to production

2. **Restore Systems in Isolation**
   - Restore from last clean backup
   - Update antivirus definitions
   - Scan thoroughly
   - Patch all systems

3. **Verify Clean Systems**
   - Multiple antivirus scans
   - Check for persistence mechanisms
   - Verify no malware present
   - Test functionality

4. **Gradual Production Return**
   - Connect to production one by one
   - Monitor closely
   - Have rollback plan ready

5. **Post-Recovery Actions**
   - Change all passwords
   - Review security logs
   - Implement additional security
   - Document lessons learned

### Scenario 3: Single Critical Server Failure

**Assumption:** One server failed, others functional

**Recovery Steps:**

1. **Assess Impact**
   - What services affected?
   - Are users impacted?
   - Is there redundancy?

2. **Attempt Repair**
   - Can server be restarted?
   - Can it be repaired quickly?
   - Is it hardware or software?

3. **If Repair Not Possible:**
   - Restore VM from backup OR
   - Failover to secondary server OR
   - Rebuild VM from template

4. **Recovery Time:** Should meet RTO for that system

### Scenario 4: Storage System Failure

**Assumption:** Storage array failed, VMs inaccessible

**Recovery Steps:**

1. **Assess Storage**
   - Check storage system status
   - Contact storage vendor
   - Determine repair time

2. **If Storage Not Recoverable:**
   - Provision alternate storage
   - Restore all VMs from backup
   - Follow VM restoration procedures

3. **If Storage Partially Recoverable:**
   - Recover what's accessible
   - Restore only failed VMs

### Scenario 5: Network Outage

**Assumption:** Network connectivity lost

**Recovery Steps:**

1. **Check Internet Circuit**
   - Verify circuit status with ISP
   - Test backup circuit
   - Failover if needed

2. **Check Internal Network**
   - Verify switch functionality
   - Check for spanning tree issues
   - Test routing

3. **Restore Connectivity**
   - Fix identified issues
   - Verify all VLANs accessible
   - Test connectivity to all systems

---

## 7. BACKUP VERIFICATION

### Backup Verification Procedures

**Daily Verification:**
- [ ] Check backup job status
- [ ] Verify all jobs completed
- [ ] Check for errors or warnings
- [ ] Verify backup size reasonable

**Weekly Verification:**
- [ ] Perform test restore of random VM
- [ ] Verify VM boots
- [ ] Verify application functions
- [ ] Document results

**Monthly Verification:**
- [ ] Perform test restore of critical application
- [ ] Full end-to-end testing
- [ ] Verify all components work
- [ ] Document any issues

### Backup Storage

**Primary Backup Storage:**
- **Location:** [Physical location]
- **Type:** [NAS, SAN, Cloud]
- **Capacity:** [Size]
- **Retention:** [Policy]

**Offsite Backup:**
- **Location:** [Offsite location or cloud]
- **Method:** [Replication, tape, cloud backup]
- **Frequency:** [Daily, weekly]
- **Last Offsite Backup:** [Date]

---

## 8. DR SITE INFORMATION

### DR Site Configuration

**DR Site Location:** [If applicable - address]  
**DR Site Access:** [How to access, keys, access codes]  
**DR Site Status:** [Active/Cold/Warm/Hot]

**DR Site Equipment:**

| Equipment | Quantity | Status | Purpose |
|-----------|----------|--------|---------|
| Hypervisor Hosts | [Count] | [Powered/Ready] | [Purpose] |
| Storage Array | [Count] | [Online/Standby] | [Purpose] |
| Network Equipment | [List] | [Active/Standby] | [Purpose] |

**DR Site Network:**
- **IP Range:** [Different from production]
- **Internet Circuit:** [Provider and circuit ID]
- **VPN Tunnel:** [To primary site if applicable]

**DR Site Limitations:**
- [Capacity limitations]
- [Network bandwidth limitations]
- [Equipment age/performance]

---

## 9. ALTERNATE WORK LOCATIONS

### Emergency Work Locations

**If Primary Office Unavailable:**

**Location 1:** [Address]
- Capacity: [Number of people]
- Internet: [Available/Need to establish]
- VPN Access: [Available]
- Access After Hours: [How to get in]

**Location 2:** Work from Home
- VPN Required: Yes
- Equipment: [Laptops, VPN clients]
- Communication: [Teams, Zoom, etc.]

---

## 10. COMMUNICATION PLAN

### Internal Communications

**Status Update Frequency:**
- First Hour: Every 15 minutes
- Hours 2-8: Every hour
- After Hour 8: Every 2 hours
- Once stable: Every 4 hours until complete

**Status Update Method:**
- Email to: [Distribution list]
- Teams Channel: [Channel name]
- Phone Tree: [If email unavailable]

**Status Update Content:**
- Current situation
- What's been restored
- What's in progress
- ETA for next milestone
- Next update time

### External Communications

**Customer/User Communications:**

**Initial Notification (Within 30 minutes):**
```
Subject: IT Service Disruption

We are experiencing an IT service disruption affecting [systems].
Our team is actively working on restoration.
Estimated restoration time: [Time]
Next update at: [Time]
```

**Progress Updates (Regular intervals):**
```
Subject: IT Restoration Update #[X]

Current Status:
- [System A]: Restored
- [System B]: In progress
- [System C]: Pending

Estimated completion: [Time]
Next update at: [Time]
```

**Final Notification (When complete):**
```
Subject: IT Services Restored

All IT services have been restored.
Please contact helpdesk if you experience any issues.
Summary of incident: [Brief summary]
```

### Executive Management Communications

**Notification Requirements:**
- Disaster declaration: Immediate
- Status updates: Every 2 hours
- Major milestones: Immediate
- Recovery complete: Immediate
- Post-incident report: Within 48 hours

---

## 11. TESTING AND MAINTENANCE

### DR Plan Testing Schedule

**Tabletop Exercise:**
- **Frequency:** Quarterly
- **Duration:** 2 hours
- **Participants:** DR team
- **Purpose:** Walk through scenarios, identify gaps

**Partial DR Test:**
- **Frequency:** Semi-annually
- **Duration:** 4 hours
- **Scope:** Restore non-critical VMs in isolated environment
- **Purpose:** Verify backup restore procedures

**Full DR Test:**
- **Frequency:** Annually
- **Duration:** 8+ hours
- **Scope:** Restore all critical systems, simulate complete failover
- **Purpose:** Validate entire DR capability

**Test Documentation:**

| Test Date | Type | Scope | Results | Issues Found | Action Items |
|-----------|------|-------|---------|--------------|--------------|
| [Date] | [Type] | [Scope] | [Pass/Fail/Partial] | [Issues] | [Actions] |

### Plan Maintenance

**Review Schedule:**
- **Quarterly:** Review contact information
- **Semi-annually:** Update recovery procedures
- **Annually:** Complete plan review
- **As Needed:** After infrastructure changes

**Change Control:**
- All DR plan changes logged
- Changes reviewed by DR team
- Updated plan distributed to all stakeholders

---

## 12. RECOVERY COMPLETION

### Recovery Validation Checklist

Before declaring recovery complete:

**Technical Validation:**
- [ ] All Priority 1 systems operational
- [ ] All Priority 2 systems operational
- [ ] Network connectivity normal
- [ ] All critical services tested
- [ ] No significant errors in logs
- [ ] Monitoring systems operational
- [ ] Backup systems operational

**Business Validation:**
- [ ] Users can perform critical functions
- [ ] Applications responding normally
- [ ] Data integrity verified
- [ ] No major issues reported
- [ ] Business owners approve

**Documentation:**
- [ ] Incident timeline documented
- [ ] All actions logged
- [ ] Issues documented
- [ ] Recovery time documented
- [ ] Lessons learned captured

### Return to Normal Operations

**Cutover Plan:**
1. Verify all systems stable for 24 hours
2. Monitor closely for 48 hours
3. Return to normal change control process
4. Deactivate DR team (but remain on standby)
5. Schedule post-incident review

**If Using DR Site:**
1. Stabilize operations at DR site
2. Plan return to primary site
3. Reverse migration process
4. Cut over during maintenance window
5. Verify all systems
6. Return DR site to standby

---

## 13. POST-DISASTER REVIEW

### Post-Incident Review (PIR)

**Schedule:** Within 1 week of recovery

**Participants:**
- DR team members
- IT management
- Affected business units
- Executive sponsor (if major disaster)

**Review Topics:**
1. What happened?
2. Timeline of events
3. What went well?
4. What didn't go well?
5. RTO/RPO met or missed?
6. Plan effectiveness
7. Communication effectiveness
8. Resource adequacy
9. Lessons learned
10. Action items for improvement

**Deliverables:**
- Post-incident report
- Updated DR plan
- Action item list with owners and due dates

### Continuous Improvement

**Action Item Tracking:**

| Action Item | Owner | Due Date | Status | Completed |
|-------------|-------|----------|--------|-----------|
| [Action] | [Owner] | [Date] | [Status] | [Date] |

---

## 14. FINANCIAL CONSIDERATIONS

### Insurance

**Coverage:**
- Business interruption insurance: [Yes/No]
- Policy number: [Number]
- Coverage amount: [Amount]
- Contact: [Insurance agent]

### Emergency Procurement

**Pre-Approved Spending Authority:**
- DR Team Lead: $[Amount] without approval
- IT Manager: $[Amount] without approval
- Amounts above require: [Executive approval]

**Emergency Vendors:**

| Vendor | Service | Contact | Account # |
|--------|---------|---------|-----------|
| [Vendor] | [Hardware rental] | [Contact] | [Account] |
| [Vendor] | [Cloud services] | [Contact] | [Account] |

---

## 15. APPENDICES

### Appendix A: Critical System Configurations

[Reference to detailed configurations in Server Configuration Database]

### Appendix B: Network Diagrams

[Reference to Network Topology Diagrams]

### Appendix C: Vendor Contacts

[Reference to Vendor Escalation Contacts]

### Appendix D: Recovery Checklists

**Quick Reference Checklists:**
- [ ] Hypervisor restore checklist
- [ ] VM restore checklist
- [ ] Network restore checklist
- [ ] Application restore checklist

### Appendix E: Emergency Supplies

**Location of Emergency Supplies:**
- [ ] Current backup tapes/drives
- [ ] Critical system documentation (printed)
- [ ] Emergency contact lists (printed)
- [ ] Vendor support numbers (printed)
- [ ] Admin passwords (sealed envelope)
- [ ] Installation media
- [ ] License keys and certificates

**Storage Location:** [Physical location]  
**Access:** [Who has keys/access]

---

## NOTES FOR USING THIS PLAN

**For the DR Team:**
- This is your primary reference during a disaster
- Familiarize yourself with all procedures
- Know where critical information is located
- Participate in all DR tests
- Suggest improvements after tests or actual use

**For Maintenance:**
- Update after all infrastructure changes
- Update contact information quarterly
- Review and update procedures annually
- Incorporate lessons learned from tests and incidents
- Keep printed copy in emergency supplies

**For Populating This Template:**
- Start with critical system identification
- Document current backup procedures
- Identify recovery priorities with business
- Document detailed recovery procedures
- Test procedures and refine
- Update contact information
- Include specific commands and steps
- Add screenshots where helpful

**Critical Success Factors:**
- Regular testing is essential
- Keep plan current
- All team members must be familiar with plan
- Business must validate RTOs and priorities
- Backups must be verified regularly
- Communication is critical during disaster

---

**Template Status:** Ready for population  
**Priority:** CRITICAL - Essential for business continuity  
**Estimated Time to Complete:** 15-20 hours for comprehensive planning  
**Next Steps:**
1. Identify critical systems and priorities with business
2. Document current backup procedures
3. Create detailed recovery procedures
4. Schedule initial DR test  
**Review Frequency:** Quarterly review, annual full update, after any major changes

**Classification:** CONFIDENTIAL - Contains critical infrastructure information

