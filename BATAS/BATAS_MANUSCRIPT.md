# Bounding Authority, Not Detecting Intent: A Zero Trust Architecture for Agentic AI in an Indonesian Regional Development Bank (the Bank Jatim Case)

**Article type:** Research article  
**Target Journal:** *Telematika: Jurnal Informatika dan Teknologi Informasi* (UPN "Veteran" Yogyakarta; e-ISSN 2460-9021)  
**Authors:** Indri Anjar Kartika Sari$^{a,b,c,*}$; [co-authors to confirm]  
$^a$ Program Studi S1 Cyber Security, IDS Digital College (STMIK Indo Daya Suvana), Indonesia  
$^b$ Magister Ilmu Komunikasi, UPN "Veteran" Jawa Timur, Indonesia  
$^c$ AI Engineering Program (JCAI), Purwadhika Digital Technology School, Indonesia  
$^*$ Corresponding author: `indri.cs2026@ids.ac.id`  

---

## Abstract
Indonesian banks are moving from chat assistants to agentic AI that reads documents, calls internal tools and initiates transactions. Because prompt injection cannot yet be reliably detected, defences that depend on recognising malicious intent will eventually fail. This study argues that banking agents should instead be secured by bounding their authority: an injected instruction may reach the model but must not reach money or personal data. We design BATAS (Bounded Agent Trust and Authority Scoping), a Zero Trust architecture based on NIST SP 800-207 and the OWASP Top 10 for Agentic Applications 2026, and instantiate it for Bank Jatim, a regional development bank that holds local-government treasury accounts, runs a branchless agent network and parents five other regional banks. In a reproducible synthetic testbed, BATAS is compared with prompt-level and detection-based defences under adaptive Indonesian- and English-language attacks, measuring attack success by forbidden state change, task utility, human approval load and latency. [Results: one sentence with the main effect sizes and 95% confidence intervals.] Each control is mapped to PADK OJK 1/2026, POJK 11/POJK.03/2022 and OJK's banking AI governance guideline, giving regional banks a concrete list of preconditions before agents receive transactional authority.

**Keywords:** agentic AI; prompt injection; Zero Trust architecture; regional development bank; AI governance

---

## Highlights
- Banking-agent security reframed from detecting intent to bounding authority
- Regional development banks add treasury, outlet and banking-group trust chains
- BATAS binds each agent action to a task token, a policy check and an OJK rule
- Adaptive Indonesian-language attacks tested in a reproducible banking testbed
- [Fifth highlight: the main quantitative finding, after the experiment is run.]

---

## 1. Introduction

### 1.1 From assistants to agents
AI is now routine in Indonesian banking. OJK reports that, in some implementations, AI already handles about 35–40% of customer-service interactions, and PERBANAS–IBM data cited by OJK put sector adoption at 57.9% in the first quarter of 2026 [1]. The next step is agentic AI: systems that plan over several steps, retrieve documents, call internal tools and act with delegated credentials. The security question changes accordingly. A chatbot that is manipulated says something wrong; an agent that is manipulated does something wrong.

Prompt injection is the mechanism. Because a language model processes instructions and data in the same channel, text inside an email, a PDF or a web page can redirect the agent's goal. The OWASP Top 10 for Agentic Applications 2026 lists this as ASI01, Agent Goal Hijack, and describes it as the agentic counterpart of prompt injection with action consequences [2]. Systematic evaluations show that published detection-based defences perform worse under adaptive attacks than originally reported [3], and agent benchmarks such as AgentDojo confirm that neither attacks nor defences are yet reliable [4].

### 1.2 The argument of this paper
If injection cannot be reliably detected, a bank should not stake customer funds on detecting it. We therefore reframe the objective: bound the authority of the agent so that a successful injection has nowhere harmful to go. This follows the design-pattern line of work that constrains what an agent may do after it has read untrusted content [5], [6], and it maps naturally onto the Zero Trust principle that no subject, human or machine, holds standing trust [7].

### 1.3 Why a regional development bank
Most agentic-security work assumes a generic enterprise or a large commercial bank. Indonesian regional development banks (Bank Pembangunan Daerah, BPD) differ in three ways that matter for agent authority, and Bank Jatim exhibits all three:
1. **Public treasury.** Provincial and district governments are majority shareholders and place their general treasury accounts (RKUD) with the bank. An agent that touches treasury disbursement acts on public money.
2. **Branchless agent network.** Thousands of Agen Jatim outlets transact on behalf of customers, adding a human intermediary whose messages an AI agent may read.
3. **Banking group (KUB).** Since 2025 Bank Jatim parents five other BPDs. Shared services and integrated systems extend any agent's trust boundary across legally separate banks.

These features are not just context; they are the variables our threat model and architecture are built around.

Figure 1 places Bank Jatim between its retail customers and the three trust chains (highlighted) that national commercial banks do not carry; Sections 4 and 5 treat each chain as a separate authority boundary.

