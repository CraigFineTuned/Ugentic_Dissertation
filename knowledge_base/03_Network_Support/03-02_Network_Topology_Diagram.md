# Network Topology Diagram

**Purpose:** This document contains comprehensive network topology diagrams, physical layouts, logical network architecture, and cable/connection documentation for the entire network infrastructure.

**Last Updated:** [Date]  
**Maintained By:** Network Support Team

---

## 1. DOCUMENT OVERVIEW

### What This Document Contains

This document provides visual and textual representations of:
- **Physical Topology:** How devices are physically connected
- **Logical Topology:** How data flows through the network
- **Network Segments:** VLANs, subnets, and security zones
- **Connection Details:** Cable types, fiber runs, ports used
- **Rack Diagrams:** Physical equipment layout

### Diagram Conventions

**Standard Symbols:**
```
[Router] = Router device
[Switch] = Network switch
(AP) = Wireless access point
[FW] = Firewall
[Server] = Server
(PC) = End user computer
─── = Ethernet cable
~~~ = Fiber optic cable
... = Wireless connection
=== = WAN/Internet connection
```

**Color Coding:** (if using colored diagrams)
- **Blue:** Internal network connections
- **Red:** External/Internet connections
- **Green:** Management network
- **Orange:** DMZ/security zone
- **Yellow:** Wireless coverage

---

## 2. HIGH-LEVEL NETWORK OVERVIEW

### Network Architecture Diagram

```
                    INTERNET
                       ║
                       ║ (Fiber - [Speed])
                       ║
                   [FIREWALL]
            (Primary + Secondary)
                       ║
                   [Router]
              (Core Network Gateway)
                       ║
            ┌──────────┼──────────┐
            │          │          │
       [Switch 1]  [Switch 2]  [Switch 3]
       (Core/      (Building    (Building
        Distro)     A)           B)
            │          │          │
        [Access    [Access    [Access
         Layer]     Layer]     Layer]
            │          │          │
       (Users)    (Users)    (Users)
```

**Key Components:**
- **Internet Connection:** [Type and speed]
- **Firewall:** [Make/model]
- **Core Router:** [Make/model]
- **Distribution Switches:** [Count and purpose]
- **Access Switches:** [Count and locations]
- **Total End Points:** [Approximate count]

**Network Hierarchy:**
- **Tier 1 (Core):** [Core devices]
- **Tier 2 (Distribution):** [Distribution layer]
- **Tier 3 (Access):** [Access layer devices]

---

## 3. DETAILED PHYSICAL TOPOLOGY

### Complete Physical Network Diagram

```
                                INTERNET
                                   ║
                        ISP Router [IP: xxx.xxx.xxx.xxx]
                                   ║
                                   ║ Fiber Link
                                   ║
┌────────────────────────────────────────────────────────────┐
│                    FIREWALL CLUSTER                         │
│  [FW-Primary]              [FW-Secondary]                  │
│  IP: 10.0.0.1              IP: 10.0.0.2                    │
│  External: x.x.x.x         External: x.x.x.x               │
│  (Active)                  (Standby)                       │
└────────────────────┬───────────────────────────────────────┘
                     │
                     │ Port 1/0/1
                     │
              [CORE-ROUTER-01]
           Hostname: core-rt-01
           IP: 10.0.0.10
           Model: [Router model]
                     │
     ┌───────────────┼───────────────┬────────────────┐
     │ Port 1/0/2    │ Port 1/0/3    │ Port 1/0/4     │
     │               │               │                │
[DIST-SW-01]   [DIST-SW-02]   [DIST-SW-03]     [DIST-SW-04]
Building A     Server Room     Building B      Management
IP: 10.0.0.21  IP: 10.0.0.22  IP: 10.0.0.23   IP: 10.0.0.24
Model: [Model] Model: [Model] Model: [Model]  Model: [Model]
     │              │              │               │
     │              │              │               │
  (Access     (Servers &      (Access        (Network
   Layer       Storage)         Layer)        Devices)
   Switches)                    Switches)
```

**Physical Location Map:**
```
[Building Layout or Floor Plan Reference]

Building A:
- Server Room (Main IDF): DIST-SW-01, Servers
- Floor 1 IDF: ACCESS-SW-A1
- Floor 2 IDF: ACCESS-SW-A2
- Floor 3 IDF: ACCESS-SW-A3

Building B:
- MDF: DIST-SW-03
- Floor 1 IDF: ACCESS-SW-B1
- Floor 2 IDF: ACCESS-SW-B2
```

