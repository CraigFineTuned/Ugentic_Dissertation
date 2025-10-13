# Network Tool Parameter Validation Analysis

**Date:** October 12, 2025  
**Session:** 12  
**Issue:** Priority 1 - Network tool parameter validation enhancement

---

## Current State Analysis

### Network Tools Inventory

| Tool | Parameters | Current Defaults |
|------|------------|------------------|
| check_network_bandwidth | interface: str = "eth0" | ✅ 'interface': 'eth0' (EXISTS) |
| ping_test | host: str, count: int = 10 | ❌ 'host' missing |
| check_dns_resolution | domain: str = "google.com" | ❌ 'domain' missing |
| traceroute | destination: str, max_hops: int = 15 | ❌ 'destination' missing |
| measure_network_latency | source: str = "localhost", destination: str = "8.8.8.8" | ❌ 'source', 'destination' missing |
| check_firewall_rules | host: str = "localhost" | ❌ 'host' missing |
| get_network_utilization | interface: str = "eth0" | ✅ 'interface': 'eth0' (EXISTS) |

### Identified Gaps

**Missing Defaults (5 parameters):**
1. `host` - Used by: ping_test, check_firewall_rules
2. `destination` - Used by: traceroute, measure_network_latency
3. `domain` - Used by: check_dns_resolution
4. `source` - Used by: measure_network_latency
5. `count` / `max_hops` - Integer validation needed

**Parameter Types Needing Validation:**
1. IP addresses (IPv4 format: xxx.xxx.xxx.xxx)
2. Hostnames (valid domain format)
3. Interface names (eth0, wlan0, lo, etc.)
4. Integer ranges (count: 1-100, max_hops: 1-30)

---

## Enhancement Requirements

### 1. Add Network-Specific Defaults

```python
# Add to _infer_missing_parameter defaults:
'host': 'localhost',
'destination': '8.8.8.8',  # Google DNS
'domain': 'google.com',
'source': 'localhost',
'count': 10,
'max_hops': 15
```

### 2. Add Network-Specific Validation

**IP Address Validation:**
- Check format: xxx.xxx.xxx.xxx
- Each octet: 0-255
- Handle 'localhost' as special case

**Hostname Validation:**
- Allow alphanumeric + dots + hyphens
- Valid TLD

**Interface Validation:**
- Common: eth0, eth1, wlan0, lo, ens33
- Pattern: letters + numbers

**Integer Range Validation:**
- count: 1-100 (reasonable ping count)
- max_hops: 1-30 (reasonable traceroute limit)

### 3. Parameter Inference Intelligence

**Context-Aware Defaults:**
- If troubleshooting specific host → use that host
- If investigating connectivity → use external destination (8.8.8.8)
- If local testing → use localhost

---

## Implementation Plan

### Step 1: Enhance Smart Defaults ✅

Location: `tool_registry.py` → `_infer_missing_parameter()`

```python
# Add network defaults
defaults = {
    # ... existing defaults ...
    'host': 'localhost',
    'destination': '8.8.8.8',
    'domain': 'google.com',
    'source': 'localhost',
    'count': 10,
    'max_hops': 15
}
```

### Step 2: Add Network Validation Method ✅

New method: `_validate_network_parameter(param_name, value) -> Any`

Features:
- IP address format checking
- Hostname validation
- Interface name validation
- Integer range enforcement

### Step 3: Integrate Validation into Execute Flow ✅

Update: `_validate_parameters()` to call network validation for network tools

### Step 4: Enhanced Error Messages ✅

Update: `_generate_parameter_hint()` to include network-specific guidance

---

## Expected Outcomes

**Before Enhancement:**
```python
# LLM calls ping_test without host parameter
ping_test()  # → TypeError: missing required argument 'host'
```

**After Enhancement:**
```python
# LLM calls ping_test without host parameter  
ping_test()  # → Inferred: host='localhost', successfully executes
```

**With Invalid Values:**
```python
# LLM provides invalid IP
ping_test(host="999.999.999.999")
# → Validation error: "Invalid IP address format"
# → Hint: "Valid format: xxx.xxx.xxx.xxx (0-255 each)"
```

---

## Risk Assessment

**Low Risk:**
- Adding defaults is backward compatible
- Validation is additive (doesn't break existing functionality)
- Falls back gracefully on validation errors

**Testing Required:**
- All 7 network tools with missing parameters
- Invalid IP addresses
- Invalid hostnames
- Out-of-range integers
- Edge cases (localhost, 127.0.0.1, 0.0.0.0)

---

## Success Criteria

1. ✅ All 7 network tools can execute with missing parameters
2. ✅ Invalid network parameters are caught and corrected
3. ✅ Helpful error messages guide LLM to correct usage
4. ✅ No regression in existing tool functionality
5. ✅ Validation adds < 5ms overhead per tool call

---

**Status:** Analysis complete, ready for implementation  
**Next Step:** Implement enhanced validation in tool_registry.py
