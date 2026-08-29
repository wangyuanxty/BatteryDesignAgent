AnalogAgent: Self-Improving Analog Circuit Design Automation with LLM Agents
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2603.23910v1 [cs.AI] 25 Mar 2026
AnalogAgent: Self-Improving Analog Circuit Design Automation with LLM Agents
DOI:
XXXXXXX.XXXXXXX
Conference:
Make sure to enter the correct
conference title from your rights confirmation email; June 03–05,
2018; Woodstock, NY
ISBN:
978-1-4503-XXXX-X/2018/06
Zhixuan Bao
Affiliation:
Nanyang Technological University
,
Singapore
Note:
Work done during internship at A*STAR.
email:
zhixuan005@e.ntu.edu.sg
,
Zhuoyi Lin
Affiliation:
Institute for Infocomm Research
,
Singapore
Note:
Corresponding author.
email:
Lin_Zhuoyi@a-star.edu.sg
,
Jiageng Wang
Affiliation:
Nanyang Technological University
,
Singapore
email:
WANG2396@e.ntu.edu.sg
,
Jinhai Hu
Affiliation:
Institute of Microelectronics
,
Singapore
email:
hujh@a-star.edu.sg
,
Yuan Gao
Affiliation:
Institute of Microelectronics
,
Singapore
email:
gaoy@a-star.edu.sg
,
Yaoxin Wu
Affiliation:
Eindhoven University of Technology
,
Eindhoven
,
Netherlands
email:
y.wu2@tue.nl
,
Xiaoli Li
Affiliation:
Singapore University of Technology
,
and Design, Singapore
email:
xiaoli_li@sutd.edu.sg
and
Xun Xu
Affiliation:
Institute for Infocomm Research
,
Singapore
email:
Xu_Xun@a-star.edu.sg
2018; © , 2018; Received  5 June 2009
Abstract.
Recent advances in large language models (LLMs) suggest strong potential for automating analog circuit design. Yet most LLM-based approaches rely on a single-model loop of generation, diagnosis, and correction, which favors succinct summaries over domain-specific insight and suffers from context attrition that erases critical technical details.To address these limitations, we propose
AnalogAgent
, a training-free agentic framework that integrates an LLM-based multi-agent system (MAS) with self-evolving memory (SEM) for analog circuit design automation. AnalogAgent coordinates a Code Generator, Design Optimizer, and Knowledge Curator to distill execution feedback into an adaptive playbook in SEM and retrieve targeted guidance for subsequent generation, enabling cross-task transfer without additional expert feedback, databases, or libraries. Across established benchmarks, AnalogAgent achieves 92% Pass@1 with Gemini and 97.4% Pass@1 with GPT-5. Moreover, with compact models (e.g., Qwen-8B), it yields a +48.8% average Pass@1 gain across tasks and reaches 72.1% Pass@1 overall, indicating that AnalogAgent substantially strengthens open-weight models for high-quality analog circuit design automation.
Keywords:
Analog Circuit Design, Large Language Model, Agentic AI.
1.
Introduction
Analog circuit design is a cornerstone of modern scientific discovery, enabling the reliable translation of physical phenomena into calibrated electrical signals that can be measured, controlled, and computed with high fidelity. It underpins core instrumentation across biomedical sensing, environmental monitoring, and large-scale experimental facilities, where noise, accuracy, and stability directly shape data quality and reproducibility
(
11
)
.
In contrast to digital design, which benefits from standardized abstractions and mature automation pipelines, analog design relies heavily on expert knowledge, heuristic reasoning, and iterative simulation-driven refinement. Although conventional electronic design automation (EDA) tools have achieved progress in areas such as device sizing and topology optimization
(
31
;
4
)
, they are typically limited to predefined architectures
(
24
)
, require extensive manual configuration
(
16
)
, and scale poorly when exploring novel circuit structures or heterogeneous design objectives
(
20
;
23
)
.
Figure 1
.
Illustration of context attrition on the hard Task 25.
As context accumulates across iterations, LLM agents tend to compress it into shorter, less informative summaries, diminishing instruction salience and degrading detailed guidance. AnalogCoder Pro takes
∼
\sim
7 minutes to produce its first correct circuit, whereas AnalogAgent succeeds in 17.13 seconds with learned knowledge.
Recent advancements in large language models (LLMs) have revitalized academic interest in analog circuit design automation. By leveraging their capabilities in code generation, structured reasoning, and broad generalization, LLMs offer an alternative to traditional workflows that rely primarily on hand-crafted rules or tightly coupled numerical optimization
(
12
;
13
;
30
;
32
)
.
Early evidence is provided by AnalogCoder, which shows the feasibility of generating executable design scripts for analog circuits in a code-centric pipeline
(
12
)
.
AnalogCoder-Pro further introduces a multimodal feedback-enhanced design flow
(
13
)
. These efforts establish an important benchmark for LLM-driven analog design automation with training-free code generation.
However, LLM-based analog circuit design automation remains constrained by several challenges.
(1) Single LLM paradigm.
Most approaches rely on a single LLM to jointly handle code generation, error diagnosis, and iterative refinement, coupling heterogeneous subtasks within one monolithic loop.
(2) Context attrition.
As shown in Figure
1
, LLM agents tend to frequently rewrite the detailed specification and prior findings during iterative refinement, which progressively erode salient technical details and degrade the performance.
(3) Dependence on circuit libraries.
Most of the existing methods assume access to additional circuit databases (e.g., topology library, circuit textbooks, and literature) to scaffold circuit design, which limits applicability in settings where such resources are unavailable or proprietary.
In this paper, we introduce AnalogAgent, a training-free agentic framework for analog circuit design automation. Unlike prior LLM-based methods that center on a single agent augmented with circuit libraries, AnalogAgent integrates an LLM-based
multi-agent system (MAS)
with
self-evolving memory (SEM)
to adaptively execute design, evaluation, and knowledge reuse.
Specifically, AnalogAgent coordinates three agents. (1) The Code Generator generates task-specific SPICE/Python design scripts. (2) The Design Optimizer evaluates candidates through simulation-driven checks and converts execution feedback into targeted corrections and reusable best practices.
(3) The Knowledge Curator distills optimization feedback into structured, reusable design knowledge and incrementally updates the
Adaptive Design Playbook
within SEM. The playbook then supplies targeted guidance to the Code Generator, grounding subsequent generations in accumulated experience.
By coupling workflow decomposition with iterative execution feedback and structured memory updates, AnalogAgent converts outcomes into actionable guidance, reduces redundant experimentation, and accelerates convergence to specification-compliant designs.
In summary, the main contributions of this work are:
(1)
Conceptual
: AnalogAgent represents an early attempt at a training-free agentic framework for analog circuit design automation that operates without additional circuit libraries.
(2)
Algorithmic:
AnalogAgent employs a coordinated multi-agent system with Code Generation, Design Optimization, and Knowledge Curation agents to support structured reasoning and sustained self-improvement. Its self-evolving memory mechanism retrieves guidance from an Adaptive Design Playbook and distills validated heuristics into reusable rules, mitigating context attrition and improving robustness and cross-task generalization.
(3)
Empirical:
We evaluate AnalogAgent and strong baselines on analog circuit design tasks spanning multiple complexity levels. Results show consistent gains and successful adaptation to compact open-weight models (e.g., Qwen-8B).
2.
Related Work
2.1.
Circuit Design Automation
Conventional analog automation tools provide practical benefits, yet key constraints remain. Recent device-sizing methods improve sample efficiency
(
31
;
26
)
, with further gains from learned optimization and parallelization
(
3
;
4
)
; related learning-based sizing approaches report similar efficiency improvements
(
7
;
14
)
, and newer systems advance sample-efficient optimization
(
22
;
25
)
. Despite this progress, these methods are largely confined to predetermined circuit architectures, consistent with earlier pipelines
(
16
)
, which limits transfer when meeting specifications requires architectural adaptation, alternative biasing, or changes in feedback structure; they work best when the topology class is known and the objective reduces to parameter selection within a fixed template. In contrast, topology exploration often incurs substantial simulation overhead
(
20
;
23
)
, depends on expert-derived analytical formulations
(
29
;
21
;
35
)
, and offers limited structural diversity
(
19
)
, while risking invalid configurations
(
18
)
. Costs are dominated by feasibility screening across many candidates, with frequent failures from bias infeasibility, missing DC paths, or non-convergent operating points; expert dependence further reduces portability across circuit families, regimes, or process assumptions. Moreover, automated synthesis approaches such as
(
24
)
often require substantial up-front setup, restricting deployment to predefined component or topology libraries, including block curation, interface/range specification, and constraint encoding for correctness and simulator stability, which raises the barrier to extending the system to new components, macro-blocks, or architectural motifs.
2.2.
LLM-based Circuit Design Automation
Early LLM-based analog circuit design approaches largely rely on prompt-driven generation, using curated instructions and in-context exemplars to steer LLMs toward synthesizing SPICE or Python netlists, as demonstrated by SPICEPilot
(
30
)
, Artisan
(
6
)
, and Ado-llm
(
32
)
.
A complementary paradigm explores training-based solusions, improving circuit synthesis via supervised fine-tuning, reinforcement learning, or dataset augmentation. Representative methods include AnalogGenie
(
10
)
, LaMAGIC
(
5
)
, and CKTGNN
(
8
)
. While effective, these approaches typically require additional labeled data and may demand repeated retraining when generalizing to new circuit families.
To further enhance reliability and reduce iterative search cost, recent work introduces external knowledge resources such as topology libraries, circuit tool repositories, or structured databases to condition generation, including AnalogXpert
(
33
)
, AMSnet-KG
(
27
)
, LADAC
(
17
)
, LayoutCopilot
(
15
)
, AnalogCoder
(
12
)
, and AnalogCoder-pro
(
13
)
.
In contrast, AnalogAgent is training-free and does not rely on an additional database or a pre-built circuit library.
Instead, it leverages execution signals from simulation and checker diagnostics, distilling both failures and successes into reusable rules that are stored in SEM and retrieved to guide subsequent generations, thereby forming a cross-task self-improvement loop.
Moreover, AnalogAgent maintains strong performance with smaller models that are suitable for local or self-hosted deployment, reducing reliance on large proprietary backbones while retaining reliable first-pass synthesis and iterative refinement for industry companies.
Figure 2
.
AnalogAgent Framework Overview.
Left
: Existing LLM-based methods typically rely on a single LLM with static prompts, which often produce suboptimal solutions even when augmented with external circuit libraries.
Right
: AnalogAgent coordinates multiple agents and curates reusable design knowledge. It retrieves prior knowledge from SEM to refine instructions and perform self-improvement, improving convergence toward functionally complete circuits without additional libraries.
3.
Methodology
3.1.
Problem Formulation
We formulate analog circuit design automation as a training-free code generation problem with simulation-based verification. Formally, the input is a task instance
ℐ
=
(
x
,
τ
,
Ω
,
Φ
task
)
\mathcal{I}=(x,\tau,\Omega,\Phi_{\text{task}})
, where
x
x
is the natural-language instruction,
τ
\tau
is the circuit/task type,
Ω
\Omega
specifies hard interface/API constraints enforced by the evaluation criteria (e.g., required node names, subcircuit pins, and simulator settings), and
Φ
task
=
{
φ
k
}
k
=
1
K
\Phi_{\text{task}}=\{\varphi_{k}\}_{k=1}^{K}
is a set of task-specific functional assertions evaluated on simulation outputs. Given
ℐ
\mathcal{I}
, our AnaglogAgent outputs an executable design candidate
c
∈
𝒫
c\in\mathcal{P}
(SPICE/Python), where
𝒫
\mathcal{P}
denotes the space of candidate SPICE/Python programs that satisfy the required interface and API constraints.
Executing
c
c
yields
(
e
,
s
,
z
)
=
ℰ
⁡
(
c
)
(e,s,z)=\mathcal{E}(c)
, where
e
∈
{
0
,
1
}
e\in\{0,1\}
indicates program-level or evaluation-criteria results,
s
∈
{
0
,
1
}
s\in\{0,1\}
indicates simulator-level results, and
z
z
denotes the corresponding simulated results and waveforms used to verify design requirements. A candidate design is valid only if all hard constraints and task assertions hold:
(1)
PASS
​
(
c
)
=
1
⟺
(
e
=
0
)
∧
(
s
=
0
)
∧
(
⋀
k
=
1
K
φ
k
​
(
z
)
=
1
)
.
\texttt{PASS}(c)=1\Longleftrightarrow(e=0)\ \land\ (s=0)\ \land\ \Big(\bigwedge_{k=1}^{K}\varphi_{k}(z)=1\Big).
Violations of
Ω
\Omega
are captured by
e
=
1
e=1
or
s
=
1
s=1
. In summary, the objective is to map
ℐ
\mathcal{I}
to a candidate
c
∈
𝒫
c\in\mathcal{P}
such that
PASS
​
(
c
)
=
1
\texttt{PASS}(c)=1
.
3.2.
Framework Overview
In this paper, we present AnalogAgent, a training-free agentic framework for analog circuit design automation that integrates a multi-agent system (MAS) with self-evolving memory (SEM). As shown in Figure
2
, the MAS consists of three specialized agents for code generation, circuit design optimization, and knowledge curation, respectively.
Through iterative self-improvement, the MAS progressively consolidates acquired circuit design knowledge into an Adaptive Design Playbook within the SEM module.
This mitigates context attrition via structured, incremental updates that preserve fine-grained circuit design knowledge while ensuring contextual representations remain comprehensive during the learning process.
A more detailed workflow is provided in Appendix
C
. We detail each component in the following subsections.
3.3.
Multi-agent Systems for Circuit Design
In analog design tasks, context attrition is particularly acute as the LLM agent must (i) generate executable SPICE/Python code under strict interface constraints across repeated revisions, and (ii) preserve simulation-critical details rather than collapsing them into shorter, less informative summaries that dilute the original instructions and obscure useful guidance.
This motivates the design of MAS that decouples generation, optimization, and knowledge curation into a structured workflow with persistent memory.
MAS maintains a continuously evolving Adaptive Design Playbook that stores distilled, validated heuristics and design constraints.
Consequently, the Code Generator Agent conditions on task-relevant knowledge retrieved from this playbook, instead of repeatedly reconstructing instructions from transient context.
Code Generator Agent.
Given a natural-language instruction
x
x
, the code generator produces task-specific SPICE/Python design scripts.
Let
t
∈
{
1
,
2
,
…
}
t\in\{1,2,\dots\}
index the iteration. The code generation prompt
P
t
P_{t}
is constructed by augmenting the task instruction with domain knowledge retrieved from the Adaptive Design Playbook:
(2)
P
t
=
P
task
​
(
x
)
⊕
r
t
,
r
t
=
ℛ
⁡
(
M
t
,
τ
)
,
P_{t}=P_{\mathrm{task}}(x)\oplus r_{t},\qquad r_{t}=\mathcal{R}(M_{t},\tau),
where
P
task
​
(
x
)
P_{\mathrm{task}}(x)
is the task requirements;
r
t
r_{t}
is the retrieved task-specific knowledge;
ℛ
⁡
(
⋅
)
\mathcal{R}(\cdot)
is the retrieval operator;
M
t
M_{t}
is the SEM state (i.e., the playbook) at iteration
t
t
; and
τ
\tau
denotes the circuit/task type.
The code generator then produces a candidate script
c
t
c_{t}
:
(3)
c
t
=
𝒢
⁡
(
P
t
)
,
c_{t}=\mathcal{G}(P_{t}),
where
𝒢
\mathcal{G}
denotes the code generator agent.
Design Optimizer Agent.
After generating the script, a design optimizer agent evaluates it and converts execution feedback into actionable guidance for circuit revision.
Specifically, it performs multi-stage checks: (i) requirement compliance; (ii) DC feasibility via simulation and operating-point inspection; (iii) DC-sweep transfer validation; (iv) task-specific functional tests; and (v) waveform sanity checks
(
13
;
12
)
.
Formally, given a candidate script
c
t
c_{t}
, the execution routine returns structured signals:
(4)
(
e
t
,
s
t
,
ℓ
t
,
z
t
)
=
ℰ
⁡
(
c
t
)
,
\small(e_{t},\ s_{t},\ \ell_{t},\ z_{t})=\mathcal{E}(c_{t}),
where
ℰ
⁡
(
⋅
)
\mathcal{E}(\cdot)
denotes the execution and evaluation routine;
e
t
∈
{
0
,
1
}
e_{t}\in\{0,1\}
indicates whether a runtime error occurred at iteration
t
t
(
e
t
=
1
e_{t}=1
for failure,
e
t
=
0
e_{t}=0
otherwise);
s
t
∈
{
0
,
1
}
s_{t}\in\{0,1\}
denotes whether a simulator-level failure occurred;
ℓ
t
\ell_{t}
is the diagnostic log used for feedback; and
z
t
z_{t}
denotes simulated measurements and waveforms used to verify design requirements.
A candidate is accepted if Eq. (
1
) evaluates to true, yielding
PASS
(
c
t
)
(c_{t})
.
Noted that for circuit classes requiring transfer-curve validation, the design optimizer additionally performs a DC sweep on the current candidate
c
t
c_{t}
to identify a feasible bias point, and constructs an auxiliary bias-updated candidate for re-evaluation:
(5)
v
t
=
ℬ
⁡
(
𝒟
⁡
(
c
t
)
)
,
c
~
t
=
𝒯
⁡
(
c
t
,
v
t
)
,
\small v_{t}=\mathcal{B}\!\left(\mathcal{D}(c_{t})\right),\hskip 18.49988pt\tilde{c}_{t}=\mathcal{T}(c_{t},v_{t}),
where
𝒟
⁡
(
⋅
)
\mathcal{D}(\cdot)
produces sweep results for
c
t
c_{t}
,
ℬ
⁡
(
⋅
)
\mathcal{B}(\cdot)
selects a feasible bias point from these results, and
𝒯
⁡
(
⋅
,
⋅
)
\mathcal{T}(\cdot,\cdot)
injects the selected bias.
Knowledge Curator Agent.
Inspired by recent agentic frameworks that store salient contextual information for accumulate, retrieve, and reason over long-horizon experiences
(
28
;
34
;
1
)
, we propose a Knowledge Curator that consolidates the design optimizer’s feedback into SEM by maintaining and refining an Adaptive Design Playbook.
Rather than rewriting the full context, it performs incremental updates that extract compact, reusable rules and code-level patterns from both failures and successes.
This preserves validated guidance while incorporating task-driven insights, mitigating context attrition and enabling reliable retrieval of domain-specific tactics for reference.
Formally, given a validated feedback bundle, the curator distills reusable knowledge and exemplars conditioned on the circuit/task type
τ
\tau
, which are then incorporated into SEM through incremental memory updates across iterations.
(6)
f
t
=
(
x
,
c
t
,
e
t
,
s
t
,
ℓ
t
,
z
t
,
PASS
​
(
c
t
)
)
,
Δ
t
=
ϕ
⁡
(
f
t
)
,
f_{t}=\bigl(x,c_{t},e_{t},s_{t},\ell_{t},z_{t},\texttt{PASS}(c_{t})\bigr),\Delta_{t}=\phi(f_{t}),
where
f
t
f_{t}
aggregates the feedback information and
ϕ
⁡
(
⋅
)
\phi(\cdot)
maps this feedback to structured circuit design knowledge
Δ
t
\Delta_{t}
, which is stored in the memory mechanism described in the following subsection.
3.4.
Self-Evolving Memory Mechanism
LLMs benefit from long, detailed circuit-design instructions, yet as instruction complexity and iteration depth grow, LLMs exhibit a tendency to compress contexts into distilled summaries, which accelerates context attrition.
This motivates the introduction of self-evolving memory (SEM), maintained as an Adaptive Design Playbook that incrementally refines structured reusable circuit design knowledge.
Specifically, SEM constitutes a training-free, dynamically updated repository that facilitates cross-task generalization and enhances convergence on complex circuit design tasks. In doing so, it reduces reliance on repeated full-context rewrites and mitigates information loss across iterative self-improvement, while operating without expert feedback or reliance on predefined circuit libraries or databases.
Overall, by continuously updating the Adaptive Design Playbook and retrieving task-relevant design knowledge, MAS and SEM establish a closed-loop self-improvement paradigm for analog circuit design automation.
Adaptive Design Playbook Update.
AnalogAgent maintains a SEM repository as an Adaptive Design Playbook that accumulates validated rules and exemplars across iterations through incremental, curator-approved updates.
Given the circuit design knowledge extracted by the Knowledge Curator Agent, the playbook is continuously updated as follows:
(7)
M
t
+
1
=
𝒰
⁡
(
M
t
,
Δ
t
)
=
Dedup
⁡
(
Filter
⁡
(
M
t
∥
Δ
t
,
Ω
)
)
,
M_{t+1}=\mathcal{U}\left(M_{t},\ \Delta_{t}\right)=\mathrm{Dedup}\big(\mathrm{Filter}(M_{t}\mathbin{\|}\Delta_{t};\Omega)\big),
where
𝒰
⁡
(
⋅
)
\mathcal{U}(\cdot)
updates the playbook
M
t
M_{t}
with conflict checking under interface/API constraints
Ω
\Omega
, followed by filtering, deduplication process to suppress erroneous experience updates, eliminate redundant entries, and maintain a compact, structured memory.
Design Knowledge Retrieval.
When encountering a new circuit design task, relevant knowledge is retrieved from the playbook to guide script generation, thereby improving both consistency and efficiency.
Given the current task type
τ
\tau
(and optional recent failure reflection
ℱ
\mathcal{F}
), a retriever first queries task-specific memory in
M
t
M_{t}
by type match and resorts to substring-based retrieval when such a match is unavailable, and then forms
(8)
r
(
τ
)
=
{
ℛ
⁡
[
τ
]
,
τ
∈
keys
⁡
(
r
)
,
ℛ
⁡
[
k
∗
]
,
k
∗
=
min
⁡
{
k
∈
keys
⁡
(
r
)
:
k
≺
str
⁡
(
τ
)
}
,
∅
,
otherwise
.
r(\tau)=\begin{cases}\mathcal{R}[\tau],&\tau\in\mathrm{keys}(r),\\
\mathcal{R}[k^{*}],&k^{*}=\min\{k\in\mathrm{keys}(r):k\prec\mathrm{str}(\tau)\},\\
\varnothing,&\text{otherwise}.\end{cases}
where
k
≺
str
⁡
(
τ
t
)
k\prec\mathrm{str}(\tau_{t})
denotes a substring match i.e.,
k
k
is contained within the string representation of
τ
\tau
.
This prioritizes exact task-aligned matches, while enabling approximate reuse of related entries when exact matches are unavailable, thereby improving robustness and coverage.
Closed-loop Self-improvement.
During the self-improving process, AnalogAgent forms a closed loop in which the updated memory state
M
t
+
1
M_{t+1}
is retrieved to construct the retrieved knowledge
r
t
+
1
r_{t+1}
, which is then combined with the task instruction to form
P
t
+
1
P_{t+1}
for generating the next candidate
c
t
+
1
c_{t+1}
:
(9)
r
t
+
1
\displaystyle r_{t+1}
=
ℛ
⁡
(
M
t
+
1
,
τ
)
,
\displaystyle=\mathcal{R}(M_{t+1},\tau),
P
t
+
1
\displaystyle P_{t+1}
=
P
task
​
(
x
)
⊕
r
t
+
1
,
\displaystyle=P_{\mathrm{task}}(x)\oplus r_{t+1},
c
t
+
1
\displaystyle c_{t+1}
=
𝒢
⁡
(
P
t
+
1
)
.
\displaystyle=\mathcal{G}(P_{t+1}).
This completes the loop between generation, verification, and knowledge updates and retrieval. In summary, MAS provides the operational mechanism for producing and applying structured feedback for circuit design knowledge curation, while SEM serves as persistent memory that preserves these updates and supports self-improving across iterations and cross-task knowledge transfer.
3.5.
Circuit Optimization
After a feasible circuit design is generated, the design is further refined through parameter optimization.
Following AnalogCoder-Pro
(
13
)
, the circuit is first validated via simulation to ensure executability.
Based on the task instruction
x
x
and simulated results
z
t
z_{t}
, the LLM identifies key tunable variables (e.g., device dimensions or component values) together with their corresponding search ranges.
Bayesian optimization using the Tree-structured Parzen Estimator (TPE) implemented in Optuna
(
9
)
is then employed to iteratively evaluate candidate parameter configurations through simulation and select the configuration that satisfies the target specifications.
4.
Experiments
4.1.
Experimental Settings
Benchmark.
We evaluate on a 30-task analog circuit benchmark grouped by component count and topological complexity (Tasks 1–8
Easy
, Tasks 9–13
Medium
, Tasks 14–30
Hard
), which is publicly available
1
1
1
https://github.com/laiyao1/AnalogCoder
and adopted from prior work
(
12
;
13
)
.
We provide clear, detailed descriptions of how evaluation data are collected through SPICE/Python execution (e.g., simulation logs, measurements, and waveforms), how these artifacts are preprocessed and managed across runs, and how results are analyzed under a unified protocol to ensure rigorous, reproducible assessment. Please refer to Appendix
B
for more details.
Baselines.
We compare AnalogAgent with
SPICEPilot
(
30
)
,
AnalogCoder
(
12
)
, and
AnalogCoder-Pro
(
13
)
. SPICEPilot uses prompt-based generation with curated instructions and in-context examples
(
30
)
. AnalogCoder introduces a Circuit Tool Library for reusable components and structured synthesis
(
12
)
, and AnalogCoder-Pro further adds a multimodal feedback-enhanced design flow
(
13
)
.
The evaluation includes a diverse set of LLMs, including DeepSeek-V2-Lite, Llama-3-8B, Gemini-2.5-Flash, GPT-5.
All methods use identical configurations for fair comparisons, with full experimental configurations provided in Appendix
B
.
Metrics.
We follow prior work
(
12
;
13
)
and use Pass@
k
k
to assess the reliability of generated circuit designs, defined as the probability of obtaining at least one valid solution among
k
k
samples:
Pass@k
=
1
−
(
n
−
c
k
)
(
n
k
)
\text{Pass@k}=1-\frac{\binom{n-c}{k}}{\binom{n}{k}}
,
where
n
n
is the total number of candidates and
c
c
is the number of correct solutions. Throughout, we fix
n
=
30
n=30
to obtain stable estimates under stochastic model outputs.
4.2.
Experimental Results
Table
I
reports primary results on 30 analog circuit design tasks under a unified benchmark and evaluation protocol, spanning multiple open-source LLMs and LLM baselines. The open-source DeepSeek-V2-Lite achieves Pass@1/Pass@5 of 6.7/11.4, while Llama3-8B attains 8.6/27.0.
SPICEPilot exhibits relatively low Pass@1 (50.1) but much higher Pass@5 (96.5), indicating that it often reaches a valid executable solution only after multiple independent samples rather than in the first attempt.
Under GPT-5, AnalogCoder performs poorly on Hard tasks (Pass@1 36.5), while AnalogCoder-Pro improves the average Pass@1/Pass@5 to 88.6/98.2 but remains limited on several high-difficulty cases (e.g., Tasks 24–25). On the other hand, AnalogAgent consistently attains the best overall Pass@1 and Pass@5 among all methods. Specifically, with GPT-5 backbone, AnalogAgent achieves 97.4/100.0 Pass@1/Pass@5 and improves Hard-task Pass@1 over AnalogCoder-Pro by around 12.5%. With Gemini-2.5-Flash, AnalogAgent reaches 92.0/99.9, suggesting a lower first-try success rate but a comparable multi-sample ceiling.
Table
II
complements these aggregate results with statistics over five random trials, reporting Pass@1 as mean±std for Easy/Medium/Hard groups. AnalogAgent achieves the highest mean Pass@1 with smaller variance across trials, including
87.1
±
2.9
\mathbf{87.1\pm 2.9}
on Medium and
88.7
±
0.9
\mathbf{88.7\pm 0.9}
on Hard tasks, indicating more stable first-attempt performance in the regimes where prior methods struggle. Beyond success rates, Table
II
also summarizes efficiency using the average tokens and runtime required to reach the first success across all 30 tasks. AnalogAgent reduces Time-to-First-Success to 1.3 minutes on average (vs. 2.6 for SPICEPilot and 2.1 for AnalogCoder-Pro) and lowers tokens to first success to
(
∼
)
32
K
(
v
s
.
(
∼
)
40
K
(\sim)32K(vs.(\sim)40K
for AnalogCoder-Pro). Taken together, these results indicate that AnalogAgent’s gains are not driven by increased search effort; instead, by structuring reusable knowledge into an Adaptive Design Playbook and retrieving targeted guidance in subsequent iterations, our framework improves both first-shot reliability and convergence efficiency relative to existing baselines.
Table I
.
Main results.
Across diverse LLM backbones and model variants under a unified benchmark and evaluation protocol, reporting per-task and total tasks Pass@1 and Pass@5.
Model
DeepSeek-V2-Lite
Llama3-8B
SPICEPilot
(Gemini-2.5-Flash)
AnalogCoder
(Gemini-2.5-Flash)
AnalogCoder
(GPT-5)
AnalogCoder-Pro
(Gemini-2.5-Flash)
AnalogCoder-Pro
(GPT-5)
AnalogAgent
(Gemini-2.5-Flash)
AnalogAgent
(GPT-5)
Task ID
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
1
83.3
100.0
26.7
81.5
60.0
99.4
73.3
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
2
0.0
0.0
30.0
85.7
63.3
99.7
70.0
99.9
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
3
0.0
0.0
20.0
70.2
66.7
99.8
90.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
4
0.0
0.0
3.3
16.7
60.0
99.4
73.3
100.0
100.0
100.0
80.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
5
0.0
0.0
0.0
0.0
63.3
99.7
80.0
100.0
100.0
100.0
93.3
100.0
100.0
100.0
100.0
100.0
100.0
100.0
6
13.3
53.8
26.7
81.5
60.0
99.4
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
7
0.0
0.0
30.0
85.7
43.3
95.7
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
8
3.3
16.7
13.3
53.8
40.0
94.0
80.0
100.0
76.7
100.0
76.7
100.0
100.0
100.0
100.0
100.0
100.0
100.0
9
20.0
70.2
0.0
0.0
50.0
97.9
10.0
43.3
96.7
100.0
26.7
81.5
100.0
100.0
66.7
99.8
100.0
100.0
10
0.0
0.0
23.3
76.4
56.7
99.1
96.7
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
11
0.0
0.0
0.0
0.0
33.3
89.1
16.7
62.7
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
12
0.0
0.0
0.0
0.0
46.7
96.9
23.3
76.4
43.3
95.7
30.0
85.7
66.7
99.8
70.0
99.9
100.0
100.0
13
0.0
0.0
26.7
81.5
53.3
98.6
33.3
89.1
86.7
100.0
96.7
100.0
100.0
100.0
96.7
100.0
100.0
100.0
14
80.0
100.0
33.3
89.1
63.3
99.7
83.3
100.0
93.3
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
15
0.0
0.0
20.0
70.2
46.7
96.9
23.3
76.4
50.0
97.9
90.0
100.0
56.7
99.1
100.0
100.0
100.0
100.0
16
0.0
0.0
0.0
0.0
53.3
98.6
0.0
0.0
23.3
76.4
66.7
99.8
16.7
62.7
70.0
99.9
83.3
100.0
17
0.0
0.0
3.3
16.7
43.3
95.7
0.0
0.0
0.0
0.0
76.7
100.0
100.0
100.0
86.7
100.0
90.0
100.0
18
0.0
0.0
0.0
0.0
63.3
99.7
93.3
100.0
90.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
19
0.0
0.0
0.0
0.0
56.7
99.1
0.0
0.0
0.0
0.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
20
0.0
0.0
0.0
0.0
53.3
98.6
0.0
0.0
0.0
0.0
100.0
100.0
80.0
100.0
100.0
100.0
83.3
100.0
21
0.0
0.0
0.0
0.0
36.7
91.8
0.0
0.0
0.0
0.0
93.3
100.0
96.7
100.0
100.0
100.0
100.0
100.0
22
0.0
0.0
0.0
0.0
33.3
89.1
0.0
0.0
0.0
0.0
100.0
100.0
90.0
100.0
100.0
100.0
86.7
100.0
23
0.0
0.0
0.0
0.0
50.0
97.9
90.0
100.0
0.0
0.0
83.3
100.0
80.0
100.0
73.3
100.0
100.0
100.0
24
0.0
0.0
0.0
0.0
43.3
95.7
16.7
62.7
0.0
0.0
33.3
89.1
36.7
91.8
86.7
100.0
100.0
100.0
25
0.0
0.0
0.0
0.0
30.0
85.7
26.7
81.5
0.0
0.0
3.3
16.7
40.0
94.0
53.3
98.6
86.7
100.0
26
0.0
0.0
0.0
0.0
33.3
89.1
83.3
100.0
100.0
100.0
96.7
100.0
100.0
100.0
100.0
100.0
100.0
100.0
27
0.0
0.0
0.0
0.0
50.0
97.9
90.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
100.0
93.3
100.0
28
0.0
0.0
0.0
0.0
36.7
91.8
0.0
0.0
33.3
89.1
100.0
100.0
96.7
100.0
100.0
100.0
100.0
100.0
29
0.0
0.0
0.0
0.0
56.7
99.1
73.3
100.0
100.0
100.0
100.0
100.0
100.0
100.0
96.7
100.0
100.0
100.0
30
0.0
0.0
0.0
0.0
56.7
99.1
0.0
0.0
30.0
85.7
3.3
16.7
96.7
100.0
60.0
99.8
100.0
100.0
Avg
6.7
11.4
8.6
27.0
50.1
96.5
47.6
66.4
60.8
71.5
81.7
93.0
88.6
98.2
92.0
99.9
97.4
100.0
Imp
1362.4
780.5
1039.2
270.8
94.5
3.7
104.9
50.6
60.3
39.9
19.3
7.5
10.0
1.8
5.9
0.1
0
0
Table II
.
Average Pass@1 success rates by task difficulty and average token (K) /runtime (min) cost to first success (mean
±
\pm
std over five trials). All methods use Gemini-2.5-Flash for fairness; NA denotes at least one task unsolved, rendering the aggregate undefined.
Model
Easy
Medium
Hard
Avg Results
Avg Tokens
Avg Time
DeepSeek-V2-Lite
12.7
±
2.91
12.7\pm 2.91
10.0
±
2.9
10.0\pm 2.9
3.4
±
1.3
3.4\pm 1.3
6.4
±
2.5
6.4\pm 2.5
NA
NA
Llama3-8B
18.9
±
11.9
18.9\pm 11.9
10.1
±
5.6
10.1\pm 5.6
1.8
±
1.2
1.8\pm 1.2
7.8
±
4.5
7.8\pm 4.5
NA
NA
SPICEPilot
48.4
±
15.0
48.4\pm 15.0
47.1
±
13.1
47.1\pm 13.1
40.7
±
6.3
40.7\pm 6.3
43.7
±
9.3
43.7\pm 9.3
251.5
2.6
AnalogCoder
87.6
±
4.8
87.6\pm 4.8
34.0
±
4.2
34.0\pm 4.2
39.1
±
1.9
39.1\pm 1.9
50.9
±
2.6
50.9\pm 2.6
NA
NA
AnalogCoder-Pro
91.9
±
3.4
91.9\pm 3.4
83.2
±
4.4
83.2\pm 4.4
73.3
±
1.7
73.3\pm 1.7
81.7
±
1.1
81.7\pm 1.1
40.2
2.1
AnalogAgent (Ours)
98.3
±
1.6
\mathbf{98.3\pm 1.6}
87.1
±
2.9
\mathbf{87.1\pm 2.9}
88.7
±
0.9
\mathbf{88.7\pm 0.9}
92.3
±
0.6
\mathbf{92.3\pm 0.6}
32.0
1.3
Table III
.
Ablation study.
A series of ablation studies on the AnalogAgent built on Gemini-2.5-Flash validate the effectiveness of the proposed method by systematically removing individual components of the framework.
Model
Gemini-2.5-Flash
AnalogAgent
(w/o MAS, w/o SEM)
AnalogAgent
(w/ MAS, w/o SEM)
AnalogAgent
(w/o MAS, w/ SEM)
AnalogAgent
Task Level
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Pass@1
Pass@5
Easy
78.3
85.2
82.9
97.7
94.2
100.0
88.8
98.6
100.0
100.0
Medium
60.0
60.0
64.7
80.0
75.3
92.5
56.0
66.2
86.7
99.6
Hard
34.5
41.0
43.7
52.8
68.8
70.9
45.1
54.3
89.8
100.0
Avg
50.4
56.0
63.8
76.8
79.4
87.8
58.6
68.1
92.0
99.9
4.3.
Ablation Studies
To assess the contributions of SEM and MAS, we conduct ablations with Gemini-2.5-Flash under four configurations: (i) the baseline Gemini without agentic famework AnalogAgent; MAS only retains multi-agent system with iteration-level feedback exchange, but disables curator-driven memory updates and playbook retrieval; SEM only enables curator-style rule distillation with playbook-guided generation, but removes multi-agent and operates in a single-agent loop.
As summarized in Table
III
, the removal of both modules results in a clear reduction in the success of analog circuit design automation, with the most pronounced degradation observed in high-complexity tasks. On Hard tasks, Pass@1 decreases from 89.8 in the full framework to 43.7 when both modules are removed, and the overall Avg Pass@1/Pass@5 drops from 92.0/99.9 to 63.8/76.8. The SEM is associated with higher performance on Easy tasks by adding revelant knowledge. Easy-task Pass@1 improves from 78.3 to 88.8 with SEM only and reaches 100.0 in the full model. In contrast, MAS shows a larger effect on Medium and Hard tasks, where multi-agent design patterns assist in resolving complex topological constraints and bias relationships. Medium-task Pass@1 increases from 60.0 to 75.3 with MAS only, while Hard-task Pass@1 increases from 34.5 to 68.8. The full framework yields the strongest results among all variants, demonstrating that short-term refinement and long-term information reuse are jointly necessary and most effective when combined.
Figure 3
.
Self-Improving Refinement Case Study.
The flow shows an error-driven refinement loop for Hard Task 25, in which execution failures are diagnosed, distilled into curator rules, and written into Adaptive Design Playbook to guide subsequent generations and accelerate convergence. Hard Task 25 is an op-amp comparator that outputs high when
V
in
>
V
ref
V_{\text{in}}>V_{\text{ref}}
and low when
V
in
<
V
ref
V_{\text{in}}<V_{\text{ref}}
. The final iterations correct the topology and pin semantics to meet this specification.
Figure 4
.
Cross-Task Transfer across Amplifiers.
Reusable knowledge distilled from the basic Amplifier Task 1 transfers to Tasks 9 and Task 10, improving success rates and demonstrating that long-term memory is effectively reusable across tasks.
4.4.
Self-Improving Refinement Case Study
To better understand the behavior of the proposed framework during circuit synthesis, this section analyzes representative design trajectories and iterative correction patterns. Task 25, an Op-amp Comparator, is selected as an illustrative example to demonstrate the progression from initial failure to a valid solution. As shown in Figure
3
, the process spans 30 iterations, during which successive generations are refined based on execution feedback. Early attempts exhibit library usage errors and netlist construction issues, such as duplicated element definitions. In contrast to baseline frameworks that frequently repeat similar syntax-level mistakes, AnalogAgent shows a progressive reduction of such errors across iterations. Execution feedback highlights concrete problems, which are recorded by the Knowledge Curator as reusable correction rules, including ensuring unique identifiers for MOSFET instances and passing subcircuit objects rather than string labels. In later iterations, the generated topology and pin connections conform to the comparator specification, with
V
o
​
u
​
t
V_{out}
switching behavior aligned with the condition
V
i
​
n
=
V
r
​
e
​
f
V_{in}=V_{ref}
. Notably, AnalogAgent attains a final Pass@1 of 86.7 on Task 25, representing a substantial accuracy improvement over other frameworks on this high-difficulty case.
Throughout the iteration, AnalogAgent first learns the exact number and ordering of positional arguments needed to instantiate each subcircuit topology. When generating the corresponding netlist, it enforces globally unique instance identifiers within each scope to avoid name collisions and to ensure a one-to-one mapping between devices and their stamped mathematical objects during SPICE equation assembly. Building on these rules, AnalogAgent then generates a hierarchical comparator: it defines the “Opamp” subcircuit with a consistent pin order, and then instantiates it at the top level with correctly named, fully connected pins, including supplies and references, yielding a SPICE-simulatable circuit.
4.5.
Case Study: Cross-Task Knowledge Transfer
The cumulative experience further supports convergence on related tasks through cross-task reuse of previously recorded design information. For example, information derived from Basic Task 1 regarding explicit supply definition and bulk-tie conventions is retrieved by the Adaptive Design Playbook when addressing Medium Tasks 9 and 10. As illustrated in Figure
4
, such reuse preserves consistent biasing strategies and interface naming conventions across tasks, thereby narrowing the range of candidate designs explored for more complex circuits. By incorporating feedback from unsuccessful attempts into updated Playbook entries, the framework replaces isolated sampling with a process guided by stored diagnostic information.
During the generation for Task 1, AnalogAgent learns and retains the circuit-construction grammar required for SPICE netlisting. Concretely, it internalizes the physical pin ordering and connectivity rules for each primitive; for instance, a MOSFET instance is specified in the order of unique identifier, drain, gate, source, body, model name, length, and width, while passive elements require valid two-terminal node connections. It also learns the need for unique instance names (e.g., M1, R1, Vdd) to avoid identifier collisions during parsing and device stamping in simulation. With this foundational “syntax + wiring” knowledge established in Task 1, which implements a simple NMOS pull-down with a resistive pull-up and a safety resistor, the agent transfers the same rules to more complex topologies in Task 9 and Task 10.
For Task 9, it reuses the MOSFET netlisting template and expands from a single-stage inverter-like behavior to a two-stage biased CMOS structure by introducing intermediate nodes (Vint1), bias sources (Vbias1, Vbias2), complementary PMOS loads, and a coupling capacitor (Cc), while preserving correct pin order, valid node naming, and model references. For Task 10, it again applies the same instantiation rule-set to generate a regenerative/inverter-style topology (NMOS pull-down plus diode-connected or feedback PMOS load), ensuring the feedback connection, where M2 gate is tied to Vout, remains physically meaningful and simulatable. Overall, AnalogAgent’s workflow reflects a progressive transfer from syntax correctness to connectivity consistency and then to topology composition: it first learns how to write valid device lines and assign instance names in Task 1, and subsequently reuses this knowledge to reduce trial-and-error iterations when assembling larger hierarchical or multi-device circuits in Tasks 9 and 10, thereby focusing the remaining search on architectural choices such as biasing, intermediate nodes, and feedback rather than re-learning netlist formatting from scratch.
4.6.
Agentic Reasoning with "Small" LLMs
Commercial IC design often cannot use APIs to access cloud-hosted LLMs because PDKs are proprietary and protected under non-disclosure agreements (NDAs). Therefore, it is important to maintain agent efficiency even when using smaller models, which are more suitable for on-premises or locally hosted servers.
To this end, we replace the backbone LLMs with compact open-weight models (i.e.,
Qwen3-1.7B
,
Qwen3-4B-Instruct
,
Qwen3-8B
, and
Qwen3-14B
) while keeping the agentic workflows unchanged.
As shown in Fig.
5
, AnalogAgent achieves higher success rates and solves more tasks than both AnalogCoder-Pro and the corresponding base models on all LLM scales. At the 1.7B scale, Pass@1 improves from 2.4 to 22.2. At 4B and 8B, Pass@1 improves from 28.2
→
\rightarrow
62.3 and 23.3
→
\rightarrow
72.1, respectively. At 14B, Pass@1 further improves from 35.3
→
\rightarrow
76.7. In contrast, AnalogCoder-Pro does not consistently improve performance on compact LLMs and can even degrade performance in certain cases (e.g., Qwen3-14B). Overall, improvements remain consistent across model scales and become more pronounced for larger backbones, indicating that execution-driven feedback and Self-Evolving Memory amplify, rather than substitute for, backbone model capacity. Full results are reported in
A
ppendix
G
.
These findings lend empirical support to the potential of small agents as an efficiency-oriented strategy for practical deployments
(
2
)
and further underscore that the benefits of AnalogAgent are not merely a consequence of scaling the backbone model, but arise from the agentic reasoning of iterative feedback and the accumulation and retrieval of reusable design knowledge.
From a practical standpoint, this suggests a cost-effective path for industry adoption, as many organizations prefer to deploy compact open-weight models on local servers for privacy, controllability, and reduced inference cost.
Figure 5
.
Performance comparison of Qwen base models, AnalogCoder-Pro, and AnalogAgent. AnalogAgent consistently enhances compact Qwen models across all model scales.
5.
Conclusion and Future Work
In this work, we propose a training-free agentic framework for analog circuit design automation that seamlessly integrates an LLM-based multi-agent system with a self-evolving memory mechanism.
By learning an Adaptive Design Playbook that accumulates reusable design knowledge, AnalogAgent effectively mitigates context attrition and surpasses existing baselines without relying on pre-specified expert knowledge, curated circuit libraries, or external databases. Notably, AnalogAgent substantially improves performance for small open-weight LLMs, spanning 1.7B to 14B Qwen models, indicating that high-quality design reasoning can be achieved even with compact backbones.
Looking ahead, this framework opens several avenues for advancing LLM-driven analog design. Future work will expand the evaluation to more complex analog circuits and broader real-world constraints, and will establish new benchmarks that better reflect practical design scenarios.
References
Agrawal
et al.
(2025)
L. A. Agrawal, S. Tan, D. Soylu, N. Ziems, R. Khare, K. Opsahl-Ong, A. Singhvi, H. Shandilya, M. J. Ryan, M. Jiang,
et al.
Gepa: reflective prompt evolution can outperform reinforcement learning
.
arXiv preprint arXiv:2507.19457
.
Cited by:
§3.3
.
Belcak
et al.
(2025)
P. Belcak, G. Heinrich, S. Diao, Y. Fu, X. Dong, S. Muralidharan, Y. C. Lin, and P. Molchanov
Small language models are the future of agentic ai
.
arXiv preprint arXiv:2506.02153
.
Cited by:
§4.6
.
Budak
et al.
(2021)
A. F. Budak, P. Bhansali, B. Liu, N. Sun, D. Z. Pan, and C. V. Kashyap
Dnn-opt: an rl inspired optimization for analog circuit sizing using deep neural networks
.
In
2021 58th ACM/IEEE Design Automation Conference (DAC)
,
pp. 1219–1224
.
Cited by:
§2.1
.
Budak
et al.
(2023)
A. F. Budak, D. Smart, B. Swahn, and D. Z. Pan
APOSTLE: asynchronously parallel optimization for sizing analog transistors using dnn learning
.
In
Proceedings of the 28th Asia and South Pacific Design Automation Conference
,
pp. 70–75
.
Cited by:
§1
,
§2.1
.
Chang
et al.
(2024)
C. Chang, Y. Shen, S. Fan, J. Li, S. Zhang, N. Cao, Y. Chen, and X. Zhang
Lamagic: language-model-based topology generation for analog integrated circuits
.
arXiv preprint arXiv:2407.18269
.
Cited by:
§2.2
.
Chen
et al.
(2024)
Z. Chen, J. Huang, Y. Liu, F. Yang, L. Shang, D. Zhou, and X. Zeng
Artisan: automated operational amplifier design via domain-specific large language model
.
In
Proceedings of the 61st ACM/IEEE Design Automation Conference
,
pp. 1–6
.
Cited by:
§2.2
.
Choi
et al.
(2023)
M. Choi, Y. Choi, K. Lee, and S. Kang
Reinforcement learning-based analog circuit optimizer using g m/i d for sizing
.
In
2023 60th ACM/IEEE Design Automation Conference (DAC)
,
pp. 1–6
.
Cited by:
§2.1
.
Dong
et al.
(2023)
Z. Dong, W. Cao, M. Zhang, D. Tao, Y. Chen, and X. Zhang
CktGNN: circuit graph neural network for electronic design automation
.
arXiv preprint arXiv:2308.16406
.
Cited by:
§2.2
.
Frazier (2018)
P. I. Frazier
A tutorial on bayesian optimization
.
arXiv preprint arXiv:1807.02811
.
Cited by:
§3.5
.
Gao
et al.
(2025)
J. Gao, W. Cao, J. Yang, and X. Zhang
AnalogGenie: a generative engine for automatic discovery of analog circuit topologies
.
arXiv preprint arXiv:2503.00205
.
Cited by:
§2.2
.
Gray
et al.
(2024)
P. R. Gray, P. J. Hurst, S. H. Lewis, and R. G. Meyer
Analysis and design of analog integrated circuits
.
John Wiley & Sons
.
Cited by:
§1
.
Lai
et al.
(2025a)
Y. Lai, S. Lee, G. Chen, S. Poddar, M. Hu, D. Z. Pan, and P. Luo
Analogcoder: analog circuit design via training-free code generation
.
In
Proceedings of the AAAI Conference on Artificial Intelligence
,
Vol.
39
,
pp. 379–387
.
Cited by:
§B.1
,
§1
,
§2.2
,
§3.3
,
§4.1
,
§4.1
,
§4.1
.
Lai
et al.
(2025b)
Y. Lai, S. Poddar, S. Lee, G. Chen, M. Hu, B. Yu, P. Luo, and D. Z. Pan
Analogcoder-pro: unifying analog circuit generation and optimization via multi-modal llms
.
arXiv preprint arXiv:2508.02518
.
Cited by:
§B.1
,
§1
,
§2.2
,
§3.3
,
§3.5
,
§4.1
,
§4.1
,
§4.1
.
Li
et al.
(2021)
Y. Li, Y. Lin, M. Madhusudan, A. Sharma, S. Sapatnekar, R. Harjani, and J. Hu
A circuit attention network-based actor-critic learning approach to robust analog transistor sizing
.
In
2021 ACM/IEEE 3rd Workshop on Machine Learning for CAD (MLCAD)
,
pp. 1–6
.
Cited by:
§2.1
.
Liu
et al.
(2025)
B. Liu, H. Zhang, X. Gao, Z. Kong, X. Tang, Y. Lin, R. Wang, and R. Huang
Layoutcopilot: an llm-powered multi-agent collaborative framework for interactive analog layout design
.
IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems
.
Cited by:
§2.2
.
Liu
et al.
(2009)
B. Liu, Y. Wang, Z. Yu, L. Liu, M. Li, Z. Wang, J. Lu, and F. V. Fernández
Analog circuit optimization system based on hybrid evolutionary algorithms
.
Integration
42
(
2
),
pp. 137–148
.
Cited by:
§1
,
§2.1
.
Liu
et al.
(2024)
C. Liu, Y. Liu, Y. Du, and L. Du
Ladac: large language model-driven auto-designer for analog circuits
.
Authorea Preprints
.
Cited by:
§2.2
.
Lu
et al.
(2023)
J. Lu, Y. Li, F. Yang, L. Shang, and X. Zeng
High-level topology synthesis method for
Δ
\Delta
-
Σ
\Sigma
modulators via bi-level bayesian optimization
.
IEEE Transactions on Circuits and Systems II: Express Briefs
70
(
12
),
pp. 4389–4393
.
Cited by:
§2.1
.
Maulik
et al.
(2002)
P. C. Maulik, L. R. Carley, and R. A. Rutenbar
Integer programming based topology selection of cell-level analog circuits
.
IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems
14
(
4
),
pp. 401–412
.
Cited by:
§2.1
.
McConaghy
et al.
(2007)
T. McConaghy, P. Palmers, G. Gielen, and M. Steyaert
Simultaneous multi-topology multi-objective sizing across thousands of analog circuit topologies
.
In
Proceedings of the 44th annual Design Automation Conference
,
pp. 944–947
.
Cited by:
§1
,
§2.1
.
McConaghy
et al.
(2008)
T. McConaghy, P. Palmers, G. Gielen, and M. Steyaert
Automated extraction of expert knowledge in analog topology selection and sizing
.
In
2008 IEEE/ACM International Conference on Computer-Aided Design
,
pp. 392–395
.
Cited by:
§2.1
.
Oh
et al.
(2024)
Y. Oh, D. Kim, Y. H. Lee, and B. Hwang
CRONuS: circuit rapid optimization with neural simulator
.
In
2024 Design, Automation & Test in Europe Conference & Exhibition (DATE)
,
pp. 1–6
.
Cited by:
§2.1
.
Palmers
et al.
(2009)
P. Palmers, T. McConnaghy, M. Steyaert, and G. Gielen
Massively multi-topology sizing of analog integrated circuits
.
In
2009 Design, Automation & Test in Europe Conference & Exhibition
,
pp. 706–711
.
Cited by:
§1
,
§2.1
.
Poddar
et al.
(2024)
S. Poddar, A. Budak, L. Zhao, C. Hsu, S. Maji, K. Zhu, Y. Jia, and D. Z. Pan
A data-driven analog circuit synthesizer with automatic topology selection and sizing
.
In
2024 Design, Automation & Test in Europe Conference & Exhibition (DATE)
,
pp. 1–6
.
Cited by:
§1
,
§2.1
.
Poddar
et al.
(2025)
S. Poddar, Y. Oh, Y. Lai, H. Zhu, B. Hwang, and D. Z. Pan
INSIGHT: a universal neural simulator framework for analog circuits with autoregressive transformers
.
In
2025 62nd ACM/IEEE Design Automation Conference (DAC)
,
pp. 1–7
.
Cited by:
§2.1
.
Settaluri
et al.
(2020)
K. Settaluri, A. Haj-Ali, Q. Huang, K. Hakhamaneshi, and B. Nikolic
Autockt: deep reinforcement learning of analog circuit designs
.
arXiv preprint arXiv:2001.01808
.
Cited by:
§2.1
.
Shi
et al.
(2025)
Y. Shi, Z. Tao, Y. Gao, T. Zhou, C. Chang, Y. Wang, B. Chen, G. Zhang, A. Liu, Z. Yu,
et al.
AMSnet-kg: a netlist dataset for llm-based ams circuit auto-design using knowledge graph rag
.
ACM Transactions on Design Automation of Electronic Systems
30
(
6
),
pp. 1–37
.
Cited by:
§2.2
.
Suzgun
et al.
(2025)
M. Suzgun, M. Yuksekgonul, F. Bianchi, D. Jurafsky, and J. Zou
Dynamic cheatsheet: test-time learning with adaptive memory
.
arXiv preprint arXiv:2504.07952
.
Cited by:
§3.3
.
Veselinovic
et al.
(1995)
P. Veselinovic, D. Leenaerts, W. Van Bokhoven, F. Leyn, F. Proesmans, G. Gielen, and W. Sansen
A flexible topology selection program as part of an analog synthesis system
.
In
Proceedings the European Design and Test Conference. ED&TC 1995
,
pp. 119–123
.
Cited by:
§2.1
.
Vungarala
et al.
(2024)
D. Vungarala, S. Alam, A. Ghosh, and S. Angizi
Spicepilot: navigating spice code generation and simulation with ai guidance
.
In
2024 IEEE International Conference on Rebooting Computing (ICRC)
,
pp. 1–6
.
Cited by:
§1
,
§2.2
,
§4.1
.
Wang
et al.
(2020)
H. Wang, K. Wang, J. Yang, L. Shen, N. Sun, H. Lee, and S. Han
GCN-rl circuit designer: transferable transistor sizing with graph neural networks and reinforcement learning
.
In
2020 57th ACM/IEEE Design Automation Conference (DAC)
,
pp. 1–6
.
Cited by:
§1
,
§2.1
.
Yin
et al.
(2024)
Y. Yin, Y. Wang, B. Xu, and P. Li
Ado-llm: analog design bayesian optimization with in-context learning of large language models
.
In
Proceedings of the 43rd IEEE/ACM International Conference on Computer-Aided Design
,
pp. 1–9
.
Cited by:
§1
,
§2.2
.
Zhang
et al.
(2025a)
H. Zhang, S. Sun, Y. Lin, R. Wang, and J. Bian
Analogxpert: automating analog topology synthesis by incorporating circuit design expertise into large language models
.
In
2025 International Symposium of Electronics Design Automation (ISEDA)
,
pp. 772–777
.
Cited by:
§2.2
.
Zhang
et al.
(2025b)
Q. Zhang, C. Hu, S. Upasani, B. Ma, F. Hong, V. Kamanuru, J. Rainton, C. Wu, M. Ji, H. Li,
et al.
Agentic context engineering: evolving contexts for self-improving language models
.
arXiv preprint arXiv:2510.04618
.
Cited by:
§3.3
.
Zhao and Zhang (2020)
Z. Zhao and L. Zhang
An automated topology synthesis framework for analog integrated circuits
.
IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems
39
(
12
),
pp. 4325–4337
.
Cited by:
§2.1
.
Appendix A
Definitions and Notations
Table IV.
Definitions and Notations.
Notations are organized following the execution pipeline of AnalogAgent.
Notation
Definition
S
S
Circuit specification (task description and pass criteria).
g
i
g_{i}
Sub-goal at iteration
i
i
.
K
K
Max attempts per task (iteration budget).
N
N
Number of benchmark tasks.
M
M
Long-term memory of reusable rules and fixes.
E
i
E_{i}
Retrieved memory entries at iteration
i
i
.
Δ
i
\Delta_{i}
Prompt directives distilled from
E
i
E_{i}
.
𝒫
i
\mathcal{P}_{i}
Adaptive Design Playbook assembled at iteration
i
i
.
F
i
F_{i}
Generated executable design script at iteration
i
i
.
L
i
L_{i}
Execution feedback from running
F
i
F_{i}
.
O
i
O_{i}
Aggregated execution evidence up to iteration
i
i
.
V
⁡
(
⋅
)
V(\cdot)
Validator for constraint and functional checks.
v
i
v_{i}
Validation result at iteration
i
i
.
m
i
m_{i}
Failure message if
v
i
v_{i}
is false.
C
⁡
(
⋅
)
C(\cdot)
Constraint checker for structural/API/naming constraints.
c
i
c_{i}
Checker outcome at iteration
i
i
(pass/fail and/or violations).
P
⁡
(
⋅
)
P(\cdot)
Simulation procedure (e.g., operating point, DC sweep, transient).
W
i
W_{i}
Waveform evidence at iteration
i
i
(if applicable).
δ
i
\delta_{i}
Targeted fix suggested by the Design Optimizer.
r
i
r_{i}
Curated rule written back to memory.
f
success
f_{\text{success}}
Whether the task is solved.
T
TTFS
T_{\text{TTFS}}
Time-to-first-success (elapsed time until first verified success).
CSR
(k)
Cumulative success rate within the first
k
k
attempts.
Appendix B
DATA AND REPRODUCIBILITY
This appendix first details the construction, collection, preprocessing, and standardization of the domain-specific benchmark dataset,
and then describes the reproducible experimental configuration used in this work.
Both the implementation code and benchmark data are released via an anonymous artifact repository to support
independent verification, trajectory reconstruction, and full experimental reproduction.
B.1.
Domain-Specific Data Integration
Table V
.
Benchmark Descriptions. Difficulties are distinguished by background colors
(
easy
,
medium
, and
hard
).
Id
Type
Circuit Description
Id
Type
Circuit Description
1
Amplifier
Single-stage CS amplifier with resistive load
16
Oscillator
RC phase-shift oscillator
2
Amplifier
Three-stage CS amplifier with resistive loads
17
Oscillator
Wien Bridge oscillator
3
Amplifier
Common-drain (source follower) amplifier
18
Integrator
Op-amp integrator
4
Amplifier
Single-stage common-gate amplifier
19
Differentiator
Op-amp differentiator
5
Amplifier
Single-stage NMOS cascode amplifier
20
Adder
Op-amp adder
6
Inverter
NMOS inverter with resistive load
21
Subtractor
Op-amp subtractor
7
Inverter
CMOS logical inverter
22
Schmitt
Non-inverting Schmitt trigger
8
CurrentMirror
NMOS constant current source
23
VCO
Voltage-controlled oscillator
9
Amplifier
Two-stage amplifier with Miller compensation
24
PLL
Phase-locked loop
10
Amplifier
CS amplifier with diode-connected PMOS load
25
Comparator
Op-amp comparator
11
Opamp
Differential op-amp with PMOS mirror load
26
Filter
Passive low-pass filter
12
CurrentMirror
Cascode current mirror
27
Filter
Passive high-pass filter
13
Opamp
Single-stage differential CS op-amp
28
BandPass
Passive band-pass filter
14
Opamp
Two-stage differential op-amp with active loads
29
BandStop
Passive band-stop filter
15
Opamp
Telescopic cascode op-amp
30
Mixer
Gilbert cell mixer
Dataset Origin and Domain-Specific Motivation.
The benchmark used in this work is constructed from domain-specific analog circuit design datasets originally introduced in prior LLM-based analog design frameworks, including AnalogCoder
(
12
)
and AnalogCoder-Pro
(
13
)
. These prior works established curated benchmark suites for evaluating code-generation-based circuit synthesis under executable simulation constraints.
Analog circuit design represents a highly domain-specific scientific workflow, where usable data must capture circuit topology, device-level behavior, simulation constraints, and verification criteria simultaneously. General-purpose code corpora or synthetic programming datasets cannot provide sufficient supervision signals for executable circuit synthesis. As a result, the benchmark follows a domain-specific data design principle, emphasizing executable validity, simulator-grounded feedback, and physics-consistent verification signals.
Data Collection and Integration.
The final benchmark consists of 30 circuit synthesis tasks derived by consolidating and extending task instances from the AnalogCoder and AnalogCoder-Pro benchmark suites. Task definitions were collected from publicly described benchmark configurations and reconstructed into a unified task specification format. The integrated benchmark spans multiple circuit families, including amplifiers, current mirrors, op-amps, oscillators, filters, comparators, and mixed-signal building blocks.
During integration, task definitions were normalized to ensure consistent specification structure, verification criteria, and execution interfaces. When multiple source benchmarks contained semantically overlapping circuit types, representative task variants were selected based on topology diversity and simulation difficulty, ensuring coverage across open-loop, closed-loop, and multi-block circuit categories.
Data Preprocessing and Normalization.
All collected task specifications were preprocessed to ensure compatibility with a unified execution and evaluation pipeline. Preprocessing includes:
•
Standardizing circuit specification format, including required node naming conventions and interface definitions;
•
Normalizing simulation configuration, including DC operating point setup, transient analysis configuration, and sweep parameter definitions;
•
Converting verification criteria into executable checker logic, enabling automated pass/fail evaluation;
•
Aligning device model references and simulation library dependencies across tasks.
These preprocessing steps ensure that all tasks can be executed under identical runtime orchestration conditions, eliminating evaluation variance introduced by heterogeneous simulation setups.
Data Management and Artifact Organization.
All benchmark tasks are managed using a per-task workspace design. Each workspace stores structured artifacts including task specifications, generated design scripts, simulator execution logs, verification outputs, and optional waveform visualizations. This artifact-level management enables full reconstruction of execution trajectories and supports detailed failure diagnosis analysis.
Structured logging is used to record iteration-level execution evidence, including simulator convergence behavior, checker violations, and runtime error signatures. This design ensures that both successful and unsuccessful trajectories can be analyzed systematically.
Data Analysis and Evaluation Signals.
Benchmark performance is analyzed using execution-grounded metrics computed across all tasks under a fixed iteration budget. Primary evaluation metrics include Pass@
k
k
, cumulative success rate, and Time-to-First-Success. In addition, structured execution evidence is used to analyze failure modes, convergence behavior, and repair effectiveness across iterations.
For waveform-sensitive circuits such as oscillators and transient-dependent designs, waveform outputs are additionally generated and used for functional verification and diagnostic interpretation. These signals provide domain-specific evaluation evidence beyond static code correctness.
Extension Beyond Prior Benchmarks.
The benchmark used in this work is constructed by consolidating domain-specific circuit synthesis tasks from AnalogCoder and AnalogCoder-Pro into a unified specification and execution framework.
The primary contribution is not the introduction of new benchmark tasks, but the standardization of execution interfaces, verification pipelines, and evaluation protocols, enabling systematic study of execution-driven iterative circuit synthesis under a multi-agent feedback-repair paradigm.
This unified configuration enables consistent evaluation of code generation quality, execution-grounded diagnosis, and iterative repair effectiveness across heterogeneous model backbones and runtime settings.
As shown in Table
V
, the benchmark consists of 30 domain-specific circuit synthesis tasks spanning multiple circuit families. Difficulty labels are assigned based on circuit topology complexity, feedback structure, and sensitivity to simulation convergence behavior.
B.2.
Implementation and Reproducible Experimental Configuration
This section summarizes key implementation mechanisms and runtime configurations required to reproduce the AnalogAgent experimental pipeline. Detailed source code, runtime scripts, and reproduction instructions are provided in the anonymous artifact repository on github:
https://github.com/artifact-repro/analogagent-artifact
Execution Environment and Reproducibility.
All experiments were conducted on Ubuntu 20.04.6 LTS with Python 3.10 using a dedicated Conda environment.
The machine learning runtime stack includes CUDA-enabled PyTorch, vLLM for high-throughput inference serving,
and Transformers-based model integration. Experiments were executed on a dual-GPU workstation equipped with
two NVIDIA RTX A6000 GPUs using CUDA 12.4 and NVIDIA driver 550.54.
To ensure reproducibility, all experiments were executed under fixed iteration budgets and standardized task
specifications. Random seeds were fixed where applicable. For each task, the system records intermediate artifacts
including generated design scripts, execution logs, verification outputs, and waveform plots when required.
These artifacts enable full reconstruction of execution trajectories for both successful and unsuccessful runs,
supporting detailed failure analysis and independent verification.
Execution-Driven Multi-Agent Runtime.
AnalogAgent is implemented as an execution-grounded multi-agent orchestration pipeline operating on executable circuit artifacts. The runtime integrates specification-conditioned code generation, structured execution feedback collection, rule-level retrieval from Self-Evolving Memory (SEM), and curator-controlled rule consolidation. Internal prompts act as structured interfaces for transporting sub-goals, execution observations, and retrieved rule-level constraints rather than as standalone knowledge sources. Circuit-domain constraints and repair heuristics are stored in SEM and injected through the Adaptive Design Playbook during runtime.
During each iteration, the runtime constructs a task-specific instruction context combining circuit specification, current sub-goal derived from execution observations, and retrieved rule-level SEM entries. Execution feedback including simulator logs, checker outputs, operating-point diagnostics, and waveform evidence is normalized into structured observations and consumed by the Design Optimizer and Knowledge Curator for targeted repair and rule consolidation.
Multi-Backbone Support.
AnalogAgent is backbone-agnostic and supports both local open-weight inference and API-based inference. Local experiments use vLLM-based serving, while cloud inference uses vendor SDK integrations. Evaluated backbone families include Qwen3 series (local deployment), Gemini API models, and GPT-series API models. All models are evaluated under identical task settings, iteration budgets, and execution-feedback pipelines.
Appendix C
ANALOGAGENT INFERENCE WORKFLOW
This appendix details the end-to-end inference workflow of AnalogAgent, describing how multi-agent execution feedback, Self-Evolving Memory (SEM), and Adaptive Design Playbook–guided generation interact during iterative circuit synthesis.
C.1.
System Overview and Core Components
AnalogAgent is an execution-driven agentic framework for automated analog circuit design. The system couples iterative code execution, multi-agent diagnosis, and long-term experience accumulation to improve correctness, robustness, and convergence efficiency across heterogeneous circuit tasks.
At a high level, AnalogAgent operates through three tightly coupled layers:
(1) Self-Evolving Memory (SEM).
SEM is a persistent rule-level long-term memory that stores curated and transferable knowledge distilled from historical execution trajectories. Instead of storing raw traces or full prompts, SEM maintains compact structured rules such as validated repair patterns, topology-specific constraints, and stable checker-compliant design practices. SEM corresponds to the long-term memory
M
M
used during inference.
(2) Adaptive Design Playbook.
The Adaptive Design Playbook is a per-iteration instruction layer constructed dynamically by retrieving relevant entries from SEM and combining them with iteration-specific design constraints. The playbook contains:
(i)
Design Instruction
, which encodes task-specific requirements such as node naming, supply conventions, and functional verification constraints; and
(ii)
Relevant Knowledge
, which includes transferable experience such as previously validated fixes and task-type-specific heuristics.
The playbook therefore acts as a task-conditioned operational view over SEM.
(3) Multi-Agent System (MAS).
AnalogAgent adopts a tight, three-agent refinement loop operating over executable artifacts and execution traces at runtime:
•
Code Generator Agent:
Generates executable PySpice circuit implementation and testbench code conditioned on the specification and playbook directives.
•
Design Optimizer Agent:
Diagnoses execution failures using structured signals such as checker outputs, simulation diagnostics, and waveform evidence, and proposes concrete, targeted fix directives.
•
Knowledge Curator Agent:
Converts evidence-backed fixes into transferable rule entries through filtering, conflict checking, and deduplication before writing them into SEM.
To control computational cost and standardize evaluation, each task is associated with a fixed iteration budget (Max Attempts), which caps the number of generate–execute–refine cycles.
C.2.
Execution-Driven Iterative Inference Loop
The AnalogAgent inference procedure follows an iterative design – execute – diagnose – refine cycle.
Sub-goal formation and experience retrieval.
At the beginning of each iteration, the system aggregates execution observations (e.g., checker violations, simulation results, diagnostic messages, and waveform anomalies) together with the original circuit specification to form the next actionable sub-goal. The playbook then retrieves a small set of relevant SEM entries and distills them into concise prompt directives, forming structured delta context injected into the generation prompt.
Executable generation and validation-driven feedback.
Conditioned on the specification and playbook directives, the Code Generator produces an executable PySpice design script. The script is executed to produce multi-source feedback signals, including:
netlist-level structural checks,
operating-point and DC sweep diagnostics,
functional verification outcomes,
and waveform evidence when applicable.
A validation module enforces structural correctness, connectivity integrity, and task-level functional constraints. When validation fails, failure messages are propagated as structured feedback for the next iteration rather than triggering full prompt re-generation.
Failure diagnosis, rule curation, and memory evolution.
The Design Optimizer analyzes full execution trajectories (code, logs, checker output, and waveform evidence) to localize root causes and produce minimal targeted fix directives. The Knowledge Curator then converts evidence-backed fixes into admission-controlled rule entries and writes them into SEM. This separation between short-term iterative refinement and long-term rule consolidation prevents prompt bloat and preserves stable task-specific constraints across successive iterations.
Workspace materialization and traceability.
For reproducibility and debugging, the system materializes per-iteration workspace artifacts, including task specification, sub-goal history, retrieved memory entries, execution logs, waveform plots, and generated executable scripts.
A formal algorithmic description is provided in Algorithm
1
.
C.3.
Multi-Agent Execution Process Visualization
Figure
6
provides a system-level visualization of the multi-agent execution loop. The Code Generator produces executable circuit implementations under specification and playbook guidance. The Design Optimizer closes the execution feedback loop by performing requirement validation, simulation diagnostics, and curve-level waveform analysis when applicable, and converts failure evidence into targeted fix directives. The Knowledge Curator aggregates diverse multimodal execution evidence and writes conflict-checked transferable rules into SEM, enabling cross-iteration and task-level knowledge reuse.
Appendix D
Algorithmic Procedure
Input:
Circuit specification
S
S
Output:
Final executable design script
F
exec
F_{\text{exec}}
and verified outputs
Initialize aggregated observations
O
←
∅
O\leftarrow\emptyset
;
f
success
←
false
f_{\text{success}}\leftarrow\text{false}
;
attempts
←
0
\leftarrow 0
;
while
¬
f
success
\neg f_{\text{success}}
and
attempts
<
K
<K
do
//
Memory-guided planning
Form the next actionable sub-goal
g
g
from
S
S
and
O
O
;
Retrieve relevant memory entries
E
E
(design rules, constraints, and validated repair patterns);
Distill
E
E
into concise directives
Δ
\Delta
;
//
Code generation and execution
Generate executable PySpice script
F
exec
←
CodeGenerator
​
(
S
,
g
,
Δ
)
F_{\text{exec}}\leftarrow\textsc{CodeGenerator}(S,g,\Delta)
;
Execute
F
exec
F_{\text{exec}}
to obtain feedback
L
L
(checker diagnostics, simulation outcomes, and verification signals);
Update observations
O
←
O
∪
{
L
}
O\leftarrow O\cup\{L\}
;
//
Validation and diagnosis
v
,
m
←
Validate
​
(
S
,
O
)
v,m\leftarrow\textsc{Validate}(S,O)
;
if
¬
v
\neg v
then
δ
←
DesignOptimizer
​
(
S
,
F
exec
,
O
,
m
)
\delta\leftarrow\textsc{DesignOptimizer}(S,F_{\text{exec}},O,m)
;
Use
δ
\delta
to guide regeneration in the next iteration;
//
Curation and memory update
if
new actionable evidence is identified
then
r
←
Agent
​
(
S
,
O
,
v
)
r\leftarrow\textsc{Agent}(S,O,v)
;
Write
r
r
into long-term memory and update the playbook;
attempts
←
\leftarrow
attempts
+
1
+1
;
//
Stop criterion
f
success
←
IsSolved
​
(
S
,
O
)
f_{\text{success}}\leftarrow\textsc{IsSolved}(S,O)
;
return
final executable design script and verified outputs
Algorithm 1
AnalogAgent Inference Process
The AnalogAgent inference process is summarized in Algorithm
1
.
Given a circuit specification, the system performs iterative memory-guided synthesis through a
generate–execute–diagnose–refine loop under a fixed attempt budget.
At each iteration, the system constructs an Adaptive Design Playbook by retrieving transferable
rule-level knowledge from Self-Evolving Memory and distilling it into actionable generation
directives. The Code Generator produces an executable circuit implementation conditioned on the
specification and playbook constraints, and execution feedback is collected through structural
checks, simulation diagnostics, and functional verification. When validation fails, the Design
Optimizer proposes localized repair directives that guide regeneration in subsequent iterations.
Evidence-backed repair patterns are optionally consolidated into memory through curator-controlled
filtering and deduplication, enabling cross-task knowledge accumulation without rewriting existing
rules.
The inference loop terminates when a verified design is obtained or when the maximum attempt budget
is reached. Because memory updates are strictly incremental and retrieval is deterministic, the
framework maintains stable constraint conditioning across iterations while allowing new
evidence-backed knowledge to be incorporated over time.
Figure 6
.
AnalogAgent workflow with MAS–SEM coupling.
The system solves each task by iterating an inner
Multi-Agent System (MAS)
loop
(Code Generator
→
\rightarrow
Design Optimizer
→
\rightarrow
Knowledge Curator) over executable PySpice artifacts.
Execution feedback (checker logs, operating-point/DC-sweep diagnostics, and waveform evidence when available)
is used for diagnosis and targeted fixes.
The curator distills evidence-backed rules with conflict checking and deduplication,
writes transferable entries into
Self-Evolving Memory (SEM)
, and the retrieved rules are injected as
playbook-style constraints to guide subsequent iterations and related tasks.
Appendix E
CONTEXT ATTRITION CASE STUDY ON TASK 25)
E.1.
Checkpoint Evidence of Context Attrition
Context Attrition Case Study (Task 25): Checkpoint Evidence
[Representative Iterations]
it1
:
4.1K
prompt tokens
it10
:
2.4K
prompt tokens
it30
:
1.4K
prompt tokens
[Attrition Pattern]
Type-1 (Executable feedback
→
\rightarrow
removed):
simulator-level convergence traces are progressively pruned.
Type-2 (Concrete diagnosis
→
\rightarrow
abstract rule):
failure mode evidence is replaced by generic MOSFET operating principles.
Type-3 (Circuit semantics
→
\rightarrow
surface exception):
the retained context collapses to a Python runtime error without analog debug cues.
[Evidence @it1: Simulator-grounded diagnostics]
--
Failure mode indicator:
‘‘Warning: singular matrix: check nodes vin and vin’’
--
Solver trajectory:
gmin stepping
→
\rightarrow
dynamic gmin stepping
→
\rightarrow
source stepping
--
Termination signals:
‘‘doAnalyses: iteration limit reached’’; ‘‘run simulation(s) aborted’’
[Evidence @it10: Abstracted operating-point rules]
--
Rule-of-thumb constraints:
‘‘ensure
V
G
​
S
>
V
T
​
H
V_{GS}>V_{TH}
’’; ‘‘ensure
V
D
​
S
>
V
G
​
S
−
V
T
​
H
V_{DS}>V_{GS}-V_{TH}
’’
--
Loss:
convergence trace and node-level singularity context no longer retained as an executable debugging trajectory
[Evidence @it30: Surface-level exception]
--
Runtime symptom only:
‘‘KeyError: ‘Source_M1_M2 ’ ’’
--
Loss:
no simulator-level evidence (e.g., singular matrix / stepping / abort reason) to diagnose the original circuit failure
[Conclusion: Context Attrition]
Across iterations, the prompt compresses from it1 to it30 while shifting away from simulator-grounded evidence.
As a result, key task information and diagnostic cues are
no longer retained in full
, leaving an underspecified context that weakens targeted debugging and subsequent corrections.
E.2.
Mechanism and Impact of Context Attrition
In Task 25, context attrition manifests as a shift from simulator-grounded executable feedback (convergence traces) to abstract rule-of-thumb diagnostics and finally to a superficial runtime exception, progressively erasing the domain-specific evidence.
We present a checkpoint-based case study to illustrate context attrition under iterative LLM prompting. On Task 25, the retained context exhibits a pronounced brevity bias, with the prompt tokens shrinking from 4.1k at it1 to 1.4k at it30, a 65.9% reduction relative to it1. This compression is not merely stylistic, as it progressively removes executable feedback that encodes domain-specific debugging value. At it1, the prompt preserves simulator-level evidence, including ngspice convergence traces such as gmin stepping, explicit failure indicators such as singular matrix and check nodes, escalation events such as dynamic gmin stepping failed and starting source stepping, and the termination rationale such as iteration limit reached and simulation aborted. By it10, the prompt is shorter and increasingly abstracts these trajectories into higher-level guidance, retaining task keywords such as Vin, Vref, Vout, sweep, and comparator while omitting parts of the diagnostic chain. By it30, the long-form convergence trace is no longer retained, leaving mainly high-level task framing without the fine-grained simulator feedback required for targeted fixes. These checkpoints concretely demonstrate context attrition, where repeated rewrites compress and smooth specialized diagnostic details, thereby weakening the prompt as a carrier of domain expertise across iterations.
The Case 25 trajectory also demonstrates how failure evidence can be distilled into reusable diagnostic constraints through SEM-mediated consolidation, grounded in concrete runtime observations rather than hypothetical cross-task transfer scenarios.
Appendix F
SELF-EVOLVING MEMORY AND ADAPTIVE DESIGN PLAYBOOK
F.1.
Memory Entry Semantics
Self-Evolving Memory (SEM) stores
transferable diagnostic rules
distilled from execution trajectories, rather than free-form narrative summaries. Each entry is intended to be actionable in subsequent runs: it links an observable
failure signature
(or other salient execution evidence) to a corresponding
corrective heuristic
that can be applied as a localized patch. The primary evidence sources include simulator logs, checker outputs, operating-point and sweep diagnostics, and (when applicable) waveform plots. This evidence-grounded representation encourages precise reuse: later iterations can condition generation on concrete “what to check” and “what to change” guidance under specified observed conditions, instead of re-deriving procedures from scratch.
For consistency and auditability, entries are kept atomic and scoped. Operationally, an entry can be read as a compact mapping:
Trigger
(task type and/or observed signature)
→
\rightarrow
Evidence
(what was observed)
→
\rightarrow
Rule/Patch
(what to enforce or modify)
→
\rightarrow
Applicability
(when the rule should be invoked). Atomic scoping also supports compositional retrieval: a small subset of entries can be assembled into iteration directives without expanding the prompt with broad, loosely relevant text. Importantly, SEM primarily accumulates failure-derived corrective rules rather than full successful circuit designs. Successful designs are used as short-term guidance within the same task but are not directly written into SEM as reusable rules unless they expose transferable structural constraints or stability guarantees. This design choice prevents overfitting memory to task-specific topology details and improves cross-task generalization.
F.2.
Memory Format and Example
Curator-Processed Long-Term Memory Structure Illustration
[General Rules]
- Outputs must be named exactly: Voutp and Vout.
- NMOS bulk must tie to source; PMOS bulk must tie to Vdd.
- CRITICAL API: Never use circuit.add_nodes(); nodes are created implicitly.
- CRITICAL API: Capacitor initial condition must use ic=... (not initial_condition=...).
- Opamp subcircuit interface: exactly three pins (non-inv, inv, out); do not redefine Opamp.
[Task-Type Rules: Comparator]
- Subcircuit pin names must be passed as a single iterable to subcircuit().
- Any circuit.X(...) instantiation requires the subcircuit to be defined/loaded beforehand.
[Task-Type Rules: Oscillator]
- Place each Python statement on its own line (avoid concatenation causing SyntaxError).
- Apply initial conditions to active loop nodes (kickstart), not fixed supply/bias nodes.
- Ensure every node has a DC path to a reference for operating-point convergence.
[Task-Type Rules: Integrator / Differentiator]
- Strictly follow explicit checker constraints on allowed op-amp modeling; prefer task-specific
requirements over generic API rules.
- Keep statement separation strict to avoid SyntaxError.
The box illustrates the curator-processed memory structure used for retrieval, organized into general rules and task-type rules. General rules encode API constraints and invariant circuit conventions, while task-type rules capture failure signatures and corrective constraints commonly observed for a circuit family.
Not all execution experiences are written into SEM. The Knowledge Curator applies admission control before memory insertion. A candidate rule must satisfy at least one of the following criteria:
(i) resolves a repeated failure pattern across iterations,
(ii) enforces checker or simulator constraints violated in multiple attempts,
(iii) represents a stable design practice independent of specific parameter values.
This admission process prevents noisy or task-specific artifacts from polluting long-term memory.
To control memory growth, SEM stores compact rule-level entries rather than full trajectories, and lightweight deduplication and conflict filtering are applied during curation. Retrieval is bounded to a small number of high-relevance entries per iteration.
F.3.
Success vs. Failure Evidence Handling
The workflow produces two categories of reusable information: (i)
evidence-backed repair rules
derived from failures and verification violations, and (ii)
stabilizing patterns
observed in verified runs that help maintain invariants across subsequent iterations. The update policy is intentionally conservative about what is promoted into SEM: only entries that can be stated as transferable constraints or diagnostic procedures, and that are supported by concrete execution evidence, are admitted. In contrast, task-specific incidental details that do not generalize beyond a single run are treated as short-term context (e.g., reference artifacts within the current iteration loop) rather than long-term rules.
This separation supports two objectives. First, failure-driven rules reduce repeated mistakes by encoding specific signatures and fixes (e.g., “operating-point does not converge due to missing DC path”
→
\rightarrow
“add a bias resistor or reference path”). Second, stabilizing patterns from verified executions preserve conventions that are easy to regress under iterative prompting (e.g., required node naming and API usage invariants). In both cases, the decision to store information is guided by transferability and evidence: the system prefers compact, auditable entries that can be retrieved and assembled into iteration directives without inflating the prompt with full code histories.
F.4.
Curator Filtering and Update Policy
The Knowledge Curator enforces a lightweight but explicit admission pipeline before writing to SEM. Candidate entries are first checked for conflicts with invariant conventions (e.g., required node naming and API constraints) and for logical consistency with existing rules. Entries that duplicate recently stored guidance are filtered through semantic de-duplication to avoid accumulating redundant phrasing of the same constraint. Finally, accepted entries are normalized into an itemized representation so that retrieval can remain targeted and compositional.
Table VI
.
Per-task Pass@k performance comparison across small-scale LLM backbones. Results report AnalogCoder, AnalogCoder-Pro, and AnalogAgent performance on 30 benchmark circuit design tasks.
Model (Avg | Solved)
Metric
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
Qwen3-1.7B
Avg: 2.4/10.0 | Sol: 10/30
Pass@1
0
0
0
3.3
3.3
3.3
3.3
0
0
13.3
13.3
3.3
3.3
23.3
3.3
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
Pass@5
0
0
0
16.7
16.7
16.7
16.7
0
0
53.8
53.8
16.7
16.7
76.4
16.7
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
AnalogCoder-Pro (Qwen3-1.7B)
Avg: 3.8/11.0 | Sol: 7/30
Pass@1
0
0
0
3.3
10
0
0
3.3
0
0
26.7
10
6.7
53.3
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
Pass@5
0
0
0
16.7
43.3
0
0
16.7
0
0
81.5
43.3
31
98.6
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
AnalogAgent (Qwen3-1.7B)
Avg: 22.2/37.7 | Sol: 13/30
Pass@1
53.3
0
0
56.7
33.3
80
3.3
33.3
0
90
43.3
83.3
10
76.7
80
0
0
0
0
0
0
0
0
0
0
53.3
0
0
0
0
Pass@5
98.6
0
0
99.1
89.1
99.9
16.7
89.1
0
100
95.5
99.9
43.3
99.9
99.9
0
0
0
0
0
0
0
0
0
0
98.6
0
0
0
0
Qwen3-4B
Avg: 28.2/41.2 | Sol: 13/30
Pass@1
23.3
0
0
56.7
0
66.7
86.7
100
30
100
93.3
66.7
40
70
0
0
0
0
0
0
0
0
0
0
0
0
0
0
86.7
26.7
Pass@5
76.4
0
0
99.1
0
99.8
100
100
85.7
100
100
99.8
93.9
99.9
0
0
0
0
0
0
0
0
0
0
0
0
0
0
100
81.5
AnalogCoder-Pro (Qwen3-4B)
Avg: 27.8/37.3 | Sol: 14/30
Pass@1
70
63.3
0
73.3
3.3
100
83.3
93.3
0
3.3
83.3
86.7
50
100
20
0
0
0
3.3
0
0
0
0
0
0
0
0
0
0
0
Pass@5
99.9
99.7
0
100
16.7
100
100
100
0
16.7
100
100
97.9
100
70.2
0
0
0
16.7
0
0
0
0
0
0
0
0
0
0
0
AnalogAgent (Qwen3-4B)
Avg: 62.3/66.7 | Sol: 20/30
Pass@1
100
100
100
100
100
100
100
100
86.7
100
100
100
100
93.3
83.3
0
0
0
66.7
0
0
0
0
0
0
93.3
70
0
76.7
100
Pass@5
100
100
100
100
100
100
100
100
100
100
100
100
100
100
99.9
0
0
0
99.8
0
0
0
0
0
0
100
99.9
0
99.9
100
Qwen3-8B
Avg: 23.3/42.5 | Sol: 15/30
Pass@1
40
3.3
26.7
60
26.7
43.3
56.7
96.7
3.3
53.3
50
46.7
0
70
63.3
0
0
60
0
0
0
0
0
0
0
0
0
0
0
0
Pass@5
93.9
16.7
81.2
99.5
81.5
95.5
99.1
100
16.7
98.6
97.3
96.6
0
99.9
99.8
0
0
99.5
0
0
0
0
0
0
0
0
0
0
0
0
AnalogCoder-Pro (Qwen3-8B)
Avg: 24.2/45.9 | Sol: 16/30
Pass@1
33.3
43.3
36.7
90
33.3
40
40
96.7
0
6.7
40
56.7
50
66.7
60
0
0
30
3.3
0
0
0
0
0
0
0
0
0
0
0
Pass@5
89.1
95.7
91.8
100
89.1
94
94
100
0
31
94
99.1
97.9
99.8
99.4
0
0
85.7
16.7
0
0
0
0
0
0
0
0
0
0
0
AnalogAgent (Qwen3-8B)
Avg: 72.1/79.5 | Sol: 24/30
Pass@1
100
100
100
100
93.3
100
96.7
100
96.7
100
90
100
100
80
96.7
0
76.7
63.3
100
0
0
50
33.3
0
0
100
93.3
0
93.3
100
Pass@5
100
100
100
100
100
100
100
100
100
100
100
100
100
99.9
100
0
99.9
99.8
100
0
0
97.3
89.1
0
0
100
100
0
100
100
Qwen3-14B
Avg: 35.3/51.7 | Sol: 18/30
Pass@1
90.0
3.3
96.7
83.3
93.3
83.3
96.7
56.7
50.0
76.7
63.3
70.0
63.3
40.0
90.0
0
0
10.0
0
0
0
0
0
0
0
0
0
0
20.0
6.7
Pass@5
100
16.7
100
100
100
100
100
99.1
97.9
100
99.7
99.9
99.7
94.0
100
0
0
43.3
0
0
0
0
0
0
0
0
0
0
70.2
31.0
AnalogCoder-Pro (Qwen3-14B)
Avg: 18.1/39.9 | Sol: 18/30
Pass@1
73.3
53.3
36.7
83.3
30
50
50
10
3.3
3.3
26.7
33.3
23.3
13.3
20
0
0
23.3
3.3
0
6.7
0
0
0
0
0
0
0
0
0
Pass@5
100
98.6
91.8
100
85.7
97.9
97.9
43.3
16.7
16.7
81.5
89.1
76.4
53.8
70.2
0
0
76.4
16.7
0
31
0
0
0
0
0
0
0
0
0
AnalogAgent (Qwen3-14B)
Avg: 76.7/85.7 | Sol: 26/30
Pass@1
100
100
100
100
100
93.3
100
100
96.7
80.0
73.3
100
86.7
80.0
100
66.7
0
100
70.0
66.7
33.3
100
83.3
0
0
100
73.3
0
96.7
100
Pass@5
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
99.8
0
100
99.9
99.8
89.1
100
100
0
0
100
100
0
100
100
Updates are incremental: newly admitted entries are appended as additional rules rather than triggering wholesale rewriting of the memory. This conservative update policy is designed to preserve stable, previously validated conventions while still incorporating new, evidence-backed heuristics as they arise during execution. As a result, the playbook built from retrieved entries remains interpretable and reproducible across iterations: the same core constraints persist, and only localized, verifiable additions are introduced over time.
Appendix G
ADDITIONAL RESULTS ON COMPACT LLMS
Table
VI
reports detailed per-task results under small and mid-scale backbone models. This table is provided to complement the main experimental results and to demonstrate that the performance gains of AnalogAgent are not restricted to large-capacity models, but remain consistent across a wide range of backbone sizes. All models are evaluated under the same iterative execution-driven synthesis pipeline and identical attempt budgets. Pass@
k
k
is computed over iterative attempts rather than independent sampling, and therefore reflects the cumulative probability that a task is solved within the first
k
k
execution-refinement iterations. For each model, “Avg” denotes the average Pass@1 across all tasks, while “Solved” indicates the number of benchmark tasks for which at least one valid solution is found within the maximum attempt budget. Columns 1–30 correspond to individual benchmark tasks. Rows group results by backbone model and framework variant, including the base model, AnalogCoder-Pro, and AnalogAgent.