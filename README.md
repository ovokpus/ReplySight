<p align="center"><img src="assets/banner.jpg" alt="Brass service bell beside a bundle of letters tied with red string and a magnifying glass on a dark surface" width="100%"></p>

# ReplySight

<p align="center"><img src="docs/assets/hero.svg" alt="ReplySight" width="100%"/></p>

**Research-backed customer-service replies from an agentic LangGraph workflow.**

A support agent pastes a customer complaint. A GPT-4o agent searches arXiv for service-recovery research and the web (Tavily) for real-world examples, then drafts an empathetic reply with citations.

![Chat page](docs/screenshots/chat.png)

---

## Business case

Support agents lose time finding the right words for difficult complaints, and research on 5,179 support agents found AI assistance raised their productivity by 14% on average. ReplySight drafts an empathetic reply backed by service-recovery research and real examples, for the agent to edit and send. It works best as a drafting aid for newer agents. [docs/BUSINESS_CASE.md](docs/BUSINESS_CASE.md) covers the sourced evidence, use cases, an illustrative ROI model and the limits.

## 1. The problem

Support reps lose minutes per ticket hunting for good phrasing and best practice. ReplySight puts that research behind a single button.

## 2. How it works

<p align="center"><img src="docs/assets/flow.svg" alt="ReplySight data flow" width="100%"/></p>

```mermaid
flowchart LR
    UI["Next.js frontend<br/>:3000"] -->|POST /respond| API["FastAPI<br/>:8000"]
    API --> G
    subgraph G["LangGraph workflow"]
        S([start]) --> A[agent<br/>GPT-4o]
        A -.-> AX[arxiv_tools] --> EA[extract_arxiv] --> A
        A -.-> TV[tavily_tools] --> ET[extract_tavily] --> A
        A -. action .-> C[compose]
        C -. continue .-> A
        C -. end .-> E([end])
    end
    AX --> ARXIV[(arXiv)]
    TV --> TAV[(Tavily web search)]
    A --> OAI[(OpenAI)]
```

The diagram follows the live `/workflow/graph` output (8 nodes, 10 edges); see [`docs/screenshots/api-samples.json`](docs/screenshots/api-samples.json).

## 3. Run it locally

```bash
cp .env.example .env        # add OPENAI_API_KEY and TAVILY_API_KEY to get real replies
docker compose up -d --build --wait
open http://localhost:3000  # UI
open http://localhost:8000/docs
docker compose down
```

Without keys, the stack still starts and reports healthy. `/health` shows `openai: false, tavily: false`, and generating a reply returns an error (see below).

## 4. What you get

| Screen | Screenshot |
| --- | --- |
| Chat: paste a complaint | ![chat](docs/screenshots/chat.png) |
| Workflow view: the LangGraph diagram, rendered live from the API | ![workflow](docs/screenshots/workflow.png) |
| API docs (FastAPI) | ![api docs](docs/screenshots/api-docs.png) |

### Model-dependent screen: not run

These screenshots were taken **without an OpenAI or Tavily key**, so no reply was generated. This is what the app really shows when you submit a complaint with no key (the API returns 500 because OpenAI rejects the request):

![no key](docs/screenshots/chat-no-key.png)

With valid keys in `.env`, this panel shows the drafted reply and its citations. That output has not been captured here.

## 5. Tests and CI

```bash
uv run --no-project --python 3.12 --with-requirements requirements.txt \
  --with-requirements requirements-dev.txt pytest -q tests/test_offline.py
```

`tests/test_offline.py` covers `/health` (keys reported missing), `/workflow/graph`, and input validation on `/respond`, all without network access. GitHub Actions runs those tests and then `docker compose build`. The older suites in `tests/` and `evals/` call OpenAI and Tavily live, so CI doesn't run them.

Regenerate the screenshots with the stack running:

```bash
uv run --no-project --with playwright python scripts/screenshots.py
```

## 6. Stack

FastAPI, LangGraph and LangChain, OpenAI GPT-4o, arXiv and Tavily tools, optional LangSmith tracing, and Next.js with Tailwind.

---

The original README (business case, deployment notes, demo scenarios) is in [`docs/ORIGINAL_README.md`](docs/ORIGINAL_README.md).
