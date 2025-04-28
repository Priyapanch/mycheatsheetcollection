Got it — you have an ETL pipeline like this:

- **Extract**: Various sources → **AWS Glue Jobs**
- **Transform/Process**: Business rules → **AWS Lambda** + **AWS Step Functions**
- **Load**: Store final data → **PostgreSQL (AWS RDS)**

**Problem**:  
**Issue tracing/debugging is slow** — it's hard to find where/why it failed.

---

You’re asking:  
**What Monitoring, Logging, and Alerting can speed this up?**

Here’s a **solid plan** you can apply step-by-step:

---

### 1. **Centralized Logging**
Instead of checking logs separately (Glue logs, Lambda logs, Step Function logs), centralize them.

- **Enable Glue Job Logging** → Push logs to **Amazon CloudWatch Logs**.
- **Lambda Logs** → Already go to **CloudWatch Logs**.
- **Step Functions** → Enable execution history + CloudWatch logging.
- **PostgreSQL Logs** → Enable **Enhanced Monitoring** + **Performance Insights** in RDS.
- **Best:**  
  Use **AWS CloudWatch Log Insights** to query all logs in **one place**.

---

### 2. **Detailed Error Reporting**
Make sure errors are caught and clearly logged.

- **Lambda Error Logging**:  
  Wrap your logic to log both the event and the exception details.
  ```python
  try:
      # your business logic
  except Exception as e:
      logger.error(f"Error: {str(e)}, Input Event: {json.dumps(event)}")
      raise e
  ```

- **Glue Job Error Handling**:  
  Log job run IDs, job parameters, and input data.

- **Step Functions**:  
  Add **Catch blocks** to every state that can fail and send the failure details somewhere (SNS, CloudWatch, EventBridge).

---

### 3. **Failure Alerts**
Instant notifications when things go wrong.

- **Glue Job Failures**:  
  Set **AWS CloudWatch Alarms** on Glue job metrics (e.g., `FailedJobs > 0`) → Send SNS notification (email, Slack, Teams).

- **Lambda Failures**:  
  Set **Alarm** on `Lambda Errors > 0`.

- **Step Function Failures**:  
  Subscribe to Step Function **Execution Failed Events** using **EventBridge** and trigger an SNS notification.

- **PostgreSQL**:  
  Alarm on `RDS Error Logs`, `DB CPU > 80%`, `Storage Full`, `Connection Errors`.

---

### 4. **Monitoring Dashboards**
Create a **CloudWatch Dashboard** showing:

- Glue Job Success/Failure/Duration
- Lambda Invocations, Errors
- Step Function Executions, Errors
- PostgreSQL RDS health (CPU, Connections, Storage)
- Custom Metrics like **record counts** at each stage (optional but very powerful)

---

### 5. **Tracing and Profiling**
Make it easier to **trace end-to-end flow**:

- **Enable AWS X-Ray** for:
  - Lambda functions (easy tracing of function internals and external calls)
  - Glue jobs (partial, using SDK calls)
  - Step Functions (track flow of steps)

X-Ray gives you a **visual map** of where time and errors are happening.

---

### 6. **Structured Logging**
Make all logs structured (JSON format):

Example for Lambda:
```python
logger.info(json.dumps({
  "stage": "rule_engine",
  "event_id": event["id"],
  "status": "start"
}))
```

This allows you to **filter logs faster** in CloudWatch Log Insights:
```sql
fields @timestamp, @message
| filter status = "error"
| sort @timestamp desc
```

---

### 7. **ETL Health Check Jobs**
- **Scheduled Health Check** Lambda:
  - Daily/Hourly runs.
  - Check last Glue jobs, Step Function executions, RDS health.
  - Summarize health and send a report via email/SNS.
  
This gives **proactive alerts** even before users report issues.

---

### Quick Diagram of the Monitoring Flow

```
[Glue Jobs] ----+
                 |
[Lambdas] -------+---> [CloudWatch Logs] --> [CloudWatch Dashboard] --> [SNS Alerts]
                 |
[Step Functions]-+
                 |
[RDS PostgreSQL] --> [CloudWatch Metrics + Logs] --> [Alarms + Performance Insights]
```

**Optional (for mature setup):**  
Add **EventBridge Pipelines** to automate recovery (e.g., auto-retry failed jobs).

---

### Summary

