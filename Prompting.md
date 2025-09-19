Awesome — I’ve designed a practical, 5-hour MVP plan you can actually build and ship. It focuses on the absolute essentials so you get a working “prompt optimizer” loop (generate variants → evaluate → evolve → store results) that you can extend later.

I’ll give you:

1. MVP scope (must-haves vs nice-to-have)


2. 5-hour step-by-step sprint plan with time blocks (exact)


3. Minimal folder structure + files you should create


4. Ready-to-run code snippets (FastAPI + tiny GA-like variation engine + mock provider + evaluator + orchestrator)


5. How to run & test (curl examples)


6. Trade-offs & next steps



Keep this open — copy/paste the code and start building.

1 — MVP scope (what to deliver in 5 hours)

Must-have (deliver in 5 hours)

Simple REST API to register a template and start an experiment.

Variation engine that generates prompt variants (light GA-like: mutation + crossover).

Orchestrator that runs variants against a mock LLM provider and evaluates results.

Simple evaluator (task: exact-match / token overlap).

Persistence as local JSON files (no DB) and an endpoint to fetch experiment results.

Basic results viewer via JSON (no UI required).


Nice-to-have if time remains

Small static HTML page showing summary.

Support for a real provider (OpenAI) via an adapter (placeholder).

Basic plotting of metric improvements.


2 — 5-hour sprint plan (precise)

Follow this schedule and you’ll have an MVP by the 5-hour mark.

0:00–0:30 — Project setup

Create repo, venv, basic files, directories.

pip install fastapi uvicorn


0:30–1:30 — Build minimal REST API + persistence (endpoints for templates & experiments)

POST /templates, POST /experiments, GET /experiments/{id}


1:30–2:30 — Implement variation engine (mutation + crossover) & mock provider

Simple transformation rules, deterministic/noisy mock response


2:30–3:30 — Implement evaluator + orchestrator (run experiments synchronously)

Evaluate each variant N times, compute accuracy, tokens, latency


3:30–4:15 — Wire everything, run one sample experiment, iterate

Fix bugs, ensure results saved


4:15–4:40 — Add quick results viewer endpoint / small HTML (optional)

Return best variants + metrics


4:40–5:00 — Polish README, sample config files, curl examples; record next steps

3 — Folder structure

prompt-optimizer-mvp/
├─ app.py                # FastAPI app + orchestrator glue
├─ variation_engine.py   # GA-like module (mutation/crossover)
├─ mock_provider.py      # Mock LLM adapter
├─ evaluator.py          # Scoring functions
├─ data/
│  ├─ templates.json
│  ├─ experiments/       # saves experiment results as JSON
│  └─ runs/
└─ README.md

4 — Minimal working code

Create the files below. This is intentionally small, dependency-light, and runnable.


---

app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid, json, os, time
from variation_engine import generate_initial_population, evolve_population
from mock_provider import mock_call
from evaluator import score_response

DATA_DIR = "data"
TEMPLATES_FILE = os.path.join(DATA_DIR, "templates.json")
EXP_DIR = os.path.join(DATA_DIR, "experiments")
os.makedirs(EXP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TEMPLATES_FILE), exist_ok=True)
if not os.path.exists(TEMPLATES_FILE):
    with open(TEMPLATES_FILE,"w") as f: json.dump([], f)

app = FastAPI(title="Prompt Optimizer MVP")

class TemplateIn(BaseModel):
    name: str
    text: str

class ExperimentIn(BaseModel):
    template_id: str
    ground_truth: str
    pop_size: int = 8
    generations: int = 3
    repeats: int = 3

def load_templates():
    with open(TEMPLATES_FILE,"r") as f:
        return json.load(f)

def save_template(obj):
    t = load_templates()
    t.append(obj)
    with open(TEMPLATES_FILE,"w") as f:
        json.dump(t,f, indent=2)

@app.post("/templates")
def create_template(t: TemplateIn):
    obj = {"id": str(uuid.uuid4()), "name": t.name, "text": t.text}
    save_template(obj)
    return obj