### Device Interconnections

#### Core to Distribution Layer

| Source Device | Source Port | Destination Device | Dest Port | Cable Type | Length | Notes |
|--------------|-------------|-------------------|-----------|------------|--------|-------|
| CORE-RT-01 | Gi1/0/2 | DIST-SW-01 | Gi1/0/48 | Fiber OM3 | 50m | 10Gbps |
| CORE-RT-01 | Gi1/0/3 | DIST-SW-02 | Gi1/0/48 | Fiber OM3 | 30m | 10Gbps |
| CORE-RT-01 | Gi1/0/4 | DIST-SW-03 | Gi1/0/48 | Fiber OM4 | 200m | 10Gbps |

#### Distribution to Access Layer

| Source Device | Source Port | Destination Device | Dest Port | Cable Type | Length | Notes |
|--------------|-------------|-------------------|-----------|------------|--------|-------|
| DIST-SW-01 | Gi1/0/1 | ACCESS-SW-A1 | Gi1/0/24 | Cat6 | 40m | 1Gbps |
| DIST-SW-01 | Gi1/0/2 | ACCESS-SW-A2 | Gi1/0/24 | Cat6 | 60m | 1Gbps |

---

## 4. LOGICAL NETWORK TOPOLOGY

### VLAN Topology Diagram

```
                    CORE ROUTER
                   (10.0.0.10)
                        │
                        │ Router on a Stick
                        │ (All VLANs tagged)
                        │
                DISTRIBUTION SWITCH
               (10.0.0.21 - VLAN 10)
                        │
        ┌───────────────┼───────────────┬───────────────┐
        │               │               │               │
    VLAN 10         VLAN 20         VLAN 30         VLAN 40
   Management       Servers          Users           Voice
  10.0.0.0/24     10.1.0.0/24     10.2.0.0/22     10.3.0.0/24
        │               │               │               │
   [Network        [Production    [Workstations]  [IP Phones]
    Devices]        Servers]
```

### VLAN Segmentation

**VLAN Table:**

| VLAN ID | Name | Subnet | Gateway | Purpose | Allowed To |
|---------|------|--------|---------|---------|-----------|
| 1 | Default | Unused | - | Not used | None |
| 10 | Management | 10.0.0.0/24 | 10.0.0.1 | Device management | Management team |
| 20 | Servers | 10.1.0.0/24 | 10.1.0.1 | Production servers | All VLANs (filtered) |
| 30 | Users | 10.2.0.0/22 | 10.2.0.1 | End user workstations | Internet, Servers |
| 40 | Voice | 10.3.0.0/24 | 10.3.0.1 | VoIP phones | Voice servers only |
| 50 | Guest | 10.4.0.0/24 | 10.4.0.1 | Guest WiFi | Internet only |
| 99 | DMZ | 192.168.100.0/24 | 192.168.100.1 | Public servers | Internet (controlled) |

**Inter-VLAN Routing:**
```
VLAN 30 (Users) ──→ VLAN 20 (Servers) [Allowed - Firewall filtered]
VLAN 30 (Users) ──→ Internet [Allowed]
VLAN 30 (Users) ──╳ VLAN 10 (Management) [Denied]
VLAN 50 (Guest) ──→ Internet [Allowed]
VLAN 50 (Guest) ──╳ All Internal VLANs [Denied]
```

### Traffic Flow Diagram

**User Internet Access:**
```
[User PC] → [Access Switch] → [Distribution Switch] → [Core Router] → [Firewall] → Internet
VLAN 30      VLAN 30           VLAN 30 trunk        Routes         NAT         External
```

**User to Server Access:**
```
[User PC] → [Access Switch] → [Distribution Switch] → [Core Router] → [Distribution Switch] → [Server]
VLAN 30      VLAN 30           VLAN 30 trunk        Routes to       VLAN 20 trunk        VLAN 20
                                                     VLAN 20
                                                     (Firewall rules apply)
```

---

## 5. WIRELESS NETWORK TOPOLOGY

### Wireless Architecture

```
                [Wireless Controller]
                 (10.0.0.30)
                 VLAN 10
                      │
                      │ Manages all APs
                      │
      ┌───────────────┼───────────────┬─────────────┐
      │               │               │             │
   [AP-01]        [AP-02]        [AP-03]       [AP-04]
  Floor 1         Floor 1        Floor 2       Floor 2
Building A      Building A      Building A    Building B
10.3.0.101      10.3.0.102     10.3.0.103    10.3.0.104
```

