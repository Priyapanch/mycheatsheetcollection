Perfect — let's continue the momentum!

---

# **Day 2: Deployment (CI/CD Pipelines — CodePipeline, CodeDeploy, CodeBuild)**

## **Domain Focus:**  
- Automate deployments  
- Understand how AWS native CI/CD tools integrate  
- Build, Test, Deploy pipelines securely and reliably

---

## **Scenario 1:**  
> **You are building a serverless app. It must be automatically deployed when developers push code to GitHub. How can you design the pipeline?**

**Answer:**  
- **CodePipeline** as the orchestrator  
- **Source Stage**: GitHub webhook triggers the pipeline  
- **Build Stage**: Use **CodeBuild** to package and prepare artifacts  
- **Deploy Stage**: Use **CodeDeploy** to deploy to Lambda

**Key Tip:**  
- CodePipeline **pulls from source** (GitHub, S3, CodeCommit)  
- Webhooks = *Instant trigger* (real-time)

---

## **Scenario 2:**  
> **You need to ensure your app passes unit tests before being deployed. Where do you configure that?**

**Answer:**  
- In **CodeBuild** phase (buildspec.yml file)  
- You run `pytest`, `npm test`, etc., in the **build commands**.

**buildspec.yml sample:**
```yaml
version: 0.2
phases:
  install:
    commands:
      - pip install -r requirements.txt
  build:
    commands:
      - pytest tests/
artifacts:
  files:
    - app.zip
```

**Memory Hack:**  
- **buildspec.yml = brain of CodeBuild**

---

## **Scenario 3:**  
> **Your EC2 app deployment needs automatic rollback if health checks fail. What AWS tool is best?**

**Answer:**  
- **CodeDeploy** with EC2/On-Premises deployment  
- Use **AppSpec.yml** file to define hooks (`BeforeInstall`, `AfterInstall`, `ApplicationStart`, `ValidateService`)

**Mini Tip:**  
- If health check fails, CodeDeploy will **auto rollback** to previous version if configured.

---

# **Critical AWS Service Pitfalls (Exam traps)**

| Wrong Thinking | Correct Thinking |
|:---|:---|
| CodeDeploy only for EC2 | Wrong — it also deploys to Lambda, ECS now |
| CodeBuild only builds code | It can **test**, **lint**, **package**, **run scripts** too |
| CodePipeline handles everything automatically | No — you must configure stages explicitly (Source, Build, Deploy) |

---

# **Memory Visual Hack**

**CodePipeline = Traffic Cop**  
(Controls the order — Source -> Build -> Test -> Deploy)

**CodeBuild = Construction Worker**  
(Builds, tests, packages code.)

**CodeDeploy = Delivery Truck**  
(Deploys app carefully to EC2, Lambda, ECS.)

---

# **Self-Test:**

> **Q:** You want to deploy new versions of a Lambda function using CodePipeline. Which components must you use? (Choose 2)

- A) Source stage (GitHub repo)
- B) Build stage (CodeBuild creates .zip)
- C) Elastic Beanstalk environment
- D) AppSpec.yml file for EC2
- E) CodeDeploy deployment group for Lambda

**(Answer below — try first!)**

.

.

.

**Answer: A) and E)**

- A) GitHub repo triggers the pipeline (Source stage)
- E) CodeDeploy deployment group for Lambda (special deployment type for functions)

---

# **Day 2 Summary Keywords to Memorize:**
> CodePipeline Orchestration — CodeBuild Build/Test — CodeDeploy Hooks/Rollback

---

# **Tomorrow Preview:**  
**Day 3 — Hardcore Security Day (IAM Policies, STS AssumeRole, KMS encryption, Secret Manager tricks)**

---

Would you like me to also include **a 5-question mini-exam** for each day starting Day 3?  
(Realistic "choose 2", "choose 3" AWS-style — super useful to build exam stamina.)  
Ready for Day 3 tomorrow? (Say "GO" if yes!)