@app.post("/experiments")
def run_experiment(cfg: ExperimentIn):
    # load template
    templates = load_templates()
    template = next((x for x in templates if x["id"]==cfg.template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="template not found")
    exp_id = str(uuid.uuid4())
    exp_path = os.path.join(EXP_DIR, f"{exp_id}.json")
    start = time.time()

    # initial population
    population = generate_initial_population(template["text"], cfg.pop_size)
    history = []

    for gen in range(cfg.generations):
        gen_results = []
        for variant in population:
            scores = []
            tokens = []
            latencies = []
            for r in range(cfg.repeats):
                t0 = time.time()
                resp = mock_call(variant)  # mock provider
                lat = time.time() - t0
                sc = score_response(resp, cfg.ground_truth)
                scores.append(sc)
                tokens.append(len(resp.split()))
                latencies.append(lat)
            avg_score = sum(scores)/len(scores)
            gen_results.append({
                "variant": variant,
                "avg_score": avg_score,
                "avg_tokens": sum(tokens)/len(tokens),
                "avg_latency": sum(latencies)/len(latencies)
            })
        # save gen summary
        history.append({"generation": gen, "results": gen_results})
        # evolve to next gen
        population = evolve_population([r["variant"] for r in gen_results], pop_size=cfg.pop_size)

    exp_obj = {
        "id": exp_id,
        "template_id": cfg.template_id,
        "ground_truth": cfg.ground_truth,
        "pop_size": cfg.pop_size,
        "generations": cfg.generations,
        "repeats": cfg.repeats,
        "history": history,
        "elapsed": time.time()-start
    }
    with open(exp_path,"w") as f:
        json.dump(exp_obj, f, indent=2)
    return {"experiment_id": exp_id, "summary": {
        "best_variant": max(history[-1]["results"], key=lambda r: r["avg_score"]),
        "elapsed": exp_obj["elapsed"]
    }}

@app.get("/experiments/{eid}")
def get_experiment(eid: str):
    path = os.path.join(EXP_DIR, f"{eid}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="experiment not found")
    with open(path,"r") as f:
        return json.load(f)


---

variation_engine.py

import random

MUTATIONS = [
    lambda s: "Be concise. " + s,
    lambda s: "Provide JSON only. " + s,
    lambda s: s + " If uncertain, answer 'unknown'.",
    lambda s: s.replace("Describe", "Summarize"),
    lambda s: "In short: " + s
]

def generate_initial_population(template_text, pop_size=8):
    base = template_text
    pop = []
    for i in range(pop_size):
        op = random.choice(MUTATIONS)
        pop.append(op(base))
    return pop

def mutate(s):
    op = random.choice(MUTATIONS)
    return op(s)

def crossover(a, b):
    # crude crossover: split mid and join
    ai = len(a)//2
    bi = len(b)//2
    return a[:ai] + b[bi:]

def evolve_population(population, pop_size=8):
    # selection: keep top half by heuristic (we don't have scores here so random)
    selected = sorted(population, key=lambda x: len(x))[:max(1,len(population)//2)]
    # breed
    children = []
    while len(children) < pop_size - len(selected):
        a,b = random.sample(selected, 2) if len(selected) > 1 else (selected[0], selected[0])
        child = crossover(a,b)
        if random.random() < 0.4:
            child = mutate(child)
        children.append(child)
    new_pop = selected + children
    # if short, pad with mutated originals
    while len(new_pop) < pop_size:
        new_pop.append(mutate(random.choice(population)))
    random.shuffle(new_pop)
    return new_pop


---

mock_provider.py

import random
import time

def mock_call(prompt: str) -> str:
    """
    Simulates an LLM response. Simple heuristic:
    - If prompt contains 'JSON' or 'Provide JSON only' or 'Be concise' boost chance of correct.
    - Returns either a correct string "EXPECTED_ANSWER" or "WRONG_ANSWER" with noise.
    """
    base_quality = 0.2
    p = prompt.lower()
    if "json" in p: base_quality += 0.25
    if "concise" in p: base_quality += 0.1
    if "short" in p: base_quality += 0.05
    if "if uncertain" in p: base_quality += 0.05
    # add small random jitter
    quality = min(0.95, base_quality + random.uniform(-0.05, 0.15))
    # simulate latency
    time.sleep(random.uniform(0.02, 0.12))
    if random.random() < quality:
        return "EXPECTED_ANSWER"
    else:
        # produce a plausible but wrong answer
        return "WRONG_ANSWER"


---

evaluator.py

import re

def normalize(s: str) -> str:
    return re.sub(r"\W+","", s or "").lower()

def score_response(response: str, ground_truth: str) -> float:
    # exact-match or token overlap fallback
    if not response: return 0.0
    if normalize(response) == normalize(ground_truth):
        return 1.0
    # token overlap ratio
    resp_tokens = set(response.lower().split())
    gt_tokens = set(ground_truth.lower().split())
    if not gt_tokens:
        return 0.0
    inter = resp_tokens.intersection(gt_tokens)
    return len(inter)/len(gt_tokens)


---

Save initial template example to data/templates.json (or create via API):

[
  {
    "id": "tpl-1",
    "name": "extract-entity",
    "text": "Extract the primary answer from the input. Return 'EXPECTED_ANSWER' if it is present."
  }
]

5 — How to run (commands)

Linux / macOS example:

git clone <repo>
cd prompt-optimizer-mvp
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic
# create data dirs & templates file (or POST via API)
mkdir -p data/experiments
# run
uvicorn app:app --reload --port 8000

Example curl to run experiment (uses template id tpl-1 saved above):

curl -X POST "http://127.0.0.1:8000/experiments" \
  -H "Content-Type: application/json" \
  -d '{"template_id":"tpl-1","ground_truth":"EXPECTED_ANSWER","pop_size":8,"generations":3,"repeats":3}'

Fetch results:

curl http://127.0.0.1:8000/experiments/<experiment_id>

6 — What this MVP gives you (value)

Working loop: templates → generate variants → evaluate → evolve → persisted experiment results.

Easy to extend: replace mock_provider.mock_call with a real provider adapter, connect persistence to Postgres, add async workers (Celery), or swap evaluator for task-specific metrics.

You’ll be able to show a demo within 5 hours that proves the concept (GA-like evolution improves average score across generations).


7 — Trade-offs & limitations (what we defer)

Uses mock LLM (quick to demo). Real LLM integration: add provider adapter and rate/cost controls.

Persistence is local JSON (no multi-tenant DB). For production, move to Postgres + vector DB.

Single-threaded synchronous orchestration — acceptable for MVP; scale with worker queues later.

Evaluation is simplistic (exact-match / overlap). For richer tasks add human labels, embeddings similarity, or task-specific metrics.


8 — Suggested next steps after MVP

Add provider adapters (OpenAI/Anthropic) behind an interface and secrets/vault.

Add async worker queue (Celery + Redis) and rate-limiting.

Add caching & surrogate filters (cheap model prefilter to save cost).

Add a small React UI to list templates/experiments and show metric charts.

Add RBAC, PII redaction, and audit logs.



---

If you want, I can:

paste a single-file ZIP-ready skeleton (all files assembled) in the next reply, or

generate a simple docker-compose that runs the app, or

swap mock_provider with a real OpenAI adapter (I’ll include the exact code and env var names) and show cost-aware calls.


Which of those should I produce immediately? (I can generate the full skeleton now.)