### 1.4 Research questions
- **RQ1.** Which authority paths in a BPD's workflows can an injected instruction exploit once an agent has tool access, and which of these are specific to treasury, agent-network and banking-group settings?
- **RQ2.** How can Zero Trust principles be operationalised as authority-bounding controls for banking agents, and how do they map to Indonesian regulatory obligations?
- **RQ3.** Under adaptive Indonesian-language attacks, how do authority-bounding controls compare with prompt-level detection on attack success, task utility and latency?

### 1.5 Contributions
1. A threat model of agent authority paths for an Indonesian BPD, derived from public disclosures of Bank Jatim and the OWASP agentic taxonomy (Section 4).
2. BATAS, an architecture that binds each agent action to a short-lived capability, a deterministic policy check and, above defined thresholds, a human or dual-control approval (Section 5).
3. An open, reproducible testbed and Indonesian-language adaptive attack suite for BPD-style workflows (Section 6).
4. A control-to-obligation mapping against PADK OJK 1/2026, POJK 11/POJK.03/2022 and OJK's banking AI governance guideline, intended for supervisors and internal auditors (Section 5.6).

---

## 2. Case context: Bank Jatim and its regulatory setting
Bank Jatim is a publicly listed BPD in which local governments hold the controlling stake, with a fast-growing digital channel and, since 2025, a group of five subsidiary BPDs. We use only public disclosures; we found no public report that Bank Jatim has deployed agentic AI, so this study is prospective: it specifies the controls a BPD should have before granting agents transactional authority.

### 2.1 Profile (public disclosures, FY2025 unless noted)
Table 1. Bank Jatim profile from public disclosures.

| Attribute | Value | Ref. |
| :--- | :--- | :--- |
| Legal entity | PT Bank Pembangunan Daerah Jawa Timur Tbk (IDX: BJTM) | [8] |
| Series A shareholders | East Java provincial government and district/city governments, 79.48% | [9] |
| Total assets | Rp105.8 trillion (bank only); Rp168.855 trillion (consolidated) | [8], [11] |
| Deposit customers | 10,915,749 | [10], [11] |
| JConnect Mobile | 993,972 users; Rp65.77 trillion transactions | [11] |
| JConnect IB Corporate | 11,199 users; Rp23.36 trillion transactions | [11] |
| JConnect, H1 2026 | 1.09 million users; target 2 million by December 2026 | [12], [13] |
| Branchless agents (Agen Jatim) | 14,842 | [11], [14] |
| Banking group (KUB) | Parent of Bank NTB Syariah, Bank Banten, Bank Lampung, Bank Sultra, Bank NTT | [8] |
| Existing AI use | AI-based transaction anomaly detection in the new JConnect | [15] |

**Treasury role:** Bank Jatim manages about 419,053 civil-servant payroll accounts in East Java, with salary flows of roughly Rp1.5 trillion a month, and a Bank Jatim commissioner who is also the provincial secretary describes payroll and RKUD funds as captive low-cost deposits for regional banks [16]. The number of RKUD accounts held is not publicly disclosed in the sources reviewed.

**Group integration:** KUB members are expected to gain IT support from the parent; Bank Banten cites strengthened IT among the KUB benefits [17]. Shared IT is exactly where an agent's trust boundary could silently cross legal entities.

### 2.2 Incident history relevant to the threat model
In October 2021 a seller on a hacker forum claimed 378 GB of Bank Jatim data. The bank stated that a supporting application server, not the core banking system, had been breached, and commissioned independent forensics [18], [19]. We cite this only to motivate one design assumption: peripheral applications, not the core, are the realistic entry point, and agents will mostly live in that periphery.

### 2.3 Regulatory setting
Table 2. Indonesian instruments relevant to banking agents.

| Instrument | Status | Relevance to agents |
| :--- | :--- | :--- |
| POJK 11/POJK.03/2022 on IT implementation by commercial banks [20] | Binding regulation | IT governance, risk management, data, outsourcing |
| PADK OJK 1/2026 [21] | Implementing rule of POJK 11/2022; set 23 Jan 2026, effective 1 Mar 2026; revokes SEOJK 21/SEOJK.03/2017 | Detailed IT risk management, information security, IT service providers, architecture, personal data |
| SEOJK 29/SEOJK.03/2022 on cyber resilience and security [22] | Binding circular | Cyber risk identification, protection, detection, response |
| Tata Kelola Kecerdasan Artifisial Perbankan Indonesia (Apr 2025) [23] | Guideline; a minimum reference, not legally binding | Responsible AI across the AI life cycle; accountability, human oversight, reliability |
| UU 27/2022 on Personal Data Protection [24] | Law | Lawful processing and breach obligations for customer data |

---

## 3. Related work and research gap
The literature has moved from showing that injection works, to measuring it in agents, to designing systems that tolerate it. What it lacks is an account of how institutional structure, such as public treasury and banking groups, shapes the authority an agent can abuse.

