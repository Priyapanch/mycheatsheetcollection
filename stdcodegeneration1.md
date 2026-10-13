For example, for **Subtask #2 — Create the project from the extracted code**, I would use this prompt:

Act as a senior Python engineer.

I have extracted multiple code snippets from a documentation/example source. Your task is to reconstruct them into a **runnable, cleanly structured Python project**.

### Objectives

1. Analyze all extracted code snippets.
2. Identify which snippets belong together and determine their execution order.
3. Identify:

   * required imports
   * external packages
   * environment variables
   * configuration
   * helper functions/classes
   * missing dependencies
   * assumptions made by the original examples
4. Create a logical project structure rather than putting everything into one file.
5. Preserve the original functionality as much as possible.
6. Do not invent business functionality that is not present in the source.
7. Where source code is incomplete, explicitly identify the gap and implement only the minimum required scaffolding.

### Expected project structure

Create an appropriate structure similar to:

```text
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── llm_client.py
│   └── ...
├── tests/
│   └── ...
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

Modify this structure if the source code requires a better design.

### LLM integration requirement

The project must use an abstraction such as:

```python
class LLMClient:
    ...
```

Do not tightly couple the application code to a specific LLM provider.

The LLM client must be designed so that a **custom LLM API Gateway/base URL** can be configured later through environment variables.

Include configuration placeholders such as:

```text
LLM_API_BASE_URL=
LLM_API_KEY=
LLM_MODEL=
LLM_VERIFY_SSL=false
```

Do not hard-code secrets.

### Important

For the current environment, HTTPS certificate verification must be configurable and default to:

```text
LLM_VERIFY_SSL=false
```

Keep this configuration centralized rather than scattering `verify=False` throughout the code.

### Deliverables

Provide:

1. Final project tree
2. Complete source files
3. Dependency file
4. `.env.example`
5. Basic test/smoke test
6. README with exact setup and execution commands
7. A table showing:

| Source snippet | Destination file | Dependencies | Changes made | Validation status |
| -------------- | ---------------- | ------------ | ------------ | ----------------- |

### Validation requirement

Before declaring the project complete, perform a static review of the reconstructed code and identify:

* syntax problems
* missing imports
* missing packages
* undefined variables
* incorrect function calls
* configuration problems
* incomplete source examples
* likely runtime failures

Do **not** claim the project is runnable merely because the code looks correct.

Clearly separate:

**Confirmed working**
from
**Needs runtime validation**

The final goal is a project that can be installed and executed from a clean environment with minimal manual changes.

This is stronger than simply asking *“convert these snippets into a project”* because it forces the LLM to perform **dependency reconstruction + architecture + configuration + validation**, which is what you actually need for your workflow.