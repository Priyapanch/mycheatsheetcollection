GH 200 GITHUB ACTIONS Practice Question and Answers.

# GitHub Actions Practice Questions & Answers

This comprehensive practice set covers essential GitHub Actions concepts for test automation and CI/CD pipelines, tailored for intermediate to advanced practitioners.

***

## Interactive Practice Quiz

An interactive quiz with 20 questions covering GitHub Actions fundamentals, workflow configuration, and advanced features is available for self-assessment:



***

## Study Questions by Category

### **Core Concepts & Workflow Structure**

**Q1: What are the fundamental components of a GitHub Actions workflow, and how do they relate to each other?**

The three fundamental components are:
- **Workflow**: An automated procedure that runs one or more jobs, triggered by events
- **Job**: A set of steps that execute on the same runner, running in parallel or sequentially
- **Step**: An individual task that can run commands or actions, executing sequentially within a job

**Q2: What is the correct syntax for naming a workflow in the YAML file?**

```yaml
name: CI Pipeline for API Tests
```

The `name` field appears at the root level of the workflow YAML file and displays in the Actions tab.

**Q3: How do you specify that a workflow should trigger on push to the main branch AND on pull requests targeting the main branch?**

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

**Q4: What is the difference between `runs-on: ubuntu-latest` and `runs-on: self-hosted`?**

- `ubuntu-latest`: Uses GitHub-hosted runners with pre-configured Ubuntu environments
- `self-hosted`: Uses your own infrastructure, providing custom hardware, software, and security configurations

### **Events & Triggers**

**Q5: Which event would you use to trigger a workflow when a new release is published?**

```yaml
on:
  release:
    types: [published]
```

**Q6: How can you schedule a workflow to run daily at 2 AM UTC?**

```yaml
on:
  schedule:
    - cron: '0 2 * * *'
```

**Q7: What is the purpose of `workflow_dispatch` and how do you configure input parameters?**

`workflow_dispatch` enables manual triggering with custom inputs:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
```

### **Jobs & Steps**

**Q8: How do you force one job to run after another job completes successfully?**

Use the `needs` keyword:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building"
  
  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - run: echo "Testing after build"
```

**Q9: What is the difference between `actions/checkout@v4` and `actions/setup-node@v4`?**

- `actions/checkout@v4`: Checks out your repository code into the runner's workspace
- `actions/setup-node@v4`: Sets up a Node.js environment with specified version

**Q10: How do you run a shell command as a step in a workflow?**

```yaml
steps:
  - name: Run API tests
    run: |
      npm install
      npm run test:api
```

### **Environment Variables & Secrets**

**Q11: How do you set environment variables at the workflow level and access them in steps?**

```yaml
env:
  NODE_VERSION: '18'
  DATABASE_URL: 'postgres://localhost:5432/test'

steps:
  - name: Use Node version
    run: echo "Using Node ${{ env.NODE_VERSION }}"
```

**Q12: What is the correct way to reference a GitHub secret in a workflow?**

```yaml
steps:
  - name: Deploy to production
    run: |
      echo "${{ secrets.DATABASE_PASSWORD }}" | deploy.sh
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

**Q13: How do you mask sensitive values in logs?**

GitHub automatically masks values from secrets. For other values, use:

```yaml
steps:
  - name: Mask sensitive value
    run: echo "::add-mask::${{ secrets.SENSITIVE_VALUE }}"
```

### **Matrix Builds & Strategy**

**Q14: How do you run the same job across multiple Node.js versions and operating systems?**

```yaml
strategy:
  matrix:
    node-version: [16, 18, 20]
    os: [ubuntu-latest, windows-latest, macos-latest]

runs-on: ${{ matrix.os }}

steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node-version }}
```

**Q15: How do you exclude specific combinations from a matrix strategy?**

```yaml
strategy:
  matrix:
    node-version: [16, 18, 20]
    os: [ubuntu-latest, windows-latest]
    exclude:
      - node-version: 16
        os: windows-latest
```

### **Artifacts & Caching**

**Q16: How do you upload test results as workflow artifacts?**

```yaml
steps:
  - name: Run tests
    run: npm test
    
  - name: Upload test results
    uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results
      path: |
        test-results/
        coverage/
      retention-days: 30
```

**Q17: How do you cache npm dependencies to speed up workflow execution?**

```yaml
steps:
  - uses: actions/checkout@v4
  
  - name: Cache node modules
    uses: actions/cache@v4
    with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-
```

### **Reusable Workflows & Composite Actions**

**Q18: How do you call a reusable workflow from another repository?**

```yaml
jobs:
  call-workflow:
    uses: org/repo/.github/workflows/reusable-workflow.yml@main
    with:
      environment: staging
    secrets:
      token: ${{ secrets.REPO_TOKEN }}
