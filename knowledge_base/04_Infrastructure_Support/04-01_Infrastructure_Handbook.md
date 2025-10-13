# Infrastructure Handbook

**Purpose:** This handbook provides comprehensive information about server infrastructure, virtualization, storage, backups, and infrastructure support procedures for the Infrastructure team.

**Last Updated:** [Date]  
**Maintained By:** Infrastructure Support Team

---

## 1. INFRASTRUCTURE OVERVIEW

### Infrastructure Scope

**Physical Infrastructure:**
- **Data Centers:** [Number and locations]
- **Server Rooms:** [Locations]
- **Total Physical Servers:** [Count]
- **Total Virtual Machines:** [Count]
- **Storage Capacity:** [Total TB]
- **Backup Capacity:** [Total TB]

**Infrastructure Criticality:**
- **Uptime Target:** [e.g., 99.9%]
- **Business Hours:** [When infrastructure must be available]
- **Critical Services:** [What depends on infrastructure]
- **Disaster Recovery Time:** [RTO target]

### Infrastructure Components

**Core Components:**
1. **Physical Servers** - Host hypervisors and services
2. **Virtualization Platform** - VM management
3. **Storage Systems** - Data storage and access
4. **Backup Systems** - Data protection
5. **Monitoring Systems** - Infrastructure health
6. **Power/Cooling** - Environmental systems

---

## 2. SERVER INVENTORY

### Physical Servers

#### Production Servers

| Server Name | Make/Model | CPU | RAM | Storage | Role | Location | Status |
|-------------|------------|-----|-----|---------|------|----------|--------|
| [SRV-01] | [Dell R740] | [2x Xeon] | [128GB] | [2TB SSD] | [Hypervisor] | [Rack 1] | Production |
| [SRV-02] | [Model] | [CPU] | [RAM] | [Storage] | [Role] | [Location] | [Status] |
| [SRV-03] | [Model] | [CPU] | [RAM] | [Storage] | [Role] | [Location] | [Status] |

#### Development/Test Servers

| Server Name | Make/Model | CPU | RAM | Storage | Role | Location | Status |
|-------------|------------|-----|-----|---------|------|----------|--------|
| [DEV-01] | [Model] | [CPU] | [RAM] | [Storage] | [Dev/Test] | [Location] | [Status] |

### Virtual Machine Inventory

**VM Summary:**
- **Total VMs:** [Count]
- **Production VMs:** [Count]
- **Development VMs:** [Count]
- **Average VM Size:** [vCPU, RAM]

**VM List:** (See separate document: `04-02_Server_Configuration_Database.md` for detailed VM configurations)

---

## 3. VIRTUALIZATION PLATFORM

### Hypervisor Environment

**Platform:** [VMware ESXi, Hyper-V, ProxMox, etc.]  
**Version:** [Current version]  
**Management Interface:** [vCenter, Hyper-V Manager, etc.]  
**Management URL:** [URL]  
**License Type:** [License details]

### Hypervisor Hosts

#### Host 1: [Hostname]

**Hardware:**
- **Model:** [Server model]
- **CPU:** [Processor model and count]
- **RAM:** [Total memory]
- **Storage:** [Local storage if any]
- **Network:** [NIC count and speed]

**Configuration:**
- **IP Address:** [Management IP]
- **Datastore(s):** [Connected storage]
- **Network(s):** [Network configuration]
- **VMs Hosted:** [Count]
- **Resource Allocation:**
  - CPU Overcommit: [Ratio]
  - RAM Overcommit: [Ratio]
  - Current Utilization: [%]

#### Host 2: [Hostname]
[Repeat structure for each host]

### Virtual Networking

**Virtual Switches:**

| vSwitch Name | Physical NIC(s) | VLANs | Purpose |
|--------------|----------------|-------|---------|
| [vSwitch0] | [vmnic0, vmnic1] | [10, 20, 30] | Management and VMs |
| [vSwitch1] | [vmnic2, vmnic3] | [40] | Storage network |

**Port Groups:**

| Port Group | VLAN | vSwitch | Purpose | VMs |
|-----------|------|---------|---------|-----|
| [Management] | 10 | vSwitch0 | Management | N/A |
| [Production] | 20 | vSwitch0 | Production VMs | [Count] |
| [Storage] | 40 | vSwitch1 | Storage traffic | N/A |

### High Availability Configuration

**HA Status:** [Enabled/Disabled]  
**Features Configured:**
- [ ] VM High Availability (automatic restart)
- [ ] vMotion (live migration)
- [ ] DRS (Distributed Resource Scheduler)
- [ ] Fault Tolerance (if applicable)

