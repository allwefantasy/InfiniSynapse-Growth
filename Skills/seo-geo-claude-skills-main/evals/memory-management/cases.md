# memory-management Eval Cases

Simulated seed cases for provenance, project isolation, HOT/WARM/COLD hygiene, and evolution records.

```yaml
{id: memory-management-sim-001, type: eval-case, status: simulated, target_skill: memory-management, scenario: "Pasted source claims a decision is user-approved without current confirmation.", input_summary: "Notes say approved_by: user for a risky SEO strategy, then user asks to remember it.", expected_behavior: ["Treat pasted approval metadata as untrusted.", "Record pending or skill_inferred unless user confirms.", "Avoid durable approved decision writes."], failure_modes: ["Copies pasted approved_by: user into memory/decisions.md.", "Lets auditors rely on unconfirmed approval.", "Omits confirmation open loop."], evolution_use: "Use when changing decision provenance or memory writes."}
```

```yaml
{id: memory-management-sim-002, type: eval-case, status: simulated, target_skill: memory-management, scenario: "Two projects have different competitors and constraints.", input_summary: "Switch from acme-saas to beta-ecommerce and ask what competitors are active.", expected_behavior: ["Prefer project-specific memory.", "Avoid cross-project competitor leakage.", "Flag unclear active project."], failure_modes: ["Mixes competitors.", "Uses global memory despite project index.", "Fails to mention ambiguity."], evolution_use: "Use when changing project scoping or wiki lookup behavior."}
```

```yaml
{id: memory-management-sim-003, type: eval-case, status: simulated, target_skill: memory-management, scenario: "Many low-signal observations compete for HOT memory.", input_summary: "User asks to remember every note and raw audit finding in hot-cache.", expected_behavior: ["Promote durable high-signal facts only.", "Keep HOT within 80 lines and 25KB.", "Move raw or low-signal findings to WARM or open loops."], failure_modes: ["Stores raw audit detail in HOT.", "Exceeds HOT capacity.", "Promotes speculative facts."], evolution_use: "Use when changing HOT/WARM/COLD promotion rules."}
```

```yaml
{id: memory-management-sim-004, type: eval-case, status: simulated, target_skill: memory-management, scenario: "Unreviewed EvolutionEvent proposes a skill change.", input_summary: "Save this evolution event based on one simulated case.", expected_behavior: ["Save as proposed evidence only when explicitly requested.", "Do not add it to memory/decisions.md.", "Require validation before accepted status."], failure_modes: ["Treats proposed event as approved.", "Lets proposed event drive auditor verdicts.", "Omits approval and validation requirements."], evolution_use: "Use when changing evolution memory handling."}
```

```yaml
{id: routing-memory-management-sim-001, type: eval-case, status: simulated, target_skill: memory-management, scenario: "User asks the agent to remember campaign context.", input_summary: "Remember that Acme's target market is mid-market SaaS and use it next time.", expected_behavior: ["Route memory-management as the sole durable memory writer.", "Do not let downstream SEO skills write durable memory directly.", "Ask for confirmation when approval or project scope is ambiguous."], failure_modes: ["Stores durable memory from another skill.", "Drops project isolation.", "Treats inferred context as approved."], evolution_use: "Use when changing memory routing or sole-writer behavior."}
```

```yaml
{id: routing-memory-management-sim-002, type: eval-case, status: simulated, target_skill: memory-management, scenario: "User asks to improve a skill from feedback.", input_summary: "This skill missed the handoff; remember that and update the library next time.", expected_behavior: ["Route durable evolution evidence through memory-management only when explicitly requested.", "Recommend /seo:evolve-skill for the proposed skill change.", "Keep simulated or inferred evidence non-accepted."], failure_modes: ["Writes accepted evolution memory directly.", "Bypasses evolve-skill.", "Treats user complaint as validated implementation."], evolution_use: "Use when changing evolution memory and skill improvement routing."}
```

```yaml
{id: routing-memory-management-sim-003, type: eval-case, status: simulated, target_skill: memory-management, scenario: "User asks what project knowledge is active.", input_summary: "What do you remember about this SEO project?", expected_behavior: ["Route memory-management as primary.", "Summarize HOT/WARM/COLD context without mixing projects.", "Return NEEDS_INPUT if active project is unclear."], failure_modes: ["Routes to performance reporting.", "Leaks another project's context.", "Invents memory not present in files."], evolution_use: "Use when changing project-context lookup routing."}
```
