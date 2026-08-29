HeaRT: A Hierarchical Circuit Reasoning Tree-Based Agentic Framework for AMS Design Optimization
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2511.19669v2 [cs.AI] 26 Mar 2026
HeaRT: A
H
i
e
r
a
rchical Circuit
R
easoning
T
ree-Based Agentic Framework for AMS Design Optimization
Souradip Poddar
Affiliation:
ECE Department, The University of Texas at Austin
Chia-Tung Ho
Affiliation:
NVIDIA Corporation
Ziming Wei
Affiliation:
ECE Department, The University of Texas at Austin
Weidong Cao
Affiliation:
The George Washington University{souradippddr1@,
dpan@ece.}utexas.edu
Haoxing Ren
Affiliation:
NVIDIA Corporation
David Z. Pan
Affiliation:
ECE Department, The University of Texas at Austin
Abstract
Conventional AI-driven AMS design automation algorithms remain constrained by their reliance on high-quality datasets to capture underlying circuit behavior, coupled with poor transferability across architectures, and a lack of adaptive mechanisms.
This work proposes HeaRT, a hierarchical circuit reasoning-based agentic framework for automation loops and a step toward adaptive, human-style design optimization.
HeaRT consistently improves
F
1
,
subcircuits
F_{1,\mathrm{subcircuits}}
by
≥
13.5
%
\geq 13.5\%
and
F
1
,
loops
F_{1,\mathrm{loops}}
by
≥
37.8
%
\geq 37.8\%
over few-shot prompting baselines across multiple LLM backbones on our 40-circuit AMS benchmark of flattened SPICE netlists,
even as circuit complexity increases.
Our experiments further show that HeaRT achieves
≥
3
×
\geq 3\times
faster convergence in incremental design adaptation tasks under specification shifts across diverse optimization approaches, supporting both topology reconfiguration and sizing.
I
Introduction
Analog and mixed-signal (AMS) circuit design remains challenging to automate due to its fully custom flows, intricate trade-offs in deep sub-micron technologies, and the high cost of re-optimization when specifications change.
Conventional Bayesian Optimization (BO) methods
[
44
,
70
,
60
]
offer strong sample efficiency but struggle to scale effectively in complex, high-dimensional design spaces.
Recent learning-based approaches, particularly reinforcement learning (RL)
[
50
,
58
,
40
,
10
,
7
,
16
,
69
,
46
,
55
,
5
]
, demonstrate improved scalability for larger circuits,
yet incur prohibitive simulation costs.
Moreover, their reliance on manually defined functional decompositions or handcrafted sub-block reward formulations limits autonomy and scalability
[
55
,
5
]
.
Being purely data-driven, these models exhibit an inherent
black-box
nature
[
2
]
, hindering their ability to capture circuit intuition or physical causality.
Consequently, they struggle to adapt to incremental architectural changes, often requiring new data collection,
and the lack of explainability of the design trade-offs considered erodes designer confidence in the quality of the results
[
23
]
(Fig.
1
(a)).
Most recently, Large Language Model (LLM)-based methods
[
15
,
66
,
37
,
38
,
51
,
68
,
21
,
19
,
33
,
65
,
14
,
2
]
have shown promise in advancing AMS design automation.
By leveraging reasoning and agentic capabilities, these models can emulate key aspects of human design workflows.
However, current vanilla LLM-based approaches fail to incorporate the
hierarchical cognitive structure underlying expert AMS design
[
48
,
36
,
22
]
,
resulting in unstructured and inconsistent reasoning that limits both their credibility and practical effectiveness (Fig.
1
(b)).
Moreover, existing automation methods lack explicit mechanisms to adaptively balance design reuse and redesign within topology-sizing co-optimization, thereby treating each specification update as a new problem.
In turn, they re-optimize entire circuits from scratch,
leading to
catastrophic forgetting
[
32
]
of previously acquired design knowledge.
In real AMS workflows, many subcircuits are already layout-planned, variation-optimized
[
8
,
9
,
53
,
20
,
11
]
, or even silicon-proven, making such full re-optimization impractical.
This lack of architectural and contextual awareness causes redundant computation, degraded sample efficiency, and inconsistent reliability, limiting the practical deployability of current automation frameworks in industrial design flows.
To fully harness the potential of LLMs
for AMS automation, we propose HeaRT,
a multi-level agentic reasoning framework
that enables reasoning-grounded downstream applications.
HeaRT draws inspiration from the hierarchical abstraction principles inherent to human circuit design, constructing a hierarchical circuit reasoning tree to enable
structured, context-aware reasoning
with query-conditioned traversal paths for improved interpretability and debugging
[
42
]
(Fig.
1
(c)).
Our key contributions are summarized as follows:
Fig. 1
:
An illustration of comparisons of traditional black-box optimization algorithm, vanilla LLM-based approach, and the proposed HeaRT framework for the AMS design task.
Fig. 2
:
Overall workflow of the HeaRT framework.
Left: offline hierarchical circuit reasoning tree construction from SPICE netlists via top-down graph-guided subcircuit identification, hierarchical abstraction, and bottom-up knowledge consolidation.
Middle: query-conditioned traversal and agentic retrieval for AMS design tasks.
Right: topology knowledge database with metric-wise ranking for objective-driven topology retrieval.
•
We develop HeaRT, a multi-level agentic reasoning framework that performs
graph-guided top-down circuit decomposition with hierarchical organization, followed by bottom-up knowledge consolidation into a hierarchical
circuit reasoning tree,
enabling structured, context-aware LLM reasoning for AMS design tasks.
•
We construct a 40-circuit AMS benchmark repository spanning multiple circuit families and complexity tiers, together with expert-annotated ground-truth labels.
The benchmark will be publicly released upon acceptance.
•
We evaluate HeaRT across multiple LLM backbones on this benchmark and show that it consistently boosts
F
1
,
subcircuits
F_{1,\mathrm{subcircuits}}
by
≥
\geq
13.5% and
F
1
,
loops
F_{1,\mathrm{loops}}
by
≥
\geq
37.8% over few-shot prompting baselines.
When integrated with existing optimization algorithms, HeaRT further enables
≥
3
×
\geq 3\times
faster convergence in incremental design-adaptation tasks involving both sizing and topology reconfiguration.
II
Preliminaries
II-A
LLM-Aided AMS Design Automation
The emergence of reasoning-enabled LLMs endowed with multimodal understanding and agentic decision-making capabilities
[
61
,
59
,
30
,
63
,
62
,
64
,
13
,
27
,
49
]
has redefined autonomous problem-solving across diverse domains, motivating their evaluation within EDA.
Critically, expert AMS designers reason about unseen circuit structures through hierarchical cognitive processes of abstraction, analysis, and bottom-up interpretation
[
48
,
36
,
22
]
.
However, existing LLM-based AMS approaches do not explicitly exploit this structured reasoning paradigm, leading to inconsistencies, hallucinations
[
28
]
, and limited reasoning traceability that conflict with the precision, determinism, and verifiability required in circuit design
[
42
]
.
Moreover, recent LLM-aided efforts
[
15
,
66
,
37
,
51
,
68
,
21
,
19
,
33
,
65
,
14
,
2
]
remain task-specific,
often deploying LLMs within narrowly scoped optimization roles rather than leveraging their broader reasoning capabilities.
EEsizer
[
41
]
employs Chain-of-Thought (CoT) reasoning
[
61
]
with simulation-in-the-loop,
operating primarily at the parameter level for sizing rather than structural circuit interpretation.
Similarly,
[
45
]
uses
metric-driven identification of local transistor patterns (e.g., diff pairs, current mirrors),
in contrast to the topology-centric hierarchical abstraction used by human designers,
where structural reasoning precedes consideration of performance metrics.
These limitations highlight the need for structured reasoning frameworks that align LLM capabilities with human design reasoning.
II-B
Structural Interpretation of AMS Circuits
Flattened SPICE netlists represent circuits as a single connectivity graph where devices share arbitrary interconnections,
obscuring the structural organization designers rely on to interpret circuit functionality.
Structural abstraction is therefore necessary for modular analysis and optimization, thereby better unlocking the capabilities of LLM in AMS design.
Existing subcircuit identification methods rely on hand-crafted rule-based
[
1
]
, template library-based
[
39
]
, learning-based
[
34
,
35
]
, or class-specific few-shot approaches
[
47
]
.
These methods remain constrained by template coverage or training data distribution and primarily focus on identifying local transistor patterns.
In this paper, we use the term
subcircuits
to denote modular functional blocks corresponding to the block-level abstractions commonly used by analog designers.
Examples include gain stages in amplifiers;
resistor dividers, error amplifiers, and pass devices in LDO regulators
[
48
]
.
However, given the diversity of analog circuit architectures, automated structural partitioning
to recover high-level functional abstractions remains challenging
[
47
]
,
since electrically coupled fragments hinder independent functional interpretation and disrupt feedback loop relationships.
When correctly identified, such abstractions preserve subcircuit-level functional integrity and expose the modular structure required for hierarchical circuit reasoning and systematic interpretation of circuit blocks and their feedback interactions
[
22
,
36
]
.
To quantitatively evaluate the correctness of subcircuit decomposition and feedback loop identification, we introduce two F1-score-based metrics:
F
1
,
subcircuits
=
2
​
|
𝒮
∩
𝒮
∗
|
|
𝒮
|
+
|
𝒮
∗
|
,
F
1
,
loops
=
2
​
|
ℒ
∩
ℒ
∗
|
|
ℒ
|
+
|
ℒ
∗
|
,
F_{1,\mathrm{subcircuits}}=\frac{2|\mathcal{S}\cap\mathcal{S}^{*}|}{|\mathcal{S}|+|\mathcal{S}^{*}|},\qquad F_{1,\mathrm{loops}}=\frac{2|\mathcal{L}\cap\mathcal{L}^{*}|}{|\mathcal{L}|+|\mathcal{L}^{*}|},
(1)
where
𝒮
∗
\mathcal{S}^{*}
and
𝒮
\mathcal{S}
denote the ground-truth and identified subcircuit sets, respectively, and
ℒ
∗
\mathcal{L}^{*}
and
ℒ
\mathcal{L}
denote the ground-truth and identified feedback loop sets.
A subcircuit match requires agreement in device membership and internal net connectivity,
whereas a feedback loop match requires agreement in participating devices (or hierarchical blocks), loop polarity, and functional role.
II-C
Performance Figure of Merit (FoM)
Given
m
m
normalized performance metrics
{
f
r
​
(
x
)
}
r
=
1
m
\{f_{r}(x)\}_{r=1}^{m}
defined over their acceptable bound intervals
S
r
bound
=
[
L
r
,
H
r
]
S_{r}^{\mathrm{bound}}=[L_{r},H_{r}]
,
with
f
r
​
(
x
)
≥
0
f_{r}(x)\geq 0
indicating satisfaction,
we define the performance Figure of Merit (FoM) as follows:
FoM
⁡
(
x
)
=
∑
r
=
1
m
w
r
​
min
⁡
(
1
,
max
⁡
(
0
,
f
r
​
(
x
)
)
)
,
\mathrm{FoM}(x)=\sum_{r=1}^{m}w_{r}\,\min\!\left(1,\max\!\left(0,f_{r}(x)\right)\right),
(2)
where
w
r
w_{r}
is the weighting factor.
The
max
⁡
(
⋅
)
\max(\cdot)
operator truncates negative values arising from
constraint violation, while the
min
⁡
(
⋅
)
\min(\cdot)
operator bounds
each metric contribution, preventing any single term from
dominating the FoM beyond full satisfaction.
II-D
Design Effort Reuse Under Specification Shift
To complement the performance-centric FoM,
it is also essential to assess how effectively an optimization process preserves prior design effort
in scenarios where incremental design adaptation is preferred over full re-optimization.
In practical AMS workflows, re-optimizing solely for performance under updated specifications, without contextual awareness,
may inadvertently discard valuable prior efforts, such as robustness across PVT corners, device mismatch, and layout parasitics.
Hence, analogous to parameter drift induced by fine-tuning in machine learning literature
[
32
,
31
,
67
]
,
we introduce a design effort reuse score, denoted by
ℛ
effort
\mathcal{R}_{\mathrm{effort}}
, to quantify deviation of design variables under specification shifts within a fixed architecture relative to a previously validated reference design, defined as:
ℛ
effort
=
1
/
M
∑
j
=
1
M
[
1
−
min
(
1
,
|
log
10
(
x
j
/
x
j
(
0
)
)
|
)
]
.
\mathcal{R}_{\mathrm{effort}}={1}/{M}\sum_{j=1}^{M}\Big[1-\min\!\left(1,\left|\log_{10}(x_{j}/x_{j}^{(0)})\right|\right)\Big].
(3)
Here,
M
M
is the number of design variables,
and
x
j
(
0
)
x_{j}^{(0)}
and
x
j
x_{j}
represent the initial and modified values of the
j
j
-th design variable, respectively.
The
min
⁡
(
⋅
,
1
)
\min(\cdot,1)
cap prevents single large deviations from dominating the score.
ℛ
effort
∈
[
0
,
1
]
\mathcal{R}_{\mathrm{effort}}\in[0,1]
, where
1
1
indicates complete parameter reuse within the fixed architecture and
smaller values
reflect substantial deviation from the validated reference design.
III
The HeaRT Framework
Current LLM-based approaches for AMS design fall short of the explainability and structured reasoning exhibited by human design flows, and their opaque, inconsistent reasoning limits trustworthiness and practical deployment.
Inspired by the cognitive process through which human designers analyze, abstract, and interpret circuits, we propose HeaRT as a hierarchical reasoning framework that leverages human-inspired design philosophy to achieve transparent, context-consistent circuit understanding for downstream agentic tasks.
As depicted in Fig.
2
(left),
HeaRT begins with
graph-guided LLM-assisted subcircuit extraction, followed by hierarchical organization and bottom-up architectural knowledge consolidation.
By combining top-down circuit decomposition with bottom-up reasoning, the framework mirrors the hierarchical abstraction principles used in circuit design.
Local metadata provides informative cues, while access to the full netlist as global context maintains semantically consistent multi-level circuit reasoning.
The framework of HeaRT operates through two complementary phases: an offline, one-time knowledge-building stage that constructs the hierarchical circuit reasoning tree (Section
III-A
), and an online, real-time agentic retrieval stage that leverages standard LLM reasoning capabilities while grounding responses in this tree,
enabling structured,
context-grounded inference beyond single-shot full-circuit reasoning
(Section
III-B
).
The following subsections describe each phase in further detail.
To promote reproducibility and further research, we will release HeaRT as an open-source framework upon acceptance.
Fig. 3
:
An illustrative example of HeaRT’s circuit decomposition.
III-A
Hierarchical Circuit Reasoning Tree Construction
This phase constitutes a one-time offline process that constructs a hierarchical circuit reasoning tree directly from raw SPICE netlists,
grounding subsequent agentic retrieval inference tasks.
III-A
1
Graph-Guided Reasoning for Tree Construction
We first transform the SPICE-level circuit netlist into a device–net bipartite graph
G
=
(
V
D
,
V
N
,
E
)
G=(V_{D},V_{N},E)
, where device nodes
V
D
V_{D}
represents circuit components (e.g., transistors, resistors, capacitors), and net nodes
V
N
V_{N}
correspond to unique net names.
Each net node is labeled by its type as
SUPPLY_PORT
,
SIGNAL_PORT
, or
INTERNAL_NET
, and
each edge
e
∈
E
e\in E
encodes a unique device-terminal-net connection.
For decomposition purposes, MOSFETs are simplified to three-terminal devices (
D
,
G
,
S
), omitting body connections.
From this graph, we extract DC-connected components that capture conductive paths between supply rails,
exposing the circuit’s biasing structure commonly used by designers to reason about functional organization.
These components serve as structural cues for LLM-assisted circuit decomposition
into the functional subcircuits defined
in Section
II-B
, with metadata generated via Chain-of-Thought (CoT) reasoning
[
61
]
and in-context examples
[
6
]
as described in Algorithm
1
.
Fig.
3
illustrates an example of this decomposition.
The extracted subcircuits,
𝐒
𝐝𝐞𝐜𝐨𝐦𝐩
\mathbf{S_{decomp}}
, together with their metadata
(e.g.,
subcircuit_ID
,
role_hint
, architectural context, port annotations, etc.),
are provided to a second LLM stage to construct the hierarchical reasoning tree for subsequent bottom-up knowledge consolidation.
III-A
2
Bottom-Up Knowledge Consolidation
In this step, the LLM performs bottom-up hierarchical reasoning from leaf to root,
aggregating subcircuit-level reasoning and propagating structural and functional insights upward through the hierarchy.
Local and global metadata guide
contextual consistency,
enabling the model to interpret each subcircuit’s role relative to its parent and the broader circuit.
At each node, the LLM identifies local feedback loops among its immediate children and assigns unique loop IDs where applicable.
As reasoning progresses upward, annotated netlists with corresponding signal and supply ports are synthesized and stored at each node,
forming consistent
representations across abstraction levels.
Finally, all inferred functional relations are consolidated into the hierarchical circuit reasoning tree for subsequent retrieval during inference.
Algorithm 1
LLM-Assisted Functional Subcircuit Decomposition
1:
Raw SPICE netlist
𝒩
\mathcal{N}
2:
Subcircuits
𝒮
decomp
\mathcal{S}_{\text{decomp}}
enriched with contextual metadata
3:
function
ExtractDCSubcircuits
(
G
G
)
4:
G
DC
←
G_{\text{DC}}\leftarrow
remove all non–DC-conductive terminals (MOS gates, capacitor nodes), then drop isolated nodes
5:
Initialize
ℛ
VDD
←
∅
\mathcal{R}_{\mathrm{VDD}}\leftarrow\emptyset
,
ℛ
GND
←
∅
\mathcal{R}_{\mathrm{GND}}\leftarrow\emptyset
,
D
DCAlive
←
∅
D_{\mathrm{DCAlive}}\leftarrow\emptyset
6:
Perform multi-source BFS on
G
DC
G_{\mathrm{DC}}
from {
VDD
,
GND
}
7:
ℛ
VDD
,
ℛ
GND
←
\mathcal{R}_{\mathrm{VDD}},\,\mathcal{R}_{\mathrm{GND}}\leftarrow
terminals reachable from
VDD
and
GND
, respectively
8:
D
DC
​
alive
←
{
d
=
(
n
1
,
n
2
)
∈
D
∣
(
n
1
∈
ℛ
VDD
∧
n
2
∈
ℛ
GND
)
∨
(
n
2
∈
ℛ
VDD
∧
n
1
∈
ℛ
GND
)
}
D_{\mathrm{DC\,alive}}\leftarrow\{\,d=(n_{1},n_{2})\in D\mid(n_{1}\in\mathcal{R}_{\mathrm{VDD}}\land n_{2}\in\mathcal{R}_{\mathrm{GND}})\;\lor\;(n_{2}\in\mathcal{R}_{\mathrm{VDD}}\land n_{1}\in\mathcal{R}_{\mathrm{GND}})\,\}
9:
𝒮
D
​
C
←
\mathcal{S}_{DC}\leftarrow
connected components formed by DC-alive devices
10:
return
𝒮
D
​
C
\mathcal{S}_{DC}
11:
end
function
12:
function
ProcessResidualAndACComponents
(
G
,
𝒮
D
​
C
G,\mathcal{S}_{DC}
)
13:
G
res
←
G
∖
𝒮
D
​
C
G_{\mathrm{res}}\leftarrow G\setminus\mathcal{S}_{DC}
14:
𝒮
A
​
C
←
\mathcal{S}_{AC}\leftarrow
connected components of
G
res
G_{\mathrm{res}}
15:
return
𝒮
A
​
C
\mathcal{S}_{AC}
16:
end
function
17:
G
⁡
(
V
D
,
V
N
,
E
)
←
NetlistToBipartite
​
(
𝒩
)
G(V_{D},V_{N},E)\leftarrow{\color[rgb]{0,0,1}\textsc{NetlistToBipartite}}(\mathcal{N})
⊳
\triangleright
device–net bipartite graph construction
18:
Annotate each
n
∈
V
N
n\in V_{N}
as
SUPPLY_RAIL
,
SIGNAL_PORT
, or
INTERNAL_NET
⊳
\triangleright
initial net-level metadata
19:
𝒮
D
​
C
←
ExtractDCSubcircuits
​
(
G
)
\mathcal{S}_{DC}\leftarrow{\color[rgb]{0,0,1}\textsc{ExtractDCSubcircuits}}(G)
⊳
\triangleright
DC Connectivity Cues
20:
𝒮
A
​
C
←
ProcessResidualAndACComponents
​
(
G
,
𝒮
D
​
C
)
\mathcal{S}_{AC}\leftarrow{\color[rgb]{0,0,1}\textsc{ProcessResidualAndACComponents}}(G,\,\mathcal{S}_{DC})
21:
𝒫
←
BuildPrompt
​
(
𝒩
,
𝒮
D
​
C
,
𝒮
A
​
C
,
CoT
,
In-Context Exemplars
)
\mathcal{P}\leftarrow{\color[rgb]{0,0,1}\textsc{BuildPrompt}}(\mathcal{N},\,\mathcal{S}_{DC},\,\mathcal{S}_{AC},\,\text{CoT},\,\text{In-Context Exemplars})
22:
O
LLM
←
LLM
​
(
𝒫
)
O_{\mathrm{LLM}}\leftarrow{\color[rgb]{0,0,1}\textsc{LLM}}(\mathcal{P})
⊳
\triangleright
LLM Reasoning for Circuit Decomposition
23:
𝒮
decomp
←
Parse
⁡
(
O
LLM
)
\mathcal{S}_{\mathrm{decomp}}\leftarrow\mathrm{Parse}(O_{\mathrm{LLM}})
24:
return
𝒮
decomp
\mathcal{S}_{\mathrm{decomp}}
III-B
Agentic Retrieval
This phase performs online, real-time agentic traversal and retrieval, grounding LLM reasoning in the hierarchical circuit reasoning tree built during the offline setup.
The retrieval operations are bounded by the tree depth,
reducing exploration overhead and supporting consistent, context-grounded inference.
To reduce token usage while maintaining reasoning accuracy,
we employ context engineering strategies
[
49
]
, including context compression,
local–global context coordination,
and selective context reuse.
III-B
1
Topology Knowledge Database Management
As illustrated in Fig.
2
(right),
we maintain a topology knowledge database in which circuits are organized by functional category.
Each row corresponds to a circuit topology
𝒯
\mathcal{T}
represented by its normalized circuit graph,
while columns correspond to the family-specific performance metrics defined in our circuit-family metric schema (e.g., 3-dB bandwidth, DC gain, and phase margin for OPAMPs; temperature coefficient and startup margin for bandgap references, and so on).
Each topology entry stores a metric-wise rank
r
i
​
(
𝒯
)
r_{i}(\mathcal{T})
that reflects its relative performance capability along metric
i
i
.
The database is initialized and updated using LLM reasoning grounded in analog design literature, including representative circuits and design insights from ISSCC and JSSC publications, as well as standard textbooks
[
48
,
26
]
,
in conjunction with the circuit-family metric schema.
For each topology, the LLM assigns metric-wise rankings along with concise justification cues reflecting expected performance trade-offs.
During updates, the LLM conditions on the current repository context to provide additional grounding and ensure consistency across entries.
New topologies are inserted into existing metric-wise ranking lists via ordered-list insertion, while newly introduced performance metrics are added as new ranking columns and populated accordingly.
New circuit families follow the same ranking procedure under their respective metric schemas.
To support fast lookup,
each topology entry additionally stores a Weisfeiler–Lehman (WL) graph fingerprint
[
52
]
as an auxiliary hash index.
This database
supports task-specific rank-based retrieval during downstream applications.
TABLE I:
Comparison of LLM-Based Methods for Analog and Mixed-Signal (AMS) Design.
Framework
Multiple
Hierarchical
Performance Objective-
Targeted Opt.
Commercial
Types
1
Circuit Reasoning
Driven Topology Opt.
2
Tasks
PDKs
3
Artisan
[
15
]
–
–
∙
\bullet
TR & Sizing
–
ADO-LLM
[
66
]
∙
\bullet
–
–
Sizing Only
∙
\bullet
AnalogCoder
[
37
]
∙
\bullet
–
–
TG
–
Atelier
[
51
]
–
–
∘
\circ
TG
†
& Sizing
∙
\bullet
AnalogXPert
[
68
]
–
–
–
TG
‡
–
AnalogGenie/Lite
[
21
,
19
]
∙
\bullet
–
–
TG & Sizing
–
LEDRO
[
33
]
–
–
–
Sizing Only
–
MenTeR
[
12
]
∙
\bullet
–
∙
\bullet
TG & Sizing
–
ADO-KT
[
45
]
∙
\bullet
–
–
Sizing Only
–
AnaFlow
[
2
]
–
–
–
Sizing Only
–
AnalogCoder-Pro
[
38
]
∙
\bullet
–
∘
\circ
TG & Sizing
–
HeaRT (This Work)
∙
\bullet
∙
\bullet
∙
\bullet
TR & Context-Aware Sizing
∙
\bullet
1
Demonstrates support across multiple AMS circuit families,
2
Supports target performance-conditioned topology optimization,
3
Demonstrates evaluation using commercial foundry PDKs,
†
Topology generation via retrieval followed by template-based mutation rather than synthesizing from scratch,
‡
Retrieved subcircuits from circuit library combined to generate larger composite architectures,
TR
: Topology Retrieval/Selection,
TG
: Topology Generation,
∙
\bullet
Supported,
∘
\circ
Partial, – Not Supported.
III-B
2
Reasoning-Guided and Query-Conditioned Traversal
In this stage, the agent performs a query-conditioned traversal of the hierarchical circuit reasoning tree.
A single LLM pass first assigns query-conditioned relevance weights to every edge using CoT and in-context reasoning.
Before traversal, each node
v
v
is evaluated using the following branch-admission criterion, which determines whether its children should be enqueued during BFS:
Branch_Cut
​
(
v
)
=
\displaystyle\text{Branch\_Cut}(v)=
{
max
u
∈
Children
⁡
(
v
)
⁡
w
(
v
,
u
)
<
τ
stop
or
​
max
u
∈
Children
⁡
(
v
)
​
w
(
v
,
u
)
−
min
u
∈
Children
⁡
(
v
)
<
ϵ
}
,
\displaystyle\left\{\begin{aligned} &\max_{u\in\mathrm{Children}(v)}w_{(v,u)}<\tau_{\mathrm{stop}}\\[4.0pt]
&\text{or}\;\max_{u\in\mathrm{Children}(v)}w_{(v,u)}-\min_{u\in\mathrm{Children}(v)}<\epsilon\end{aligned}\right\},
(4)
where
w
(
v
,
u
)
w_{(v,u)}
is the query-conditioned relevance of child
u
u
,
τ
stop
\tau_{\mathrm{stop}}
halts expansion when all children are weak, and
ϵ
\epsilon
stops expansion when all children are similarly strong (i.e., no dominant direction).
If condition
4
is satisfied at a node
v
v
,
all of its children are marked as non-admissible and therefore never enqueued into the BFS queue.
A BFS from the root then enqueues children only when the Branch_Cut criterion is not met.
Traversal thus naturally terminates either at suppressed nodes or true leaves.
The resulting root-to-terminal traversal paths define query-conditioned priority search regions, guiding the framework toward the most influential design variables for downstream tasks such as sizing optimization or objective-driven retrieval while maintaining full circuit context.
III-B
3
Objective-Driven Retrieval for Topology Optimization
Given a topology optimization task, HeaRT performs query-conditioned BFS traversal
to identify candidate subcircuits for objective-driven retrieval.
For each identified subcircuit, the set of performance objectives
𝒮
\mathcal{S}
is determined through LLM reasoning over the user’s system-level natural language query and the corresponding circuit family-specific performance metric schema defined in the knowledge database,
with the remaining metrics forming the constraint set
𝒰
\mathcal{U}
.
Through an agentic function call, HeaRT locates the corresponding database entries of the identified topologies
using their stored WL
hash indices
and computes an aggregate rank-based Figure of Merit (
FoM
rank
\mathrm{FoM}_{\mathrm{rank}}
) as a fast ranking proxy,
defined as:
min
𝒯
∈
ϕ
⁡
(
𝒰
)
⁡
FoM
rank
​
(
𝒯
)
=
∑
i
∈
𝒮
w
i
×
r
i
​
(
𝒯
)
,
\min_{\mathcal{T}\in\phi(\mathcal{U})}\mathrm{FoM_{rank}}(\mathcal{T})=\sum_{i\in\mathcal{S}}w_{i}\times r_{i}(\mathcal{T}),
(5)
where
w
i
w_{i}
denotes the metric weight and
ϕ
⁡
(
𝒰
)
\phi(\mathcal{U})
the feasible search region constrained by
𝒰
\mathcal{U}
:
ϕ
(
𝒰
)
=
{
𝒯
|
|
r
j
(
𝒯
)
−
r
¯
j
|
≤
ϵ
,
∀
j
∈
𝒰
}
,
\phi(\mathcal{U})=\left\{\mathcal{T}\ \middle|\ |r_{j}(\mathcal{T})-\bar{r}_{j}|\leq\epsilon,\ \forall j\in\mathcal{U}\right\},
(6)
where
r
¯
j
\bar{r}_{j}
denotes the prior rank on the
j
j
-th metric and
ϵ
\epsilon
is a small rank tolerance (set to 3 in our experiments).
If a prior rank is unavailable,
the constraint is ignored, yielding the full search space along that metric dimension.
The top-
k
k
topologies that minimize this score represent promising candidates for the given design goal,
enabling
objective-driven retrieval for topology selection.
IV
Experimental Results
IV-A
Experimental Setup
We evaluate HeaRT’s structural circuit decomposition and feedback loop identification on a curated repository of 40 AMS circuits spanning diverse types and complexity levels (Fig.
4
),
provided as flattened SPICE netlists.
Circuits are categorized into three tiers based on transistor count (excluding digital logic components) as a rough proxy for structural complexity: Simple (
<
20
<20
transistors), Medium (
20
​
–
​
40
20–40
transistors), and Hard (
>
40
>40
transistors).
The repository will be open-sourced upon acceptance.
For this task,
we evaluate HeaRT across a diverse set of LLM backbones spanning
open-source LLMs
(LLaMA-3.3-70B-Instruct
[
25
,
3
]
,
DeepSeek-V3.2
[
17
]
) and proprietary frontier models
(Gemini-2.5 Pro
[
24
]
,
GPT-5
[
54
]
, and
Claude-4.6-Sonnet
[
4
]
),
using the F1-based metrics defined in Eq.
1
.
To illustrate HeaRT’s downstream applicability beyond structural interpretation,
we further evaluate two system-level circuits: (i) a supply-insensitive relaxation oscillator and (ii) an analog front-end (AFE),
each under its corresponding design-adaptation scenario (Fig.
5
(a)-(b)).
We use Eq. (
2
) to compute the performance FoM for both scenarios
and Eq. (
3
) to evaluate design effort reuse for the fixed-architecture case in Scenario 1 (Fig.
5
(a)).
Note that since
ℛ
effort
\mathcal{R}_{\mathrm{effort}}
measures preservation of prior design effort rather than performance improvement, it is evaluated separately from the FoM.
All experiments use a 200-simulation budget.
The one-time offline
tree construction phase employs Claude-4.6-Sonnet,
while downstream interaction through the Interface Agent uses lighter LLM variants (e.g., GPT-4o
[
29
]
) to reduce LLM inference overhead during online queries.
Schematic simulations are performed using the TSMC180nm process technology with SPICE in Cadence Analog Design Environment (ADE) on a 4-core 3.3 GHz CPU Linux system.
TABLE II
:
Evaluation of HeaRT across different LLM backbones.
LLM Backbone
Approach
F
1
,
subcircuits
F_{1,\mathrm{subcircuits}}
F
1
,
loops
F_{1,\mathrm{loops}}
S
M
H
S
M
H
LLaMA-3.3-
70B-Instruct
†
HeaRT
0.724
0.513
0.336
0.561
0.362
0.191
Few-shot (Text)
0.571
0.452
0.167
0.396
0.153
0.135
Few-shot (Image)
–
–
–
–
–
–
Gemini-2.5 Pro
HeaRT
0.979
0.952
0.914
0.948
0.891
0.876
Few-shot (Text)
0.697
0.641
0.532
0.569
0.471
0.414
Few-shot (Image)
0.681
0.612
0.469
0.591
0.554
0.397
DeepSeek-V3.2
HeaRT
0.993
0.974
0.946
0.975
0.917
0.892
Few-shot (Text)
0.729
0.672
0.539
0.688
0.621
0.497
Few-shot (Image)
0.718
0.637
0.493
0.702
0.626
0.464
GPT-5
HeaRT
0.993
0.973
0.949
0.972
0.931
0.906
Few-shot (Text)
0.722
0.669
0.578
0.691
0.638
0.523
Few-shot (Image)
0.725
0.663
0.541
0.704
0.659
0.478
Claude-4.6-
Sonnet
HeaRT
0.997
0.988
0.955
0.984
0.962
0.937
Few-shot (Text)
0.762
0.709
0.684
0.741
0.675
0.614
Few-shot (Image)
0.759
0.693
0.657
0.744
0.698
0.581
S, M, and H denote Simple (
<
<
20), Medium (20–40), and Hard (
>
>
40) circuit complexity tiers in our benchmark repository, measured by transistor count excluding digital logic.
“Text” denotes SPICE netlist input, while “Image” denotes schematic image input.
†
Vision capability not supported for this model.
Fig. 4
:
Statistical summary of our curated dataset repository.
IV-B
Evaluation of Structural Decomposition and Loop Identification
Table
I
summarizes the capabilities and limitations of existing LLM-based AMS design frameworks.
We evaluate HeaRT’s ability to perform structural decomposition and feedback loop identification on flattened netlists,
assessing how effectively it recovers circuit structure from raw connectivity,
thereby enabling the hierarchical circuit reasoning paradigm described in
Section
II-B
.
Using the metrics in Eq.
1
,
the predicted subcircuits and feedback loops are manually verified against expert-provided ground-truth annotations from experienced analog circuit designers
for the circuits in the benchmark repository (Fig.
4
).
The benchmark repository, including the expert-annotated ground-truth labels used for evaluation, will be publicly released upon acceptance to facilitate reproducibility and further research.
Table
II
reports F1 scores averaged over 10 independent trials
across multiple LLM backbones,
comparing HeaRT against two CoT-based few-shot prompting baselines using netlists and schematic images
as inputs, respectively.
As shown, performance degrades from Simple to Hard circuits across both tasks as structural complexity increases.
While schematic image-based reasoning yields marginal gains over netlists on simpler circuits,
particularly for loop identification where visual feedback paths are clearer,
schematic images introduce connectivity ambiguity from wire crossings and overlapping nets on larger circuits,
degrading loop and subcircuit recovery.
Across all circuit complexity tiers, HeaRT consistently improves the F1 scores relative to the baselines,
achieving
≥
13.5
%
\geq 13.5\%
improvement in
F
1
,
subcircuits
F_{1,\mathrm{subcircuits}}
and
≥
37.8
%
\geq 37.8\%
in
F
1
,
loops
F_{1,\mathrm{loops}}
,
demonstrating its ability to infer meaningful structure from otherwise unstructured netlist representations.
These gains stem from the combination of our graph-guided partitioning heuristics and LLM reasoning.
As expected, models with stronger reasoning and instruction-following capabilities yield improved performance,
with the best results obtained using Claude-4.6-Sonnet.
IV-C
Integration within Optimization Loops
The experimental evaluation comprises two incremental design-adaptation scenarios.
Scenario 1 investigates query-conditioned priority-guided sizing optimization.
We integrate HeaRT with the TuRBO optimizer
[
18
]
,
which has been widely adopted for analog sizing
[
56
]
,
and benchmark it against standalone TuRBO and the LLM-based sizing framework LEDRO
[
33
]
.
Scenario 2 then evaluates HeaRT’s optimizer‑agnostic and context‑aware decision-making capability by integrating it with several established optimization algorithms commonly used for analog sizing, namely
Differential Evolution (DE)
[
57
]
,
the RL-inspired DNN-Opt
[
10
]
,
and the multi-agent RL-based MA-RL
[
69
,
5
]
,
alongside TuRBO.
These baselines were chosen to represent different categories of optimization approaches.
In the experiments that follow, we limit HeaRT to a one-time invocation at initialization.
For a fair convergence comparison under consistent initialization conditions, all optimizers are initialized from the same design point.
In incremental design adaptation tasks, a uniform starting point reflects practical workflows where an existing design is refined rather than redesigned from scratch.
A detailed analysis of HeaRT’s token usage across the offline and online phases versus circuit complexity tiers is provided in the Appendix
A
(Fig.
8
).
Fig. 5
:
Schematics of (a) Relaxation oscillator and (b) Analog front-end circuit with their corresponding design scenarios.
Fig. 6
:
Query-conditioned traversal and associated reasoning for (a) Scenario 1 and (b) Scenario 2.
IV-C
1
Scenario 1: Performance-Shift–Driven Priority-Guided Sizing Optimization
As shown in Fig.
5
(a), this design adaptation scenario targets a 10% reduction in frequency error in a supply-insensitive relaxation oscillator while maintaining oscillation frequency, relaxing the
I
​
Q
IQ
tradeoff, and keeping all other key specifications approximately unchanged.
During inference-time query-conditioned traversal on the hierarchical circuit reasoning tree,
HeaRT accurately identifies and prioritizes the
comparator front-end design variables.
The corresponding traversal path and its reasoning trace are illustrated in Fig.
6
(a).
The TuRBO optimizer-based sizing procedure is invoked, with HeaRT-derived priority variables
P
P
defining the initial bounds:
bounds
init
​
[
P
]
=
full range
\mathrm{bounds_{init}}[P]=\textrm{full\ range}
,
bounds
init
​
[
¬
P
]
=
nominals
\mathrm{bounds_{init}}[\neg P]=\textrm{nominals}
.
This priority-guided optimization accelerates convergence,
achieving an FoM of
∼
\sim
1.93
×
\times
and a
ℛ
effort
\mathcal{R}_{\mathrm{effort}}
of
∼
3.6
×
\sim\mathbf{3.6\times}
compared to the standalone TuRBO (Fig.
7
(a)-(b)).
Table
III
summarizes the comparative results for Scenario 1 in terms of FoM, convergence speed,
and real-time token usage.
Unlike approaches that repeatedly invoke LLM reasoning within the optimization loop, HeaRT performs a single real-time invocation to prioritize the search space.
TABLE III
:
Scenario 1: HeaRT+TuRBO vs. baselines.
Method
[0em]
FoM
[0em]
#Sims to
Converge
#Tokens
(Real-Time)
TuRBO
[
18
]
320.71
516
N/A
LEDRO
[
33
]
395.4
354
75,212
HeaRT+TuRBO
618.97
165
7,194
GPT-4o used for HeaRT online phase and LEDRO.
All results averaged over 10 independent trials.
TABLE IV
:
Scenario 2: Impact of HeaRT across different optimizers.
Optimizer
Eval. Metric
Baseline
HeaRT Optimized
Sizing
Topo+
Sizing
TuRBO
[
18
]
FoM
240.21
413.78
555
#Sims to Converge
401
37
43
DE
[
57
]
FoM
230.21
381.82
551
#Sims to Converge
479
63
68
DNN-Opt
[
10
]
FoM
269.73
467.93
556.6
#Sims to Converge
286
31
38
MA-RL
[
69
,
5
]
FoM
293.07
463.42
556.3
#Sims to Converge
314
28
39
TABLE V
:
Expert–LLM Rank Agreement (Spearman’s
ρ
s
\rho_{s}
Correlation).
Circuit
Family
GPT-4o
[-5pt]
Gemini-
2.5 Pro
DeepSeek-
V3.2
GPT-5
[-5pt]
Claude-4.6-
Sonnet
OPAMP
0.78 /
0.86
0.84 /
0.90
0.87 /
0.92
0.88 /
0.92
0.93 /
0.95
Comparator
0.74 /
0.81
0.79 /
0.88
0.89 /
0.92
0.86 /
0.91
0.92 /
0.93
Results averaged across corresponding family-specific metrics over 10 trials.
Each cell reports Base / +Context agreement. Base: few-shot prompting without external grounding; +Context: with knowledge retrieved from ISSCC/JSSC corpus.
Fig. 7
:
Performance profiles for
(a) FoM and
(b)
ℛ
effort
\mathcal{R}_{\mathrm{effort}}
in Scenario 1 and
(c) FoM in Scenario 2,
plotted against simulation count. Shaded regions indicate variation across 10 independent runs.
IV-C
2
Scenario 2: Knowledge-Based, Performance-Driven Retrieval-Guided Topology Reconfiguration and Sizing
This scenario targets lower input-referred noise (higher SNR) and
reduced area under relaxed gain and offset constraints in an analog front-end (Fig.
5
(b)).
As shown in Fig.
6
(b),
HeaRT identifies the first gain stage as the dominant noise contributor,
with the associated reasoning trace shown alongside.
Its rank-based retrieval, guided by
𝒮
\mathcal{S}
= {IRN density, Area},
selects an inverter-based topology as a higher-ranked alternative and generates sized netlists for both designs,
thereby overcoming architectural bottlenecks inherent in conventional sizing-only workflows.
Fig.
7
(c) shows the resulting FoM profiles relative to standalone TuRBO,
while Table
IV
summarizes the impact across different baseline optimizers.
As shown, HeaRT achieves an FoM improvement of
≥
58
%
\geq 58\%
through sizing-only optimization, and
≥
89
%
\geq 89\%
through its retrieval-guided topology reconfiguration across all standalone baselines,
while also achieving significantly faster convergence.
Table
V
reports the Spearman rank-order correlation coefficient (
ρ
s
\rho_{s}
) between LLM-derived and human expert rankings
for 10 representative topologies per family in OPAMPs and comparators,
comparing Base (few-shot prompting) and +Context (ISSCC/JSSC-grounded) settings to assess the reliability of
LLM-assigned rankings during topology knowledge database population
(Section
III-B1
).
V
Conclusion
In this paper, we propose HeaRT, a novel hierarchical circuit reasoning tree-based agentic framework for AMS design optimization.
HeaRT combines top-down graph-guided subcircuit identification and hierarchical abstraction with bottom-up knowledge consolidation,
enabling structured, context-aware reasoning for AMS design tasks.
The framework allows natural-language instructions
to steer real-time retrieval while remaining grounded in the hierarchical reasoning structure.
Our experiments validate HeaRT’s ability to recover meaningful structure from flattened netlists across a diverse AMS benchmark.
We further demonstrate its effectiveness in practical design-adaptation scenarios
involving both topology and sizing optimization, two critical steps in AMS design.
Future directions include enriching the reasoning tree with simulation metadata and exploring applications such as layout-constraint extraction.
Overall, HeaRT represents a step toward context-aware, practical AMS design automation.
Upon acceptance, the HeaRT framework and the benchmark repository,
including the expert-annotated ground-truth labels used for evaluation,
will be publicly released as open source.
References
[1]
I. Abel, M. Neuner, and H. Graeb
(2022)
A functional block decomposition method for automatic op-amp design
.
Integration
85
,
pp. 108–120
.
Cited by:
§II-B
.
[2]
M. Ahmadzadeh K. Chen
et al.
(2025)
(Invited Paper) AnaFlow: LLM-based Workflow for Reasoning-Driven Explainable and Sample-Efficient Analog Circuit Sizing
.
In
Proc. ICCAD
,
Cited by:
§I
,
§I
,
§II-A
,
TABLE I
.
[3]
M. AI
(2024)
Llama-3.3-70B-Instruct Model Card
.
Note:
URL:
https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
.
Cited by:
§IV-A
.
[4]
Anthropic
(2026)
Introducing Claude Sonnet 4.6
.
Note:
URL: https://www.anthropic.com/news/claude-sonnet-4-6
Cited by:
§IV-A
.
[5]
J. Bao
et al.
(2024)
Multiagent Based Reinforcement Learning(MA-RL): An Automated Designer for Complex Analog Circuits
.
IEEE TCAD
.
Cited by:
§I
,
§IV-C
,
TABLE IV
.
[6]
T. Brown
et al.
(2020)
Language Models are Few-Shot Learners
.
Proc. NeurIPS
.
Cited by:
§III-A1
.
[7]
A. F. Budak
et al.
(2023)
APOSTLE: asynchronously parallel optimization for sizing analog transistors using DNN learning
.
In
Proc. ASPDAC
,
pp. 70–75
.
Cited by:
§I
.
[8]
A. F. Budak
et al.
(2023)
Joint Optimization of Sizing and Layout for AMS Designs: Challenges and Opportunities
.
In
Proc. ISPD
,
Cited by:
§I
.
[9]
A. F. Budak
et al.
(2023)
Practical Layout-Aware Analog/Mixed-Signal Design Automation with Bayesian Neural Networks
.
In
Proc. ICCAD
,
Cited by:
§I
.
[10]
A. F. Budak
et al.
(2021)
DNN-Opt: an RL inspired optimization for analog circuit sizing using deep neural networks
.
In
Proc. DAC
,
Cited by:
§I
,
§IV-C
,
TABLE IV
.
[11]
W. Cao
et al.
(2024)
RoSE-Opt: Robust and Efficient Analog Circuit Parameter Optimization With Knowledge-Infused Reinforcement Learning
.
IEEE TCAD
.
Cited by:
§I
.
[12]
P. Chen, Y. Lin, W. Lee, T. Leu, P. Hsu, A. Dissanayake, S. Oh, and C. Chiu
(2025)
MenTeR: a fully-automated multi-agent workflow for end-to-end rf/analog circuits netlist design
.
In
Proc. ICLAD
,
pp. 124–132
.
Cited by:
TABLE I
.
[13]
Q. Chen, L. Qin, J. Liu, D. Peng,
et al.
(2025)
Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models
.
arXiv preprint arXiv:2503.09567
.
Cited by:
§II-A
.
[14]
W. Chen
et al.
(2025)
AnalogTester: A Large Language Model-Based Framework for Automatic Testbench Generation in Analog Circuit Design
.
In
Proc. ISEDA
,
Cited by:
§I
,
§II-A
.
[15]
Z. Chen
et al.
(2024)
Artisan: Automated Operational Amplifier Design via Domain-specific Large Language Model
.
In
Proc. DAC
,
Cited by:
§I
,
§II-A
,
TABLE I
.
[16]
M. Choi
et al.
(2023)
Reinforcement Learning-based Analog Circuit Optimizer using gm/ID for Sizing
.
In
Proc. DAC
,
Cited by:
§I
.
[17]
DeepSeek-AI
(2025)
DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models
.
arXiv preprint arXiv:2512.02556
.
Cited by:
§IV-A
.
[18]
D. Eriksson, M. Pearce, J. Gardner, R. D. Turner, and M. Poloczek
(2019)
Scalable Global Optimization via Local Bayesian Optimization
.
Advances in neural information processing systems
32
.
Cited by:
§IV-C
,
TABLE III
,
TABLE IV
.
[19]
J. Gao, W. Cao, and X. Zhang
(2025)
AnalogGenie-Lite: Enhancing Scalability and Precision in Circuit Topology Discovery through Lightweight Graph Modeling
.
In
Proc. ICML
,
Cited by:
§I
,
§II-A
,
TABLE I
.
[20]
J. Gao
et al.
(2023)
RoSE: Robust Analog Circuit Parameter Optimization with Sampling-Efficient Reinforcement Learning
.
In
Proc. DAC
,
Cited by:
§I
.
[21]
J. Gao
et al.
(2025)
AnalogGenie: A Generative Engine for Automatic Discovery of Analog Circuit Topologies
.
In
Proc. ICLR
,
Cited by:
§I
,
§II-A
,
TABLE I
.
[22]
G. G. Gielen
(2002)
Modeling and analysis techniques for system-level architectural design of telecom front-ends
.
IEEE Transactions on Microwave Theory and Techniques
50
(
1
),
pp. 360–368
.
Cited by:
§I
,
§II-A
,
§II-B
.
[23]
G. G. Gielen
(2025)
A Brief 20-Year History and Future Perspectives on Sizing and Layout Synthesis of Analog/RF ICs
.
IEEE Design & Test
42
(
6
),
pp. 63–74
.
Cited by:
§I
.
[24]
Google DeepMind
(2025)
Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities
.
arXiv preprint arXiv:2507.06261
.
Cited by:
§IV-A
.
[25]
A. Grattafiori
et al.
(2024)
The Llama 3 Herd of Models
.
arXiv preprint arXiv:2407.21783
.
Cited by:
§IV-A
.
[26]
P. R. Gray, P. J. Hurst, S. H. Lewis, and R. G. Meyer
(2024)
Analysis and design of analog integrated circuits
.
John Wiley & Sons
.
Cited by:
Appendix B
,
§III-B1
.
[27]
D. Guo, D. Yang, H. Zhang, J. Song, Zhang,
et al.
(2025)
DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
.
arXiv preprint arXiv:2501.12948
.
Cited by:
§II-A
.
[28]
L. Huang
et al.
(2025)
A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
.
ACM Transactions on Information Systems
.
Cited by:
§II-A
.
[29]
A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford,
et al.
(2024)
GPT-4o System Card
.
arXiv preprint arXiv:2410.21276
.
Cited by:
§IV-A
.
[30]
C. Jiang
et al.
(2024)
LLMOPT: Learning to Define and Solve General Optimization Problems from Scratch
.
arXiv preprint arXiv:2410.13213
.
Cited by:
§II-A
.
[31]
S. Kim, L. Noci, A. Orvieto, and T. Hofmann
(2023)
Achieving a Better Stability-Plasticity Trade-off via Auxiliary Networks in Continual Learning
.
In
Proceedings of the IEEE/CVF conference on computer vision and pattern recognition
,
pp. 11930–11939
.
Cited by:
§II-D
.
[32]
J. Kirkpatrick
et al.
(2017)
Overcoming catastrophic forgetting in neural networks
.
Proceedings of the national academy of sciences
.
Cited by:
§I
,
§II-D
.
[33]
D. V. Kochar
et al.
(2025)
LEDRO: LLM-Enhanced Design Space Reduction and Optimization for Analog Circuits
.
In
Proc. ICLAD
,
Cited by:
§I
,
§II-A
,
TABLE I
,
§IV-C
,
TABLE III
.
[34]
K. Kunal, T. Dhar, M. Madhusudan, J. Poojary, A. K. Sharma, W. Xu, S. M. Burns, J. Hu, R. Harjani, and S. S. Sapatnekar
(2020)
GANA: Graph Convolutional Network Based Automated Netlist Annotation for Analog Circuits.
.
In
DATE
,
pp. 55–60
.
Cited by:
§II-B
.
[35]
K. Kunal, T. Dhar, M. Madhusudan, J. Poojary, A. K. Sharma, W. Xu, S. M. Burns, J. Hu, R. Harjani, and S. S. Sapatnekar
(2023)
GNN-Based Hierarchical Annotation for Analog Circuits
.
IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems
42
(
9
),
pp. 2801–2814
.
Cited by:
§II-B
.
[36]
K. Kundert
(2003)
Principles of Top-Down MixedSignal Design
.
The Designer’s Guide Community http://www. designers-guide. org
.
Cited by:
§I
,
§II-A
,
§II-B
.
[37]
Y. Lai
et al.
(2025)
AnalogCoder: Analog Circuit Design via Training-Free Code Generation
.
In
Proc. AAAI
,
Cited by:
§I
,
§II-A
,
TABLE I
.
[38]
Y. Lai, S. Poddar, S. Lee,
et al.
(2026)
AnalogCoder-Pro: Unifying Analog Circuit Generation and Optimization via Multi-modal LLMs
.
IEEE TCAD
.
Cited by:
§I
,
TABLE I
.
[39]
B. Li, S. Wang, T. Chen, Q. Sun, and C. Zhuo
(2024)
Efficient subgraph matching framework for fast subcircuit identification
.
In
Proceedings of the 2024 ACM/IEEE International Symposium on Machine Learning for CAD
,
pp. 1–7
.
Cited by:
§II-B
.
[40]
Y. Li, Y. Lin, M. Madhusudan,
et al.
(2021)
A Circuit Attention Network-Based Actor-Critic Learning Approach to Robust Analog Transistor Sizing
.
In
Proc. MLCAD
,
Cited by:
§I
.
[41]
C. Liu and D. Chitnis
(2025)
EEsizer: LLM-Based AI Agent for Sizing of Analog and Mixed Signal Circuit
.
IEEE Transactions on Circuits and Systems I: Regular Papers
.
Cited by:
§II-A
.
[42]
C. Liu and J. Yang
(2025)
IC + AI: a no-human-in-loop design paradigm?
.
Science China Information Sciences
.
Cited by:
§I
,
§II-A
.
[43]
J. Liu
et al.
(2023)
LlamaIndex
.
Note:
URL:
https://github.com/run-llama/llama_index
Cited by:
Appendix B
.
[44]
W. Lyu
et al.
(2018)
Batch Bayesian optimization via multi-objective acquisition ensemble for automated analog circuit design
.
In
Proc. ICML
,
Cited by:
§I
.
[45]
K. S. NS and P. Li
(2025)
AI Analog Circuit Design Agents: On Knowledge Extraction and Transfer with Knowledge Graphs
.
In
2025 IEEE/ACM International Conference On Computer Aided Design (ICCAD)
,
pp. 1–9
.
Cited by:
§II-A
,
TABLE I
.
[46]
Y. Oh
et al.
(2024)
CRONuS: Circuit Rapid Optimization with Neural Simulator
.
In
Proc. DATE
,
Vol.
,
pp. 1–6
.
Cited by:
§I
.
[47]
P. Pham, A. Venkitaraman, C. Hsieh, A. Bonetti, S. Uhlich, M. Leibl, S. Hofmann, E. Ohbuch, L. Servadei, U. Schlichtmann,
et al.
(2025)
GENIE-ASI: Generative Instruction and Executable Code for Analog Subcircuit Identification
.
In
2025 ACM/IEEE 7th Symposium on Machine Learning for CAD (MLCAD)
,
pp. 1–21
.
Cited by:
§II-B
.
[48]
B. Razavi
(2000)
Design of Analog CMOS Integrated Circuits
.
McGraw-Hill, Inc.
.
Cited by:
Appendix B
,
§I
,
§II-A
,
§II-B
,
§III-B1
.
[49]
P. Schmid
(2025)
The New Skill in AI is Not Prompting, It’s Context Engineering
.
Blog Article www. pmworldjournal. com Featured Paper by Massimo Pirozzi
.
Cited by:
§II-A
,
§III-B
.
[50]
K. Settaluri
et al.
(2020)
AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs
.
In
Proc. DATE
,
pp. 490–495
.
Cited by:
§I
.
[51]
J. Shen, Z. Chen, J. Zhuang,
et al.
(2025)
Atelier: An Automated Analog Circuit Design Framework via Multiple Large Language Model-Based Agents
.
IEEE TCAD
.
Cited by:
§I
,
§II-A
,
TABLE I
.
[52]
N. Shervashidze, P. Schweitzer, E. J. Van Leeuwen, K. Mehlhorn, and K. M. Borgwardt
(2011)
Weisfeiler-Lehman Graph Kernels
.
Journal of Machine Learning Research
12
(
9
).
Cited by:
§III-B1
.
[53]
W. Shi
et al.
(2022)
RobustAnalog: Fast Variation-Aware Analog Circuit Design Via Multi-task RL
.
In
Proc. MLCAD
,
Cited by:
§I
.
[54]
A. Singh, A. Fry, A. Perelman, A. Tart, A. Ganesh, A. El-Kishky, A. McLaughlin, A. Low, A. Ostrow, A. Ananthram,
et al.
(2025)
OpenAI GPT-5 System Card
.
arXiv preprint arXiv:2601.03267
.
Cited by:
§IV-A
.
[55]
H. Sun
et al.
(2024)
EVDMARL: Efficient Value Decomposition-based Multi-Agent Reinforcement Learning with Domain-Randomization for Complex Analog Circuit Design Migration
.
In
Proc. DAC
,
Cited by:
§I
.
[56]
K. Touloupas, N. Chouridis, and P. P. Sotiriadis
(2021)
Local Bayesian Optimization For Analog Circuit Sizing
.
In
2021 58th ACM/IEEE design automation conference (DAC)
,
pp. 1237–1242
.
Cited by:
§IV-C
.
[57]
C. Vişan, O. Pascu, M. Stănescu, E. Şandru, C. Diaconu, A. Buzo, G. Pelz, and H. Cucu
(2022)
Automated circuit sizing with multi-objective optimization based on differential evolution and Bayesian inference
.
Knowledge-Based Systems
258
,
pp. 109987
.
Cited by:
§IV-C
,
TABLE IV
.
[58]
H. Wang
et al.
(2020)
GCN-RL Circuit Designer: Transferable Transistor Sizing with Graph Neural Networks and Reinforcement Learning
.
In
Proc. DAC
,
Cited by:
§I
.
[59]
L. Wang
et al.
(2024)
A survey on large language model based autonomous agents
.
Frontiers of Computer Science
.
Cited by:
§II-A
.
[60]
X. Wang
et al.
(2023)
Recent Advances in Bayesian Optimization
.
ACM Computing Surveys
55
(
13s
),
pp. 1–36
.
Cited by:
§I
.
[61]
J. Wei
et al.
(2022)
Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
.
Proc. NeurIPS
35
,
pp. 24824–24837
.
Cited by:
§II-A
,
§III-A1
.
[62]
J. Wu, J. Zhu, Y. Liu,
et al.
(2025)
Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with Agentic Tools
.
arXiv preprint arXiv:2502.04644
.
Cited by:
§II-A
.
[63]
Z. Xi
et al.
(2025)
The rise and potential of large language model based agents: A survey
.
Science China Information Sciences
.
Cited by:
§II-A
.
[64]
F. Xu, Q. Hao, Z. Zong,
et al.
(2025)
Towards Large Reasoning Models: A Survey of Reinforced Reasoning with Large Language Models
.
arXiv preprint arXiv:2501.09686
.
Cited by:
§II-A
.
[65]
H. Xu, C. Liu, Q. Wang,
et al.
(2025)
Image2Net: Datasets, Benchmark and Hybrid Framework to Convert Analog Circuit Diagrams into Netlists
.
In
Proc. ISEDA
,
Cited by:
§I
,
§II-A
.
[66]
Y. Yin, Y. Wang, B. Xu, and P. Li
(2024)
ADO-LLM: Analog Design Bayesian Optimization with In-Context Learning of Large Language Models
.
In
Proc. ICCAD
,
Cited by:
§I
,
§II-A
,
TABLE I
.
[67]
F. Zenke, B. Poole, and S. Ganguli
(2017)
Continual Learning Through Synaptic Intelligence
.
In
International conference on machine learning
,
pp. 3987–3995
.
Cited by:
§II-D
.
[68]
H. Zhang
et al.
(2025)
AnalogXpert: Automating Analog Topology Synthesis by Incorporating Circuit Design Expertise into Large Language Models
.
In
Proc. ISEDA
,
Cited by:
§I
,
§II-A
,
TABLE I
.
[69]
J. Zhang
et al.
(2023)
Automated Design of Complex Analog Circuits with Multiagent based Reinforcement Learning
.
In
Proc. DAC
,
Cited by:
§I
,
§IV-C
,
TABLE IV
.
[70]
S. Zhang F. Yang
et al.
(2022)
An Efficient Batch-Constrained Bayesian Optimization Approach for Analog Circuit Synthesis via Multiobjective Acquisition Ensemble
.
IEEE TCAD
.
Cited by:
§I
.
Appendix A
Token Cost Analysis
To quantify HeaRT’s overall token cost, we report the total token usage across circuits in our benchmark repository at different stages of the offline and online phases (Fig.
8
),
grouped by circuit complexity tiers.
As shown, token usage generally increases with circuit complexity across stages,
with the increase most pronounced in the top-down graph-guided subcircuit decomposition and tree construction stage.
The subsequent bottom-up knowledge consolidation stage shows comparatively smaller variation across complexity tiers.
In contrast, online reasoning stages exhibit noticeably lower variation.
This two-phase design amortizes the higher offline construction cost across downstream applications,
reducing per-task inference overhead compared to single-shot prompting, particularly for more complex circuits,
while preserving circuit-level reasoning fidelity.
Fig. 8
:
Token usage across different stages of the HeaRT workflow.
For the experiments reported in Table
III
(Scenario 1) and Table
IV
(Scenario 2),
the total real-time token usage was approximately 7,194 and 10,216 tokens, respectively.
Appendix B
Additional Implementation Details
This appendix details the external grounding mechanism for topology knowledge database updates (Fig.
2
, Section
III-B1
).
We use LlamaIndex
[
43
]
to index a curated corpus of ISSCC and JSSC publications,
alongside standard analog design textbooks
[
48
,
26
]
,
with each document parsed into structured chunks capturing
(i) the document title, (ii) circuit family, (iii) architectural description, and (iv) reported performance characteristics and trade-offs.
Retrieval queries are constructed from the circuit family label and an LLM-generated architectural description of the candidate topology.
The retrieved context, together with the circuit-family metric schema and current repository state,
is provided as input to the LLM to guide metric-wise ranking updates.
Future extensions could incorporate schematic image-to-graph conversion for richer structural retrieval from analog circuit literature.
Furthermore, while Table
V
evaluates the reliability of LLM ranking in a
bulk setting
(all topologies are ranked simultaneously),
it does not capture the incremental insertion scenario described in Section
III-B1
,
where a new topology is slotted into an existing repository whose entries already carry metric-wise rankings and concise justification cues reflecting expected performance trade-offs.
To evaluate this, we adopt a leave-one-out protocol over the 10 representative topologies per family used in Table
V
:
in each trial, one topology is held out and inserted into a repository of the remaining 9, with
ρ
s
\rho_{s}
measured against human expert ground truth.
This is repeated across all 10 topologies, with results averaged over 10 independent LLM runs.
Table
VI
reports
ρ
s
\rho_{s}
under two conditions:
without and with conditioning on the existing repository state, both grounded in ISSCC/JSSC literature.
TABLE VI
:
Incremental Topology Insertion: LLM–Expert Ranking Correlation (Spearman’s
ρ
s
\rho_{s}
, mean
±
\pm
std).
Condition
Claude-4.6-Sonnet
GPT-5
OPAMP
Comparator
OPAMP
Comparator
w/o Repository
Context
0.74
±
0.09
0.74\pm 0.09
[0pt]
0.70
±
0.11
0.70\pm 0.11
[0pt]
0.72
±
0.10
0.72\pm 0.10
[0pt]
0.69
±
0.11
0.69\pm 0.11
[0pt]
w/ Repository
Context
0.92
±
0.04
0.92\pm 0.04
[0pt]
0.90
±
0.03
0.90\pm 0.03
[0pt]
0.89
±
0.06
0.89\pm 0.06
[0pt]
0.85
±
0.04
0.85\pm 0.04
[0pt]
Both conditions are grounded in ISSCC/JSSC literature. Results averaged over 10 independent trials under a leave-one-out protocol over 10 topologies per family.
Appendix C
Efficacy of
FoM
rank
\mathrm{FoM_{rank}}
For Topology Retrieval
To further validate the effectiveness of our top-k
FoM
rank
\mathrm{FoM_{rank}}
-based topology retrieval strategy, we evaluate the performance profiles across candidates at different rank positions for Scenario 2, under identical optimization settings using TuRBO.
All results are averaged over 10 independent trials.
As shown in Fig.
9
, higher-ranked candidates generally achieve higher FoM, supporting the utility of our
FoM
rank
\mathrm{FoM_{rank}}
-based retrieval as an effective proxy for topology selection.
Fig. 9
:
Performance FoM Profiles Across Retrieved Topology Ranks.