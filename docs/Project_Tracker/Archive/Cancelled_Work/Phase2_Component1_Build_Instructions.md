# 🛠️ PHASE 2 - COMPONENT 1: MCP MEMORY SERVER BUILD INSTRUCTIONS

**Component:** MCP Memory Server Setup  
**Time:** ~30 minutes  
**Status:** ⏳ READY TO BUILD  
**Prerequisites:** Node.js v22.11.0 ✅

---

## 📍 STEP-BY-STEP BUILD INSTRUCTIONS

### **Step 1: Navigate to Memory Server Directory**

```bash
cd C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\servers-main\src\memory
```

---

### **Step 2: Install Node.js Dependencies**

```bash
npm install
```

**Expected Output:**
```
added 50 packages, and audited 51 packages in 15s
found 0 vulnerabilities
```

**This installs:**
- @modelcontextprotocol/sdk
- TypeScript compiler
- Type definitions
- Build tools

---

### **Step 3: Build the TypeScript Server**

```bash
npm run build
```

**Expected Output:**
```
> @modelcontextprotocol/server-memory@0.6.3 build
> tsc && shx chmod +x dist/*.js

(TypeScript compilation output...)
```

**What This Does:**
- Compiles `index.ts` → `dist/index.js`
- Creates `dist/` directory with compiled JavaScript
- Makes the output executable

---

### **Step 4: Verify Build Success**

**Check for dist folder:**
```bash
dir dist
```

**Expected Files:**
```
index.js
index.js.map
```

**✅ Build Successful if both files exist!**

---

### **Step 5: Test Server Startup**

```bash
node dist/index.js
```

**Expected Output:**
```
Knowledge Graph MCP Server running on stdio
```

**What This Means:**
- Server is operational ✅
- Listening on stdin/stdout (MCP protocol)
- Waiting for JSON-RPC messages
- Ready to store knowledge graph data

**To stop the server:**
- Press `Ctrl+C`

---

## 🎯 WHAT YOU JUST BUILT

### **MCP Memory Server Architecture:**

```
servers-main/src/memory/
├── index.ts              (TypeScript source)
├── dist/
│   ├── index.js          (Compiled JavaScript) ✅
│   └── memory.json       (Knowledge graph storage - created on first use)
├── package.json          (Dependencies)
├── tsconfig.json         (TypeScript config)
└── README.md
```

### **Knowledge Graph Structure:**

**Entities** (Nodes):
```json
{
  "name": "shared_drive_issue",
  "entityType": "problem",
  "observations": [
    "Users cannot access \\\\fileserver\\shared",
    "Error: Network path not found"
  ]
}
```

**Relations** (Edges):
```json
{
  "from": "shared_drive_issue",
  "to": "dns_misconfiguration",
  "relationType": "caused_by"
}
```

**Storage:** `dist/memory.json` (newline-delimited JSON)

---

## 🧪 TESTING THE SERVER

### **Test 1: Create Entity** (Optional Manual Test)

You can test the server by sending it JSON-RPC messages, but this is advanced and not necessary. The Python AgentMemory class (Component 2) will handle all communication.

**Skip this test** - The Python integration tests will verify everything works.

---

## 📦 DELIVERABLE CHECKLIST

**After completing these steps, you should have:**
- ✅ `node_modules/` folder with dependencies
- ✅ `dist/index.js` compiled JavaScript server
- ✅ Server starts successfully with `node dist/index.js`
- ✅ No error messages during build

---

## 🚨 TROUBLESHOOTING

### **Problem: `npm install` fails**

**Solution:**
```bash
# Try with --legacy-peer-deps
npm install --legacy-peer-deps

# Or clean cache first
npm cache clean --force
npm install
```

---

### **Problem: TypeScript compilation errors**

**Solution:**
```bash
# Check TypeScript version
npx tsc --version

# Should be 5.6.2 or newer
# If old, update:
npm install typescript@latest --save-dev
npm run build
```

---

### **Problem: `chmod +x` fails on Windows**

**Expected:** This is normal on Windows! The build script includes chmod for Unix systems, but it's not required on Windows. The server will work fine.

**Ignore this warning:**
```
'chmod' is not recognized as an internal or external command
```

---

### **Problem: Server starts but shows error**

**Check Node.js version:**
```bash
node --version
```

**Should be:** v22.11.0 (or v18+)

**If older:** Update Node.js from nodejs.org

---

## ✅ SUCCESS CRITERIA

**Component 1 is COMPLETE when:**
1. ✅ `npm install` completed without errors
2. ✅ `npm run build` completed successfully
3. ✅ `dist/index.js` file exists
4. ✅ `node dist/index.js` starts server successfully
5. ✅ Server outputs: "Knowledge Graph MCP Server running on stdio"

---

## 🎯 NEXT STEP

**After successful build:**
- ✅ Component 1 complete!
- ⏭️ Ready for **Component 2: AgentMemory Class** (Python interface)

---

## 📊 TIME TRACKING

**Estimated Time:** 30 minutes  
**Actual Time:** _____ minutes (you fill this in)  
**Difficulty:** Easy ⭐⭐☆☆☆  
**Status:** ⏳ Ready to build

---

**When you complete this component, report back with:**
1. ✅ Build successful?
2. ✅ Server starts successfully?
3. ✅ Any errors encountered?
4. ⏭️ Ready for Component 2?

---

**END OF BUILD INSTRUCTIONS**