```

**Q19: What is the difference between a reusable workflow and a composite action?**

- **Reusable Workflow**: Entire workflow file that can be called from other workflows, supports multiple jobs, can use secrets, runs in separate context
- **Composite Action**: Combines multiple steps into a single action, runs within a job, cannot directly use secrets (must pass them as inputs), better for sharing step logic

**Q20: Create a composite action that runs linting and returns the result:**

```yaml
# .github/actions/lint/action.yml
name: 'Lint Code'
description: 'Runs ESLint on the codebase'
inputs:
  eslint-config:
    description: 'Path to ESLint config'
    required: false
    default: '.eslintrc.js'
runs:
  using: 'composite'
  steps:
    - name: Install dependencies
      run: npm ci
      shell: bash
    
    - name: Run linter
      run: npx eslint . --config ${{ inputs.eslint-config }}
      shell: bash
```

### **Security & Permissions**

**Q21: How do you limit workflow permissions to read-only for contents?**

```yaml
permissions:
  contents: read
  pull-requests: write
```

**Q22: What is the principle of least privilege in GitHub Actions, and how do you implement it?**

Grant only necessary permissions at the job level:

```yaml
jobs:
  deploy:
    permissions:
      contents: read
      id-token: write  # For OIDC token
```

**Q23: How do you use OpenID Connect (OIDC) for secure cloud provider authentication?**

```yaml
jobs:
  deploy:
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
```

### **Testing & QA Automation**

**Q24: How do you run API tests with Newman (Postman) in GitHub Actions?**

```yaml
jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install Newman
        run: npm install -g newman
      
      - name: Run API tests
        run: newman run collection.json -e environment.json
        
      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: newman-report
          path: newman/
```

**Q25: How do you implement test result reporting with JUnit XML format?**

```yaml
steps:
  - name: Run tests
    run: npm test -- --reporter junit
    
  - name: Publish Test Results
    uses: mikepenz/action-junit-report@v4
    if: always()
    with:
      report_paths: '**/junit.xml'
      check_name: 'API Test Results'
```

**Q26: How do you conditionally run tests only when API-related files change?**

```yaml
on:
  pull_request:
    paths:
      - 'api/**'
      - 'tests/api/**'
      - '.github/workflows/api-tests.yml'
```

**Q27: How do you implement a manual approval gate before running production tests?**

```yaml
jobs:
  approve:
    runs-on: ubuntu-latest
    environment: production-approval
    steps:
      - name: Wait for approval
        run: echo "Approved for production testing"
  
  test-production:
    needs: approve
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running production tests"
```

### **Advanced Features**

**Q28: How do you use `concurrency` to prevent multiple workflow runs from interfering?**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Q29: How do you access contextual information about the workflow run?**

```yaml
steps:
  - name: Show context
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Actor: ${{ github.actor }}"
      echo "Event: ${{ github.event_name }}"
      echo "SHA: ${{ github.sha }}"
      echo "Branch: ${{ github.ref_name }}"
```

**Q30: How do you implement error handling and job status checks?**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests with continue-on-error
        run: npm test
        continue-on-error: true
      
      - name: Upload results regardless of test outcome
        if: always()
        run: upload-results.sh
      
      - name: Notify on failure
        if: failure()
        run: notify-team.sh
```

***

## Practical Scenarios for Test Automation

### **Scenario 1: Full CI/CD Pipeline for API Testing**

```yaml
name: API Test Automation Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  NODE_VERSION: '18'
  API_BASE_URL: 'https://api.staging.example.com'

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      
      - name: Install dependencies
        run: npm ci

  lint:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint

  api-tests:
    needs: [setup, lint]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-suite: [auth, users, orders]
      fail-fast: false
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ${{ matrix.test-suite }} tests
        run: npm run test:${{ matrix.test-suite }}
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.test-suite }}
          path: |
            test-results/
            coverage/
          retention-days: 7

  report:
    needs: api-tests
    runs-on: ubuntu-latest
    if: always()
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Download all test results
        uses: actions/download-artifact@v4
      
      - name: Publish test report
        uses: mikepenz/action-junit-report@v4
        with:
          report_paths: '**/junit.xml'
          check_name: 'API Test Report'
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

### **Scenario 2: Database Migration Testing**

```yaml
name: Database Migration Validation

on:
  pull_request:
    paths:
      - 'migrations/**'
      - 'tests/migration/**'

jobs:
  test-migration:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r test-requirements.txt
      
      - name: Run migration tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: pytest tests/migration/ -v --junitxml=migration-results.xml
      
      - name: Upload migration test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: migration-test-results
          path: migration-results.xml
```

***

## Key Takeaways for QA/Test Automation Professionals

GitHub Actions provides powerful capabilities for test automation workflows:

- **Matrix strategies** enable comprehensive testing across multiple environments and configurations
- **Reusable workflows** promote DRY principles across repository and organizational levels
- **Caching mechanisms** significantly reduce execution time for dependency-heavy test suites
- **Service containers** allow integration testing with databases, caches, and external services
- **Artifact management** preserves test results, coverage reports, and debugging information
- **Security features** like OIDC and environment protection rules enable safe production testing
- **Conditional execution** with path-based filters and status checks optimizes resource usage

These patterns align with enterprise QA requirements for scalability, maintainability, and reliability in continuous testing pipelines.
