# Business case: ReplySight

**Research-backed draft replies to customer complaints, with citations.**

## Who buys this

The buyer is a customer-support director at a company with a busy support queue. The users are support agents, especially new ones, who need a good first draft for a difficult complaint.

## The problem and what it costs

Agents lose time finding the right words and best practice for each complaint. There is good evidence that AI assistance helps here. A study of **5,179 customer-support agents** found that a generative AI assistant raised issues resolved per hour by **14% on average, and by 34% for novice and low-skilled workers**, with little effect on the most experienced ([Brynjolfsson, Li and Raymond, NBER w31161](https://www.nber.org/papers/w31161); published in the Quarterly Journal of Economics, 2025).

## How the repo solves it

| Need | What in the repo does it |
|---|---|
| Research | A LangGraph workflow in which a GPT-4o agent searches arXiv for service-recovery research and the web (Tavily) for real examples |
| Draft | A compose step writes an empathetic reply with citations, looping back for more research if needed (8 nodes, 10 edges, from the live `/workflow/graph`) |
| Evaluate | An `evals/` folder for checking reply quality |
| Run | FastAPI backend and a web UI. Without keys the stack still starts and reports what is missing. |

## Use-case scenarios

All of these organisations are fictional.

1. **An airline's complaints team** gets a cited draft for a delayed-baggage complaint and edits it before sending.
2. **A subscription box company** uses the drafts to train new agents on service-recovery language.
3. **A software company's support desk** speeds up replies to angry billing complaints.

## ROI: a worked model (illustrative)

These figures are **illustrative assumptions** unless a source is linked.

| Input | Value | Basis |
|---|---|---|
| Support agents using it | 20 | Assumption |
| Agent loaded cost a year | US$55,000 | Assumption |
| Productivity gain | 5% | Assumption, deliberately well below the study's 14% average, because this tool covers only complaint replies |

Value of time freed: 20 × $55,000 × 5% = **US$55,000 a year**, minus model and search API costs. The NBER study is the evidence that gains are possible. It is not a forecast for this tool.

## Path to production

1. Pilot with a group of agents and a control group, and measure handle time and customer satisfaction.
2. Ground replies in your own policies and help-centre content, not only arXiv and the web.
3. Keep agents in control: drafts only, never auto-send.

## Risks and limits

- Citing research papers in a customer reply may feel odd to customers, so the citations may be for the agent rather than the customer.
- Model errors in policy (refunds, compensation) can cost money, so policy grounding matters.
- The screenshots were taken without API keys, so reply quality is not shown.

**Case strength:** **Good.** The evidence for AI help in customer support is strong and the use is narrow. Quality still has to be proved on real tickets.

## Sources

- Brynjolfsson, E., Li, D. and Raymond, L., Generative AI at Work, NBER Working Paper 31161: https://www.nber.org/papers/w31161