### Access Point Coverage Map

**Building A - Floor 1:**
```
┌─────────────────────────────────┐
│                                 │
│  [AP-01]        Conf Room       │
│    │            [AP-02]          │
│    │               │             │
│  Coverage       Coverage         │
│  Circle         Circle           │
│                                 │
└─────────────────────────────────┘
```

**AP Details:**

| AP Name | Location | IP | MAC | SSID(s) Broadcast | Power | Channel | Coverage |
|---------|----------|----|----|------------------|-------|---------|----------|
| AP-01 | Bldg A-F1-NW | 10.3.0.101 | [MAC] | Corp, Guest | High | 1 | NW quadrant |
| AP-02 | Bldg A-F1-SE | 10.3.0.102 | [MAC] | Corp, Guest | High | 6 | SE quadrant |
| AP-03 | Bldg A-F2-C | 10.3.0.103 | [MAC] | Corp, Guest | Medium | 11 | Center |
| AP-04 | Bldg B-F2-E | 10.3.0.104 | [MAC] | Corp, Guest | High | 1 | East side |

**Wireless Topology Notes:**
- All APs on VLAN 40 (Management)
- Corp SSID broadcasts on VLAN 30
- Guest SSID broadcasts on VLAN 50
- Controller performs CAPWAP tunneling

---

## 6. WAN AND EXTERNAL CONNECTIONS

### Internet Connectivity

```
                        ┌─────────────┐
                        │  Internet   │
                        └──────┬──────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
            [ISP Router 1]              [ISP Router 2]
            Primary Link                Backup Link
            Fiber 1Gbps                 Cable 100Mbps
            Static: x.x.x.x             DHCP
                 │                           │
                 └──────────┬────────────────┘
                            │
                      [Firewall]
                   (Load balanced/
                    Failover)
                            │
                   [Internal Network]
```

**Primary Internet:**
- **ISP:** [Provider name]
- **Circuit ID:** [ID]
- **Technology:** [Fiber/Cable/etc]
- **Speed:** [Download / Upload]
- **Static IPs:** [IP range]
- **Router:** [Device and IP]

**Backup Internet:**
- **ISP:** [Provider name]
- **Circuit ID:** [ID]
- **Technology:** [Type]
- **Speed:** [Download / Upload]
- **Failover Trigger:** [Condition that triggers switch]

### VPN Topology

**Remote Access VPN:**
```
[Remote User] ──→ Internet ──→ [Firewall VPN Endpoint] ──→ [Internal Network]
                               (x.x.x.x:443)                  (VPN Pool: 10.5.0.0/24)
```

**Site-to-Site VPN:**
```
[Main Site] ←────────────→ [Remote Site 1]
  10.0.0.0/8               172.16.0.0/16
              Internet VPN
              IPsec Tunnel
```

**VPN Tunnel Details:**

| Tunnel Name | Local Subnet | Remote Subnet | Encryption | Status Check |
|------------|-------------|---------------|------------|--------------|
| HQ-to-Branch1 | 10.0.0.0/8 | 172.16.0.0/16 | AES-256 | [How to check] |
| HQ-to-Branch2 | 10.0.0.0/8 | 172.17.0.0/16 | AES-256 | [How to check] |

---

## 7. SECURITY ZONES AND DMZ

### Security Zone Diagram

```
                    INTERNET
                       ║
            ┌──────────╬──────────┐
            │   EXTERNAL ZONE      │
            │  (Untrusted)         │
            └──────────┬───────────┘
                       │
                  [FIREWALL]
                   /   │   \
                  /    │    \
                 /     │     \
            ┌───┘  ┌───┴───┐  └───┐
            │      │       │      │
        [DMZ]  [INTERNAL] [MGT]  │
     192.168.100   10.0.0   10.0.0  │
       .0/24        .0/8    .0/24
            │         │        │
        [Web    [All Internal [Network
         Servers]  Resources]  Devices]
         [Mail
         Servers]
```

**Zone Definitions:**

**External Zone:**
- Purpose: Internet and untrusted networks
- Access to Internal: Denied by default
- Access to DMZ: Specific services allowed (HTTP, HTTPS, SMTP)

**DMZ Zone:**
- Purpose: Public-facing servers
- Subnet: 192.168.100.0/24
- Devices: [List of servers in DMZ]
- Access to Internal: Denied except specific
- Access from Internal: Allowed for management