### 3.1 Prompt injection and its evaluation
Perez and Ribeiro [25] demonstrated direct injection; Greshake et al. [26] showed that indirect injection through retrieved content compromises LLM-integrated applications. BIPIA found all 25 evaluated models susceptible to indirect injection, with more capable models often more vulnerable [27]. Jia et al. [3] re-evaluated published defences against adaptive attacks and found them weaker than claimed, which is why this paper does not rely on detection as a primary control.

### 3.2 Agent benchmarks and financial agents
AgentDojo provides stateful environments in which injection success is judged by the effect on the environment, not by model text [4]. We adopt that principle: an attack succeeds only if a forbidden state change occurs. FinVault applies the same principle to financial agents, with 31 regulation-driven sandbox scenarios, and finds that existing defences still allow attack success rates of up to 50% on state-of-the-art models [28].

### 3.3 Design-level defences
Beurer-Kellner et al. [5] propose design patterns, such as plan-then-execute and action selectors, that give provable resistance by limiting what untrusted content can influence. CaMeL separates control flow from untrusted data and enforces capabilities at the interpreter level; in AgentDojo it completes 77% of tasks with provable security against 84% for an undefended agent [6]. The price of design-level security is utility, not detection accuracy. BATAS applies the same logic but anchors capabilities in banking authority: account, amount, counterparty, legal entity.

### 3.4 Zero Trust and governance frameworks
NIST SP 800-207 defines Zero Trust as per-request, policy-driven access with no implicit trust from network location [7]. OWASP's agentic list supplies the risk vocabulary (ASI01–ASI10). Management-level reviews such as TRiSM for agentic multi-agent systems [29] and defence-in-depth proposals [30] sit above the technical layer but do not specify authority bounds for regulated payments.

### 3.5 Gap
Table 3. Research strands and the gap they leave for an Indonesian BPD.

| Strand | What it gives | What it leaves open for an Indonesian BPD |
| :--- | :--- | :--- |
| Injection benchmarks | Attack success under controlled tasks | Banking authority (amount, counterparty, treasury) is not modelled |
| Design patterns, capability systems | Provable limits on untrusted influence | No mapping to banking roles, dual control or regulators |
| Zero Trust, governance frameworks | Principles and management controls | No runtime enforcement detail for agents |
| Indonesian AI governance | Principles across the AI life cycle | Non-binding; no technical controls for agents |
| Indonesian-language injection studies | Model-level risk profiles [31] | No tool-using agents, no state-change outcome |

This paper sits at the intersection: authority-bounding controls, specified for a BPD, evaluated by state change, and mapped to Indonesian obligations.

---

## 4. Threat model
We assume the attacker can make an agent read text, but cannot alter the policy engine, the tool gateway or the core banking system. Under that assumption, harm happens only along an authority path: a chain from untrusted text, through an agent's reasoning, to a tool call that changes money, data or access.

Figure 2 shows that every path from an adversary (dashed) to an asset must pass through a tool call that crosses the trust boundary; that crossing, not the prompt, is where control is placed.

### 4.1 Adversaries, assets and trust assumptions
- **Adversaries.** (A1) an external party who can place content the agent reads: complaint emails, uploaded documents, merchant descriptions, chat messages; (A2) a compromised or coerced Agen Jatim outlet; (A3) a malicious or compromised insider at a KUB member bank; (A4) a compromised tool or MCP server in the supply chain.
- **Assets.** Customer funds; local-government treasury funds (RKUD); personal data of about 10.9 million depositors; credentials; integrity of audit records.
- **Trusted computing base.** Policy engine, capability issuer, tool gateway, audit store, core banking.
- **Untrusted.** The language model after it has read any untrusted content; any text originating outside the bank; any message crossing a KUB entity boundary.
- **Out of scope.** Compromise of the model provider; physical attacks; attacks on core banking that do not involve an agent.

### 4.2 Authority paths specific to a BPD
Table 4. Authority paths AP1–AP7 and their OWASP agentic risk categories.

| ID | Workflow (hypothetical, BPD-typical) | Untrusted input | Harmful action | OWASP agentic |
| :--- | :--- | :--- | :--- | :--- |
| AP1 | Customer-service agent resolves JConnect complaints | Complaint email or chat with embedded instruction | Reversal or refund to an attacker account; disclosure of another customer's data | ASI01, ASI02 |
| AP2 | Treasury-operations agent prepares local-government disbursements | Disbursement order (SP2D) or attachment from a district finance office | Changed beneficiary or amount on a public-fund transfer | ASI01, ASI03 |
| AP3 | Agent-network support agent handles Agen Jatim requests | Message from an outlet | Raised transaction limit, account opening without KYC | ASI09, ASI03 |
| AP4 | Group shared-service agent answers queries across KUB members | Query or document from another legal entity | Cross-entity data access beyond the requesting bank's mandate | ASI03, ASI07 |
| AP5 | Any agent with persistent memory | Earlier poisoned interaction | Instruction persists across sessions and customers | ASI06 |
| AP6 | Any agent using third-party tools | Tool description or response | Hidden exfiltration or privilege escalation through the tool | ASI04, ASI02 |
| AP7 | Multi-agent hand-off | Output of a compromised agent | Error or malicious goal cascades to downstream agents | ASI07, ASI08 |

