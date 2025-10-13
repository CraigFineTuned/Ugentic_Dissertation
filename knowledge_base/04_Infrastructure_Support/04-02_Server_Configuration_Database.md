# Server Configuration Database

**Purpose:** This document serves as the centralized database for all server configurations, including physical servers, virtual machines, and their detailed specifications.

**Last Updated:** [Date]  
**Maintained By:** Infrastructure Support Team

---

## 1. DOCUMENT OVERVIEW

### Purpose of This Database

This configuration database provides:
- **Complete Server Inventory:** Every server documented
- **Configuration Details:** Specifications for troubleshooting
- **Change Tracking:** History of configuration changes
- **Relationship Mapping:** Server dependencies and connections
- **Quick Reference:** Fast lookup during incidents

### How to Use This Database

**For Troubleshooting:**
- Find server by name or IP
- Check specifications and dependencies
- View configuration history
- Identify similar servers

**For Planning:**
- Review capacity by server
- Identify servers needing upgrades
- Plan migrations or consolidations
- Track software versions

**For Compliance:**
- Audit server configurations
- Track unauthorized changes
- Verify security settings
- Document all systems

---

## 2. PHYSICAL SERVER INVENTORY

### Production Physical Servers

#### Server: [SRV-HYPER-01]

**Basic Information:**
- **Hostname:** [SRV-HYPER-01]
- **Role:** [VMware ESXi Hypervisor]
- **Environment:** [Production]
- **Status:** [Active/Maintenance/Decommissioned]
- **Criticality:** [High/Medium/Low]