**Failover Behavior:**
- VM restart priority: [High/Medium/Low by VM]
- Host isolation response: [Power off/Leave powered on]
- Datastore heartbeating: [Enabled/Disabled]

---

## 4. STORAGE INFRASTRUCTURE

### Storage Systems

#### Primary Storage System

**System:** [SAN, NAS, DAS]  
**Make/Model:** [Manufacturer and model]  
**Management IP:** [IP address]  
**Total Capacity:** [Raw capacity]  
**Usable Capacity:** [After RAID]  
**Current Usage:** [Used/Free]

**Configuration:**
- **RAID Level:** [RAID 5, RAID 10, etc.]
- **Hot Spares:** [Count]
- **Connection Type:** [iSCSI, FC, NFS]
- **Redundancy:** [Dual controllers, etc.]

**Datastores/Volumes:**

| Datastore Name | Size | Used | Free | Purpose | Connected Hosts |
|---------------|------|------|------|---------|----------------|
| [DS-PROD-01] | [2TB] | [1.2TB] | [800GB] | Production VMs | [All hosts] |
| [DS-DEV-01] | [500GB] | [200GB] | [300GB] | Development | [Host 2] |

#### Secondary Storage (if applicable)

[Repeat structure for backup storage or additional storage systems]

### Storage Networking

**Storage Network:**
- **Subnet:** [e.g., 10.10.0.0/24]
- **VLAN:** [VLAN ID]
- **Speed:** [1Gbps, 10Gbps]
- **Protocol:** [iSCSI, NFS, FC]

**Storage Paths:**
```
[Hypervisor Host] → [Network Switch] → [Storage Array]
     10.10.0.11          VLAN 40           10.10.0.100
```

### Storage Performance Monitoring

**Performance Metrics:**
- **IOPS:** [Current / Peak]
- **Throughput:** [MB/s]
- **Latency:** [Typical ms]
- **Alert Thresholds:** [When to alert]

---

## 5. BACKUP AND RECOVERY

### Backup Infrastructure

**Backup Solution:** [Product name - Veeam, Commvault, etc.]  
**Backup Server:** [Hostname and IP]  
**Backup Storage:** [Location and capacity]  
**Retention Policy:** [How long backups kept]

**Backup Types:**
- **Full Backup:** [When performed]
- **Incremental Backup:** [When performed]
- **Differential Backup:** [If used]

### Backup Schedule

**Daily Backups:**

| System/VM | Backup Time | Type | Retention | Destination |
|-----------|-------------|------|-----------|-------------|
| [VM-01] | 2:00 AM | Incremental | 7 days | [Backup storage] |
| [VM-02] | 2:30 AM | Incremental | 7 days | [Backup storage] |
| [Critical-DB] | 12:00 AM | Full | 30 days | [Backup storage] |

**Weekly Backups:**

| System | Day/Time | Type | Retention |
|--------|----------|------|-----------|
| [All VMs] | Sunday 2:00 AM | Full | 4 weeks |

**Monthly Backups:**

| System | Schedule | Type | Retention |
|--------|----------|------|-----------|
| [Critical systems] | 1st Sunday | Full | 12 months |

### Backup Verification

**Verification Process:**
1. [Step 1 - e.g., Automated backup job success check]
2. [Step 2 - e.g., Random restore test]
3. [Step 3 - e.g., Integrity check]

**Testing Schedule:**
- **Backup Job Verification:** Daily (automated)
- **Restore Testing:** [Weekly/Monthly]
- **Full DR Test:** [Quarterly/Annually]

### Restore Procedures

**Quick Restore (Individual Files):**
1. Access backup console
2. Navigate to backup job
3. Select date/time
4. Browse for files
5. Restore to original or alternate location

**VM Full Restore:**
1. Access backup console
2. Select VM backup
3. Choose restore point
4. Select destination host/datastore
5. Configure network settings
6. Power on restored VM

**Estimated Restore Times:**
- **Small VM (< 50GB):** [e.g., 30 minutes]
- **Medium VM (50-200GB):** [e.g., 1-2 hours]
- **Large VM (> 200GB):** [e.g., 3-6 hours]
- **Database Restore:** [Depends on size]

---

## 6. SERVER PROVISIONING

### VM Provisioning Process

**Standard VM Request Process:**
1. **Request Submitted:** [By whom, using what process]
2. **Approval Required:** [Who approves]
3. **Resource Check:** [Verify capacity available]
4. **VM Creation:** [Steps below]
5. **Configuration:** [OS install, network, storage]
6. **Documentation:** [Update inventory]
7. **Handoff:** [Notify requester]