**Internal Zone:**
- Purpose: Corporate network
- Subnets: All 10.x.x.x networks
- Access to DMZ: Allowed for management
- Access to Internet: Allowed with NAT

**Management Zone:**
- Purpose: Network device management
- Subnet: 10.0.0.0/24
- Access: Restricted to IT staff
- Devices: All network infrastructure

---

## 8. DATA CENTER / SERVER ROOM TOPOLOGY

### Server Room Layout

```
Rack 1          Rack 2          Rack 3          Rack 4
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ [FW-1] │     │[APP-01]│     │[DB-01] │     │[DIST-  │
│ [FW-2] │     │[APP-02]│     │[DB-02] │     │ SW-02] │
│        │     │[APP-03]│     │[FILE-  │     │        │
│[CORE-  │     │        │     │ 01]    │     │[UPS-2] │
│ RT-01] │     │[BACKUP │     │[BACKUP │     │        │
│        │     │ -01]   │     │ -02]   │     │        │
│[UPS-1] │     │        │     │        │     │        │
└────────┘     └────────┘     └────────┘     └────────┘
```

**Server Room Network:**
```
                 [DIST-SW-02]
                      │
        ┌─────────────┼─────────────┬─────────────┐
        │             │             │             │
   [APP-01]      [APP-02]      [DB-01]      [FILE-01]
   10.1.0.11     10.1.0.12     10.1.0.21     10.1.0.31
   Port 11       Port 12       Port 21       Port 31
```

**Server Connections:**

| Server | Switch | Port | IP | VLAN | Cable | Speed |
|--------|--------|------|----|----|-------|-------|
| APP-01 | DIST-SW-02 | Gi1/0/11 | 10.1.0.11 | 20 | Cat6 | 1Gbps |
| APP-02 | DIST-SW-02 | Gi1/0/12 | 10.1.0.12 | 20 | Cat6 | 1Gbps |
| DB-01 | DIST-SW-02 | Gi1/0/21 | 10.1.0.21 | 20 | Fiber | 10Gbps |
| FILE-01 | DIST-SW-02 | Gi1/0/31 | 10.1.0.31 | 20 | Cat6 | 1Gbps |

---

## 9. RACK ELEVATIONS

### Rack 1 - Core Network Equipment

```
U48  ═══════════════════════════
U47  ─ Blank Panel ─
U46  ═══════════════════════════
U45  ┌──────────────────────┐
U44  │  FIREWALL-PRIMARY    │
U43  │  (FW-01)             │
U42  └──────────────────────┘
U41  ─ Blank Panel ─
U40  ┌──────────────────────┐
U39  │  FIREWALL-SECONDARY  │
U38  │  (FW-02)             │
U37  └──────────────────────┘
U36  ─ Patch Panel 48-port ─
U35  ─ Patch Panel 48-port ─
U34  ┌──────────────────────┐
U33  │  CORE-ROUTER-01      │
U32  └──────────────────────┘
U31  ─ Blank Panel ─
...
U03  ┌──────────────────────┐
U02  │  UPS-1               │
U01  │  (2000VA)            │
U00  └──────────────────────┘
```

### Rack 2 - Application Servers

```
U48  ═══════════════════════════
...
[Create similar elevation for each rack]
```

**Rack Inventory:**

| Rack | Equipment Count | Power Draw | Cooling | Notes |
|------|----------------|------------|---------|-------|
| Rack 1 | [Count] | [Watts] | [CFM needed] | Core network |
| Rack 2 | [Count] | [Watts] | [CFM needed] | App servers |
| Rack 3 | [Count] | [Watts] | [CFM needed] | Database/storage |
| Rack 4 | [Count] | [Watts] | [CFM needed] | Distribution |

---

## 10. CABLE MANAGEMENT

### Structured Cabling

**Cable Types in Use:**
- **Cat5e:** [Where used - typically legacy]
- **Cat6:** [Where used - standard desktop]
- **Cat6a:** [Where used - high bandwidth]
- **Fiber OM3:** [Where used - short runs]
- **Fiber OM4:** [Where used - long runs]
- **Single Mode Fiber:** [Where used - very long runs]

### Fiber Runs

