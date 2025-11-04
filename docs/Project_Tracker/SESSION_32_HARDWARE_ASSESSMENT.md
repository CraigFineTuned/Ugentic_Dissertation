# SESSION 32 - HARDWARE & INFRASTRUCTURE ASSESSMENT

**Purpose:** Hardware requirements analysis for local vs cloud LLM deployment
**Location:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\SESSION_32_HARDWARE_ASSESSMENT.md`
**Date:** October 27, 2025
**Status:** ✅ COMPLETE

---

## USER'S CURRENT HARDWARE

### System Specifications

**From Windows System Information:**

```
Computer Name: C9000
Operating System: Windows 11 Home 64-bit (Build 26100)
Processor: AMD Ryzen 7 5700U with Radeon Graphics (16 CPUs), ~1.8GHz
Memory: 16384MB RAM (15756MB available)
GPU: AMD Radeon(TM) Graphics (Integrated)
GPU VRAM: 536870912 bytes (512MB)
GPU Driver: 31.0.21923.11000 (dated 2025-07-01)
```

**Key Constraints:**
- ❌ **512MB VRAM** (insufficient for LLM inference)
- ⚠️ AMD Radeon integrated graphics (not NVIDIA CUDA)
- ✅ 16GB System RAM (adequate)
- ✅ Ryzen 7 5700U CPU (adequate for CPU inference, but slow)
- ✅ Windows 11 (compatible with Ollama)

---

## LLM INFERENCE REQUIREMENTS

### Model Size Analysis

**Fine-tuned Models:**

| Model | Quantization | File Size | Minimum VRAM | Recommended VRAM |
|-------|-------------|-----------|--------------|-------------------|
| Qwen 2.5 3B | Q4_K_M | 1.93 GB | 3 GB | 4-6 GB |
| Qwen 2.5 1.5B | Q4_K_M | 1.2 GB | 2 GB | 3-4 GB |
| Qwen 2.5 3B | F16 | ~6 GB | 8 GB | 12 GB |
| Qwen 2.5 7B | Q4_K_M | 4.2 GB | 6 GB | 8 GB |

**Baseline Model:**

| Model | Type | Infrastructure | Performance |
|-------|------|----------------|-------------|
| deepseek-v3.1:671b-cloud | Cloud API | Remote inference | 9.62s avg |

---

### VRAM Requirements Breakdown

**For Q4_K_M Quantized Models:**

```
Model weights:        1.93 GB (for 3B model)
Context buffer:       0.5 GB (for 2048 token context)
Computation overhead: 0.5 GB
==================================
Total minimum:        ~3 GB VRAM
Recommended:          4-6 GB VRAM
```

**User's Hardware:**
```
Available VRAM:       512 MB
Deficit:              2.5 GB (5x too small)
```

**Result:** Model cannot fit in GPU memory, falls back to CPU.

---

### CPU vs GPU Inference

**GPU Inference (with adequate VRAM):**
- Token generation: 50-100 tokens/second
- Response time (100 tokens): 1-2 seconds
- Concurrent requests: 2-4 (depending on VRAM)

**CPU Inference (fallback on user's system):**
- Token generation: 5-10 tokens/second
- Response time (100 tokens): 10-20 seconds
- Concurrent requests: 1
- Memory swapping causes additional slowdowns

**Observed Performance:**
- Fine-tuned 3B on user's CPU: **113.21s average**
- Baseline cloud model: **9.62s average**
- **Slowdown factor: 11.8x**

---

## HARDWARE UPGRADE OPTIONS

### Option 1: Dedicated GPU (Local Deployment)

**Minimum Spec GPU:**
- **NVIDIA GTX 1660 Ti**
  - VRAM: 6 GB
  - Cost: ~$250-300 (used)
  - Power: 120W (may require PSU upgrade)
  - Performance: 40-60 tokens/sec
  - Can run: 3B models comfortably, 7B models acceptably

**Recommended GPU:**
- **NVIDIA RTX 3060**
  - VRAM: 12 GB
  - Cost: ~$300-400
  - Power: 170W (may require PSU upgrade)
  - Performance: 60-80 tokens/sec
  - Can run: Up to 13B models

**Enthusiast GPU:**
- **NVIDIA RTX 4060 Ti (16GB)**
  - VRAM: 16 GB
  - Cost: ~$500-600
  - Power: 165W
  - Performance: 80-100 tokens/sec
  - Can run: Up to 20B models

**Installation Considerations:**
- ✅ User has Ryzen 7 5700U (laptop processor)
- ❌ **Likely a laptop or compact system** (cannot upgrade GPU)
- ⚠️ May require desktop/tower system purchase
- ⚠️ PSU requirements (350-550W needed)
- ⚠️ Physical space in case

**Total Cost for Desktop Upgrade:**
- GPU: $300-600
- Desktop tower (if laptop): $400-800
- PSU upgrade (if needed): $50-100
- **Total: $750-1,500**

**Timeline:**
- Purchase + shipping: 1-2 weeks
- Installation: 1-2 hours
- Setup + testing: 1-2 days
- **Total: 2-3 weeks**

---

### Option 2: Cloud GPU Rental

**Rent GPU instances for inference:**

**RunPod:**
- RTX 3090 (24GB): $0.34/hour
- RTX 4090 (24GB): $0.69/hour
- A40 (48GB): $0.79/hour
- Community pods: $0.20-0.30/hour

**Vast.ai:**
- RTX 3090: $0.25-0.40/hour
- Various GPUs: $0.15-0.50/hour
- Auction-based pricing

**Lambda Labs:**
- A10 (24GB): $0.75/hour
- V100 (16GB): $1.10/hour

**Phase 3 Cost Estimate:**
- 10-14 interviews
- 1 hour per interview
- Average: $0.40/hour
- **Total: $4-6** for entire Phase 3

**Pros:**
- ✅ Very low cost
- ✅ Immediate availability
- ✅ No hardware investment
- ✅ Can test if fine-tuning actually works

**Cons:**
- ⚠️ Requires deployment setup (1-2 days)
- ⚠️ Internet dependency
- ⚠️ Data privacy considerations
- ⚠️ Ongoing costs (minimal for dissertation)

---

### Option 3: Cloud API Services

**Deploy fine-tuned model to managed services:**

**Hugging Face Inference API:**
- Custom model hosting
- Pricing: ~$0.001-0.01 per request
- Setup: Upload model, configure endpoint
- Time: 2-3 hours

**AWS SageMaker:**
- ml.g4dn.xlarge: $0.736/hour
- Setup complexity: High
- Time: 1-2 days

**Azure ML:**
- NCv3 instances: $0.90-1.80/hour
- Setup complexity: Medium
- Time: 1 day

**Phase 3 Cost (HuggingFace):**
- 4 investigations per interview × 12 interviews = 48 investigations
- At $0.005 per investigation = **$0.24 total**

**Phase 3 Cost (AWS/Azure):**
- 12 hours of interviews
- At $0.75/hour = **$9 total**

---

### Option 4: Continue with Cloud Baseline

**Use deepseek-v3.1:671b-cloud (current baseline):**

**Pros:**
- ✅ Already working (100% success rate)
- ✅ Zero additional cost
- ✅ Zero setup time
- ✅ Proven performance (9.62s average)
- ✅ No hardware investment
- ✅ Dissertation-ready NOW
- ✅ Zero risk for Phase 3

**Cons:**
- ⚠️ Cannot test fine-tuned models
- ⚠️ Dependent on cloud service
- ⚠️ No custom model evaluation
- ⚠️ Missed learning opportunity

**Cost:** $0 (using existing Ollama cloud service)

**Timeline:** Immediate (already configured)

---

## PERFORMANCE COMPARISON

### Response Time Analysis

| Deployment Method | Hardware | Response Time | Success Rate | Cost (Phase 3) |
|------------------|----------|---------------|--------------|----------------|
| **User's Laptop (CPU)** | 512MB VRAM | 113.21s | 0% | $0 |
| **Dedicated GPU** | 12GB VRAM | ~5-8s* | ~95%* | $300-600 |
| **Cloud GPU Rental** | 24GB VRAM | ~5-8s* | ~95%* | $4-6 |
| **Cloud API** | Managed | ~8-12s* | ~90%* | $0.24-9 |
| **Baseline (deepseek)** | Cloud | 9.62s | 100% | $0 |

*Estimated if training data fixed

---

## AMD vs NVIDIA FOR LLM INFERENCE

### Why AMD Radeon Doesn't Work Well

**Technical Issues:**

1. **CUDA vs ROCm:**
   - Ollama optimized for NVIDIA CUDA
   - AMD ROCm support limited
   - Many LLM frameworks CUDA-only

2. **Driver Maturity:**
   - NVIDIA drivers well-tested for LLM inference
   - AMD drivers less optimized for ML workloads

3. **Integrated vs Dedicated:**
   - User has integrated AMD graphics (512MB shared VRAM)
   - Not designed for compute workloads
   - Shared memory with system RAM

4. **Library Support:**
   - PyTorch: Better NVIDIA support
   - llama.cpp: NVIDIA preferred
   - GGML: NVIDIA optimized

**Verdict:** AMD Radeon integrated graphics unsuitable for LLM inference regardless of VRAM size.

---

## RECOMMENDATIONS

### For Phase 3 Expert Validation (IMMEDIATE)

**Recommendation:** ✅ **Continue with deepseek-v3.1:671b-cloud**

**Rationale:**
1. ✅ Proven 100% success rate
2. ✅ Excellent 9.62s response time
3. ✅ Zero additional cost
4. ✅ Zero setup time
5. ✅ Dissertation deadline safety (December 5)
6. ✅ No hardware investment needed

**Risk:** None. This configuration is validated and working.

**Action:** Continue Phase 3 with baseline. Fine-tuning is exploratory, not required.

---

### For Testing Fine-tuned Models (POST-DISSERTATION)

**Recommendation:** ⚠️ **Cloud GPU Rental (RunPod/Vast.ai)**

**Rationale:**
1. ✅ Low cost ($4-6 for Phase 3 testing)
2. ✅ Immediate availability
3. ✅ Tests if training data fixes work
4. ✅ No hardware investment
5. ✅ Can abandon if not working

**Risk:** Medium. Still requires training data fixes first.

**Action:** 
1. Fix training data (130+ proper examples)
2. Retrain model on Colab
3. Deploy to RunPod/Vast.ai
4. Test against baseline
5. Evaluate if worth continuing

**Timeline:** 3-4 weeks (1-2 weeks training data, 1 week train/deploy, 1 week test)

---

### For Future Optimization (POST-DISSERTATION)

**Recommendation:** ⚠️ **Dedicated GPU or Cloud API**

**Decision Factors:**

**Choose Dedicated GPU if:**
- ✅ Need frequent local inference (daily use)
- ✅ Privacy/security requirements
- ✅ Have desktop system (not laptop)
- ✅ Budget for hardware ($300-600)
- ✅ Willing to maintain hardware

**Choose Cloud API if:**
- ✅ Occasional inference (weekly/monthly)
- ✅ No hardware investment desired
- ✅ Professional deployment (HuggingFace, AWS)
- ✅ Need scalability
- ✅ Minimal maintenance preferred

**Current Recommendation:** Given user has laptop (Ryzen 7 5700U), **Cloud API** is better choice than hardware upgrade.

---

## INFRASTRUCTURE DECISION MATRIX

| Factor | Laptop CPU | Dedicated GPU | Cloud GPU | Cloud API | Baseline |
|--------|-----------|---------------|-----------|-----------|----------|
| **Cost (Phase 3)** | $0 | $300-600 | $4-6 | $0.24-9 | $0 |
| **Setup Time** | 0 | 2-3 weeks | 1-2 days | 1 day | 0 |
| **Performance** | 113s ❌ | ~5-8s* ✅ | ~5-8s* ✅ | ~8-12s* ✅ | 9.62s ✅ |
| **Success Rate** | 0% ❌ | ~95%* ⚠️ | ~95%* ⚠️ | ~90%* ⚠️ | 100% ✅ |
| **Risk** | Total failure | Hardware investment | Low | Medium | None |
| **Maintenance** | None | Moderate | Low | Low | None |
| **Scalability** | None | Limited | High | High | High |
| **Phase 3 Ready** | ❌ No | ❌ No | ⚠️ Maybe | ⚠️ Maybe | ✅ Yes |
| **Deadline Safe** | ❌ No | ❌ No | ⚠️ Maybe | ⚠️ Maybe | ✅ Yes |

*Assumes training data fixed

**Winner for Phase 3:** **Baseline (deepseek-v3.1:671b-cloud)**

**Winner for Post-Dissertation Exploration:** **Cloud GPU Rental** (if training data fixed)

---

## COST-BENEFIT ANALYSIS

### Phase 3 Validation (12 interviews, 48 investigations)

| Option | Upfront Cost | Hourly Cost | Phase 3 Total | Setup Time |
|--------|--------------|-------------|---------------|------------|
| User's Laptop | $0 | $0 | $0 | 0 | 
| Dedicated GPU | $300-600 | $0 | $300-600 | 2-3 weeks |
| Cloud GPU | $0 | $0.40/hr | $4-6 | 1-2 days |
| Cloud API | $0 | $0.02/request | $1-9 | 1 day |
| **Baseline** | **$0** | **$0** | **$0** | **0** |

**Clear Winner:** Baseline has zero cost and zero setup time.

---

### One Year Production Use (100 investigations/month)

| Option | Year 1 Cost | Ongoing Cost/Year | Maintenance |
|--------|-------------|-------------------|-------------|
| Dedicated GPU | $300-600 | Electricity (~$20) | Moderate |
| Cloud GPU | $0 | $480 ($0.40/hr × 100hrs) | Low |
| Cloud API | $0 | $24-1,200 (depends on pricing) | Low |
| Baseline | $0 | $0 (if free tier) | None |

**For Production:** Dedicated GPU becomes cost-effective after 8-15 months of continuous use.

---

## TECHNICAL SPECIFICATIONS SUMMARY

### Minimum Requirements for Local Deployment

**For 3B Quantized Models:**
- GPU: NVIDIA GTX 1660 Ti or better
- VRAM: 6GB minimum, 8GB recommended
- System RAM: 16GB
- Storage: 50GB SSD
- OS: Windows 11 / Linux
- Power Supply: 350W+ (for GPU)

**For 7B Quantized Models:**
- GPU: NVIDIA RTX 3060 or better
- VRAM: 12GB minimum, 16GB recommended
- System RAM: 32GB
- Storage: 100GB SSD
- OS: Windows 11 / Linux
- Power Supply: 550W+ (for GPU)

**User's Hardware Gap:**
- ❌ Need: 6-12GB VRAM → Have: 512MB (12-24x too small)
- ❌ Need: NVIDIA GPU → Have: AMD integrated
- ✅ Have: 16GB RAM → Sufficient
- ❌ Need: Desktop → Have: Laptop (likely)

---

## CONCLUSION

**Hardware Assessment:** User's current hardware (512MB AMD integrated GPU) is **insufficient for local LLM inference** of any meaningful size. Minimum hardware upgrade would cost $300-600 for GPU alone, likely requiring full desktop system ($750-1,500 total).

**Practical Alternatives:**
1. **Cloud GPU rental** ($4-6 for Phase 3) - viable for testing
2. **Cloud API** ($0.24-9 for Phase 3) - viable for testing
3. **Baseline cloud model** ($0 for Phase 3) - **optimal choice**

**Recommendation:** Use baseline deepseek-v3.1:671b-cloud for Phase 3. Hardware constraints are real but not dissertation-critical. Fine-tuning exploration is valuable learning but not required for research validation.

**Key Insight:** Even if training data were perfect, user's hardware would still prevent local deployment. Hardware is independent constraint from training data quality.

---

**Document:** SESSION_32_HARDWARE_ASSESSMENT.md  
**Location:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\`  
**Status:** ✅ COMPLETE  
**Last Updated:** October 27, 2025 - 12:30  
**Next:** Update SESSION_ENTRY.md with Session 32 summary