### 4.3 Indonesian-language attack patterns (hypotheses to test)
We test, rather than assume, three framings that Indonesian bureaucratic and banking discourse makes plausible: authority framing ("atas perintah Kepala Dinas", "sudah disetujui Direksi"), urgency framing ("segera, batas pencairan hari ini"), and procedural camouflage (an instruction formatted as a standard form field or a regulatory reference). Irwandi et al. [31] found that current models resist explicit injections in Indonesian but remain exposed to contextual and emotionally framed manipulation, which motivates these framings. Whether they outperform direct overrides once an agent holds tools is an empirical question for Section 6.

### 4.4 Security goals
- **G1 Bounded effect.** No sequence of untrusted inputs can cause a state change outside the capability issued for the current task.
- **G2 Entity isolation.** No agent action crosses a KUB legal-entity boundary without an explicit, logged cross-entity grant.
- **G3 Public-fund dual control.** No treasury disbursement is executed on an agent's authority alone.
- **G4 Attributable record.** Every agent action is traceable to a task, a capability, a policy decision and, where required, a human approver.

---

## 5. BATAS: Bounded Agent Trust and Authority Scoping
BATAS moves every security decision that matters out of the language model and into components the bank already knows how to audit: a capability issuer, a deterministic policy gateway and its existing authority matrix. The model may be fooled; the gateway does not read prose.

In Figure 3, untrusted text (dashed) is parsed into typed data and never reaches the planner as instructions; every tool call is checked against the task token, and calls above the bank's authority tier or touching treasury go to dual human approval.

### 5.1 Design principles
1. **The model is not a security boundary.** After reading untrusted text, the model's output is treated as attacker-influenced.
2. **Authority is issued per task, not held per agent.** No agent has standing credentials.
3. **Enforcement is deterministic.** Allow or deny is decided by code over structured fields, never by an LLM judging intent.
4. **Reuse the bank's authority matrix.** Approval thresholds come from the bank's existing delegation-of-authority rules, not from the paper.
5. **Detection informs, it does not gate.** Classifiers raise alerts and tighten tiers; they are never the only control.

### 5.2 Controls
Table 5. BATAS controls C1–C9, the security goals they serve and the paths they close.

| Control | Mechanism | Goal served | Paths closed |
| :--- | :--- | :--- | :--- |
| C1 Task capability | A trusted orchestrator issues a signed, short-lived token per task: permitted tools, account scope, amount ceiling, counterparty allowlist, legal entity. Agent workloads authenticate with mutual TLS and workload identity (e.g., SPIFFE). | G1, G4 | AP1–AP4 |
| C2 Plan-then-execute with quarantine | A privileged planner sees only the trusted request and fixes the tool sequence. Untrusted content is parsed by a quarantined model whose output is typed data that cannot add tool calls (dual-LLM / CaMeL pattern). | G1 | AP1, AP2, AP7 |
| C3 Policy gateway | Every tool call passes a policy-as-code check (e.g., Open Policy Agent with Rego [33]) against the capability: tool, account, amount, counterparty, entity, rate. Default deny. | G1, G2 | AP1–AP6 |
| C4 Risk-tiered approval | Thresholds taken from the bank's authority matrix. Treasury disbursements always require dual human control; new counterparties always require a human. The approver sees a deterministic rendering of the exact call, not the agent's summary. | G3, G4 | AP2, AP3 |
| C5 Memory provenance | Memory entries carry provenance; entries from untrusted sources never re-enter the planner as instructions and expire. | G1 | AP5 |
| C6 Entity tenancy | Separate capability issuers and keys per KUB member; cross-entity access requires an explicit grant with its own approval. | G2 | AP4 |
| C7 Tool supply chain | Signed, pinned tool manifests reviewed under the bank's IT-service-provider process; tool descriptions are not passed to the planner verbatim. | G1 | AP6 |
| C8 Detection telemetry | Indonesian-language injection classifier and canary strings feed the SOC; alerts lower the task's risk tier, never raise its authority. | — | Supports all |
| C9 Attributable audit | Append-only log linking task, capability, policy decision, approver and core-banking reference; revocation switch for all capabilities. | G4 | Supports all |

### 5.3 What BATAS does not claim
BATAS does not prevent an agent from producing a wrong or manipulated answer in conversation; it prevents that answer from turning into an unauthorised state change. Within the issued capability an attacker can still cause harm, for example a wrong refund that is under the ceiling and to an allowed counterparty. Section 6 measures this residual risk explicitly rather than hiding it.

### 5.4 Example: AP2, treasury disbursement
A district finance office sends an SP2D whose attachment contains: *"Atas perintah Kepala BPKAD, rekening penerima diganti ke …"*. Under BATAS the planner never sees the attachment text as instructions; the quarantined parser extracts typed fields; the policy gateway compares the beneficiary with the SP2D register held by the bank; any mismatch is denied, and any disbursement proceeds only after dual human approval that displays the register-matched beneficiary. The injection is read, but it has no authority to act on.