| Run ID | Start Location | End Location | Type | Distance | Termination | Status |
|--------|---------------|--------------|------|----------|-------------|--------|
| F-01 | MDF Rack 1 | IDF Bldg A | OM3 | 50m | LC-LC | Active |
| F-02 | MDF Rack 1 | IDF Bldg B | OM4 | 200m | LC-LC | Active |

### Patch Panel Documentation

**MDF Patch Panel 1:**

| Port | Cable ID | Destination | Device | Status |
|------|----------|-------------|--------|--------|
| 1 | C-001 | Bldg A-F1-J001 | User PC | Active |
| 2 | C-002 | Bldg A-F1-J002 | User PC | Active |
| 3 | C-003 | Bldg A-F1-J003 | Printer | Active |
...

**Cable Labeling Standard:**
```
Format: [Building]-[Floor]-[Room]-[Jack Number]
Example: A-1-101-J001
- A = Building A
- 1 = Floor 1
- 101 = Room 101
- J001 = Jack number 1
```

---

## 11. NETWORK PATHS AND ROUTING

### Routing Table Summary

**Static Routes:**

| Destination | Next Hop | Interface | Purpose |
|------------|----------|-----------|---------|
| 0.0.0.0/0 | [Firewall IP] | [Interface] | Default route |
| 172.16.0.0/16 | [VPN gateway] | [Interface] | Remote site 1 |
| 172.17.0.0/16 | [VPN gateway] | [Interface] | Remote site 2 |

**Dynamic Routing:**
- Protocol: [OSPF / EIGRP / BGP / None]
- Areas: [If OSPF]
- AS Number: [If BGP]

### Traceroute Examples

**User to Internet:**
```
PC (10.2.0.100) →
Access Switch (10.2.0.1) →
Distribution Switch →
Core Router (10.0.0.10) →
Firewall Internal (10.0.0.1) →
Firewall External (x.x.x.x) →
Internet
```

**User to Server:**
```
PC (10.2.0.100) →
Access Switch (VLAN 30) →
Distribution Switch →
Core Router (Routes VLAN 30 → VLAN 20) →
Distribution Switch →
Server (10.1.0.11)
```

---

## 12. REDUNDANCY AND HIGH AVAILABILITY

### Redundant Connections

```
             [ISP Router 1]     [ISP Router 2]
                    \              /
                     \            /
                   [FW-Primary] [FW-Secondary]
                      \         /
                       \       /
                    [Core Router]
                     /         \
              [DIST-SW-01]   [DIST-SW-02]
                LACP          LACP
              Active/Active
```

**Redundancy Details:**

| Component | Primary | Secondary | Failover Method | Failover Time |
|-----------|---------|-----------|-----------------|---------------|
| Internet | ISP 1 | ISP 2 | Automatic | < 30 seconds |
| Firewall | FW-01 | FW-02 | HA Cluster | < 5 seconds |
| Core Switch | DIST-SW-01 | DIST-SW-02 | LACP | Immediate |

### LACP / Link Aggregation

**LAG Groups:**

| LAG ID | Member Ports | Speed | Protocol | Purpose |
|--------|-------------|-------|----------|---------|
| LAG-1 | Gi1/0/47-48 | 2x10Gbps | LACP | Core uplink |
| LAG-2 | Gi1/0/45-46 | 2x10Gbps | LACP | Server connections |

---

## 13. OUT-OF-BAND MANAGEMENT

### Management Network

```
[Management Laptop]
        │
[Management Switch]
(10.0.0.24)
        │
    ┌───┴───┬───────┬────────┬────────┐
[FW-01] [FW-02] [CORE-RT] [DIST-SW] [Others]
Console Console Console   Console
Ports   Ports   Ports     Ports
```

**Management Access Methods:**

| Device | Management IP | Console Access | Out-of-Band | Notes |
|--------|--------------|----------------|-------------|-------|
| FW-01 | 10.0.0.1 | Serial | Yes | Console server port 1 |
| CORE-RT-01 | 10.0.0.10 | Serial | Yes | Console server port 2 |
| DIST-SW-01 | 10.0.0.21 | Serial | Yes | Console server port 3 |

**Console Server:**
- Model: [Model]
- IP: [IP address]
- Ports: [Number of ports]
- Access Method: [SSH, Telnet, Web]

---

## 14. MONITORING NETWORK DIAGRAM

### Monitoring Architecture

```
              [Monitoring Server]
               (10.0.0.50)
                    │
                    │ SNMP v3
            ┌───────┼────────┬────────┐
            │       │        │        │
        [Routers] [Switches] [FW] [Servers]
           │         │        │       │
       SNMP Traps sent to Monitoring Server
```

