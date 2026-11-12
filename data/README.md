# The tables and their columns

All tables are comma-separated text files in UTF-8 with a header row. Where one cell holds several values, they are separated by ` | `. Values printed `like this` are codes, and `method/codebook.md` defines each of them in full. An empty cell means that the value does not apply or is not known.

The tables join on three identifiers: `document_id` (a document of the corpus), `event_id` (a security event) and `step_id` (one step of an event, such as `B-002-S03` for the third step of event B-002).

The names of events and the descriptions of steps summarise what the cited public sources report. They are not findings of this study about the organisations named.

## documents.csv

One row for each of the 83 standards and guidance documents.

| Column | Meaning |
|---|---|
| `document_id` | Identifier of the document in this study |
| `title` | Title of the document |
| `edition` | Edition, version or publication details as the document states them |
| `date` | Publication date of the edition that was coded. Some documents give only a year or a month |
| `issuer` | Organisation that published it |
| `document_class` | `standard` for standards, technical specifications and normative government publications, `guidance` for guidance documents, 19 from public authorities or a public development bank and two from OWASP and MITRE |
| `draft` | `yes` for the three public drafts of an edition that is not yet in force |
| `catalogue` | `yes` for the twelve documents that define how vulnerabilities, weaknesses and attack patterns are listed, scored and exchanged, among them formats for lists of the components of a piece of software and taxonomies of attacks on AI systems, and that set no security requirements for a system or an organisation beyond the format itself |
| `document_type` | Finer type: `standard` (a standard from a standards body), `technical_specification` (a technical specification from a standards body or an industry alliance), `technical_report` (a technical report from a standards body), `government_normative` (a normative technical publication from a government body), `authority_guidance` (guidance from a public authority or a public development bank), `industry_guidance` (guidance from an industry or community body), `directive` (a binding order from an authority to the bodies it oversees), `threat_report` (a report on current threats from an authority that tells its readers what to do), `framework_release_note` (a release note of a security framework), `other` (another kind of text from an authority) |
| `layers` | The layers of smart city infrastructure the document addresses: field devices, networks and protocols, platforms and data, applications and services, operations and governance |
| `text_obtained_as` | `publisher_text` when the text came from the publisher's own file, `ocr` when it was read from page images by optical character recognition, `machine_translation` when the coded text is a machine translation of another language edition |
| `coded_on_12_november` | `yes` for the seven standards whose full text was obtained on 12 November 2026, after the first results for the other 76 documents were known |

## events.csv

One row for each of the 68 security events that have attack steps.

| Column | Meaning |
|---|---|
| `event_id` | Identifier of the event |
| `name` | Short name of the event |
| `event_type` | `incident` for one attack or compromise against a named or described victim, `campaign` for a series of related attacks by one actor, with one set of tools or by one AI system, `vulnerability` for a weakness in a product that was made public with a catalogue number (CVE) or a supplier's advisory |
| `control_event` | `yes` for the three events with no reported AI involvement, kept for comparison |
| `date_occurred` | When the event began, as far as the sources say. Empty where they do not say |
| `date_disclosed` | When it became public. It can precede `date_occurred` where a weakness was made public before it was used |
| `autonomy_level` | 0 no AI system took part in carrying out the event, 1 people attack with AI help, 2 an AI system carries out most steps under human approval, 3 an AI system chooses and carries out the steps, `unclear` when the sources do not settle it |
| `ai_roles` | The parts an AI system had in the event: `attacker_assisted` (a person carried out the attack and an AI system helped), `attacker_orchestrated` (an AI system carried out most steps while people set the goal and approved), `attacker_autonomous` (an AI system chose and carried out the steps with no person directing it after the start), `autonomous_malware` (malicious software that calls an AI model while it runs), `discoverer` (an AI system found the weakness, for attackers or for defenders), `target` (an AI model, an AI agent, its tools or an AI service was the thing attacked), `unintended_actor` (an AI agent caused harm with no attacker behind it). Empty for the three control events |
| `sectors` | Sectors affected, as the sources name them |
| `evidence_grade` | A letter and a digit on the scale known as the Admiralty code. The letter grades how reliable the source is, from A (completely reliable) to F (cannot be judged). The digit grades how credible the account is, from 1 (confirmed by other sources) to 6 (cannot be judged) |
| `primary_sources` | Links to accounts by parties with direct knowledge, with publisher and date |
| `secondary_sources` | Links to reporting about the event |
| `number_of_steps` | Number of attack steps taken from the event |

