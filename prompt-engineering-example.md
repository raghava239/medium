# 🛠️ The Prompt Engineering Blueprint: 10 Production-Ready Templates

**Author:** Raghu Pothula  
**Purpose:** To help cross-functional teams (from business ops to DevOps) move away from treating LLMs like search engines, and start treating them like junior engineers that need clear, structured instructions.

Hey team, 

Over the last few months, I've noticed we spend a lot of time wrestling with AI to get the outputs we actually need. The issue usually isn't the model; it's the prompt. When we are working in real-time, whether we are drafting an email to a stakeholder or debugging a broken Kubernetes cluster, we need precision. 

Below is a curated repository of 10 "Strong" prompts that can be used in daily workflow. I’ve broken this down into **General Business** and **Cloud & DevOps**. 

Feel free to copy, paste, and adapt these to your specific context. 

---

## 🏢 Part 1: General Business & Operations 
*These prompts are designed for non-technical workflows: communication, strategy, and content creation. Notice how we establish the Persona, Tone, and Format upfront.*

### 1. The "Difficult Communication" Helper
**Use Case:** When you need to push back on a vendor or stakeholder without burning bridges.
> **Prompt:** > "Act as an experienced corporate communications coach. I need to write an email to a third-party vendor because they missed a critical delivery deadline, which is now delaying our internal launch. 
> **Task:** Write a concise email addressing the missed deadline and asking for an updated timeline. 
> **Tone:** Firm, professional, but empathetic (assume they might be facing internal blockers). 
> **Format:** Provide two options—one slightly softer, and one more direct. No corporate buzzwords."

### 2. Strategic Brainstorming (SWOT Analysis)
**Use Case:** Quickly mapping out the risks and benefits of a new business decision.
> **Prompt:** > "Act as a Senior Business Strategist. Our company is considering shifting our primary software product from a one-time perpetual license model to a monthly SaaS subscription.
> **Task:** Conduct a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for this specific transition. 
> **Format:** Present the output as a Markdown table.
> **Constraint:** Focus specifically on customer retention and initial revenue dips in the 'Weaknesses' and 'Threats' sections."

### 3. Summarizing Messy Meeting Notes
**Use Case:** Turning a chaotic brain-dump of notes into an actionable project update.
> **Prompt:** > "Act as a highly organized Technical Project Manager. 
> **Context:** I am pasting a raw, disorganized transcript of my notes from our Q3 planning meeting below.
> **Task:** Clean up these notes and organize them.
> **Format:** Use three clear headers: 'Key Decisions Made', 'Open Questions/Blockers', and 'Action Items (with assigned owners)'. 
> **Tone:** Objective and easily scannable for an executive summary."
> *[Paste raw notes here]*

---

## ☁️ Part 2: Cloud Engineering & DevOps
*This is where we get highly technical. Notice the use of "Chain of Thought" (asking the AI to explain its reasoning) and strict formatting constraints (like specifying JSON or YAML).*

### 4. Infrastructure as Code (Terraform) Generation
**Use Case:** Bootstrapping boilerplate IaC safely.
> **Prompt:** > "Act as a Senior Cloud Architect. 
> **Context:** I am building a foundational network layer in AWS using Terraform. 
> **Task:** Generate the Terraform code (`main.tf`) to create a VPC with a CIDR block of `10.0.0.0/16`. It must include 2 public subnets, 2 private subnets across two Availability Zones, an Internet Gateway, and a NAT Gateway. 
> **Constraint:** Do not use hardcoded values; utilize variables (`variables.tf`) for the CIDR blocks and region. 
> **Format:** Provide the raw `.tf` code blocks with inline comments explaining the routing table logic."

### 5. Kubernetes Debugging (Chain of Thought)
**Use Case:** Real-time troubleshooting during an incident.
> **Prompt:** > "Act as a Site Reliability Engineer (SRE). 
> **Context:** I have a Kubernetes pod for a Node.js microservice that is stuck in a `CrashLoopBackOff` state. 
> **Task:** Explain your reasoning step-by-step for how to troubleshoot this specific state. After explaining your logic, provide the exact `kubectl` CLI commands I should run to diagnose the issue (e.g., checking logs, describing the pod, checking previous container states). 
> **Format:** Numbered list for the workflow, followed by bash code blocks for the commands."

### 6. Writing Strict AWS IAM Policies
**Use Case:** Generating security policies while enforcing the Principle of Least Privilege.
> **Prompt:** > "Act as a Cloud Security Specialist. 
> **Task:** Write an AWS IAM policy in valid JSON format. 
> **Context:** This policy will be attached to a Lambda function. It needs permission to read objects from a specific S3 bucket named `app-customer-data-prod` and write execution logs to CloudWatch.
> **Constraint:** Strictly adhere to the Principle of Least Privilege. Do NOT use wildcards (`*`) for S3 actions; specify exactly `s3:GetObject` and `s3:ListBucket`. Explain the Resource ARNs you used underneath the JSON block."

### 7. CI/CD Pipeline Creation (GitHub Actions)
**Use Case:** Setting up automated deployment workflows.
> **Prompt:** > "Act as a DevOps Engineer. 
> **Task:** Create a GitHub Actions workflow YAML file for a React frontend application. 
> **Context:** The pipeline needs to trigger automatically on a push to the `main` branch. The jobs must: check out the code, run `npm install`, run `npm test`, build the static files, and sync the build folder to an AWS S3 bucket.
> **Constraint:** Use OIDC (OpenID Connect) for AWS authentication. Do not use long-lived AWS Access Keys or secrets in the workflow. 
> **Format:** Valid YAML code block."

### 8. Cloud Cost Optimization (FinOps)
**Use Case:** Analyzing billing spikes and getting actionable reduction strategies.
> **Prompt:** > "Act as a Cloud FinOps Analyst. 
> **Context:** Our monthly AWS bill spiked by 30% this month. The cost explorer shows the spike is driven entirely by underutilized `m5.2xlarge` EC2 instances and unattached EBS volumes. 
> **Task:** Suggest 4 highly actionable steps our engineering team can take this week to optimize and reduce these specific costs without impacting production application performance. 
> **Format:** Bullet points, categorized by 'Immediate Quick Wins' and 'Long-term Architecture changes'."

### 9. Blameless Incident Post-Mortem
**Use Case:** Documenting an outage for the team without pointing fingers.
> **Prompt:** > "Act as an Incident Commander. 
> **Task:** Draft a blameless post-mortem document for a recent Sev-1 outage. 
> **Context:** A bad database migration script was run manually in production, which locked the primary PostgreSQL database for 45 minutes, causing a complete API outage. 
> **Format:** Use the standard SRE Post-Mortem template (Headers: Incident Summary, Timeline, Impact, Root Cause, and Action Items). 
> **Tone:** Highly objective, focusing on systemic failures (e.g., lack of automated review) rather than human error."

### 10. Architecture Migration Planning
**Use Case:** High-level system design and refactoring strategy.
> **Prompt:** > "Act as a Principal Systems Engineer. 
> **Context:** We are planning to migrate a legacy monolithic Python/Django application to containerized microservices running on Google Cloud Run. 
> **Task:** Outline a phased migration strategy using the 'Strangler Fig Pattern'. 
> **Constraint:** Focus the first phase entirely on decoupling the shared database before moving the application compute logic. 
> **Format:** A step-by-step technical guide with brief explanations of the risks involved in each phase."

---
*End of Document. Feel free to submit a PR if you have great prompts to add to this library!*
