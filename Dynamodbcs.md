Here’s a **1-page DynamoDB Exam Cheat Sheet (Mind Map)** tailored for the **AWS Developer Associate exam** (DVA-C02). This will help you quickly recall key DynamoDB concepts.

---

## 🧠 **DynamoDB Exam Mind Map**

---

### 🗄️ **1. Data Model**

* **Table**: Collection of items.
* **Item**: Individual record.
* **Attribute**: Key-Value pairs in items.

🔑 **Keys:**

* **Partition Key** (HASH): Distributes data across partitions.
* **Sort Key** (RANGE): Orders data within partition.

---

### ⚡ **2. Read Consistency**

| Type                      | Purpose                        | Example Use                       |
| ------------------------- | ------------------------------ | --------------------------------- |
| **Eventually Consistent** | Default, may return stale data | Dashboards, Reporting             |
| **Strongly Consistent**   | Always latest data             | Balance lookup, immediate updates |

---

### 🗂️ **3. Indexes**

| Index Type                       | Purpose                                | Notes                             |
| -------------------------------- | -------------------------------------- | --------------------------------- |
| **Local Secondary Index (LSI)**  | Same Partition Key, different Sort Key | Must be created at table creation |
| **Global Secondary Index (GSI)** | Different Partition & Sort Keys        | Can be added later                |

---

### 📈 **4. Capacity Modes**

| Mode            | Best for                | Auto Scaling              |
| --------------- | ----------------------- | ------------------------- |
| **Provisioned** | Predictable traffic     | With Auto Scaling         |
| **On-Demand**   | Unpredictable workloads | Auto-scales automatically |

---

### 🚀 **5. Performance & Scaling**

* **Hot Partitions** → Solution: Add **randomized suffix** to partition key.
* **Read-heavy apps** → Use **DAX (in-memory cache)**.
* **Throughput scaling** → Use **Auto Scaling** or **On-Demand Mode**.
* **Batch Operations** → `BatchGetItem`, `BatchWriteItem` for efficiency.

---

### 🔄 **6. DynamoDB Streams**

* Capture **item-level changes** (insert, modify, delete).
* Can **trigger Lambda** for event-driven processing.
* **Stream View Types**: KEYS\_ONLY, NEW\_IMAGE, OLD\_IMAGE, NEW\_AND\_OLD\_IMAGES.

---

### 🛡️ **7. Security & Backup**

* **Encryption at Rest** → Enabled by default (KMS).
* **Point-in-Time Recovery (PITR)** → Restore table to any point in past 35 days.
* **IAM Roles/Policies** → Fine-grained access control.
* **VPC Endpoints** → Private access within VPC.

---

### 🧩 **8. Common Exam Traps**

* "Most Recent Data" → **Strongly Consistent Read**.
* "Unpredictable Traffic" → **On-Demand Mode**.
* "Event-driven Processing" → **DynamoDB Streams + Lambda**.
* "Scaling Issue / Throttling" → Check **partition key design & Auto Scaling**.
* "Complex queries needed" → Use **GSIs**.

---

### 🖼️ **Visual Example: DynamoDB Architecture**

```
[Client] --> [API Gateway] --> [Lambda] --> [DynamoDB Table]
                                          |
                                      [DynamoDB Streams]
                                          |
                                       [Lambda Consumer]
```

---

### ✅ **Quick Exam Memory Hook:**

> **"POSS": Partition, On-demand, Streams, Strong Consistency**

---

### 🔽 Downloadable PDF:

I can generate this as a **high-quality mind map PDF** for your exam notes.
Reply `Yes send PDF DynamoDB Cheat Sheet` if you'd like it! 🚀
