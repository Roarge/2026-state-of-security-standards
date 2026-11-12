# Codebook

This codebook defines every code of the study and the rules the coders followed. It is version 0.3, fixed on 9 November 2026 before the coding began. The instructions the models received (`method/coder_instructions.md`) contain sections 1 to 4 and section 6. Section 5 was not given to the models.

## 1 What the coder receives

- The full text of one standard (or one part of it), with page markers
- A group of up to 20 attack steps, each with its description, technique codes, defensive need, who or what performed it (`performed_by`), whether it targeted an AI system (`ai_target`) and the autonomy level of its event
- This codebook

The coder judges each step against this one standard only.

## 2 Definitions

**Defensive need.** What a defender would have had to do to prevent the step, detect it, limit its effect or support the response, written as one sentence in the step record. The reference mitigations listed with it are the measures the taxonomy gives for the technique in general, and a measure that only they name is not part of the need. The coder judges clauses against this need, not against the technique name alone.

**Clause.** Any numbered or identifiable unit of the standard: clause, subclause, requirement, provision, control, annex item, table row. Its identifier is written as the standard writes it (for example `5.1-1`, `SR 1.5`, `PR.AA-01`, `Annex B.3`).

**Scope match** (`scope_match`). `yes` when the standard states that it covers the asset, component or activity the defensive need would protect (for example a standard for IoT devices and gateways, and a step against a gateway). `no` otherwise. It is decided from the scope statement, before looking for clauses, on the asset, component or activity the need protects, and not on a tool or actor merely used to carry the step out. A tool that the need itself protects, such as a provider's model whose misuse the need asks the provider to detect or stop, counts as an asset the need protects unless the step record shows that the attacker operates it. A standard does not cover an asset that its scope names only as the place where its subject, such as an algorithm or a data format, is used. An asset or tool that the attacker itself operates is outside scope, since the standard would govern only a comparable asset operated by a defender. An attacker that runs an open-weight model on its own systems operates that model and is its provider. An AI that a provider or a defender runs stays that party's when an attacker prompts, hijacks or drives it, also through an agent or framework that the attacker runs. Where a step's own record does not show who runs an AI that performs the step for an attacker or that an attacker uses to carry it out, the coder decides scope match on the asset, component or activity the defensive need protects, without guessing who runs that AI or inferring it from other steps. A record that names a model offered only as a provider's service shows that the provider runs it. A step is performed by an AI when `performed_by` is `ai_autonomous`, `ai_orchestrated`, `ai_malware` or `ai_unintended`. With `ai_assisted` a person performed it, and the AI is a tool that the person used. Where the step is performed by, or targets, an AI that the attacker does not operate, including an AI acting with no attacker behind it under rule 10, that AI is itself an asset the standard may cover: `scope_match = yes` when the standard covers that AI or the asset, component or activity the need protects, and, where that AI performs the step, clauses are judged against its action.

**Coverage** (`coverage`):

- `full`: one clause, or several clauses together, state measures that meet the whole defensive need, and none of those clauses depends on an assumption that the step as observed violated or is one that a decision rule limits to `partial`. Where several clauses are cited, `relationship` describes them together.
- `partial`: a clause meets part of the defensive need, or meets all of it in general terms without naming the relevant asset class or technique family, or meets it only under an assumption the step violated.
- `none`: no clause meets any part of the defensive need.

**Relationship** (`relationship`), the cited clauses, taken together, set against the defensive need in the set-theory terms of NIST IR 8477:

| Code | Meaning | IR 8477 term (need as focal element, clause as reference element) | Allowed coverage |
|---|---|---|---|
| `covers_all` | The clause requires everything the need asks for, and possibly more | equal, or subset of | full, or partial when an assumption is violated, the clause meets the need only in general terms (rule 2) or `vse_applicability` applies to it |
| `covers_part` | The clause requires some of what the need asks for, or, under rule 11, sets a measure on the AI that performs the step | superset of, or intersects with | partial |
| `unrelated` | The clause states no measure or effect that meets any part of the need | no relationship | none |

**Rationale type** (`rationale_type`), from NIST IR 8477: `syntactic` when the clause uses the same words as the need, `semantic` when it means the same thing in other words, `functional` when it produces the same effect by other means.

**Normative force** (`normative_force`): `requirement` (shall, must, or a numbered requirement in a requirements document), `recommendation` (should, may, or guidance text), `informative` (notes, examples, informative annexes). Recorded for the strongest clause cited. It does not change the coverage code.