## attack_steps.csv

One row for each of the 524 attack steps.

| Column | Meaning |
|---|---|
| `step_id`, `event_id`, `order` | The step, its event and its place in the course of the event. Event C-001 is the exception: its 14 steps that were added later, numbered 9 to 22, follow the eight earlier steps by number and not by the calendar, so for these steps the number does not say when in the event the step took place |
| `description` | What the attacker did, in one or two sentences |
| `defensive_need` | What a defender would have had to do to prevent the step, detect it, limit its effect or respond to it. The documents are judged against this sentence |
| `techniques` | Identifiers of the technique in MITRE ATT&CK (starting with `T`), MITRE ATLAS (starting with `AML.`) or the OWASP Top 10 for Agentic Applications (starting with `ASI`). The first is the main one |
| `reference_mitigations` | The countermeasures that the technique catalogue lists for the technique. Empty where the catalogue lists none |
| `performed_by` | Who carried out the step: `human`, `ai_assisted` (a person with AI help), `ai_orchestrated` (an AI system under human approval), `ai_autonomous` (an AI system that chose and carried out the step), `ai_malware` (malicious software that calls an AI model while it runs), `ai_unintended` (an AI system acting with no attacker behind it) |
| `ai_target` | `true` when the step attacks an AI system, model or agent, or its tools |
| `autonomy_level` | The level of the step's event |
| `source_url` | The public source the step rests on |
| `check_still_asked_for_revision` | `yes` when the last check of the step by a second model still asked for a change, after a revision in 75 cases and after a repeated check in one. `no` covers both the steps the check accepted and the steps that were kept unchanged against the check's objection, with a recorded reason. Of the 22 steps of event C-001, 17 are of the second kind, two were accepted and three carry `yes` |
| `source_note` | For the 22 steps of event C-001, the kind of source that supports the core of the step: `Supported by an independent investigation` for 11 steps and `Supported by the affected party's own account` for the other 11, where the affected party is the organisation whose systems were broken into. Empty for all other events |
| `text_shortened_for_publication` | `yes` when a literal secret, a piece of attack text, a path or a name in the description or the defensive need was replaced by a description of it for this public table. The coders saw the original |

## coverage.csv

One row for each of the 43,492 pairs of a document and a step, with the final code.