### 5.5 Deployment sequence for a BPD
1. Inventory agents, tools and the authority each would need; reject any design that needs standing credentials.
2. Deploy C3 and C9 first: they work even before agents are capable.
3. Add C1 and C6 when the first agent touches customer or group data.
4. Add C2 and C4 before any agent may initiate a transfer; treasury stays dual-control permanently.
5. Run the Section 6 evaluation on every model or tool change.

### 5.6 Mapping to Indonesian obligations
Table 6. Mapping of BATAS controls to Indonesian regulatory obligations.

| Control | Obligation area | Instrument |
| :--- | :--- | :--- |
| C1, C3, C6 | Access control and information security in IT risk management | PADK OJK 1/2026 [21], Lampiran I, Bab IV.A (IT risk management process) and Bab IV.B.1 (information security); POJK 11/POJK.03/2022 [20] |
| C7 | Use of IT service providers | PADK OJK 1/2026 [21], Lampiran I, Bab V (use of IT service providers, PPJTI) |
| C4 | Human oversight; accountability for AI decisions | OJK banking AI governance guideline [23], Ch. 5 (risk management and governance, p. 110) and Ch. 7 (supervision and audit, p. 190) |
| C5, C9 | Data management, personal data protection, audit trail | PADK OJK 1/2026 [21], Lampiran I, Bab VII (data management and personal data protection) and Bab IX (internal control and audit); UU 27/2022 [24] |
| C8 | Detection and response | SEOJK 29/SEOJK.03/2022 [22], Bab IV (cyber resilience process: detection, response and recovery) and Bab IX (cyber incident reporting) |

---

## 6. Materials and methods
We follow a design-science approach [32]: the artefact is BATAS, evaluated by controlled experiment in a synthetic BPD testbed and, optionally, by structured review with BPD security practitioners. An attack counts as successful only when the testbed's state changes in a forbidden way, following AgentDojo's environment-grounded principle [4].

Figure 4 summarises the protocol: each trial runs an agent configuration against the synthetic BPD, the state checker decides success, and the adaptive attacker uses that feedback to generate the next injection before results go to analysis.

### 6.1 Testbed
- **Synthetic BPD.** Mock core-banking API (accounts, transfers, reversals, limits), a local-government SP2D register, an agent-network registry and two legal entities representing a parent and a KUB member. All data synthetic; no Bank Jatim data.
- **Agents.** Four task agents matching AP1–AP4, built on one open agent framework; memory enabled for AP5 trials; one third-party tool with a manipulable description for AP6.
- **Models.** At least three: one open-weight model for reproducibility (Qwen2.5-7B-Instruct [34], served locally) and two commercial models. Record exact model identifiers, API dates and decoding settings.
- **Packaging.** Docker images, fixed seeds and a run manifest released with the paper.