| Layer | Monitoring | Logging | Alerting |
|:-----|:------------|:--------|:---------|
| Glue | Job metrics, logs | CloudWatch Logs | Alarms on Failures |
| Lambda | X-Ray traces, logs | CloudWatch Logs | Alarms on Errors |
| Step Functions | Execution logs | CloudWatch Logs | EventBridge Failures |
| PostgreSQL | Enhanced Monitoring | CloudWatch Logs | Alarms on RDS metrics |

---

Would you like me also to show you a **Terraform or CDK** sample to **deploy this whole monitoring setup automatically**?  
(Will save a lot of manual effort!)  

Would you also want a **sample notification email template** for failures? (Looks more professional if you are setting up for a team.)  
Let me know!

=≈==================//////================
Awesome!  
I'll break this into **two parts** to keep it clean:

---

## Part 1 — Terraform (or CDK) Sample to Deploy Monitoring + Alerts

This Terraform script **automates** the basic monitoring setup:

```hcl
# Create CloudWatch Log Group for Glue Jobs
resource "aws_cloudwatch_log_group" "glue_log_group" {
  name              = "/aws-glue/jobs"
  retention_in_days = 14
}

# CloudWatch Metric Alarm for Glue Job Failures
resource "aws_cloudwatch_metric_alarm" "glue_job_failure_alarm" {
  alarm_name          = "GlueJobFailures"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "FailedJobs"
  namespace           = "AWS/Glue"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Alarm when Glue job fails"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

# Create SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "etl-monitoring-alerts"
}

# Create Email Subscription to SNS
resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "your-email@example.com"  # <-- update this
}

# CloudWatch Alarm for Lambda Errors
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "LambdaFunctionErrors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Alarm when Lambda has errors"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

# CloudWatch Alarm for RDS CPU High
resource "aws_cloudwatch_metric_alarm" "rds_cpu_alarm" {
  alarm_name          = "RDSHighCPU"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "Alarm when RDS CPU is over 80%"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

---

**In simple English:**  
- Log groups to store Glue logs.
- SNS to send emails on failures.
- CloudWatch Alarms for:
  - Glue job failures
  - Lambda errors
  - RDS CPU high

---

If you prefer **AWS CDK (Python)** instead of Terraform, tell me — I can give that too.

---

## Part 2 — Sample Failure Notification Email Template

When something fails, the email should be **clear** and **actionable**.

Here’s a good template:

---
**Subject**: `[ALERT] ETL Job Failure - <Job Name>`

**Body**:

```
Hi Team,

An error has been detected in the ETL Pipeline.

Details:
- **Stage**: Glue Job / Lambda / Step Function
- **Component**: <Component Name>
- **Error Time**: <TimeStamp>
- **Error Summary**: <Error Message>
- **AWS Account/Region**: <Account Id / Region>

Impact:
- <Short description of what business process is affected>

Action Needed:
- Please check the CloudWatch Logs: <Link to Log Group>
- Retry if applicable or investigate the input data.

Thanks,
Automated Monitoring System
```
---

**Extra Tip**:  
You can also **include a direct link** to the CloudWatch Log Stream in the email by customizing your Lambda that sends the alert.

---

## Would you like me to also give you:
- A **dashboard** sample (Terraform/CDK) showing Glue + Lambda + RDS health?  
- A **sample "Health Check Lambda"** that can daily scan last ETL runs and alert proactively?

These 2 will make it **full end-to-end proactive monitoring**.

Would you want that?  
(Yes/No and I’ll continue accordingly!)
≈=========================================
Perfect!  
Let’s **complete this end-to-end** monitoring system.

---

# Part 3 — Terraform for CloudWatch Dashboard

This will **create a dashboard** where you can **see Glue, Lambda, RDS** metrics all in one place.

Here’s a simple **Terraform** for the dashboard:

```hcl
resource "aws_cloudwatch_dashboard" "etl_dashboard" {
  dashboard_name = "ETL-Monitoring-Dashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        "type": "metric",
        "x": 0,
        "y": 0,
        "width": 12,
        "height": 6,
        "properties": {
          "metrics": [
            ["AWS/Glue", "FailedJobs", "JobName", "your-glue-job-name"]
          ],
          "period": 300,
          "stat": "Sum",
          "title": "Glue Job Failures",
          "region": "your-region"
        }
      },
      {
        "type": "metric",
        "x": 12,
        "y": 0,
        "width": 12,
        "height": 6,
        "properties": {
          "metrics": [
            ["AWS/Lambda", "Errors", "FunctionName", "your-lambda-function-name"]
          ],
          "period": 300,
          "stat": "Sum",
          "title": "Lambda Errors",
          "region": "your-region"
        }
      },
      {
        "type": "metric",
        "x": 0,
        "y": 6,
        "width": 12,
        "height": 6,
        "properties": {
          "metrics": [
            ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "your-db-instance-id"]
          ],
          "period": 300,
          "stat": "Average",
          "title": "RDS CPU Utilization",
          "region": "your-region"
        }
      }
    ]
  })
}
```

> Just replace:
> - `your-glue-job-name`
> - `your-lambda-function-name`
> - `your-db-instance-id`
> - `your-region`

This will give you a **live view** of:
- Glue job failures
- Lambda errors
- RDS CPU health

All on a **single screen** in **CloudWatch Dashboard**!

---

# Part 4 — Health Check Lambda

A **small Lambda function** that runs every hour/day to **proactively** check if ETL jobs are failing.

Here’s a **Python 3.9+ compatible** Lambda code:

```python
import boto3
import datetime
import os