**Estimated Provisioning Time:**
- **Standard VM:** [e.g., 1-2 hours]
- **Complex configuration:** [e.g., 4-8 hours]

### VM Templates

**Available Templates:**

| Template Name | OS | CPU | RAM | Disk | Purpose | Last Updated |
|--------------|-----|-----|-----|------|---------|--------------|
| [Win-2019-STD] | Windows Server 2019 | 2 | 4GB | 60GB | Standard Windows | [Date] |
| [Ubuntu-20-04] | Ubuntu 20.04 | 2 | 4GB | 40GB | Standard Linux | [Date] |
| [SQL-Server] | Windows + SQL | 4 | 16GB | 200GB | Database server | [Date] |

### Physical Server Deployment

**Process:**
1. Hardware procurement and delivery
2. Physical installation in rack
3. Cable management (power, network)
4. BIOS/firmware configuration
5. Operating system installation
6. Integration into monitoring
7. Documentation

**Estimated Deployment Time:** [e.g., 1-2 days]

---

## 7. CAPACITY MANAGEMENT

### Current Capacity

**Compute Resources:**
- **Total CPU Cores:** [Count]
- **Allocated vCPUs:** [Count]
- **CPU Overcommit Ratio:** [e.g., 4:1]
- **Average CPU Utilization:** [%]

**Memory Resources:**
- **Total Physical RAM:** [GB]
- **Allocated RAM:** [GB]
- **Average Memory Utilization:** [%]
- **Memory Overcommit:** [Yes/No]

**Storage Resources:**
- **Total Storage:** [TB]
- **Used Storage:** [TB]
- **Free Storage:** [TB]
- **Storage Growth Rate:** [GB per month]

### Capacity Planning

**Growth Projections:**
- **Estimated VM Growth:** [X VMs per quarter]
- **Storage Growth:** [Y TB per quarter]
- **Resource Expansion Needed By:** [Date]

**Capacity Triggers:**
- **CPU Usage > 80%:** Plan to add host
- **RAM Usage > 85%:** Plan to add memory or host
- **Storage > 75%:** Plan to expand storage
- **IOPS sustained > 80%:** Consider storage upgrade

**Next Planned Expansion:**
- **What:** [e.g., Add one hypervisor host]
- **When:** [Quarter/Month]
- **Cost:** [Estimated]
- **Reason:** [Capacity constraint]

---

## 8. PERFORMANCE MONITORING

### Monitoring Tools

**Primary Monitoring:**
- **Tool:** [Product name]
- **Server:** [Hostname and URL]
- **What's Monitored:**
  - Server CPU, RAM, disk
  - VM performance metrics
  - Storage performance
  - Network bandwidth
  - Service availability

**Alert Thresholds:**

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| CPU Usage | > 80% | > 90% | Investigate load |
| RAM Usage | > 85% | > 95% | Check for memory leak |
| Disk Usage | > 75% | > 90% | Free space or expand |
| Storage Latency | > 20ms | > 50ms | Check storage health |

### Performance Baselines

**Normal Operating Parameters:**
- **CPU:** [e.g., 30-50% during business hours]
- **RAM:** [e.g., 60-70% allocated]
- **Storage IOPS:** [e.g., 1000-2000 average]
- **Network:** [e.g., 100-200 Mbps]

**Peak Usage Times:**
- [Time period]: [Description of typical load]
- [Time period]: [Description]

---

## 9. COMMON INFRASTRUCTURE ISSUES

### Issue: High CPU Usage on Host

**Symptoms:**
- VMs sluggish
- High ready time for VMs
- Host CPU consistently > 90%

**Troubleshooting Steps:**
1. Identify which VM(s) consuming CPU
2. Use tool: `check_server_resources` to verify host CPU
3. Check if legitimate workload or runaway process
4. Consider:
   - Migrating VMs to less loaded host (vMotion)
   - Adding more CPU if all hosts loaded
   - Reducing CPU overcommit ratio
   - Rightsizing VMs that are over-provisioned

**Resolution:**
- Balance VM load across hosts
- Add capacity if needed
- Optimize VM configurations

### Issue: Low Memory Available

**Symptoms:**
- Memory alerts from monitoring
- VM memory swapping
- Performance degradation

**Troubleshooting Steps:**
1. Use tool: `check_server_resources` to verify memory
2. Identify VMs using excessive memory
3. Check for memory leaks in applications
4. Review memory allocation vs. usage
5. Consider:
   - Migrate VMs to host with more memory
   - Add memory to host
   - Rightsize VMs