**Assumption violated** (`assumption_violated`), for full or partial coverage, the assumption of the clause, or of the risk logic the clause depends on, that the observed step broke. Record an assumption only when the cited clause, or the risk logic it depends on, actually relies on it. Count an attacker-model assumption (rule 4) as broken only where the step record shows that the step broke it. Who performed the step, or the autonomy level of its event, does not show this on its own. A clause that only enables or recommends human oversight capability, without requiring approval before the action takes effect, does not rely on a person approving or reviewing the action. A part of the defensive need that no clause meets, for example a person approving an action before it takes effect, is recorded through `coverage` and `gap_class`, not through `assumption_violated`, and `human_review` is coded only when a cited clause itself relies on a person approving or reviewing the action:

| Code | The clause assumes |
|---|---|
| `none` | Nothing that the step broke |
| `attacker_capability` | Attackers lack the skill or knowledge the step needed, for example security levels or attack potential graded by expertise and knowledge of the target |
| `attacker_cost` | The effort, time, equipment or money an attack takes will deter or limit attackers |
| `target_choice` | The asset is too small, too obscure or of too little value to be chosen as a target, or protection is scaled to how attractive the asset is |
| `human_pace` | Attacks proceed at the pace of a person, so rate limits, lockout thresholds, monitoring or response tuned to human speed are enough. Where the clause gives the defender a period to act, such as a review, response or reporting window, code `time` instead |
| `deterrence` | Attackers can be identified, held responsible or deterred |
| `time` | Defenders have days or weeks (patch windows, review cycles, reporting clocks) where the step took hours |
| `boundary` | The component, actor or tool that the clause relies on governing lies inside the system the clause governs, where the step involved one from outside it, for example a device, extension, agent or hosted service that the governed system does not include |
| `supplier_trust` | Components or suppliers that pass assessment stay trustworthy |
| `human_review` | A person reviews or approves the action before it takes effect. Outside rule 10, the step breaks this only where the step record shows that the person whose review or approval the clause relies on was bypassed or misled, not where no approval was in place |

A clause rated `covers_all` with an assumption other than `none` is coded `partial`. Where cited clauses rely on different assumptions that the step broke, record the assumption of whichever of them meets most of the need and name the others in the rationale. Where they meet it about equally, record the one that best explains the shortfall.

**Gap class** (`gap_class`), for partial or none, the main reason the standard falls short. One value, the one that best explains the shortfall:

| Code | The standard falls short because |
|---|---|
| `scope` | The asset or technique class lies outside what the standard addresses, the standard only describes it and states no measure for it, the standard states no measure for a part of the need, or the standard sets the measure only for another asset (rules 6 and 11) |
| `attacker_model` | The protection depends on who the attacker is, why it attacks, what an attack costs it, which targets it chooses or how fast it moves, and the step broke that assumption |
| `tempo` | The standard addresses the activity, but the defender's time assumptions are slower than the observed attack or discovery |
| `technical_assumption` | The protection depends on assumptions about the system, such as deterministic software or human review, that the step violated |
| `infrastructure` | The protection depends on shared vulnerability infrastructure (CVE, NVD enrichment, KEV, bug bounties, disclosure channels) that the step record shows to be degraded |
| `accountability_supply_chain` | A clause meets part or all of the need but coverage is `partial`, and the step used a component, supplier or tool for which the standard assigns no party an obligation, or whose trust rests on an assessment that the step showed no longer held. Use this only where coverage is `partial`, since `gap_class` is not recorded for `full`. Where no clause applies and the component, supplier or tool lies outside the standard altogether, code `scope` |
| `vse_applicability` | A clause meets the need, but only through capacities a very small entity (25 employees or fewer) does not have, such as round-the-clock monitoring or dedicated security staff, and the step record shows that the defender was such an entity. Such a clause gives `partial`, also where it is rated `covers_all` |

Where `assumption_violated` is not `none`, the usual pairing is `attacker_capability`, `attacker_cost`, `target_choice`, `human_pace` and `deterrence` with `attacker_model`, `time` with `tempo`, `human_review` with `technical_assumption`, `supplier_trust` with `accountability_supply_chain`, and `boundary` with `scope`. The coder departs from it only with a reason in the rationale. Where no assumption is recorded, a part of the need that no clause meets gives `scope` rather than `technical_assumption`, except where rule 10 gives `attacker_model` to a clause that protects only against actors with hostile intent.