**What's Monitored:**
- Device health (CPU, memory, temperature)
- Link status and bandwidth
- Error counters
- Environmental (if sensors present)

**Monitoring Tools:**
- Tool: [Monitoring solution name]
- Server: [Hostname and IP]
- Access: [URL or method]

---

## 15. NETWORK CHANGES HISTORY

### Topology Evolution

| Date | Change Description | Affected Areas | Updated By |
|------|-------------------|---------------|------------|
| [Date] | Added DIST-SW-03 for Building B | Building B | [Name] |
| [Date] | Upgraded core link to 10Gbps | MDF to IDF-A | [Name] |
| [Date] | Deployed 5 new APs | Building A Floor 3 | [Name] |

**Next Planned Changes:**
- [Date]: [Planned change 1]
- [Date]: [Planned change 2]

---

## 16. TROUBLESHOOTING WITH TOPOLOGY

### How to Use This Document for Troubleshooting

**Scenario: User Cannot Access Server**

1. Reference logical topology to understand VLAN routing
2. Trace path from user VLAN to server VLAN
3. Check each device in the path
4. Reference firewall rules (in separate document)
5. Verify routing at core router

**Scenario: Wireless Issues in Specific Area**

1. Reference wireless coverage map
2. Identify which AP should cover the area
3. Check AP status on topology diagram
4. Verify AP connectivity through physical topology
5. Check wireless controller status

**Scenario: Internet Connectivity Problem**

1. Reference WAN topology
2. Verify which ISP link should be active
3. Check firewall external interface
4. Trace path from core router to firewall
5. Verify routing and NAT

---

## 17. DISASTER RECOVERY NETWORK

### DR Network Topology

(If you have a DR site)

```
[Primary Site]                    [DR Site]
   10.0.0.0/8  ←──VPN Tunnel──→  172.16.0.0/16
      │                                │
  [Full Network]                  [Essential Services]
```

**DR Network Details:**
- DR Location: [Location]
- DR Network: [IP range]
- Replication: [How data replicates]
- Failover Process: [Steps to failover]

---

## 18. FUTURE EXPANSION PLANNING

### Planned Network Growth

**Capacity for Growth:**
- **Switch Ports Available:** [Count and locations]
- **Fiber Runs Installed but Unused:** [List]
- **Rack Space Available:** [Count and locations]

**Expansion Areas:**
```
[Diagram showing potential expansion]
- New building connection points identified
- Fiber conduit pre-run to expansion areas
- Power and cooling capacity for growth
```

---

## 19. NETWORK DOCUMENTATION ASSETS

### Diagram File Locations

**Master Diagram Files:**
- **Tool Used:** [Visio, Draw.io, Lucidchart, etc.]
- **File Location:** [Path to files]
- **Version Control:** [How diagrams are versioned]
- **Last Updated:** [Date]

**Physical Copies:**
- Printed diagrams location: [Where in office]
- Emergency binder: [Location]

**Export Formats:**
- Editable: [.vsdx, .drawio, etc.]
- PDF: [Location]
- PNG/JPG: [Location for quick reference]

---

## NOTES FOR USING THIS DOCUMENT

**For the AI Agent:**
- Use this document to understand physical and logical network layout
- Reference when troubleshooting connectivity issues
- Understand device relationships and dependencies
- Use cable information to identify physical layer problems
- Reference VLAN topology when investigating routing issues

**For Maintenance:**
- Update immediately after any network changes
- Keep device inventory current
- Update cable documentation as you discover labeling
- Review quarterly for accuracy
- Update after any expansion or reconfiguration

**For Populating This Template:**
- Start with high-level diagrams
- Add detail incrementally as you document
- You can create diagrams in any tool
- Text-based diagrams are fine to start
- Take photos of rack layouts if easier
- Document what you know now, expand over time
- Include device names, IPs, and connection details
- Cable documentation takes time - do it progressively

**Diagram Tips:**
- Simple text diagrams work well initially
- Can use ASCII art for quick documentation
- Take photos and annotate them
- Use consistent naming conventions
- Focus on accuracy over beauty
- Document as you troubleshoot

---

**Template Status:** Ready for population  
**Priority:** Start with high-level overview, then add device details  
**Estimated Time to Complete:** 4-6 hours for basic documentation  
**Next Steps:** Create high-level network diagram, then document device interconnections
