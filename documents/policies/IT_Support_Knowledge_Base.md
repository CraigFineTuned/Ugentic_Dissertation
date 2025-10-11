# IT SUPPORT KNOWLEDGE BASE

## Password Reset Procedures

**KB-001: Standard Password Reset**

### Procedure:
1. Verify user identity (security questions or employee ID)
2. Access password management system
3. Generate temporary password
4. Send to user's registered email
5. User must change on first login

### User Education:
- Strong password requirements: 12+ characters, mixed case, numbers, symbols
- Password manager recommendations
- Self-service portal: [company portal URL]

### Security Notes:
- Never reset without identity verification
- Log all password resets
- Monitor for suspicious patterns

---

## Email Configuration Issues

**KB-EMAIL-012: Mobile Email Sync Issues**

### Common Causes:
1. Mobile device authentication settings incorrect
2. Security certificate issues (common after updates)
3. VPN/network connectivity differences
4. Exchange ActiveSync configuration problems

### Troubleshooting Steps:
1. Verify account settings (server, username, password)
2. Check network connectivity (WiFi vs mobile data)
3. Recent phone updates? May need account re-sync
4. Certificate issues: Remove and re-add account

### Certificate Renewal Impact:
- Desktop Outlook auto-updates certificates
- Mobile devices (iOS/Android) require manual re-sync
- Solution: Remove email account, re-add to get new certificate
- Prevention: Communicate before certificate renewals

---

## Network Connectivity

**KB-NET-015: VPN Connection Problems**

### Common Issues:
1. VPN certificate expired
2. Network firewall blocking VPN ports
3. VPN server at capacity
4. User credentials incorrect

### Diagnosis:
1. Check certificate validity
2. Verify user can reach VPN server
3. Test from different network
4. Check VPN server logs

### Escalation:
- Certificate issues: Infrastructure team
- Server capacity: Infrastructure team
- Network blocks: Network Support team

---

## Application Performance

**KB-APP-045: Slow Application Response**

### Investigation Steps:
1. Single user or multiple users affected?
2. Specific application or all applications?
3. Recent application updates deployed?
4. Time-based pattern?

### Common Causes:
- Database query performance issues
- Server resource constraints
- Network latency
- Application bugs

### Collaboration Needed:
- Database issues: Infrastructure + App Support
- Network issues: Network Support
- Application bugs: App Support
- Server resources: Infrastructure

---

## Hardware Issues

**KB-HW-023: Computer Won't Start**

### Basic Troubleshooting:
1. Check power cable connected
2. Check monitor power and connection
3. Try different power outlet
4. Listen for beep codes
5. Check for lights on computer

### Advanced Diagnosis:
- No lights/sounds: Power supply issue
- Lights but no display: Monitor or graphics issue
- Beep codes: Reference motherboard manual
- Fans running but no boot: Hardware failure

### Escalation:
- Hardware replacement needed: IT Support can handle
- Complex diagnosis: Infrastructure team

---

## Software Installation

**KB-SW-018: Standard Software Installation**

### Approved Software List:
- Microsoft Office Suite
- Adobe Reader
- Web Browsers (Chrome, Firefox, Edge)
- Company VPN Client
- Antivirus Software

### Installation Process:
1. Verify software is approved
2. Check license availability
3. Remote installation via management tools
4. Verify installation successful
5. Provide basic user training

### License Management:
- Check license pool before installing
- Document all installations
- Notify if licenses running low

---

## Security Incidents

**KB-SEC-030: Suspected Security Incident**

### Immediate Actions:
1. Isolate affected system from network
2. Notify IT Manager immediately
3. Preserve evidence (don't delete anything)
4. Document timeline of events

### Information to Gather:
- What user observed
- When incident started
- What systems affected
- Any unusual emails/messages received

### Escalation Path:
**URGENT → IT Manager → Security Team**

Never attempt to resolve security incidents alone - always escalate immediately.

---

## System Performance

**KB-SYS-042: General System Slowness**

### Quick Checks:
1. Task Manager: Check CPU, memory, disk usage
2. Recent software installations?
3. Windows updates pending?
4. Multiple programs open?

### Common Solutions:
- Close unnecessary programs
- Restart computer
- Check for malware
- Clear temporary files
- Check disk space

### When to Escalate:
- Hardware failure suspected: Infrastructure
- Multiple users affected: System-wide issue
- Malware suspected: Security incident protocol

---

## Printer Issues

**KB-PRT-035: Common Printer Problems**

### Cannot Print:
1. Check printer power and connections
2. Check printer queue for stuck jobs
3. Verify printer driver installed
4. Test from different computer

### Print Quality Issues:
- Streaks/smudges: Clean print heads
- Faded output: Check toner/ink levels
- Paper jams: Follow printer's jam removal guide

### Network Printer Issues:
- Can't find printer: Check network connection
- Driver issues: Reinstall printer driver
- Authentication problems: Verify user credentials

---

## Remote Access

**KB-REM-028: Remote Access Setup**

### VPN Setup:
1. Install VPN client software
2. Configure with company VPN address
3. Use employee credentials
4. Test connection from remote location

### Remote Desktop:
1. Ensure user's computer configured for remote access
2. Provide user with computer name/IP
3. Test connection
4. Document security settings

### Security Requirements:
- VPN required for all remote access
- Multi-factor authentication enabled
- Regular password updates
- Report suspicious activity

---

## Microsoft Office Issues

**KB-OFF-050: Office Application Problems**

### Word/Excel/PowerPoint Won't Open:
1. Check for Office updates
2. Repair Office installation
3. Check file permissions
4. Try safe mode launch

### File Corruption:
- Try "Open and Repair" option
- Check for auto-save/backup copies
- Use document recovery features

### Activation Issues:
- Verify license assigned to user
- Re-activate using company license key
- Check Office 365 subscription status

---

## Ubuntu Principles in IT Support

### Collective Problem-Solving:
- Check knowledge base before troubleshooting
- Ask team when encountering novel issues
- Share solutions immediately with team

### Knowledge Sharing:
- Document all novel solutions
- Update knowledge base regularly
- Teach others what you learn

### Mutual Support:
- Offer help when teammates overloaded
- Ask for help when stuck
- Celebrate team successes

### Consensus Building:
- Discuss process improvements as team
- Build agreement on standard procedures
- Value all team members' input

---

**Last Updated:** October 6, 2025  
**Version:** 1.0  
**Maintained By:** IT Support Team
