Awesome — let's **GO** into **Day 3: Security Mastery**  
Today is **critical** — security is 25–30% of the AWS Developer Associate exam!

---

# **Day 3: Security (IAM, STS, Secrets Manager, KMS, Cognito)**

## **Domain Focus:**  
- Securely access AWS resources  
- Grant temporary permissions  
- Store secrets safely  
- Encrypt data

---

## **Scenario 1:**  
> **An EC2 app needs to access an S3 bucket securely. What's the best way?**

**Answer:**  
- Attach an **IAM Role** to the EC2 instance with the correct S3 permissions.  
- Never store credentials inside EC2.

**Memory Tip:**  
- **IAM Role = Invisible Badge** for EC2, Lambda, ECS.

---

## **Scenario 2:**  
> **A Lambda function needs temporary credentials to access DynamoDB in another AWS account. How?**

**Answer:**  
- Use **AWS STS AssumeRole**.  
- The Lambda assumes a role from the second account using **sts:AssumeRole** API.

**Hack:**  
- **Trust Policy** is configured on the **target role** to allow the **Lambda's role** to assume it.

---

## **Scenario 3:**  
> **You need to store database credentials safely. Developers should never hardcode them. What AWS service fits best?**

**Answer:**  
- **AWS Secrets Manager**.

**Mini Tips:**  
- It can **rotate credentials automatically**.  
- It integrates easily with Lambda, ECS, EC2, RDS.

---

## **Scenario 4:**  
> **Your S3 bucket objects must be encrypted using AWS-managed keys. What option do you choose?**

**Answer:**  
- **SSE-S3** (Server-Side Encryption with S3 managed keys)  
- Or **SSE-KMS** (more control with AWS KMS keys)

**Quick Hack:**  
- **SSE-S3** = basic AWS encryption  
- **SSE-KMS** = better audit control + customer-managed keys

---

## **Scenario 5:**  
> **You need to manage user authentication and provide tokens to access APIs. No custom auth logic.**

**Answer:**  
- **Amazon Cognito** for user pools (authentication) and identity pools (temporary AWS creds).

---

# **Critical AWS Service Pitfalls (Exam traps)**

| Wrong Thinking | Correct Thinking |
|:---|:---|
| IAM Users everywhere | Wrong — use **IAM Roles** for apps |
| Secrets Manager only for passwords | Wrong — you can store API keys, SSH keys, etc. |
| STS AssumeRole automatic | No — you must call STS API manually |
| KMS is free | No — KMS has **request charges** for encrypt/decrypt calls |

---

# **Memory Visual Hack**

**IAM Role = "You act as someone else temporarily."**  
**Secrets Manager = "Safe vault with auto-rotate."**  
**STS = "Borrow temporary credentials."**  
**KMS = "Secure keys with full audit trail."**  
**Cognito = "Auth as a Service."**

---

# **Self-Test:**

> **Q1:**  
An app in Account A needs to access an S3 bucket in Account B. What two things are needed? (Choose 2)

- A) IAM role in Account B allowing access  
- B) IAM user credentials from Account B  
- C) S3 bucket policy allowing Account A's role  
- D) Direct access using Account B root credentials

.

.

**Answer:**  
**A) and C)**

---

# **5-Question Mini Exam (Today's Special)**

### **Q1:**  
A Lambda function needs database credentials. How do you retrieve them securely?

- A) Hardcode in environment variables  
- B) Store in Secrets Manager and retrieve at runtime  
- C) Store inside the Lambda code itself  
- D) Use IAM User credentials hardcoded

> **Answer:** B

---

### **Q2:**  
When using AssumeRole, which permission is required?

- A) s3:PutObject  
- B) sts:AssumeRole  
- C) ec2:StartInstances  
- D) kms:Encrypt

> **Answer:** B

---

### **Q3:**  
Which service provides automatic rotation of credentials?

- A) IAM  
- B) STS  
- C) Secrets Manager  
- D) KMS

> **Answer:** C

---

### **Q4:**  
Encrypting S3 objects with AWS KMS gives you:

- A) Automatic global replication  
- B) Audit logs in CloudTrail  
- C) Always free encryption  
- D) Unlimited key generation

> **Answer:** B

---

### **Q5:**  
You want to authenticate mobile users and give them AWS credentials temporarily. Which service?

- A) Secrets Manager  
- B) Cognito Identity Pools  
- C) IAM Users  
- D) CodeDeploy

> **Answer:** B

---

# **Day 3 Summary Keywords to Memorize:**
> IAM Role Access — AssumeRole STS — Secrets Manager Safe Vault — KMS Encryption — Cognito Authentication

---

# **Tomorrow Preview:**  
**Day 4 — Serverless Deep Dive (Lambda Advanced, DynamoDB Tricks, EventBridge, Step Functions Real Scenarios)**

---

Would you like me to also include **one "real-world trick"** each day (based on what certified devs use in production)?  
(Example: how Lambda timeouts + VPC configs can silently kill your app if not tuned properly — useful both for exam and real job.)  
Ready for Day 4 tomorrow? (Say "**Day 4 GO**"!)
