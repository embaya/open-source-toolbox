# Universal Toolbox Prompt

Use the following instruction in a new ChatGPT, Claude, Gemini, Codex or other AI conversation after giving the model access to this repository.

---

I maintain a personal Open Source Toolbox in this repository. It contains open-source projects I have deliberately selected as potentially reusable components for my personal projects.

**Before recommending that I build a capability from scratch, inspect this toolbox.**

For the project/problem I give you:

1. Translate my requirement into technical capabilities.
2. Read `AI_CONTEXT.md`, search the relevant `catalog/*.jsonl` files, then inspect `TOP_PICKS.md` and `STACKS.md` when relevant.
3. Shortlist the strongest toolbox candidates.
4. For each candidate classify the intended use as **DEPLOY**, **INTEGRATE**, **EXTEND**, **INSPIRE**, or **LEARN**.
5. Compare overlapping solutions rather than listing them blindly.
6. Evaluate fit, maturity/activity, license, deployment/self-hosting, integration/API model, operational complexity, extensibility and security.
7. Recommend the minimal combination that covers the requirement.
8. Mark every architecture component as one of:
   - `TOOLBOX` — comes from my catalog
   - `EXTERNAL` — not currently in the catalog
   - `CUSTOM` — should be built specifically
9. Only recommend building a major component from scratch after explaining why existing toolbox candidates are inadequate.
10. If the catalog metadata is insufficient to make a decision, inspect the candidate repository itself before concluding.

Do not treat GitHub stars as the primary decision criterion. Optimize for practical reuse and architecture fit.

My project/request follows:

[PASTE PROJECT HERE]

---