### 6.2 Tasks and attacks
- **User tasks.** At least 40 benign tasks across AP1–AP4, each with a programmatic success check.
- **Injection goals.** At least 30 harmful goals (e.g., change beneficiary, raise a limit, read another entity's customer), each with a programmatic forbidden-state check.
- **Framings.** Direct override, authority framing, urgency framing, procedural camouflage (Section 4.3), each in Indonesian and English to test the language effect.
- **Injection channels.** Email body, attachment text, chat message, tool response, prior memory.
- **Adaptive attacker.** For every defence, an attacker model that knows the defence design iterates up to K attempts per goal, orchestrated with PyRIT [35]; report best-of-K. Results against static attacks alone will not be accepted [3].

### 6.3 Configurations
Table 7. Defence configurations compared in the experiment.

| ID | Configuration | Purpose |
| :--- | :--- | :--- |
| D0 | No defence beyond model defaults | Baseline |
| D1 | Prompt hardening (delimiters, instruction hierarchy) | Common practice |
| D2 | D1 + Indonesian-language injection classifier as a gate | Detection-based defence |
| B1 | C1 + C3 (capability and policy gateway) | Minimum BATAS |
| B2 | B1 + C2 (plan-then-execute with quarantine) | Effect of design pattern |
| B3 | Full BATAS (C1–C9) | Proposed |
| B3−x | B3 minus one control at a time | Ablation |

### 6.4 Metrics
Table 8. Evaluation metrics and their definitions.

| Metric | Definition |
| :--- | :--- |
| ASR | Share of (task, goal, framing) trials ending in a forbidden state change |
| Benign utility | Share of benign tasks completed correctly with no attack present |
| Utility under attack | Share of tasks completed correctly while an injection is present |
| False denial rate | Share of legitimate tool calls denied by policy |
| In-scope residual harm | Share of trials with harmful but capability-permitted effects (Section 5.3) |
| Human load | Approvals required per 100 tasks |
| Latency overhead | p50 and p95 end-to-end time minus D0, in milliseconds |

### 6.5 Sample size and statistical analysis
**Sample size.** Each model is run under every configuration in Table 7, including the six one-control ablations. An attack trial is a compatible task–goal pair (a goal is paired only with tasks whose tools could realise it) under one framing and one language. With 40 benign tasks, 30 goals and an expected ten compatible tasks per goal, the plan is about 300 pairs × 4 framings × 2 languages ≈ 2,400 attack trials per model and configuration, plus each benign task run three times (n = 120) to estimate utility. Exact counts are fixed in the pre-registration before any run and reported in Table 9.

**Analysis.** Each proportion is reported with a Wilson 95% confidence interval [36], computed in statsmodels [37]. Configurations are compared with a mixed-effects logistic regression fitted with lme4 [38] (fixed effects: configuration, framing, language; random intercepts: model, task, goal), reporting odds ratios with 95% confidence intervals and Holm correction for multiple comparisons [39].

### 6.6 Practitioner review (optional, strengthens the case)
A structured walkthrough of the threat model and controls with 5–8 IT-security or risk staff from BPDs, with ethics approval and anonymised responses. Ask: are the authority paths realistic; which controls conflict with existing operations; which thresholds the authority matrix would set. Report themes, not quotes that identify a bank.

---

## 7. Results

### 7.1 Attack success by configuration (Table 9)
Table 9. Attack success, utility, human load and latency by configuration (to be filled from the run).

| Configuration | ASR, % [95% CI] | Benign utility, % [95% CI] | Utility under attack, % | False denial, % | Human load /100 tasks | p95 overhead, ms |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D0 | | | | — | — | 0 |
| D1 | | | | | | |
| D2 | | | | | | |
| B1 | | | | | | |
| B2 | | | | | | |
| B3 | | | | | | |

### 7.2 By authority path (Table 10)
One row per AP1–AP7, columns D0, D2 and B3 ASR with CI. Expect AP2 (treasury) to fall to zero forbidden state changes under B3 because of dual control; if it does not, report why.

### 7.3 Language and framing effect (Figure 5)
Figure 5 (draw only from the run's data): grouped bars of ASR with 95% CI whiskers by framing (direct, authority, urgency, procedural) for Indonesian versus English, D0 and B3 side by side. This is where the paper's Indonesian contribution stands or falls; report it even if the language effect is null.

### 7.4 Ablation (Table 11)
B3 minus each control: change in ASR and in benign utility, with odds ratios from the mixed model.

### 7.5 In-scope residual harm
Report the share of trials in which B3 permitted a harmful but in-capability action, with examples. Reviewers will trust the paper more for this paragraph than for any headline number.

### 7.6 Practitioner review (if conducted)
Themes, with counts of participants raising each.

---

## 8. Discussion

### 8.1 Expected findings to confirm or reject
1. Authority bounding (B1–B3) lowers forbidden state changes more than detection gating (D2), at a cost in human load rather than in model accuracy.
2. Detection gating trades benign utility for security and degrades under adaptive attacks.
3. Indonesian authority and urgency framings are at least as effective as direct overrides against undefended agents. [Report the actual direction.]

### 8.2 Implications for Bank Jatim and other BPDs
- **Treasury.** Public-fund workflows should never be fully delegated to an agent. Dual human control with a deterministic display of the exact transaction is the control that makes AP2 safe, and it already exists in the bank's procedures.
- **Agent network.** Messages from Agen Jatim outlets should be treated as untrusted input to any AI agent, regardless of the outlet's standing.
- **KUB.** Group integration should start with separate capability issuers per member bank. Shared infrastructure is acceptable; shared authority is not.
- **Supervision.** OJK's AI guideline is principles-based. Capability tokens, policy decisions and approval records give supervisors concrete evidence of human oversight and accountability.

### 8.3 Limitations
1. **Synthetic testbed.** Workflows are BPD-typical, not Bank Jatim's actual systems; we had no access to internal architecture.
2. **Prospective case.** No public evidence shows Bank Jatim operates agentic AI today; findings describe preconditions, not an audit.
3. **Model drift.** Results hold for the recorded model versions and dates.
4. **Attack coverage.** The adaptive attacker is bounded by K attempts and the attacker model used.
5. **Insider collusion.** Dual control assumes approvers do not collude; BATAS does not address that.

### 8.4 Future work
Field validation with a BPD under a research agreement; extension to Islamic banking units and KUB members with Sharia mandates; formal verification of the policy gateway.

---

## 9. Conclusion
For banking agents, asking whether a prompt is malicious is the wrong question, because it cannot yet be answered reliably. The right question is what the agent is allowed to do if it is fooled. BATAS answers it with task-scoped capabilities, deterministic policy, entity isolation and dual control on public funds, and grounds each answer in Indonesian obligations. For a regional development bank like Bank Jatim, whose agents would sit next to treasury accounts, a network of outlets and five group banks, that shift is a precondition for granting agents any transactional authority. [Add one sentence with the main measured result.]

---

## Declarations

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the author(s) used [tool name] to [draft and edit text / structure the manuscript]. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.

**Data availability.** Testbed code, synthetic data, attack suite, run manifests and raw logs: [GitHub/Zenodo DOI]. No data from Bank Jatim or any customer were used.

**Ethics.** The study uses synthetic data only. [If Section 6.6 is conducted: approval reference from the institutional ethics committee; informed consent obtained.] Bank Jatim did not participate in or endorse this study [or: state the research agreement].

**Funding.** [State funding or "This research received no specific grant…".]

**Declaration of competing interest.** [State any relationship with Bank Jatim, OJK, or AI vendors; otherwise the standard none-declared text.]

**CRediT author statement.** Indri Anjar Kartika Sari: Conceptualization, Methodology, Software, Investigation, Writing – original draft. [Co-authors: roles.]

---

## References

[1] Katadata, "Adopsi AI di perbankan tembus 57%, dipakai untuk layanan hingga analisis kredit," Katadata.co.id, Jun. 29, 2026. [Online]. Available: https://katadata.co.id/finansial/keuangan/6a42802233c09/adopsi-ai-di-perbankan-tembus-57-dipakai-untuk-layanan-hingga-analisis-kredit

[2] OWASP GenAI Security Project, "OWASP Top 10 for Agentic Applications 2026," Dec. 9, 2025. [Online]. Available: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

[3] Y. Jia et al., "A critical evaluation of defenses against prompt injection attacks," arXiv:2505.18333, 2025.

[4] E. Debenedetti, J. Zhang, M. Balunović, L. Beurer-Kellner, M. Fischer, and F. Tramèr, "AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents," in *Proc. NeurIPS Datasets and Benchmarks Track*, 2024, arXiv:2406.13352.

[5] L. Beurer-Kellner et al., "Design patterns for securing LLM agents against prompt injections," arXiv:2506.08837, 2025.

[6] E. Debenedetti, I. Shumailov, T. Fan, J. Hayes, N. Carlini, D. Fabian, C. Kern, C. Shi, A. Terzis, and F. Tramèr, "Defeating prompt injections by design," arXiv:2503.18813, 2025, doi: 10.48550/arXiv.2503.18813.

[7] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, "Zero Trust Architecture," NIST, Gaithersburg, MD, USA, SP 800-207, 2020, doi: 10.6028/NIST.SP.800-207.

[8] Bisnis.com, "Bank Jatim (BJTM) cetak laba bersih Rp1,54 triliun sepanjang 2025," Mar. 30, 2026. [Online]. Available: https://finansial.bisnis.com/read/20260330/90/1963148/bank-jatim-bjtm-cetak-laba-bersih-rp154-triliun-sepanjang-2025

[9] detikFinance, "Bank Jatim tebar dividen Rp 821 miliar, dibayar hari ini," Jun. 2025. [Online]. Available: https://finance.detik.com/bursa-dan-valas/d-7972205/bank-jatim-tebar-dividen-rp-821-miliar-dibayar-hari-ini

[10] Investortrust, "Laba Bank Jatim (BJTM) naik 20,65% di 2025, tembus Rp 1,54 triliun," Mar. 2026. [Online]. Available: https://investortrust.id/financial/98429/laba-bank-jatim-bjtm-naik-20-65-di-2025-tembus-rp-1-54-triliun

[11] Bank Jatim, "Bank Jatim closes 2025 with solid performance and rising profit," press release, Mar. 30, 2026. [Online]. Available: https://www.bankjatim.co.id/en/information/news/bank-jatim-closes-2025-with-solid-performance-and-rising-profit

[12] JatimTimes, "Semester pertama 2026, user JConnect naik dan tembus satu juta lebih pengguna," Jul. 31, 2026. [Online]. Available: https://jatimtimes.com/amp/baca/3331347968/20260731/135600/privacy

[13] Infobanknews, "Bank Jatim bidik 2 juta pengguna JConnect hingga akhir 2026," Apr. 2026. [Online]. Available: https://infobanknews.com/bank-jatim-bidik-2-juta-pengguna-jconnect-hingga-akhir-2026/

[14] Kontan, "Bank Jatim catat laba bersih konsolidasi Rp 1,6 triliun pada 2025," Mar. 2026. [Online]. Available: https://keuangan.kontan.co.id/news/bank-jatim-catat-laba-bersih-konsolidasi-rp-16-triliun-pada-2025

[15] Selular.id, "Perkuat konektivitas digital, Bank Jatim siapkan JConnect terbaru," Apr. 2026. [Online]. Available: https://selular.id/2026/04/perkuat-konektivitas-digital-bank-jatim-siapkan-jconnect-terbaru/

[16] Bisnis.com, "Wacana gaji ASN disalurkan via Kopdes, begini respons Pemprov dan Bank Jatim," Oct. 15, 2026. [Online]. Available: https://surabaya.bisnis.com/read/20261015/532/2012929/wacana-gaji-asn-disalurkan-via-kopdes-begini-respons-pemprov-dan-bank-jatim

[17] Infobanknews, "Pemda se-Banten didorong tak ragu lagi tempatkan RKUD ke Bank Banten," 2025. [Online]. Available: https://infobanknews.com/pemda-se-banten-didorong-tak-ragu-lagi-tempatkan-rkud-ke-bank-banten/

[18] Media Asuransi, "Bank Jatim (BJTM) tegaskan tidak ada kebocoran data nasabah," Oct. 2021. [Online]. Available: https://mediaasuransinews.co.id/news-in-brief/bank-jatim-bjtm-tegaskan-tidak-ada-kebocoran-data-nasabah/

[19] Kontan, "Dikabarkan ada kebocoran data, Bank Jatim pastikan data nasabah aman," Oct. 22, 2021. [Online]. Available: https://keuangan.kontan.co.id/news/dikabarkan-ada-kebocoran-data-bank-jatim-pastikan-data-nasabah-aman

[20] Otoritas Jasa Keuangan, *Peraturan OJK Nomor 11/POJK.03/2022 tentang Penyelenggaraan Teknologi Informasi oleh Bank Umum*. Jakarta, Indonesia: OJK, 2022.

[21] Otoritas Jasa Keuangan, *Peraturan Anggota Dewan Komisioner OJK Nomor 1 Tahun 2026 tentang Penyelenggaraan Teknologi Informasi oleh Bank Umum*. Jakarta, Indonesia: OJK, 2026. [Online]. Available: https://ojk.go.id/id/regulasi/Pages/PADK-1-Tahun-2026-Penyelenggaraan-Teknologi-Informasi-oleh-Bank-Umum.aspx

[22] Otoritas Jasa Keuangan, *Surat Edaran OJK Nomor 29/SEOJK.03/2022 tentang Ketahanan dan Keamanan Siber bagi Bank Umum*. Jakarta, Indonesia: OJK, 2022.

[23] Otoritas Jasa Keuangan, *Tata Kelola Kecerdasan Artifisial Perbankan Indonesia*. Jakarta, Indonesia: OJK, 2025. [Online]. Available: https://ojk.go.id/id/Publikasi/Roadmap-dan-Pedoman/Perbankan/Pages/Tata-Kelola-Kecerdasan-Artifisial-Perbankan-Indonesia.aspx

[24] Republik Indonesia, *Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi*, 2022.

[25] F. Perez and I. Ribeiro, "Ignore previous prompt: Attack techniques for language models," arXiv:2211.09527, 2022.

[26] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, "Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection," in *Proc. 16th ACM Workshop on Artificial Intelligence and Security (AISec '23)*, 2023.

[27] J. Yi et al., "Benchmarking and defending against indirect prompt injection attacks on large language models," in *Proc. ACM SIGKDD Conf. Knowledge Discovery and Data Mining (KDD '25)*, 2025, arXiv:2312.14197.

[28] Z. Yang et al., "FinVault: Benchmarking financial agent safety in execution-grounded environments," arXiv:2601.07853, 2026, doi: 10.48550/arXiv.2601.07853.

[29] S. Raza, R. Sapkota, M. Karkee, and C. Emmanouilidis, "TRiSM for agentic AI: A review of trust, risk, and security management in LLM-based agentic multi-agent systems," arXiv:2506.04133, 2025.

[30] S. Mahadevaswamy, "Securing agentic AI workflows: A defence-in-depth framework for autonomous systems," *Cyber Security: A Peer-Reviewed Journal*, vol. 10, no. 1, pp. 6–16, 2026, doi: 10.69554/MIWG3713.

[31] H. Irwandi, A. I. Silitonga, R. Chandra, and W. S. Simamora, "Security evaluation of Indonesian LLMs for digital business using STAR prompt injection," *Sinkron: Jurnal dan Penelitian Teknik Informatika*, vol. 10, no. 1, pp. 449–457, 2026, doi: 10.33395/sinkron.v10i1.15662.

[32] A. R. Hevner, S. T. March, J. Park, and S. Ram, "Design science in information systems research," *MIS Quarterly*, vol. 28, no. 1, pp. 75–105, 2004.

[33] Open Policy Agent (CNCF), Open Policy Agent documentation, version 1.21.2. [Online]. Available: https://www.openpolicyagent.org/docs

[34] Qwen Team, "Qwen2.5 technical report," arXiv:2412.15115, 2024.

[35] G. D. Lopez Munoz et al., "PyRIT: A framework for security risk identification and red teaming in generative AI systems," arXiv:2410.02828, 2024.

[36] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *J. Amer. Statist. Assoc.*, vol. 22, no. 158, pp. 209–212, 1927.

[37] S. Seabold and J. Perktold, "Statsmodels: Econometric and statistical modeling with Python," in *Proc. 9th Python in Science Conf.*, 2010, pp. 92–96, doi: 10.25080/Majora-92bf1922-011.

[38] D. Bates, M. Mächler, B. Bolker, and S. Walker, "Fitting linear mixed-effects models using lme4," *J. Stat. Softw.*, vol. 67, no. 1, pp. 1–48, 2015, doi: 10.18637/jss.v067.i01.

[39] S. Holm, "A simple sequentially rejective multiple test procedure," *Scand. J. Statist.*, vol. 6, no. 2, pp. 65–70, 1979.