**Confidence** (`confidence`): `high` when the text is clear, `medium` when one reasonable reading supports the code, `low` when two codes are about equally defensible.

## 3 Decision rules

1. Code what the text requires, not what a competent implementer might infer from it.
2. A general clause that applies to all assets or all threats without naming the relevant class (for example "manage risks to systems") gives `partial` at most.
3. When the step depends on a time window, compare the clause's window with the observed tempo. If the step happened faster, code `assumption_violated = time` and `gap_class = tempo`.
4. Whoever performed the step, check every cited clause for attacker-model assumptions: skill or knowledge thresholds, effort or cost, target attractiveness, human pace and deterrence. If the clause depends on one that the step broke, code the assumption, and rate the pair partial where it would otherwise be full. For a step by an AI acting with no attacker behind it, rule 10 says which of these apply.
5. A clause on input validation, access control or supply chain in general covers a step with `ai_target = true` (prompt injection into an agent with tool permissions, a poisoned model or MCP server) partially at most unless it names AI or ML inputs, models, agents or their tools.
6. Informative text counts, with `normative_force = informative`, where it states or describes a measure, or the protective effect a mechanism produces when a defender applies it to an asset or activity. Text that only specifies a mechanism or states what it can achieve in general, such as an algorithm and the security properties it offers, states no measure. Text that says what a mechanism lets a party do, or lists the applications it is meant for, also states no measure, unless it says that a defender applies the mechanism to a named asset or activity, such as a device that checks the signature of each firmware update before installing it. A measure is an action a defender takes to prevent the step, detect it, limit its effect or support the response. A clause that only describes a threat, risk, weakness or attack, or only names an application, use case or deployment domain, without stating or describing a measure or its protective effect, meets no part of the defensive need: code `relationship = unrelated` and `coverage = none`. Relationship and coverage are decided by the measure or effect a clause states, at any normative force, not by topical or domain overlap alone.
7. When two coverage levels are about equally defensible, choose the **higher** level and set `confidence = low`.
8. Quotes are copied character for character from the text provided, at most 40 words each. Never paraphrase inside a quote field. If no clause meets any part of the need, leave `clauses` empty, even where the rationale names a clause under rule 6 or 11.
9. Judge each step on its own. Do not carry a judgement from one step to the next.
10. When the step was performed by an AI system acting with no attacker behind it (`performed_by = ai_unintended`), code it like any other step, with the AI as the actor. There is no attacker, so `attacker_capability`, `attacker_cost`, `target_choice` and `deterrence` do not apply. Judge whether a clause would have prevented the AI's action, detected it, limited its effect or supported the response. A clause that protects only against actors with hostile intent, or that relies on a person approving the action, meets the need partially at most. Code `human_review` when the clause relies on such approval and `boundary` when the clause relies on governing the agent or its tools and they lie outside the system it governs. Rules 3 and 4 apply to `time` and `human_pace` as for any other step. A clause that protects only against actors with hostile intent, meets part of the need and relies on no other assumption the step broke takes `relationship = covers_part`, `assumption_violated = none` and `gap_class = attacker_model`.
11. Scope match and coverage are recorded independently. A `scope_match = no` does not by itself force `coverage = none`, and `scope_match = yes` does not by itself give coverage. A clause raises coverage above `none` only when, implemented as written, the measure or effect it states would reach the asset, component or activity the defensive need protects, as a clause that applies to all assets within the standard's scope does (rule 2). A clause that sets a measure of the kind the need calls for, but only for another asset, component or environment, meets no part of the need: code `relationship = unrelated`, `coverage = none` and `gap_class = scope`, and name in the rationale the measure the standard sets elsewhere. A clause whose measure serves another defensive function also meets no part of the need: code `relationship = unrelated`, `coverage = none` and `gap_class = scope`. A measure serves the function the need calls for when, applied where the need asks for it, it would do part of what the need asks, whatever the clause calls it. As an exception to the conditions above, where the step record does not show that the attacker operates the AI that performs the step, a clause that sets a measure on that AI, its tools or its environment meets part of the need when, implemented as written, the measure would have prevented the AI's action, detected it or limited its effect, even where the need asks only for measures on other systems. A clause that meets part of the need only in this way is coded `covers_part` and does not count towards `full`. Where the asset, component or activity the need protects lies inside the system the clause governs and only the actor or tool involved lies outside it, a clause that relies on governing that actor or tool does not set its measure for another asset, component or environment: it gives `partial`, with `assumption_violated = boundary`. Confidence follows its definition, and a difference in scope is no reason on its own for `low`.

