Love the energy!  
Here we go — **Day 5 GO + Cheat Sheets** as you requested.

---

# **Day 5: DynamoDB Deep Dive (🔥 Mission Critical for Exam)**

## **Domain Focus:**  
- NoSQL data modeling basics  
- Choosing the right keys  
- Handling scale (On-Demand vs Provisioned)  
- DynamoDB Streams  
- Global Tables

---

# **Scenario 1:**  
> **You need to store millions of user profiles. Fast lookup by UserID. What is the best DynamoDB design?**

**Answer:**  
- **Partition key = UserID**  
- **Simple primary key design**

**Quick Hack:**  
- Lookup pattern = **Partition key only** = FASTEST.

---

# **Scenario 2:**  
> **You need to support queries by `email` and by `userID`. How to design?**

**Answer:**  
- Primary Table: Partition Key = userID  
- Create a **Global Secondary Index (GSI)**: Partition Key = email

**Memory Tip:**  
- **GSI = New access pattern**

---

# **Scenario 3:**  
> **An app expects unpredictable traffic spikes. You want DynamoDB to handle scaling without manual intervention.**

**Answer:**  
- **DynamoDB On-Demand mode.**

**Mini Tip:**  
- No need to specify read/write capacity. Auto-scales instantly.

---

# **Scenario 4:**  
> **You want to capture changes (insert/update/delete) to DynamoDB items for audit or replication. What feature?**

**Answer:**  
- **DynamoDB Streams**.

**Pro Tip:**  
- Streams = Firehose of changes (can trigger Lambda).

---

# **Scenario 5:**  
> **You need a multi-region, active-active database setup for disaster recovery. Which DynamoDB feature?**

**Answer:**  
- **Global Tables.**

**Bonus:**  
- Built-in conflict resolution (last-writer-wins).

---

# **Critical AWS Service Pitfalls (Exam traps)**

| Wrong Thinking | Correct Thinking |
|:---|:---|
| DynamoDB is like RDS | No — DynamoDB is **NoSQL** — no joins, no complex queries |
| Partition key design doesn't matter | Huge mistake — partition key is critical for performance |
| Streams = backup | Wrong — Streams capture changes, not backups |
| Global Tables need manual sync | No — DynamoDB handles sync automatically |

---

# **Memory Visual Hack**

**Primary Key = Direct Door**  
(Think locker key.)

**GSI = Extra Door**  
(Another way to access.)

**On-Demand = Elastic Mode**  
(No config.)

**Streams = Change Log**

**Global Tables = One DB, Many Regions**

---

# **Cheat Sheet #1: DynamoDB Capacity Mode**

| Mode | When to Use | Key Tip |
|:---|:---|:---|
| **Provisioned** | Predictable traffic | Set Read/Write capacity manually |
| **On-Demand** | Unpredictable, bursty traffic | Pay-per-request, auto-scale |

---

# **Cheat Sheet #2: Key Concepts**

| Term | Meaning |
|:---|:---|
| **Partition key** | Uniquely identifies item (single attribute) |
| **Sort key** | Orders items with same partition key |
| **GSI** | New partition/sort key combo for alternate queries |
| **LSI** | Same partition key, different sort key |
| **Streams** | Capture changes in real-time |

---

# **Self-Test:**

> **Q1:**  
Which DynamoDB feature would you use to support multi-region, fully active-active writes?

- A) Streams  
- B) GSI  
- C) Global Tables  
- D) Backup and Restore

**Answer:** C) Global Tables

---

# **5-Question Mini Exam**

### **Q1:**  
You need to query a DynamoDB table by a non-primary key attribute. What should you create?

- A) LSI  
- B) GSI  
- C) Partition key  
- D) Stream

> **Answer:** B

---

### **Q2:**  
Your app sometimes has 10x spikes in traffic. What DynamoDB capacity mode?

- A) Provisioned  
- B) On-Demand  
- C) Reserved  
- D) Pay-As-You-Go

> **Answer:** B

---

### **Q3:**  
What captures item-level changes in DynamoDB?

- A) CloudTrail  
- B) Streams  
- C) Backups  
- D) Global Tables

> **Answer:** B

---

### **Q4:**  
Which key design gives the FASTEST access to an item?

- A) Primary key lookup  
- B) GSI lookup  
- C) LSI lookup  
- D) Full table scan

> **Answer:** A

---

### **Q5:**  
You need to support two different query patterns on a table. What should you use?

- A) Only partition key  
- B) GSI  
- C) LSI  
- D) Streams

> **Answer:** B

---

# **Day 5 Summary Keywords to Memorize:**
> Partition Key = Fast Access — GSI = Alternate Access — Streams = Change Capture — Global Tables = Multiregion Writes

---

# **Tomorrow Preview:**  
**Day 6 — CI/CD for Developers (CodePipeline, CodeBuild, CodeDeploy, Exam Setup Scenarios)**  
(Also covers GitHub Actions integration!!)

---

**Would you also want a bonus "Exam Traps Special" tomorrow —**  
(Top 7 questions AWS *intentionally makes tricky* in exam, especially for CodePipeline/CodeDeploy?)  
If yes, reply "**Day 6 GO + Exam Traps**" and I’ll load it up with tomorrow’s study drop!