| Column | Meaning |
|---|---|
| `document_id`, `step_id` | The pair |
| `coverage` | `full` when the cited clauses meet the whole defensive need, `partial` when they meet part of it, or all of it only in general terms or under an assumption the step broke, `none` when no clause meets any part |
| `scope_match` | `yes` when the document states that it covers the asset, component or activity the defence would protect |
| `gap_class` | For `partial` and `none`, the main reason the document falls short: `scope`, `attacker_model`, `tempo`, `technical_assumption`, `infrastructure`, `accountability_supply_chain` or `vse_applicability`. `not_applicable` for `full`, with one exception: one pair with coverage `full` carries `scope`, as the coder recorded it |
| `assumption_violated` | What the cited clause takes for granted and the step broke: `attacker_capability`, `attacker_cost`, `target_choice`, `human_pace`, `deterrence`, `time`, `boundary`, `supplier_trust`, `human_review`, or `none` |
| `normative_force` | Of the strongest clause cited: `requirement`, `recommendation` or `informative`. `not_applicable` where coverage is `none` |
| `relationship` | The cited clauses set against the need: `covers_all`, `covers_part` or `unrelated` |
| `rationale_type` | How clause and need correspond: `syntactic` (same words), `semantic` (same meaning in other words) or `functional` (same effect by other means). `not_applicable` where coverage is `none` |
| `confidence` | The coder's own confidence: `high`, `medium`, or `low` when two codes were about equally defensible |
| `settled_by` | How the final code came about: `coders_agreed` (the two coders gave the same coverage, scope and gap class, and coder B's answer is final), `adjudicator` (they differed and a third request decided), `adjudicator_second_attempt` (the adjudicator's request was declined and was decided by a second model), `majority_of_three` (three models coded the pair and two agreed), `coder_a_only` or `coder_b_only` (one coder's answer is missing) |
| `clauses` | Identifiers of the clauses the code rests on, as the document writes them |

## clause_evidence.csv

One row for each clause cited by a final code.

| Column | Meaning |
|---|---|
| `document_id`, `step_id` | The pair |
| `clause_id` | The clause, as the document identifies it |
| `quote` | The words the coder copied from the clause, cut to the first 25 words. Empty where the quote is withheld |
| `quote_cut` | `no` when the quote is given whole, `yes` when the coder's quote was longer and was cut, `withheld` when the quote is not published because, together with other quotes of the same document, it would reproduce a passage of more than 25 words |

Every quote was checked by program against the text of the document before the code was accepted. One document, IEC 62443-3-3, was coded from a machine translation, so its quotes are not the wording of the standard.

## full_code_functions.csv

For each pair with full coverage, what two further models judged the cited clauses to do. One row for each clause and model. For six pairs only one of the two models gave a valid answer.

| Column | Meaning |
|---|---|
| `document_id`, `step_id` | The pair |
| `model` | The model that judged: Kimi K3 or GLM-5.3 |
| `clause_id` | The clause |
| `function` | What the clause does against the step: `prevent`, `detect`, `limit` (reduce the effect), `respond` (support the response) or `none` |
| `stops_step` | `yes` when the model judged that the clauses of this code, taken together, would have stopped the step |

## attacker_profiles.csv

One row for each document, with what it says about the attacker.

| Column | Meaning |
|---|---|
| `document_id` | The document |
| `attacker_classes_defined` | `yes` when the document defines classes, levels or profiles of attackers |
| `target_attractiveness_logic` | `yes` when it scales protection to how attractive or exposed an asset is |
| `human_pace_assumptions` | `yes` when it sets thresholds or monitoring that presume an attacker at human speed |
| `automated_attacks_mentioned` | `yes` when it names automated or machine-speed attacks |
| `ai_attacker_mentioned` | `yes` when it names AI used by attackers |
| `ai_target_mentioned` | `yes` when it names AI systems as something to protect |
| `attacker_factors` | The factors by which it grades attackers, such as skill, resources, motivation and time, or `none` |
| `profiled` | `no` for the one document that has no final profile, whose other cells are empty |

## agreement.csv

How far the two coders agreed, before any disagreement was settled.

| Column | Meaning |
|---|---|
| `coder_set` | `all_pairs_with_two_answers` for every pair that two coders answered, `both_answers_from_the_two_main_models` for the pairs where neither answer had to come from a replacement model |
| `autonomy_levels` | `all`, or the events at levels `0 and 1` or `2 and 3` |
| `field` | The answer compared: `coverage`, `scope_match` or `gap_class` |
| `pairs` | Number of pairs compared. One long document was coded in two parts, which count separately here. For `gap_class` only the pairs that both coders rated partial or none are compared |
| `krippendorff_alpha` | Krippendorff's alpha: 1 for complete agreement, 0 for the agreement that chance alone would give |
| `ci95_low`, `ci95_high` | The 95 per cent interval of alpha, estimated by recomputing alpha on 1,000 random redraws of the pairs |
| `percent_agreement` | Share of pairs with the same answer |

## sensitivity.csv

The main results recomputed under one changed choice at a time. The row `main` holds the results as reported.

| Column | Meaning |
|---|---|
| `variation_id`, `variation` | The changed choice, explained below |
| `pairs`, `documents`, `steps`, `events` | What remains in the analysis under this choice |
| `pairs_full_percent`, `pairs_partial_percent`, `pairs_none_percent` | Coverage of the pairs |
| `in_scope_pairs` and the three columns after it | The same for pairs in scope |
| `steps_covered_in_full`, `steps_covered_in_part`, `steps_not_covered` | Steps by the best coverage any document gives them |
| `steps_covered_in_full_percent` | The headline figure |
| `steps_covered_in_full_percent_levels_0_and_1`, `steps_covered_in_full_percent_levels_2_and_3` | The headline figure for the two groups of autonomy levels. One of the two is empty in the row that keeps a single group |
| `pairs_with_gap_class_...` | Number of pairs in each gap class other than scope |

What each variation leaves out or changes, and why it is worth testing:

| Variation | Meaning |
|---|---|
| S1 | Leaves out the four events that are known only from reports by others, such as news articles, with no account from a party that had direct knowledge. A second-hand account is more likely to be wrong about what the attacker did |
| S2 | Leaves out the twelve catalogue documents. Counting a list of attacks as protection against them could make the documents look better than they are |
| S3 | Keeps the 62 standards and leaves out the 21 guidance documents. Guidance is advice, and the question the study was given asks what standards document |
| S4a | Uses the answers of coder A alone in place of the final codes. Coder A gave full coverage far more often than coder B, and the result should not depend on which of the two is believed |
| S4b | Uses the answers of coder B alone. This coder was the stricter of the two, and its answer became the final code wherever the two agreed |
| S5 | Leaves out the three drafts. A draft can still change, and nobody is yet asked to follow it |
| S6 | Leaves out the seven standards coded on 12 November 2026, after the first results were known. This row shows what the results are without them |
| S7 | Leaves out the two events that the search missed and that entered only because they stood on an earlier list of known events, which was used to test how complete the search was. Events added from such a list may reflect what the researcher already had in mind |
| S8 | Keeps only the 337 steps from the events in which an AI system carried out most or all of the steps. These events are the centre of the study, and their result should also be seen on its own |
| S9 | Leaves out the 22 events for which the only account of what the AI system did comes from the company that built it. Nobody outside has confirmed these accounts |
| S10 | Leaves out the seven events whose record in the study's list of events was not read a second time by an independent checker. A record that nobody checked is more likely to hold an error |
| S11 | Leaves out the pairs in which one coder's answer came from a repeated request after the model had declined the first. Most of these repeats ran on the same model as the other coder, so the two answers are less independent |
| S12 | Keeps only the pairs for which both coders' answers were obtained in the first of the two technical ways in which the same requests were sent to the models, which covers 18 documents. This row checks whether the way of sending mattered. With so few documents it is not an estimate of coverage |
| X1 | Leaves out the pairs that a second adjudicator model decided after the first had declined the request. A different adjudicator, asked with an added statement of the study's defensive purpose, may judge differently |
| X2 | Leaves out the pairs whose final code rests on one of the two open-weight models that stepped in where the main models had declined. A replacement model may not judge as the main coders do |
| X3 | Leaves out the pairs that were settled by taking the answer that two of three coders shared. This rule was added during the study and decides by counting answers, not by a fresh reading of the document |
| X4 | Leaves out the pairs with an answer that was accepted only after a check had been loosened, either the check that every quote stands word for word in the document or the limit on the length of quotes and reasons |
| X5 | Leaves out the two standards that the coders did not read in the publisher's own text, one read from page images and one in a machine translation. Errors in such a text can lead to wrong codes |

## time_to_coverage.csv

For each attack technique in the steps that its catalogue listed from 2020 onwards, the wait until a corpus document covers it. One row for each technique and definition.

| Column | Meaning |
|---|---|
| `definition` | `full_coverage_after_listing`: the first document, published on or after the technique was listed, that covers a step using the technique in full. `full_coverage_after_listing_that_stops_the_step`: the same, and the clauses were judged to stop the step. `full_coverage_after_listing_by_a_requirement`: the same as the first, and the clause is a requirement. `original_definition`: full or partial coverage by any current edition, whenever published |
| `technique`, `name` | Identifier and name of the technique |
| `taxonomy` | The catalogue and its version |
| `family` | `ATT&CK`, or `ATLAS and OWASP Agentic` for techniques against AI systems |
| `technique_listed_on` | The date the catalogue first listed the technique |
| `first_covering_document_id` | The first document that covers it under this definition, empty when none does |
| `covered_on` | Publication date of that document. Where a document gives only a year or a month, its first day is used |
| `days` | Days from listing to coverage, or to 31 October 2026 when no document covers it. Under `original_definition` it is 0 when the covering document is older than the technique |
| `covered` | 1 when a document covers it, 0 when it was still waiting on 31 October 2026 |

The three drafts never count as covering documents.