## 4 Output

One JSON record per step, following the `coverage` format in `method/output_format.json`. Cite at most five clauses. Where more than five meet parts of the need, cite the five that meet most of it and name the others in the rationale. The rationale (at most 60 words) says which clause meets which part of the need, or why none does, and names any assumption the step broke.

## 5 Illustrative examples

The clause texts below are invented for illustration and come from no real standard.

**Example 1.** *Step*: the attacker sprays default and guessed passwords at the web login of an internet-reachable SCADA gateway. *Performed by*: human. *Defensive need*: no default or shared credentials, strong authentication on remote interfaces, lockout or rate limiting, and segmentation that keeps the gateway off reachable networks.

*Invented clause 6.2*: "Devices shall not use universal default passwords. Interfaces reachable over a network shall limit failed authentication attempts."

Coding: `scope_match = yes`, `coverage = partial` (passwords and rate limiting are met, segmentation is not), `relationship = covers_part`, `rationale_type = syntactic`, `normative_force = requirement`, `assumption_violated = none`, `gap_class = scope` if segmentation is outside the standard's scope, `confidence = high`.

**Example 2.** *Step*: an AI system, with no operator involved after launch, identifies the same gateway during reconnaissance, researches its protocol and generates a credential list from public and victim data. *Performed by*: `ai_autonomous`. *Defensive need*: the same as in example 1, plus detection of reconnaissance and credential attempts at machine pace.

*Invented clause 4.1*: "The security level shall be selected to protect against intentional attacks by persons with generic skills and limited resources."

Coding: `scope_match = yes`, `coverage = partial`, `relationship = covers_all` (it asks for protection against intentional attacks), `assumption_violated = attacker_capability` (the protection is scaled to an attacker without system-specific knowledge, which the AI supplied), `gap_class = attacker_model`, `confidence = medium`.

## 6 Attacker-model profile of a standard

One profile per standard, filled by each coder after reading the whole document. Every `yes` carries up to three clause identifiers with verbatim quotes of at most 40 words, and the `attacker_model_summary` has at most 60 words.

| Field | Values |
|---|---|
| `attacker_classes_defined` | yes, no: the standard defines attacker classes, levels or profiles |
| `attacker_factors` | the factors it uses to grade attackers or attacks: skill, knowledge, resources, motivation, time, equipment, access, opportunity, none. A key or other secret that the standard requires or assumes to be kept from every attacker is not `knowledge`, but grading the difficulty of attacks by whether such a secret must first be obtained is `knowledge`. Where the standard grades attacks by the computational work they need, such as a security strength in bits or a time complexity, the factor is `resources`, not `time` |
| `target_attractiveness_logic` | yes, no: protection is tied to how valuable, attractive or exposed an asset is. A statement that an asset is valuable, attractive, exposed or an easy target gives `yes` only where the standard makes protection depend on that value, attractiveness or exposure |
| `time_assumptions` | each stated time window (for example patch within a period, report within 24 hours), with its quote. A word or phrase of timing or frequency that gives no length or interval of time, such as promptly, regularly, timely or in real time, does not by itself state a time window. A period that the standard sets for its own review, such as a review every five years, is a stated time window. Other text on how a standards body runs its work, such as how often its assembly meets or the dates set for national transposition, states no time window |
| `human_pace_assumptions` | yes, no: thresholds, lockouts or monitoring stated in terms that presume human use or human attackers |
| `automated_attacks_mentioned` | yes, no: automated, scripted, bot or machine-speed attacks are named. An attack also counts, even if the text does not call it automated, where the text names a distributed denial of service attack or describes an attack as flooding or overwhelming a system, a network, a service or their defences with requests, inputs or traffic. Naming a denial of service, or setting a limit, threshold or lockout, does not count on its own |
| `ai_attacker_mentioned` | yes, no: AI or machine learning used by attackers is named |
| `ai_target_mentioned` | yes, no: AI systems, models or agents as assets to protect are named |
| `attacker_model_summary` | at most 60 words in the coder's own words |