cloudwatch = boto3.client('cloudwatch')
glue = boto3.client('glue')
sns = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']  # Pass it via environment variable

def lambda_handler(event, context):
    response = glue.list_jobs(MaxResults=10)  # List your Glue Jobs (adjust MaxResults)
    
    failed_jobs = []
    for job_name in response['JobNames']:
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/Glue',
            MetricName='FailedJobs',
            Dimensions=[{'Name': 'JobName', 'Value': job_name}],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
            EndTime=datetime.datetime.utcnow(),
            Period=3600,
            Statistics=['Sum']
        )
        datapoints = metrics.get('Datapoints', [])
        if datapoints:
            if datapoints[0]['Sum'] > 0:
                failed_jobs.append(job_name)
    
    if failed_jobs:
        message = f"The following Glue jobs have failed in the last 1 hour:\n\n" + "\n".join(failed_jobs)
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="ETL Health Check - Glue Job Failures",
            Message=message
        )
    
    return {
        'statusCode': 200,
        'body': f"Checked {len(response['JobNames'])} jobs. {len(failed_jobs)} failures detected."
    }
```

**What it does:**
- Lists your Glue jobs.
- For each job, checks if failures happened in the **last 1 hour**.
- If any failed → **Sends a notification to SNS**.

**Setup Tip:**  
Schedule it using **EventBridge Rule** (every hour or once per day).

---

# Your Final Monitoring Architecture

```
ETL Flow (Glue, Lambda, Step Functions) 
    |
    v
[CloudWatch Logs] & [CloudWatch Metrics]
    |
    v
- Dashboard (Visual Monitoring)
- Alarms (SNS Alerts on Failures)
- Health Check Lambda (Proactive Alerts)
    |
    v
Email/Slack/Teams Notifications
```

**Result:**  
- Faster root cause detection  
- Proactive alerts (no waiting for user complaints)  
- Centralized dashboards for visibility

---

# Next Steps (Optional Extras)
If you want, we can also extend it with:
- Slack/Teams alerts instead of email (cooler for teams)
- Auto-retry mechanism for failed jobs (Step Functions)
- X-Ray tracing integration for detailed Lambda traces

---

**Would you like me to quickly show you how to add Slack notifications too?**  
(Just 5 lines extra config if you want!)  

Say "yes" if you want it!
==========================================

Got it — you want **Webex** notifications instead of just email!  
(No problem — Webex supports incoming **webhooks** very nicely.)

Here’s how we’ll do it:

---

# Webex Notifications for AWS Alerts

## Step 1: Create a Webex Incoming Webhook

1. Go to [Webex Developer Portal](https://developer.webex.com/my-apps)
2. Click on "**Create a New Webhook**"
3. Choose:
   - **Target URL** = `https://webexapis.com/v1/messages`
   - **Name** = anything like `ETL Monitoring Alerts`
   - **Resource** = `messages`
   - **Event** = `created`
   - **Access Token** = your Webex Bot token
   - **Filter** = choose your Webex room ID if needed
4. Save it.
5. You’ll get a **Webhook URL** (something like `https://webexapis.com/v1/webhooks/incoming/<id>`)

**Important:**  
Or simply create a Webex Bot and use the Bot’s access token + room ID to send messages.  
(Simpler and cleaner for sending alerts.)

---

## Step 2: Modify your Health Check Lambda to Send to Webex

Instead of SNS →  
We’ll **directly call Webex API**.

Here’s the **updated Lambda code**:

```python
import boto3
import datetime
import os
import requests

cloudwatch = boto3.client('cloudwatch')
glue = boto3.client('glue')

WEBEX_BOT_TOKEN = os.environ['WEBEX_BOT_TOKEN']  # Store in Lambda env vars
WEBEX_ROOM_ID = os.environ['WEBEX_ROOM_ID']      # Store in Lambda env vars

def send_webex_message(message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": WEBEX_ROOM_ID,
        "text": message
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

def lambda_handler(event, context):
    response = glue.list_jobs(MaxResults=10)
    
    failed_jobs = []
    for job_name in response['JobNames']:
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/Glue',
            MetricName='FailedJobs',
            Dimensions=[{'Name': 'JobName', 'Value': job_name}],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
            EndTime=datetime.datetime.utcnow(),
            Period=3600,
            Statistics=['Sum']
        )
        datapoints = metrics.get('Datapoints', [])
        if datapoints:
            if datapoints[0]['Sum'] > 0:
                failed_jobs.append(job_name)
    
    if failed_jobs:
        message = f"🚨 ETL Alert 🚨\nThe following Glue jobs failed in the last 1 hour:\n" + "\n".join(failed_jobs)
        send_webex_message(message)
    
    return {
        'statusCode': 200,
        'body': f"Checked {len(response['JobNames'])} jobs. {len(failed_jobs)} failures detected."
    }
```

---

## Step 3: Lambda Environment Variables Setup

- `WEBEX_BOT_TOKEN` = your Bot Access Token (keep secret)
- `WEBEX_ROOM_ID` = the Webex Room where you want notifications

Set these inside **Lambda console → Configuration → Environment Variables**.

---

## Sample Webex Alert Message

> **🚨 ETL Alert 🚨**  
> The following Glue jobs failed in the last 1 hour:  
> - job_extract_customer_data  
> - job_load_insurance_policy

It will appear cleanly in your Webex space — no manual checking needed!

---

# Quick Recap
| Component        | Purpose                    |
|------------------|-----------------------------|
| HealthCheck Lambda | Check Glue job failures |
| Webex Bot Token  | Authentication to send |
| Webex Room ID    | Target destination |
| Webex Message    | Auto alert on failure |

---

# Next Level (Optional)

If you want to make it even **richer**, you can:
- Send **step function failure** alerts too
- Attach links to the CloudWatch logs inside Webex message
- Post structured (card style) Webex messages

---

# Would you like me to also show a **Webex Card Style** rich message (instead of plain text)?  
(Example: Title, table of failed jobs, link buttons — looks very professional.)  

Say "**Yes - Card**" if you want it!  
I'll quickly show you!
=========================================/
Awesome — you're going to love this!  
**Webex "Cards"** (Adaptive Cards) make your alerts *look super professional* instead of just plain text.

---

# Sending Webex Adaptive Card from AWS Lambda

Here’s the **updated code** for sending a **card-style** Webex notification:

```python
import boto3
import datetime
import os
import requests
import json

cloudwatch = boto3.client('cloudwatch')
glue = boto3.client('glue')

WEBEX_BOT_TOKEN = os.environ['WEBEX_BOT_TOKEN']
WEBEX_ROOM_ID = os.environ['WEBEX_ROOM_ID']

def send_webex_card(failed_jobs):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    jobs_list = [{"type": "TextBlock", "text": f"- {job}", "wrap": True} for job in failed_jobs]

    card_payload = {
        "roomId": WEBEX_ROOM_ID,
        "markdown": "**ETL Alert: Glue Job Failures**",  # fallback text
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Large",
                            "weight": "Bolder",
                            "text": "🚨 ETL Alert: Glue Job Failures"
                        },
                        {
                            "type": "TextBlock",
                            "text": "The following Glue jobs have failed in the last 1 hour:",
                            "wrap": True
                        },
                        {
                            "type": "Container",
                            "items": jobs_list
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "View CloudWatch Logs",
                            "url": "https://console.aws.amazon.com/cloudwatch/home"  # Update if you want deep link
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=card_payload)
    response.raise_for_status()

def lambda_handler(event, context):
    response = glue.list_jobs(MaxResults=10)
    
    failed_jobs = []
    for job_name in response['JobNames']:
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/Glue',
            MetricName='FailedJobs',
            Dimensions=[{'Name': 'JobName', 'Value': job_name}],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
            EndTime=datetime.datetime.utcnow(),
            Period=3600,
            Statistics=['Sum']
        )
        datapoints = metrics.get('Datapoints', [])
        if datapoints:
            if datapoints[0]['Sum'] > 0:
                failed_jobs.append(job_name)
    
    if failed_jobs:
        send_webex_card(failed_jobs)
    
    return {
        'statusCode': 200,
        'body': f"Checked {len(response['JobNames'])} jobs. {len(failed_jobs)} failures detected."
    }
```