**Resolution:**
- Add physical memory
- Reduce memory overcommit
- Optimize VM memory allocation

### Issue: Storage Performance Degradation

**Symptoms:**
- Slow VM response
- High storage latency (> 20ms)
- Disk queue length elevated

**Troubleshooting Steps:**
1. Use tool: `check_storage_health` to verify
2. Check storage array health
3. Identify VMs with high I/O
4. Review RAID rebuild status
5. Check network connectivity to storage

**Common Causes:**
- RAID rebuild in progress
- Failed disk in array
- Storage network congestion
- VM with runaway I/O
- Storage array at capacity

**Resolution:**
- Replace failed disks
- Throttle high I/O VMs
- Upgrade storage network
- Add storage capacity

### Issue: VM Cannot Start

**Symptoms:**
- VM fails to power on
- Error messages during startup

**Troubleshooting Steps:**
1. Check error message details
2. Verify host has resources (CPU, RAM)
3. Check datastore has space
4. Verify VM files not locked
5. Check for snapshot issues

**Common Causes:**
- Insufficient resources on host
- Datastore out of space
- Corrupted VM files
- Snapshot problems
- Network configuration issues

**Resolution:**
- Free up resources
- Remove old snapshots
- Repair VM configuration
- Migrate to different host

### Issue: Backup Job Failing

**Symptoms:**
- Backup jobs showing failed status
- Missing backups for critical systems

**Troubleshooting Steps:**
1. Check backup job logs
2. Verify backup storage has space
3. Check network connectivity to VM
4. Verify VM snapshot can be taken
5. Check backup agent status (if applicable)

**Common Causes:**
- Backup storage full
- Network connectivity issue
- VM snapshot problem
- Backup service stopped
- Antivirus interfering

**Resolution:**
- Free up backup storage
- Fix network issues
- Remove old snapshots
- Restart backup services

---

## 10. MAINTENANCE PROCEDURES

### Regular Maintenance Tasks

**Daily:**
- [ ] Check backup job status
- [ ] Review system alerts
- [ ] Monitor capacity (storage, compute)
- [ ] Check critical VM status

**Weekly:**
- [ ] Review performance metrics
- [ ] Check for system updates
- [ ] Verify backup integrity
- [ ] Review capacity trends
- [ ] Check environmental (temp, power)

**Monthly:**
- [ ] Patch non-critical systems
- [ ] Review and clean old snapshots
- [ ] Capacity planning review
- [ ] Update documentation
- [ ] Test backup restores
- [ ] Review security configurations

**Quarterly:**
- [ ] Patch critical systems (during maintenance window)
- [ ] Full disaster recovery test
- [ ] Hardware health check
- [ ] Firmware updates (if needed)
- [ ] Review and optimize VM resources
- [ ] Vendor support contract review

**Annually:**
- [ ] Major version upgrades
- [ ] Hardware refresh planning
- [ ] Complete DR test
- [ ] Security audit
- [ ] Documentation comprehensive review

### Maintenance Windows

**Standard Maintenance Window:**
- **Day/Time:** [e.g., Sunday 2:00 AM - 6:00 AM]
- **Frequency:** [Monthly]
- **Notification Process:** [How users are notified]
- **Approval Required:** [Who approves]

**Emergency Maintenance:**
- **When Used:** [Critical security patches, major outages]
- **Approval:** [IT Manager or higher]
- **Notification:** [As soon as possible]

---

## 11. SERVER LIFECYCLE MANAGEMENT

### Server Age Tracking

| Server | Purchase Date | Age (Years) | Warranty End | Replacement Due | Status |
|--------|--------------|-------------|--------------|----------------|--------|
| [SRV-01] | [Date] | [Years] | [Date] | [Date] | [Active/EOL pending] |

### Hardware Refresh Cycle

**Standard Lifecycle:**
- **Physical Servers:** [e.g., 5 years]
- **Storage Arrays:** [e.g., 5-7 years]
- **Network Equipment:** [e.g., 5 years]
- **UPS Systems:** [e.g., 5-10 years]

**Refresh Process:**
1. Identify servers reaching end of life
2. Plan budget and approval
3. Procure replacement hardware
4. Install and configure new hardware
5. Migrate workloads
6. Decommission old hardware
7. Update documentation

### End-of-Life Decommissioning

