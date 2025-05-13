Here’s a **Deployment Files Mind Map** that visually organizes key files involved in AWS deployment pipelines — including **CodeBuild, ECS, EKS, Elastic Beanstalk, Lambda**, and more.

---

## 🧠 **Mind Map: Deployment Files in AWS**

```
Deployment Files in AWS
│
├── ✅ CodeBuild & CodePipeline
│   └── buildspec.yml
│       ├── Define phases: install, pre_build, build, post_build
│       ├── Artifacts definition for deployable outputs
│       └── Environment variables, cache, reports
│
├── ✅ Elastic Beanstalk
│   └── .ebextensions/app.config
│       ├── Environment properties (option_settings)
│       ├── OS-level packages (yum, apt)
│       ├── Files placement (config, scripts)
│       └── Custom commands/scripts to run
│
├── ✅ CodeDeploy (for EC2, ECS, Lambda)
│   └── appspec.yml
│       ├── Hooks (BeforeInstall, AfterInstall, ApplicationStart, etc.)
│       ├── File copy mappings
│       └── Lambda function deployment settings
│
├── ✅ ECS (Fargate/EC2)
│   └── task-definition.json
│       ├── Container definitions (image, port, env variables)
│       ├── Task roles, log configuration (CloudWatch)
│       └── Networking mode (bridge, awsvpc)
│
├── ✅ EKS (Kubernetes)
│   └── manifest.yaml (Deployment, Service, Ingress)
│       ├── Kind: Deployment, Service, ConfigMap, Secret
│       ├── ReplicaSet, RollingUpdate config
│       └── ServiceType: ClusterIP, LoadBalancer, NodePort
│
├── ✅ Lambda Deployment
│   └── template.yaml (SAM template)
│       ├── AWS::Serverless::Function definitions
│       ├── CodeUri & runtime info
│       └── API Gateway integration
│
├── ✅ Common Across Deployments
│   ├── version.txt
│   │   └── Track deployed application version
│   ├── Dockerfile (ECS, EKS, Lambda Container)
│   │   └── Build container image with app dependencies
│   └── .env / config.json
│       └── Environment-specific configurations
│
└── ✅ Advanced (Infra as Code)
    ├── CloudFormation template.yaml / json
    │   └── Full stack definition (VPC, EC2, RDS, etc.)
    ├── Terraform .tf files
    │   └── Modular infrastructure deployments
    └── CDK (Python/TS) stacks
        └── Programmatic infra deployments
```

---

## 🎯 **Key Exam Traps & Notes**

| File                     | Common Traps                | Must Remember                           |
| ------------------------ | --------------------------- | --------------------------------------- |
| buildspec.yml            | Missing artifacts section   | Without it, deploy stage fails          |
| appspec.yml              | Wrong lifecycle hook names  | Must match CodeDeploy hook names        |
| task-definition.json     | Incorrect log configuration | CloudWatch log group & region needed    |
| manifest.yaml (EKS)      | Service type mismatch       | LoadBalancer vs ClusterIP               |
| template.yaml (SAM)      | API event trigger missing   | Resource path, method should be defined |
| Dockerfile               | Wrong working directory     | COPY & WORKDIR need correct paths       |
| .ebextensions/app.config | Legacy vs Modern hooks      | Use `.platform` for newer platforms     |

---

### ➡️ **Do you want a Cheat Sheet comparing `buildspec.yml`, `appspec.yml`, `task-definition.json`, `template.yaml`, and `manifest.yaml` side by side?** (like exam quick reference table)

Reply with **"Yes Deployment Files Cheat Sheet"** and I'll create it.