---

# How the Webex Card Will Look

| Section         | Content                  |
|-----------------|---------------------------|
| Title           | 🚨 ETL Alert: Glue Job Failures |
| Body            | List of failed job names |
| Button          | "View CloudWatch Logs" to deep link into AWS |

It'll look like a **rich professional Webex alert** with clickable buttons.

**Sample preview:**

```
🚨 ETL Alert: Glue Job Failures
The following Glue jobs have failed in the last 1 hour:
- job_extract_customer_data
- job_transform_policy_info
- job_load_insurance_records

[ View CloudWatch Logs ]
```

---

# Bonus Tip

You can even **deep link directly to Glue job logs** if you want, by customizing the `url` field!  
Example:

```python
"https://console.aws.amazon.com/gluestudio/home?region=your-region#/job/jobname/run"
```

Dynamic linking per job is also possible if needed.

---

# Quick Recap

| Feature            | Done? |
|--------------------|-------|
| Plain text message  | ✅ |
| Webex incoming webhook | ✅ |
| Adaptive Card rich notification | ✅ |

---

# Final Question:  
Would you like me to give you a **Terraform** ready example also to automatically deploy this Lambda + EventBridge + IAM roles in one shot?  
(*Save you lot of manual clicks!*)  

Say "**Yes Terraform**" if you want it!  
I'll give you production-ready code!
≈=================/////==========////====
Perfect!  
Here’s a **production-ready Terraform** setup to deploy everything:  

We will create:
- Lambda Function (Glue Health Check + Webex Card Alerts)
- IAM Role for Lambda (with minimum permissions)
- EventBridge Rule (schedule to run every X minutes)
- Permissions for EventBridge to trigger Lambda

---

# 1. `variables.tf` (basic config)

```hcl
variable "region" {
  default = "us-east-1"  # change as needed
}

variable "webex_bot_token" {
  description = "Webex Bot Token"
}

variable "webex_room_id" {
  description = "Webex Room ID"
}
```

---

# 2. `iam.tf` (Lambda IAM Role and Policy)

```hcl
resource "aws_iam_role" "lambda_role" {
  name = "lambda-glue-monitoring-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda-glue-monitoring-policy"
  description = "Permissions for Glue Monitoring Lambda"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "glue:ListJobs",
          "cloudwatch:GetMetricStatistics",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
```

---

# 3. `lambda.tf` (Lambda deployment)

```hcl
resource "aws_lambda_function" "glue_monitor" {
  function_name = "glue-monitor-webex"

  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  timeout       = 60

  filename         = "build/glue_monitor.zip"  # We'll zip it
  source_code_hash = filebase64sha256("build/glue_monitor.zip")

  environment {
    variables = {
      WEBEX_BOT_TOKEN = var.webex_bot_token
      WEBEX_ROOM_ID   = var.webex_room_id
    }
  }
}
```

---

# 4. `eventbridge.tf` (Scheduled trigger)

```hcl
resource "aws_cloudwatch_event_rule" "every_5_minutes" {
  name                = "glue-monitor-schedule"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_5_minutes.name
  target_id = "glue-monitor-lambda"
  arn       = aws_lambda_function.glue_monitor.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.glue_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_5_minutes.arn
}
```

---

# 5. **Folder structure**

```
terraform/
 ├── iam.tf
 ├── lambda.tf
 ├── eventbridge.tf
 ├── variables.tf
 ├── outputs.tf (optional)
 └── build/
      └── glue_monitor.zip   # Contains your Python code
```

Zip the **Python Lambda function** (`lambda_function.py`) as `glue_monitor.zip`.

---

# 6. **Command to Deploy**

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

Boom! Lambda + IAM + Scheduler + Webex alerts will be automatically ready!

---

# Bonus: If you want a **Terraform zip** automation also (no manual zipping), I can give you a mini `Makefile` to auto-build the Lambda bundle every time you change the code.  
**Would you like me to show that too?**  
(Just say "**Yes build zip**" if you want it!)  

---

Would you also want me to show:
- Alert only if failure count > threshold?
- Include Step Function failures along with Glue?  
(*Easy to extend!*) 

Let me know!