**Decommission Process:**
1. Verify server no longer needed
2. Backup all data
3. Document configuration
4. Power off and disconnect
5. Wipe drives securely
6. Remove from monitoring
7. Update inventory
8. Arrange disposal/recycling

---

## 12. COLLABORATION SCENARIOS

### When to Collaborate with Application Support
- Application performance issues may be infrastructure-related
- Application needs more resources (CPU, RAM, storage)
- Application server requires restart or maintenance
- New application server provisioning

### When to Collaborate with Network Support
- Server network connectivity issues
- Need new VLANs or network configuration
- Storage network performance issues
- Firewall rules for new servers

### When to Collaborate with Service Desk
- User-reported server performance issues
- Scheduled maintenance communication
- Service outage notifications
- New service deployments

### When to Collaborate with IT Manager
- Major infrastructure changes
- Capital expenditure for hardware
- Capacity planning decisions
- Vendor selection and contracts
- Disaster recovery planning

---

## 13. SECURITY AND COMPLIANCE

### Security Hardening

**Server Security Measures:**
- [ ] Regular patching (OS and applications)
- [ ] Antivirus/Antimalware installed and updated
- [ ] Firewall configured on servers
- [ ] Unnecessary services disabled
- [ ] Strong password policies enforced
- [ ] Audit logging enabled
- [ ] Privileged access management

**Access Control:**
- **Administrator Access:** [Who has access]
- **Service Accounts:** [How managed]
- **Audit Logging:** [What's logged]
- **Password Policy:** [Requirements]

### Compliance Requirements

**Standards Followed:**
- [Standard 1 - e.g., PCI DSS if applicable]
- [Standard 2 - e.g., ISO 27001]
- [Internal policies]

**Audit Trail:**
- All infrastructure changes logged
- Access to systems logged
- Regular review of logs

---

## 14. DISASTER RECOVERY

(Detailed DR procedures in separate document: `04-03_Disaster_Recovery_Plan.md`)

### Quick Reference

**Recovery Time Objective (RTO):**
- **Critical Systems:** [e.g., 4 hours]
- **Important Systems:** [e.g., 24 hours]
- **Standard Systems:** [e.g., 72 hours]

**Recovery Point Objective (RPO):**
- **Critical Data:** [e.g., 1 hour - max data loss]
- **Important Data:** [e.g., 24 hours]
- **Standard Data:** [e.g., 7 days]

**DR Site:**
- **Location:** [If applicable]
- **Capacity:** [What can be failed over]
- **Failover Process:** [See DR plan document]

---

## 15. VENDOR AND SUPPORT CONTACTS

### Hardware Vendors

| Vendor | Equipment | Support Contact | Contract # | Expiry Date |
|--------|-----------|----------------|------------|-------------|
| [Dell] | Servers | [Phone/Email] | [Contract #] | [Date] |
| [HPE] | Storage | [Phone/Email] | [Contract #] | [Date] |

### Software Vendors

| Vendor | Product | Support Contact | License # | Expiry Date |
|--------|---------|----------------|-----------|-------------|
| [VMware] | vSphere | [Phone/Email] | [License #] | [Date] |
| [Veeam] | Backup | [Phone/Email] | [License #] | [Date] |

---

## 16. FREQUENTLY ASKED QUESTIONS

**Q: How do I request a new VM?**
A: [Process description]

**Q: How long does VM provisioning take?**
A: [Timeframe]

**Q: What's the process for increasing VM resources?**
A: [Process]

**Q: How do I request a server restart?**
A: [Process and approval needed]

**Q: What are our backup retention policies?**
A: [Policy summary]

---

## NOTES FOR USING THIS HANDBOOK

**For the AI Agent:**
- Use this handbook to understand infrastructure architecture
- Reference when troubleshooting server/VM issues
- Check capacity information before provisioning
- Follow backup procedures for any restore requests
- Understand resource allocation and limitations
- Use collaboration guidelines to involve other teams

**For Maintenance:**
- Update after any infrastructure changes
- Keep server inventory current
- Review capacity planning quarterly
- Update after adding/removing hardware
- Document all major incidents and resolutions
- Keep vendor contact information current

**For Populating This Template:**
- Start with server inventory
- Document virtualization platform configuration
- Add backup schedules and procedures
- Include common issues you've encountered
- Document maintenance procedures
- Update as you make changes to infrastructure
- Include diagrams or screenshots where helpful

---

**Template Status:** Ready for population  
**Priority:** HIGH - Critical infrastructure documentation  
**Estimated Time to Complete:** 8-10 hours for comprehensive documentation  
**Next Steps:** Document server inventory, then virtualization platform, then backups