**Hardware Specifications:**
- **Manufacturer:** [Dell]
- **Model:** [PowerEdge R740]
- **Serial Number:** [Serial #]
- **Service Tag:** [Tag for support]
- **Purchase Date:** [Date]
- **Warranty Expiry:** [Date]

**Processor:**
- **CPU Model:** [Intel Xeon Gold 6130]
- **CPU Count:** [2 processors]
- **Cores per CPU:** [16 cores]
- **Total Cores:** [32 cores]
- **Total Threads:** [64 threads with HT]
- **CPU Speed:** [2.1 GHz base, 3.7 GHz turbo]

**Memory:**
- **Total RAM:** [256 GB]
- **RAM Type:** [DDR4 ECC 2666 MHz]
- **RAM Configuration:** [16x 16GB modules]
- **Available Slots:** [8 slots free]
- **Max Capacity:** [768 GB]

**Storage (Local):**
- **Boot Disks:** [2x 240GB SSD - RAID 1]
- **Data Disks:** [4x 1.2TB SAS 10K - RAID 10]
- **RAID Controller:** [PERC H730P]
- **Total Usable Storage:** [2.4 TB local]

**Network Interfaces:**
- **NIC 1-2:** [Intel X710 10GbE - Bonded - Production network]
- **NIC 3-4:** [Intel X710 10GbE - Bonded - Storage network]
- **iDRAC:** [Dedicated 1GbE management port]
- **iDRAC IP:** [10.0.0.111]

**Location:**
- **Data Center:** [Main DC]
- **Rack:** [Rack 1]
- **Rack Unit:** [U28-U30 (3U server)]
- **Power:** [Dual PSU - 750W each]
- **Power Sources:** [PDU A + PDU B]

**Operating System:**
- **OS:** [VMware ESXi]
- **Version:** [7.0 Update 3]
- **Install Date:** [Date]
- **License Key:** [Stored in vault]

**Management Access:**
- **Console Access:** [iDRAC - https://10.0.0.111]
- **Admin User:** [root]
- **Password Location:** [Password vault]
- **SSH Enabled:** [Yes/No]

**Network Configuration:**
- **Management IP:** [10.0.0.21]
- **Management Subnet:** [255.255.255.0]
- **Gateway:** [10.0.0.1]
- **DNS Servers:** [10.0.0.51, 10.0.0.52]
- **Domain:** [internal.company.com]

**Hosted VMs:**
- [List of VMs hosted - see VM section for details]
- [VM-PROD-01]
- [VM-PROD-02]
- [etc.]

**Monitoring:**
- **Monitoring System:** [PRTG/Nagios/etc.]
- **Monitored Metrics:** [CPU, RAM, Disk, Network, Temperature]
- **Alert Contacts:** [IT team email/pager]

**Backup:**
- **Host Backup:** [Configuration backup method]
- **VM Backup:** [Backup solution and schedule]
- **Last Backup:** [Date/time]

**Maintenance History:**

| Date | Change Type | Description | Performed By | Ticket # |
|------|-------------|-------------|--------------|----------|
| [Date] | [Hardware upgrade] | [Added 128GB RAM] | [Name] | [Ticket] |
| [Date] | [Firmware update] | [BIOS v2.10.0] | [Name] | [Ticket] |

**Related Documentation:**
- [Link to hardware manual]
- [Link to configuration guides]

**Notes:**
- [Any special configuration notes]
- [Known issues or quirks]
- [Future upgrade plans]

---

#### Server: [SRV-HYPER-02]

[Repeat full structure for each physical server]

---

#### Server: [SRV-STORAGE-01]

**Basic Information:**
- **Hostname:** [SRV-STORAGE-01]
- **Role:** [Storage Array/NAS]
- **Environment:** [Production]

[Include same detailed sections as above, adapted for storage server]

---

### Development/Test Physical Servers

#### Server: [SRV-DEV-01]

[Same structure as production servers]

---

## 3. VIRTUAL MACHINE INVENTORY

### Production Virtual Machines

#### Virtual Machine: [VM-APP-01]

**Basic Information:**
- **VM Name:** [VM-APP-01]
- **Display Name:** [Application Server 01]
- **Role:** [Primary application server]
- **Environment:** [Production]
- **Status:** [Running/Stopped/Suspended]
- **Criticality:** [High/Medium/Low]
- **Business Owner:** [Department/Person]
- **Technical Owner:** [IT contact]

**Virtual Hardware:**
- **vCPUs:** [4 virtual processors]
- **vCPU Reservation:** [MHz reserved if any]
- **vRAM:** [16 GB]
- **RAM Reservation:** [GB reserved if any]
- **Disk 1 (OS):** [100 GB thin/thick provisioned]
- **Disk 2 (Data):** [500 GB thin/thick provisioned]
- **Total Storage:** [600 GB]
- **Network Adapter(s):** [VMXNET3 x1]

**Operating System:**
- **OS:** [Windows Server 2019 Standard]
- **Version/Build:** [Build number]
- **Architecture:** [64-bit]
- **Activation:** [Activated/KMS]
- **Install Date:** [Date]
- **Service Pack/Updates:** [Current patch level]

**Network Configuration:**
- **vNIC 1:**
  - Port Group: [Production-VLAN20]
  - IP Address: [10.1.0.11]
  - Subnet Mask: [255.255.255.0]
  - Gateway: [10.1.0.1]
  - DNS Servers: [10.0.0.51, 10.0.0.52]
  - DNS Domain: [internal.company.com]
- **Hostname:** [VM-APP-01.internal.company.com]

**Storage Configuration:**
- **Datastore:** [DS-PROD-01]
- **Storage Path:** [/vmfs/volumes/DS-PROD-01/VM-APP-01/]
- **Snapshots:** [Count if any]
- **Disk Type:** [Thin/Thick provisioned]

**Hypervisor Assignment:**
- **Host:** [SRV-HYPER-01]
- **Cluster:** [PROD-Cluster if applicable]
- **Resource Pool:** [Production]
- **DRS Automation:** [Fully Automated/Manual]

**Software Installed:**
- [Application name and version]
- [Application name and version]
- [Monitoring agent]
- [Backup agent]
- [Antivirus]

**Services Running:**

| Service Name | Display Name | Startup Type | Status | Purpose |
|-------------|--------------|--------------|--------|---------|
| [Service1] | [Display name] | Automatic | Running | [Purpose] |
| [Service2] | [Display name] | Automatic | Running | [Purpose] |

**Ports in Use:**

| Port | Protocol | Purpose | Accessible From |
|------|----------|---------|-----------------|
| 80 | TCP | HTTP | [User VLAN] |
| 443 | TCP | HTTPS | [User VLAN] |
| 3389 | TCP | RDP | [Management VLAN] |
| 1433 | TCP | SQL | [This server only] |

**Dependencies:**

**Depends On (Required Services):**
- [VM-DB-01] - Database server
- [VM-AD-01] - Active Directory
- [Network share] - File server

**Depended Upon By (Services this VM provides):**
- [Web application] - Accessed by users
- [VM-WEB-01] - Web frontend

**Security:**
- **Windows Firewall:** [Enabled]
- **Antivirus:** [Product and version]
- **Local Admin Access:** [Who has access]
- **Domain Joined:** [Yes - domain.com]
- **Security Patches:** [Up to date / Pending]

**Backup Configuration:**
- **Backup Job:** [Job name in backup software]
- **Schedule:** [Daily incremental, Weekly full]
- **Retention:** [30 days]
- **Last Successful Backup:** [Date/time]
- **Backup Size:** [Typical size]
- **Verified:** [Last verification date]

**Monitoring:**
- **Monitored By:** [Monitoring system]
- **Metrics Tracked:** [CPU, RAM, Disk, Network, Services]
- **Alerts Configured:** [What triggers alerts]
- **Alert Recipients:** [Who gets notified]

**Performance Baselines:**
- **CPU Usage:** [Normal range - e.g., 20-40%]
- **Memory Usage:** [Normal range - e.g., 60-70%]
- **Disk I/O:** [Normal range]
- **Network I/O:** [Normal range]

**Maintenance Window:**
- **Preferred Day/Time:** [Sunday 2:00 AM]
- **Last Reboot:** [Date/time]
- **Uptime Required:** [99.9%]
- **Planned Maintenance:** [Any upcoming]

**Change History:**

| Date | Change Type | Description | Performed By | Ticket # | Approved By |
|------|-------------|-------------|--------------|----------|-------------|
| [Date] | [Resource change] | [Increased RAM to 16GB] | [Name] | [#] | [Manager] |
| [Date] | [Software install] | [Installed App v2.0] | [Name] | [#] | [Manager] |

**Troubleshooting History:**

| Date | Issue | Resolution | Ticket # |
|------|-------|-----------|----------|
| [Date] | [Issue description] | [How resolved] | [#] |

**Documentation Links:**
- [Link to application documentation]
- [Link to runbooks]
- [Link to architecture diagrams]

**Special Notes:**
- [Any special configuration]
- [Known issues]
- [Workarounds]
- [Future plans]

---

#### Virtual Machine: [VM-DB-01]

[Repeat full structure for each VM]

---

#### Virtual Machine: [VM-WEB-01]

[Repeat full structure for each VM]

---

### Development/Test Virtual Machines

#### Virtual Machine: [VM-DEV-01]

[Same structure as production VMs]

---

## 4. SERVER RELATIONSHIPS AND DEPENDENCIES

### Application Stack Mappings

#### Application: [Business Application Name]

**Architecture:**
```
[Load Balancer/Web Tier]
        ↓
[VM-WEB-01] [VM-WEB-02] (Web Servers)
        ↓
[VM-APP-01] [VM-APP-02] (Application Servers)
        ↓
[VM-DB-01] (Database Server - Primary)
        ↓
[VM-DB-02] (Database Server - Secondary/Read Replica)
```

**Server Roles:**

| Server | Role | Criticality | Can Fail Without Impact? |
|--------|------|-------------|-------------------------|
| VM-WEB-01 | Web Front-end | Medium | Yes - redundant |
| VM-WEB-02 | Web Front-end | Medium | Yes - redundant |
| VM-APP-01 | App Logic | High | No - single instance |
| VM-DB-01 | Database Primary | Critical | No - contains data |
| VM-DB-02 | Database Replica | Medium | Yes - read-only |

**Failure Impact Analysis:**
- If [VM-WEB-01] fails → [Users redirected to VM-WEB-02, no impact]
- If [VM-APP-01] fails → [Application completely down, critical]
- If [VM-DB-01] fails → [Application down, data loss risk]

---

## 5. SERVER CONFIGURATIONS BY TYPE

### Domain Controllers

| Server | Role | FSMO Roles | IP | Site |
|--------|------|------------|----|----|
| [VM-DC-01] | Primary DC | Schema Master, Domain Naming Master | [IP] | [Main] |
| [VM-DC-02] | Secondary DC | RID Master, PDC Emulator, Infrastructure Master | [IP] | [Main] |

### Database Servers

| Server | DB Type | Version | Role | Connections | Max Capacity |
|--------|---------|---------|------|-------------|--------------|
| [VM-DB-01] | SQL Server | 2019 | Primary | [App servers] | [Max conn] |
| [VM-DB-02] | SQL Server | 2019 | Replica | [Read-only] | [Max conn] |

### Web Servers

| Server | Web Server | Version | Sites Hosted | SSL Certs | Load Balanced |
|--------|------------|---------|--------------|-----------|---------------|
| [VM-WEB-01] | IIS | 10 | [Site names] | [Cert details] | Yes |
| [VM-WEB-02] | Apache | 2.4 | [Site names] | [Cert details] | Yes |

### File Servers

| Server | Shares Hosted | Total Storage | Used | Permissions Model |
|--------|--------------|---------------|------|------------------|
| [VM-FILE-01] | [Share names] | [TB] | [TB] | [NTFS/Share] |

---

## 6. IP ADDRESS ALLOCATION

### Production VMs - Server VLAN (10.1.0.0/24)

| IP Address | Hostname | Role | Status | Notes |
|------------|----------|------|--------|-------|
| 10.1.0.1 | Gateway | Network | Active | - |
| 10.1.0.10 | VM-DC-01 | Domain Controller | Active | Primary DC |
| 10.1.0.11 | VM-APP-01 | Application | Active | Prod app server |
| 10.1.0.12 | VM-APP-02 | Application | Active | Prod app server |
| 10.1.0.20 | VM-DB-01 | Database | Active | SQL Primary |
| 10.1.0.21 | VM-DB-02 | Database | Active | SQL Replica |
| 10.1.0.30 | VM-WEB-01 | Web | Active | IIS |
| 10.1.0.31 | VM-FILE-01 | File | Active | File shares |
| ... | | | | |
| 10.1.0.200-250 | DHCP/Reserved | - | - | Future use |

---

## 7. SOFTWARE LICENSING

### Operating System Licenses

| OS | License Type | Count Used | Total Licenses | Expiry | Notes |
|----|--------------|------------|----------------|--------|-------|
| Windows Server 2019 Std | Datacenter | Unlimited | 2 sockets | [Date] | Covers all VMs |
| Ubuntu Server | Free | N/A | N/A | N/A | Open source |

### Application Licenses

| Application | License Type | Count Used | Total Licenses | Cost | Renewal Date |
|-------------|--------------|------------|----------------|------|--------------|
| SQL Server 2019 | Per Core | 32 cores | 32 cores | [Cost] | [Date] |
| Veeam Backup | Per socket | 4 sockets | 4 sockets | [Cost] | [Date] |
| [Application] | Per user | [Count] | [Count] | [Cost] | [Date] |

---

## 8. PATCH MANAGEMENT

### Patch Status by Server

| Server | Last Patched | Pending Patches | Reboot Required | Next Patch Window |
|--------|-------------|----------------|-----------------|-------------------|
| VM-APP-01 | [Date] | [Count] | Yes | [Date] |
| VM-DB-01 | [Date] | 0 | No | [Date] |

### Patch Schedule

**Critical Security Patches:**
- **Deployed:** Within 7 days of release
- **Testing:** Required on dev systems first
- **Window:** Emergency maintenance window

**Standard Patches:**
- **Deployed:** Monthly patch cycle
- **Testing:** 1 week on dev/test
- **Window:** Standard maintenance window

**Application Updates:**
- **Deployed:** Quarterly or as needed
- **Testing:** Full UAT required
- **Window:** Scheduled maintenance

---

## 9. SECURITY CONFIGURATIONS

### Security Baseline

**All Servers Must Have:**
- [ ] Antivirus installed and updated
- [ ] Windows Firewall enabled (or equivalent)
- [ ] Audit logging enabled
- [ ] Unnecessary services disabled
- [ ] Strong password policy enforced
- [ ] Admin accounts limited
- [ ] Automatic updates configured
- [ ] Monitoring agent installed

### Security Audit Checklist

**Monthly Audit Items:**
- [ ] Review local admin accounts
- [ ] Check for disabled antivirus
- [ ] Verify firewall status
- [ ] Review open ports
- [ ] Check failed login attempts
- [ ] Verify patch status

---

## 10. PERFORMANCE TUNING NOTES

### Optimized Configurations

#### VM-DB-01 Optimizations
- **Disk:** Placed on SSD datastore for performance
- **Memory:** Set reservation to prevent swapping
- **CPU:** Pinned to specific cores (if applicable)
- **SQL:** Max memory set to 12GB (of 16GB total)
- **SQL:** TempDB on separate disk

#### VM-APP-01 Optimizations
- [Document any performance tuning performed]

---

## 11. DISASTER RECOVERY CONFIGURATIONS

### DR Priority Tiers

**Tier 1 (Critical - RTO: 4 hours):**
- VM-DC-01 - Domain Controller
- VM-DB-01 - Database Primary
- VM-APP-01 - Application Server

**Tier 2 (Important - RTO: 24 hours):**
- VM-WEB-01 - Web Server
- VM-FILE-01 - File Server

**Tier 3 (Standard - RTO: 72 hours):**
- VM-DEV-01 - Development
- VM-TEST-01 - Testing

### Failover Sequences

**Application Stack Failover Order:**
1. Restore VM-DB-01 first
2. Restore VM-APP-01 second
3. Restore VM-WEB-01 last
4. Verify connectivity and dependencies
5. Update DNS if needed

---

## 12. DECOMMISSIONED SERVERS

### Retired Server Log

| Server | Decommission Date | Reason | Data Disposition | Hardware Disposition |
|--------|------------------|--------|------------------|---------------------|
| [OLD-SRV-01] | [Date] | [EOL/Migrated] | [Backed up and deleted] | [Recycled/Resold] |

---

## 13. PLANNED CHANGES

### Upcoming Server Deployments

| Server | Purpose | Planned Date | Owner | Status |
|--------|---------|--------------|-------|--------|
| [VM-APP-03] | Load balance app tier | [Date] | [Name] | [Planning/Approved/In Progress] |

### Upcoming Upgrades

| Server | Upgrade Type | Details | Planned Date | Risk |
|--------|-------------|---------|--------------|------|
| [VM-DB-01] | Version upgrade | SQL 2019 → 2022 | [Date] | [High/Medium/Low] |

---

## 14. TROUBLESHOOTING QUICK REFERENCE

### Server-Specific Known Issues

#### VM-APP-01
- **Issue:** Memory leak in App Service
- **Symptom:** RAM usage climbs over 3 days
- **Workaround:** Weekly service restart
- **Permanent Fix:** [Pending vendor patch]

#### VM-DB-01
- **Issue:** High CPU during batch jobs
- **Symptom:** CPU > 90% between 2-4 AM
- **Expected:** Normal during batch window
- **No Action Needed:** Unless extends past 5 AM

---

## 15. CONTACT AND OWNERSHIP

### Server Ownership Matrix

| Server | Technical Owner | Business Owner | On-Call Contact |
|--------|----------------|----------------|----------------|
| VM-APP-01 | [IT person] | [Department] | [Phone/pager] |
| VM-DB-01 | [DBA name] | [Department] | [Phone/pager] |

---

## NOTES FOR USING THIS DATABASE

**For the AI Agent:**
- Use this database for detailed server information
- Reference when troubleshooting specific servers
- Check dependencies before making changes
- Verify configurations match documentation
- Update after any server changes
- Use for understanding application architectures

**For Maintenance:**
- Update immediately after any server changes
- Keep all fields current
- Document all configuration changes
- Review quarterly for accuracy
- Remove or archive decommissioned servers
- Add new servers immediately upon deployment

**For Populating This Template:**
- Start with critical production servers
- Add detail incrementally
- Update as you discover information
- Document during troubleshooting
- Use screenshots for complex configurations
- Cross-reference with monitoring systems
- Verify information periodically

**Data Collection Tips:**
- Use PowerShell/scripts to gather info
- Export from virtualization platform
- Pull from monitoring systems
- Document during maintenance windows
- Take screenshots of configurations
- Export network configs
- Pull software inventory from SCCM/similar

---

**Template Status:** Ready for population  
**Priority:** HIGH - Essential for operations  
**Estimated Time to Complete:** 10-15 hours for comprehensive documentation  
**Next Steps:** Start with critical production servers, document systematically  
**Update Frequency:** After every server change, quarterly comprehensive review

