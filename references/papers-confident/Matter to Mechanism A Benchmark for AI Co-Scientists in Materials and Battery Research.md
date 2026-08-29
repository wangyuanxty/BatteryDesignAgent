Matter to Mechanism: A Benchmark for AI Co-Scientists in Materials and Battery Research
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2606.02258v1 [cs.CE] 01 Jun 2026
Matter to Mechanism: A Benchmark for AI Co-Scientists in Materials and Battery Research
Shashwat Sourav
Affiliation:
Oak Ridge National Laboratory
Affiliation:
Lawrence Berkeley National Laboratory
Tanjin He
Affiliation:
Argonne National Laboratory
Maria K. Y. Chan
Affiliation:
Argonne National Laboratory
Anubhav Jain
Tirthankar Ghosal
Affiliation:
Oak Ridge National Laboratory
Affiliation:
UniverseTBD[0.5em]
{shashwat.sourav}@wustl.edu{tanjin.he,mchan}@anl.gov  ajain@lbl.govghosalt@ornl.gov
[0.5em]
Washington University in St. Louis
[0.3em]
Equal contribution.
Abstract
AI co-scientists are increasingly used for scientific discovery, but current evaluations still do not test them on a key task: moving from a concrete scientific or technological problem to a plausible, mechanism-grounded solution hypothesis. This gap is especially important in materials science and, in particular, battery research, where a useful proposal must identify the relevant failure mode, propose a credible intervention, and explain why that intervention should improve the target property. We introduce Matter to Mechanism, a benchmark for evaluating AI co-scientists on problem-to-hypothesis reasoning in materials science, with a focus on battery materials research. The benchmark contains 2,645 instances derived from scientific publications. Each instance includes a structured problem statement, a candidate solution hypothesis, an explicit reasoning trace, and domain-grounded annotations such as material system, component, failure mode, intervention, mechanism, target property, and claimed outcome. We also introduce a metric suite that measures reasoning fidelity, problem alignment, mechanistic specificity, novelty, plausibility, and problem decomposition quality, and combine them into a composite score. Using this framework, we evaluate several AI co-scientist systems and show that Matter to Mechanism reveals interpretable system differences that are only partially recovered by standard text-similarity metrics. We further show through adversarial stress tests that the aggregate score is more stable than individual metric dimensions under superficial gaming attacks.
1
Introduction
Large language models are now being used in more and more parts of scientific research. They are being asked to read papers, summarize prior work, retrieve useful evidence, write code, analyze data, and, in some cases, even propose new ideas. This has created excitement around the idea of AI co-scientists that can assist human researchers during discovery. At the same time, evaluation is still lagging behind the ambition of these systems. In many cases, we still do not have good ways to test whether a model can perform the scientific tasks of interest, rather than simply produce fluent scientific text or score well on a narrow benchmark
(
Prasad Majumder et al. 2024
;
Liu et al. 2025b
;
Mitchener et al. 2025
;
Chen et al. 2024
)
.
This gap is observed in materials science. Materials science research is not just a text generation problem. A useful scientific proposal has to begin from an observation, e.g. a problem with the performance of a functional material, identify what is failing, suggest an appropriate intervention, and hypothesize why that intervention should improve the target property. In battery research, for example, a strong hypothesis should do more than mention a material, additive, or interface. It should connect the proposed change to a specific mechanism such as dendrite suppression, interfacial stabilization, ionic transport improvement, structural robustness, or degradation mitigation. A proposal can sound scientific and still be vague, misaligned with the actual problem, or physically implausible. That is exactly why this setting needs a benchmark that goes beyond surface similarity or general human preference judgments
(
Dehghani et al. 2021
;
Raji et al. 2021
;
Liu et al. 2025a
)
.
Recent work has started to push benchmark design in the right direction. DiscoveryBench studies data-driven scientific discovery and evaluates whether models can derive hypotheses and workflows from datasets and discovery goals
(
Prasad Majumder et al. 2024
)
. ResearchBench decomposes scientific discovery into inspiration retrieval, hypothesis composition, and hypothesis ranking, and shows that these sub-tasks can be benchmarked separately
(
Liu et al. 2025b
)
. BixBench evaluates LLM-based agents on realistic computational biology analysis scenarios, while ScienceAgentBench focuses on data-driven scientific workflows and code-based agent performance
(
Mitchener et al. 2025
;
Chen et al. 2024
)
. In materials and chemistry, MATDESIGN studies hypothesis generation for material discovery and design, MatTools benchmarks LLMs on materials-science tool use, MaCBench evaluates multimodal chemistry and materials reasoning, and ChemBench evaluates chemical knowledge and reasoning at scale
(
Kumbhar et al. 2025
;
Liu et al. 2025a
;
Alampara et al. 2024
;
Mirza et al. 2024
)
. These are important steps, but they still leave open a specific problem that matters in practice (Table
1
): evaluating whether a system can start from a concrete materials-science problem, identify the relevant failure mode, propose an intervention at the right level, and connect that intervention to a scientifically plausible mechanism. This problem is narrower than general scientific-discovery benchmarking, but also closer to the kind of mechanistically grounded reasoning that matters in real materials and battery research.
In this work, we introduce
Matter to Mechanism
, a benchmark for evaluating AI co-scientists on problem-solution reasoning in materials science, in particular battery materials research. Each instance is built from a scientific paper and contains a problem statement, a candidate hypothesis, and an explicit reasoning trace. In addition, each instance includes structured scientific fields such as the material or battery system, battery component, failure mode, intervention, mechanism, target property, claimed outcome, evidence strength, and novelty axis. This structure is important because it turns the benchmark into more than a collection of prompts and answers. It gives us a way to ask whether the model identified the right problem, proposed the right kind of intervention, and linked that intervention to a mechanism that makes scientific sense.
We also introduce a metric suite designed for this setting. Instead of depending only on lexical overlap or broad quality judgments
(
Dehghani et al. 2021
;
Raji et al. 2021
)
, we evaluate systems along six dimensions: reasoning chain fidelity, hypothesis-problem alignment, mechanistic specificity, scientific novelty, intervention plausibility, and problem decomposition quality. These dimensions are meant to reflect how a domain researcher would distinguish a genuinely useful hypothesis from one that is linguistically polished but scientifically superficial. The resulting benchmark therefore plays two roles. First, it provides a structured dataset of materials-science problem-solution instances. Second, it provides an evaluation framework for understanding what current AI co-scientists can and cannot do in scientific discovery.
Benchmark
Problem
→
\rightarrow
Hypothesis
Materials /
Battery
Structured
Problem Decomp.
Reasoning
Trace
Domain
Metrics
LLM /
Agent Eval.
DiscoveryBench
(
Prasad Majumder et al. 2024
)
✓
✗
✗
✗
✗
✓
ResearchBench
(
Liu et al. 2025b
)
✓
✗
✓
✗
✗
✓
BixBench
(
Mitchener et al. 2025
)
✗
✗
✗
✗
✗
✓
MATDESIGN
(
Kumbhar et al. 2025
)
✓
✓
✗
✗
✓
✓
MatTools
(
Liu et al. 2025a
)
✗
✓
✗
✗
✗
✓
MaCBench
(
Alampara et al. 2024
)
✗
✓
✗
✗
✗
✓
ChemBench
(
Mirza et al. 2024
)
✗
✗
✗
✗
✓
✓
Matter to Mechanism
✓
✓
✓
✓
✓
✓
Table 1
:
Comparison of Matter to Mechanism with representative benchmarks for scientific discovery, materials science, and LLM/agent evaluation. Existing benchmarks evaluate important aspects of discovery, including data-driven hypothesis generation, inspiration-based decomposition, multimodal materials reasoning, and materials tool use. Our benchmark differs in jointly focusing on problem–solution reasoning in materials science, structured scientific decomposition, explicit reasoning traces, and domain-grounded evaluation metrics.
Our goal is not only to compare different co-scientists, but also to highlight their shortcomings. A model may generate a hypothesis that is relevant but does not actually address the stated failure mode. It may propose something novel but without a clear mechanism. It may reason for many steps without decomposing the scientific problem well enough to support a useful intervention. By making these distinctions visible, Matter to Mechanism shifts evaluation away from “does the output sound scientific?” and toward “does the system perform the scientific task well?” Overall, our contribution is a benchmark and evaluation framework for a part of scientific discovery that is important, practical, and still poorly measured. We hope this benchmark helps move the field toward more realistic evaluation of AI systems for materials research, especially in high-value domains such as batteries where the importance of mechanistic grounding and physical plausibility stands out.
Figure 1
:
Overview of the Matter to Mechanism workflow. Given a structured materials-science problem, AI co-scientist systems generate candidate solution hypotheses and associated reasoning traces. These outputs are evaluated along six dimensions: reasoning fidelity, problem alignment, mechanistic specificity, novelty, plausibility, and decomposition quality, which together yield a composite scientific quality score. The framework is designed to assess whether models can move from problem formulation to mechanistically grounded and scientifically plausible hypotheses.
2
Dataset Description
Matter to Mechanism
focuses on problem-solution reasoning, starting from a materials problem, identifying what is failing, and proposing a solution that is relevant, mechanistically specific, and physically plausible. Unlike benchmarks that evaluate broad discovery workflows or general hypothesis ranking, our dataset represents each example as a structured mapping from a problem-side description to a solution-side description.
Task formulation.
We represent each example as a structured mapping from a problem description to a solution description. The problem description includes the problem statement, the material or battery system, the affected component, and the failure mode. The solution description includes the hypothesis, the intervention, the mechanism, the target property, the claimed outcome, and the reasoning trace. Under this formulation, the benchmark asks whether a system can move from what is failing to what should be changed and why.
Dataset construction.
We built the benchmark from a corpus of 90,000 open-access papers. We filter this corpus for papers relevant to materials science and battery research and retain 2 ,645 papers. Each paper is converted into one structured problem-solution instance linking a technical problem to a candidate solution hypothesis and an associated reasoning trace. The extraction pipeline identifies problem-side fields, such as the problem statement, material or battery system, and failure mode, as well as solution-side fields, such as mechanism, target property, claimed outcome, and evidence strength. The goal of this processing step is to preserve the scientific logic of the source paper while converting it into a format suitable for evaluation. Two domain experts reviewed the schema, and field definitions.
Example of benchmark extraction from a source paper
Source signal.
A representative paper studies a disordered-rocksalt cathode for lithium-ion batteries and identifies restricted Li
+
diffusion, low electrical conductivity, and irreversible oxygen loss as bottlenecks for capacity retention.
Extracted problem fields.
Battery system: lithium-ion battery.
Component: disordered-rocksalt cathode.
Failure mode: restricted Li
+
diffusion, low conductivity, and oxygen loss.
Problem core: poor capacity retention caused by transport and redox-instability bottlenecks.
Extracted solution fields.
Intervention: fluorination of the oxygen sublattice, particle-size reduction by ball milling, and carbon coating.
Mechanism: fluorination improves Li
+
percolation and suppresses irreversible oxygen loss; ball milling shortens diffusion paths; carbon coating improves electronic transport.
Target property: Li
+
diffusion kinetics, charge-transfer resistance, and oxygen-redox reversibility.
Claimed outcome: improved discharge capacity, rate capability, and cycling stability.
Reasoning trace.
The reasoning trace links the identified bottleneck to the proposed intervention and then to a mechanism: transport limitations motivate fluorination and particle-size reduction, electronic limitations motivate carbon coating, and the combined intervention is expected to improve both kinetics and structural reversibility.
Reasoning trace.
The reasoning trace links the identified bottleneck to the proposed intervention and then to a mechanism: transport limitations motivate fluorination and particle-size reduction, electronic limitations motivate carbon coating, and the combined intervention is expected to improve both kinetics and structural reversibility.
Multiple plausible hypotheses.
A given materials problem can often admit more than one scientifically plausible solution, and different reasoning traces may support different interventions. For this reason, Matter to Mechanism does not treat the literature-derived hypothesis as the only valid answer. Instead, the literature instance serves as an anchor for benchmark construction, while our main evaluation remains reference-free with respect to hypothesis matching. Generated outputs are scored primarily against the input problem fields and their own internal scientific structure, rather than by exact overlap with a single reference hypothesis. This design makes the benchmark more suitable for open-ended scientific reasoning, where multiple solutions may exist.
Benchmark overview.
We present Matter to Mechanism (Figure
1
), a benchmark for evaluating AI co-scientists on problem-solution reasoning in materials science, with a focus on battery discovery. Each example is derived from a scientific paper and includes a problem statement, a candidate hypothesis, and a reasoning trace. Each example also includes structured scientific fields such as the material system, component, failure mode, intervention, mechanism, target property, claimed outcome, evidence strength, and novelty axis. This structure makes the benchmark useful for evaluation because it lets us measure not only whether an output is on topic but also whether it addresses the right scientific bottleneck in the right way.
Data source and composition.
The benchmark contains 2,645 problem–solution instances collected from materials-science papers, with strong coverage of battery-related research. All core structured fields are present in the released benchmark, and each example contains a reasoning trace. The benchmark covers a wide range of battery systems, components, and problem types, including transport limitations, degradation, safety, interfacial instability, diagnostics, characterization, and thermal-management challenges. This breadth is important because it reduces the risk that evaluation collapses into narrow paraphrase matching within one chemistry or one failure mode.
Evaluation.
This benchmark is intended to support the evaluation of AI co-scientists under a shared and realistic task formulation. Recent works have emphasized that evaluation itself should be studied carefully, with attention to benchmark design, scope, and interpretation
(
Tian et al. 2024
;
Zou et al. 2023
;
Longjohn et al. 2024
)
. Prior work has shown that benchmark results can be fragile and can overstate what is actually being measured
(
Dehghani et al. 2021
;
Raji et al. 2021
;
Wagstaff 2012
)
. Hence, our goal is to provide a benchmark that measures a specific, high-value task in scientific reasoning and makes system failures more interpretable.
Metric-aware design.
The benchmark is paired with a domain-based evaluation framework. We score outputs along six dimensions: reasoning-chain fidelity, hypothesis-problem alignment, mechanistic specificity, scientific novelty, intervention plausibility, and problem decomposition quality (details are given in Appendix
A
). We treat these metrics as proxies for different aspects of hypothesis quality that domain researchers care about, such as whether the output addresses the stated failure mode, proposes an intervention at the right level, connects that intervention to a specific mechanism, remains scientifically feasible, and decomposes the problem enough to support solution building. This design is intended to separate outputs that only sound scientific from outputs that address the right problem with the right mechanism. We also report a composite score, but we treat the individual dimensions as important in because they highlight different failure modes, and we use our validation experiments (Section
3
) to test whether the aggregate captures signal beyond conventional metrics and remains more stable under adversarial manipulation.
Contribution.
Matter to Mechanism contributes both a dataset and an evaluation framework. It provides structured problem-solution instances grounded in published materials-science papers. It also provides a way to study whether current co-scientists can move from a concrete scientific problem to a plausible and mechanistically grounded solution. We view this as a targeted benchmark for one important aspect of scientific discovery, rather than as a claim to measure discovery in full.
3
Experiments
We use
Matter to Mechanism
to study how well current AI systems can map a structured scientific problem to a plausible solution hypothesis. Our experiments are guided by three questions. First, can current systems approach the quality of literature-derived hypotheses under a domain-grounded evaluation? Second, which aspects of scientific reasoning remain difficult? Third, do our validation experiments show that the benchmark captures distinctions that are not fully explained by generic text-similarity metrics?
Models.
We evaluate ChemDFM-8B as a domain-specialized baseline
(
Zhao et al. 2025
)
;
Gemini-Weak
and
Gemini-Direct
as direct-generation baselines with weaker and stronger prompting;
Gemini-Retrieval
as a retrieval-augmented variant;
Open Co-Scientist
as an open LangGraph implementation of a Google co-scientist-style workflow inspired by
(
Gottweis et al. 2025
)
; and
AI-Researcher
(
Tang et al. 2025
)
as a general scientific-agent baseline. All systems receive the same problem-side input and are asked to generate a hypothesis together with structured scientific outputs. They are not given the literature hypothesis.
Evaluation Metrics.
Matter to Mechanism
evaluates generated hypotheses along six reference-free dimensions, each scaled to
[
0
,
1
]
[0,1]
. The goal is not to measure text similarity to a single reference answer, but to measure whether the generated hypothesis addresses the scientific problem in a structured and credible way. This design choice follows the broader view in recent evaluation work that benchmarks should make their target construct explicit and should avoid overstating what a single metric can mean
(
Dehghani et al. 2021
;
Raji et al. 2021
;
Longjohn et al. 2024
)
. The six dimensions capture different parts of the task. Reasoning Chain Fidelity (
rcf
) measures whether the reasoning trace is coherent and non-redundant. Hypothesis-Problem Alignment (
hpa
) measures whether the hypothesis actually addresses the stated problem. Mechanistic Specificity Index (
msi
) measures whether the output contains concrete mechanistic content rather than generic scientific language. Scientific Novelty Score (
sns
) measures how distinct the proposal is relative to the benchmark corpus. Intervention Plausibility (
ip
) measures whether the intervention is physically and materially plausible. Problem Decomposition Quality (
pdq
) measures whether the original problem has been framed sharply enough to support solution building. We also report a weighted aggregate,
cbs
, but we do not treat it as a complete substitute for the six individual dimensions.
Evaluation setup.
Our main evaluation is reference-free with respect to hypothesis matching: the six core metrics score the generated output against the input problem fields and its own internal structure, rather than against a gold reference answer (Table
2
). This choice is motivated by the fact that scientific problems can admit multiple plausible hypotheses, and by prior concerns that benchmark conclusions can become too dependent on narrow matching criteria
(
Dehghani et al. 2021
;
Raji et al. 2021
)
. We report all six metric dimensions together with the composite
cbs
score.
Validation experiments.
We also include validation experiments beyond the main leaderboard. We compare
cbs
against generic reference-based metrics such as BLEU
(
Post 2018
;
Tran et al. 2019
)
, ROUGE-L, BERTScore
(
Zhang et al. 2019
)
, and embedding cosine similarity. We also perform pairwise LLM-judge validation
(
Gu et al. 2024
)
using Gemini-family judges with swap-order evaluation, and we run a metric-gaming stress test using adversarial outputs such as problem mirroring, jargon stuffing, and verbose fake reasoning. These validation experiments help clarify what the benchmark captures, what it does not capture, and how robust it is to simple forms of manipulation.
Weighting scheme
The
cbs
weights (Table
2
) are intended to balance multiple aspects of scientific usefulness rather than rewarding only fluent text. We assign the largest weights to
rcf
and
hpa
because an output that does not address the stated problem, or whose reasoning is internally incoherent, is unlikely to be useful even if it appears scientific. We also weight
msi
and
ip
heavily because materials hypotheses must be grounded in a clear mechanism and remain physically plausible.
sns
and
pdq
are weighted somewhat lower because novelty and decomposition quality are most meaningful once the output is already relevant, mechanistically specific, and plausible. We therefore treat
cbs
as a structured summary of the six dimensions rather than a complete measure of scientific quality, and we rely on the validation experiments (Section
4.3
-
4.5
) to test whether this aggregate behaves sensibly in practice. An example of how the weighting scheme works is shown in Appendix
D
.
Table 2
:
Summary of the six core
Matter to Mechanism
metrics. Details of metric computation are provided in Appendix
A
.
Metric
Main purpose
Main inputs
Weight
rcf
reasoning coherence
reasoning, hypothesis
0.20
hpa
problem alignment
hypothesis, problem fields
0.20
msi
mechanistic detail
hypothesis, mechanism, reasoning
0.18
sns
corpus-level novelty
hypothesis, intervention, system
0.15
ip
plausibility
intervention, mechanism, outcome
0.15
pdq
problem decomposition
problem-side fields
0.12
cbs
weighted aggregate
total
1.00
4
Results
We evaluate six systems on our benchmark. The literature-derived
Reference
baseline,
ChemDFM-8B
,
Gemini-Direct
,
Gemini-Weak
,
AI-Researcher
, and
Open Co-Scientist
. Our goal is not only to compare systems by a single aggregate score, but also to understand how they differ across reasoning quality, problem alignment, mechanistic depth, novelty, plausibility, and problem decomposition. Table
3
reports the main system-level results. The literature-derived reference set remains the strongest overall system, with a
cbs
of 0.4646. Among generated systems,
ChemDFM-8B
performs best overall with a
cbs
of 0.4266, followed by
Gemini-Direct
(0.3878),
AI-Researcher
(0.3860),
Gemini-Weak
(0.3790), and
Open Co-Scientist
(0.3790). The gap between the reference and the strongest generated system is therefore non-trivial, which is a useful property for the benchmark: it suggests that the benchmark is not saturated and still distinguishes literature-quality hypotheses from current co-scientist outputs. At the same time, the metric breakdown shows that the systems do not fail in the same way.
Gemini-Direct
and
AI-Researcher
obtain the highest
rcf
scores among the generated systems, indicating strong reasoning-chain structure and fluent multi-step outputs. However, both remain very weak on
msi
, showing that high-quality reasoning traces do not automatically translate into mechanistically specific hypotheses.
Table 3:
Main leaderboard on
Matter to Mechanism
. Scores are means over all instances; 95% bootstrap confidence intervals (2,000 resamples) are shown in brackets. The reference corpus remains strongest overall. Among generated systems,
ChemDFM-8B
achieves the best composite score. A key pattern is that high
rcf
does not imply high
msi
: several systems produce coherent reasoning traces while remaining weak on mechanistic specificity.
System
N
CBS
RCF
HPA
MSI
SNS
IP
PDQ
Reference
2645
0.467
[
0.465
,
0.469
]
0.467_{\,[0.465,\,0.469]}
0.763
[
0.758
,
0.768
]
0.763_{\,[0.758,\,0.768]}
0.110
[
0.106
,
0.114
]
0.110_{\,[0.106,\,0.114]}
0.207
[
0.201
,
0.212
]
0.207_{\,[0.201,\,0.212]}
0.715
[
0.711
,
0.719
]
0.715_{\,[0.711,\,0.719]}
0.536
[
0.530
,
0.541
]
0.536_{\,[0.530,\,0.541]}
0.562
[
0.556
,
0.567
]
0.562_{\,[0.556,\,0.567]}
ChemDFM-8B
2645
0.427
[
0.424
,
0.429
]
0.427_{\,[0.424,\,0.429]}
0.554
[
0.547
,
0.559
]
0.554_{\,[0.547,\,0.559]}
0.257
[
0.252
,
0.262
]
0.257_{\,[0.252,\,0.262]}
0.171
[
0.163
,
0.178
]
0.171_{\,[0.163,\,0.178]}
0.724
[
0.718
,
0.729
]
0.724_{\,[0.718,\,0.729]}
0.385
[
0.382
,
0.389
]
0.385_{\,[0.382,\,0.389]}
0.562
[
0.556
,
0.567
]
0.562_{\,[0.556,\,0.567]}
Gemini-Direct
2645
0.388
[
0.387
,
0.389
]
0.388_{\,[0.387,\,0.389]}
0.746
[
0.744
,
0.747
]
0.746_{\,[0.744,\,0.747]}
0.189
[
0.188
,
0.191
]
0.189_{\,[0.188,\,0.191]}
0.038
[
0.037
,
0.040
]
0.038_{\,[0.037,\,0.040]}
0.724
[
0.721
,
0.728
]
0.724_{\,[0.721,\,0.728]}
0.504
[
0.502
,
0.506
]
0.504_{\,[0.502,\,0.506]}
0.501
[
0.498
,
0.504
]
0.501_{\,[0.498,\,0.504]}
Gemini-Retrieval
2645
0.388
[
0.387
,
0.389
]
0.388_{\,[0.387,\,0.389]}
0.745
[
0.744
,
0.746
]
0.745_{\,[0.744,\,0.746]}
0.188
[
0.187
,
0.190
]
0.188_{\,[0.187,\,0.190]}
0.040
[
0.038
,
0.041
]
0.040_{\,[0.038,\,0.041]}
0.724
[
0.721
,
0.728
]
0.724_{\,[0.721,\,0.728]}
0.504
[
0.502
,
0.506
]
0.504_{\,[0.502,\,0.506]}
0.501
[
0.498
,
0.504
]
0.501_{\,[0.498,\,0.504]}
AI-Researcher
2645
0.386
[
0.384
,
0.388
]
0.386_{\,[0.384,\,0.388]}
0.740
[
0.737
,
0.743
]
0.740_{\,[0.737,\,0.743]}
0.188
[
0.185
,
0.192
]
0.188_{\,[0.185,\,0.192]}
0.039
[
0.035
,
0.043
]
0.039_{\,[0.035,\,0.043]}
0.692
[
0.688
,
0.696
]
0.692_{\,[0.688,\,0.696]}
0.504
[
0.500
,
0.507
]
0.504_{\,[0.500,\,0.507]}
0.498
[
0.491
,
0.504
]
0.498_{\,[0.491,\,0.504]}
Open Co-Scientist
2645
0.379
[
0.377
,
0.381
]
0.379_{\,[0.377,\,0.381]}
0.739
[
0.737
,
0.741
]
0.739_{\,[0.737,\,0.741]}
0.158
[
0.155
,
0.160
]
0.158_{\,[0.155,\,0.160]}
0.042
[
0.039
,
0.046
]
0.042_{\,[0.039,\,0.046]}
0.722
[
0.718
,
0.725
]
0.722_{\,[0.718,\,0.725]}
0.503
[
0.499
,
0.507
]
0.503_{\,[0.499,\,0.507]}
0.498
[
0.491
,
0.505
]
0.498_{\,[0.491,\,0.505]}
Gemini-Weak
2645
0.379
[
0.378
,
0.380
]
0.379_{\,[0.378,\,0.380]}
0.720
[
0.717
,
0.723
]
0.720_{\,[0.717,\,0.723]}
0.179
[
0.178
,
0.181
]
0.179_{\,[0.178,\,0.181]}
0.038
[
0.036
,
0.040
]
0.038_{\,[0.036,\,0.040]}
0.648
[
0.644
,
0.652
]
0.648_{\,[0.644,\,0.652]}
0.502
[
0.501
,
0.504
]
0.502_{\,[0.501,\,0.504]}
0.501
[
0.498
,
0.504
]
0.501_{\,[0.498,\,0.504]}
4.1
Metric-level tradeoffs and Retrieval baseline behaviour
Table
3
shows that systems differ not only in overall
cbs
, but also in their metric profiles.
Gemini-Direct
,
Gemini-Retrieval
, and
AI-Researcher
all obtain high
rcf
scores (0.746, 0.745, and 0.740), indicating coherent and well-formed reasoning traces. However, their
msi
scores remain very low (0.038, 0.040, and 0.039), suggesting that these outputs are often better at organizing reasoning than at specifying a concrete scientific mechanism.
ChemDFM-8B
shows a different profile. It achieves the best generated scores on
hpa
(0.257),
msi
(0.171), and
pdq
(0.562), but has a lower
rcf
score (0.554). This suggests that the chemistry-specialized model is better at proposing structured, domain-grounded hypotheses, even if its reasoning traces are less specific. The reference set remains strongest overall because it balances these dimensions more effectively than any generated system. These results reveal a separation between reasoning fluency and scientific specificity. Strong general-purpose reasoning behavior does not necessarily imply strong scientific problem solving. Co-scientists also need domain grounding in failure modes, meaningful interventions, and plausible mechanisms. This supports the value of adapting strong reasoners to scientific corpora where mechanistic detail and problem decomposition are central. Gemini-Retrieval is nearly tied with
Gemini-Direct
in overall
cbs
but has a slightly higher
msi
score (0.040 vs. 0.038). This suggests that retrieval adds some mechanistic context, but generic retrieval alone does not close the gap to domain-specialized models or the literature-derived reference.
4.2
Error taxonomy
To make the benchmark more interpretable, we group outputs into recurring failure modes using threshold rules over the six metric dimensions. Each entry in Table
4
is the fraction of outputs from that system assigned to the corresponding failure mode. For example, high alignment, weak mechanism captures outputs with relatively strong
hpa
but insufficient
msi
; verbose, weak decomposition captures outputs with strong
rcf
but weak
pdq
; fluent but misaligned captures outputs with high
rcf
and low
hpa
; and specific but not novel captures outputs with high
msi
and low
sns
. Table
4
shows that verbose, weak decomposition and fluent but misaligned outputs are the most common failure modes overall.
ChemDFM-8B
has the highest rate of high alignment, weak mechanism outputs (0.220), which means that it often addresses the problem but still lacks enough mechanistic detail in some cases. This does not contradict Table
3
, where
ChemDFM-8B
has the highest generated
msi
score; rather, it shows that even the strongest generated system still has a mechanism gap relative to literature-derived hypotheses. By contrast,
Open Co-Scientist
,
AI-Researcher
, and
Gemini-Direct
show high rates of verbose, weak decomposition and fluent but misaligned outputs, suggesting that their reasoning traces can be coherent without being sharply tied to the problem structure.
Error category
Overall
Ref.
ChemDFM-8B
G-Direct
G-Weak
AI-Res.
Open-CS
High alignment, weak mechanism
0.067
0.015
0.220
0.084
0.037
0.062
0.004
Novel but implausible
0.014
0.000
0.272
0.000
0.000
0.000
0.000
Verbose, weak decomposition
0.178
0.000
0.002
0.203
0.179
0.218
0.224
Fluent but misaligned
0.175
0.000
0.010
0.226
0.201
0.220
0.228
Specific but not novel
0.024
0.041
0.082
0.008
0.011
0.009
0.009
Table 4
:
Error taxonomy on
Matter to Mechanism
. Two failure modes dominate: high alignment, weak mechanism
(concentrated in
ChemDFM-8B
) and verbose, weak decomposition (common in Gemini and agentic systems). Fluent but misaligned (
rcf
>
>
0.65 and
hpa
<
<
0.15) and specific but not novel (
msi
>
>
0.15 and
sns
<
<
0.70).
Figure 2
:
Rank heatmap comparing
cbs
with generic similarity metrics. Lower rank is better. Generic metrics recover part of the benchmark ordering, but not all domain-grounded distinctions:
ChemDFM-8B
remains first, while local reversals persist, especially between
Gemini-Retrieval
and
Gemini-Direct
.
4.3
Validation against reference-based metrics
It is possible that
cbs
is reproducing what standard text-similarity metrics already show (Figure
2
). To test this, we compare the system-level rankings under
cbs
with reference-based text-similarity metrics: BLEU
(
Post 2018
;
Tran et al. 2019
)
, ROUGE-L
(
Shi et al. 2025
;
Ganesan 2018
)
, BERTScore
(
Zhang et al. 2019
)
, and embedding cosine similarity
(
Steck et al. 2024
)
. Each generated hypothesis is compared against the literature-derived solution hypothesis extracted from the corresponding source paper, using a 500-example subset with 2,149 matched generated rows. Table
5
shows that generic metrics partially recover the benchmark ranking, but do not fully reproduce it.
ChemDFM-8B
remains strongest under all metrics, indicating that the best domain-specialized system is also relatively close to the literature hypotheses. However, agreement is weaker for lexical overlap metrics than for semantic similarity metrics. In particular, Kendall’s
τ
\tau
(
Stepanov 2015
)
between
cbs
and BLEU is 0.60, while agreement with ROUGE-L, BERTScore, and cosine similarity is higher at 0.867. This suggests that these metrics capture semantic closeness to literature hypotheses, but not the full evaluative signal. We also observe that standard metrics do not fully recover the benchmark’s local distinctions.
Gemini-Retrieval
ranks above
Gemini-Direct
under
cbs
, but the ordering changes under some similarity-based metrics. This means that conventional metrics capture semantic closeness to literature hypotheses, but do not fully capture the domain-grounded distinctions that our benchmark is designed to measure, such as mechanistic depth and intervention plausibility.
Metric
Kendall
τ
\tau
vs CBS
p
p
-value
BLEU
0.600
0.1361
ROUGE-L
0.867
0.0167
BERTScore
0.867
0.0167
Cosine sim.
0.867
0.0167
Table 5:
Agreement between
cbs
and conventional metrics. Conventional metrics partially recover the benchmark ranking, but the weaker agreement for BLEU and the remaining local ranking reversals suggest that
Matter to Mechanism
captures distinctions beyond surface overlap.
Statistic
Value
CBS-Gemini 2.5 Pro agreement
0.40
CBS-Gemini Flash agreement
0.60
Pro-Flash agreement
0.32
Mean order-flip rate
0.236
Table 6:
Summary of pairwise LLM-judge validation. Gemini Flash agrees with
cbs
more often than Gemini 2.5 Pro, while inter-judge agreement remains limited.
4.4
Pairwise LLM-judge validation
We also performed a validation experiment using pairwise LLM judging. We use Gemini 2.5 Pro and Gemini 2.5 Flash. For each system pair, we compare outputs on 50 common problems using two prompt orders (A/B and B/A) to reduce order bias
(
Ye et al. 2024
;
Li et al. 2025
;
Shi et al. 2025
)
. The full judge prompt is provided in Appendix
C
. Each comparison is run twice with swapped order to reduce position bias. Across the tested pairs, agreement between
cbs
and Gemini Flash is 0.60, while agreement between
cbs
and Gemini 2.5 Pro is 0.40. Agreement between the two judges themselves is 0.32, and the mean order-flip rate is 0.236. These numbers indicate that pairwise LLM judgment is informative in this setting, but also noisy and sensitive to both judge choice and presentation order. Gemini Flash is more decisive and more often agrees with the benchmark ranking. Gemini 2.5 Pro, by contrast, is highly tie-prone, which lowers its raw agreement with
cbs
even when it rarely makes strong contradictory judgments. For example, in the
ChemDFM-8B
versus
Gemini-Direct
comparison, Gemini 2.5 Pro returns 36 ties out of 50 cases, while Gemini Flash returns only 5 ties and strongly prefers
ChemDFM-8B
. Similar behavior appears in the
ChemDFM-8B
versus
AI-Researcher
comparison. The results are consistent with the main benchmark conclusions, especially for clearer system gaps, but they also reinforce an important methodological point: external LLM judgment in scientific settings is itself unstable and should not be treated as ground truth.
4.5
Metric-gaming test
We also tested whether the benchmark can be manipulated by adversarial strategies (Table
7
). We generate 75 adversarial examples for each of three attack styles: jargon stuffing
(
Yuan and Dasgupta 2024
)
, problem mirroring
(
Yan et al. 2024
)
, and verbose fake reasoning
(
Jiao et al. 2025
)
. These attacks were designed to produce outputs that look aligned to the problem while remaining weak in actual scientific content. We observed that none of these attacks improves the overall
cbs
score. All adversarial styles reduce
cbs
relative to the original outputs: jargon stuffing by 0.0348, problem mirroring by 0.0353, and verbose fake reasoning by 0.0543. However, some local dimensions can be manipulated.
hpa
increases under all three attack styles, with the largest increase coming from problem mirroring (+0.1327). This is expected since mirroring key problem terms can make an output appear more aligned to the input problem. However, these same attacks are strongly penalized on
msi
and
ip
. Jargon stuffing reduces
msi
by 0.1307 and
ip
by 0.1580, while verbose fake reasoning reduces
msi
by 0.1486 and
ip
by 0.1310. This means that although individual dimensions can be partially gamed, the full benchmark is substantially more resistant than any single component alone.
Type of Attack
Δ
\Delta
HPA
Δ
\Delta
MSI
Δ
\Delta
IP
Δ
\Delta
CBS
Jargon stuffing
+0.0679
-0.1307
-0.1580
-0.0348
Problem mirroring
+0.1327
-0.1295
-0.0886
-0.0353
Verbose fake reasoning
+0.0602
-0.1486
-0.1310
-0.0543
Table 7:
Metric-gaming stress test. Simple adversarial attacks can inflate local alignment signals, especially
hpa
, but they reduce mechanistic specificity, plausibility, and overall
cbs
. This suggests that the aggregate benchmark is more stable than any individual dimension alone.
5
Discussion and Limitations
Our results show that
Matter to Mechanism
is non-trivial: literature-derived hypotheses remain stronger overall than current AI co-scientist outputs. The benchmark separates systems in an interpretable way, especially along the axis of reasoning fluency versus scientific specificity. Conventional metrics recover only part of the evaluative signal. The benchmark is not trivially broken by simple adversarial strategies, although some individual dimensions are easier to manipulate than others. At the same time,
Matter to Mechanism
evaluates one specific part of scientific reasoning, which is moving from a structured materials problem to a plausible solution hypothesis. Additional ablations on metric redundancy and rare-term contamination are provided in (section
6
) The benchmark is constructed from published papers, and the structured fields are automatically extracted, so some examples may contain noise or incomplete structure. Pairwise LLM judging provides useful proxy evidence, but judges show limited agreement and remain sensitive to prompt order. Moreover, the benchmark focuses on hypotheses and mechanisms, rather than explicit tool use or experiment planning. In real material workflows, a useful output may also need to specify next-step analyses such as DFT calculations, electrochemical protocols, or characterization methods. Incorporating these decisions is an important direction for future work. Discussion of metric validity, evidence-strength limitations in
ip
, retrieval/direct parity, and reference
hpa
behavior is provided in Appendix
B
.
6
Ablation Study
We performed two additional checks. First, the six metrics are related but not redundant: pairwise correlations are generally small, with near-zero correlation between
rcf
and
sns
(
ρ
=
0.0045
\rho=0.0045
) and between
hpa
and
sns
(
ρ
=
0.0229
\rho=0.0229
), while
hpa
and
msi
(
ρ
=
0.2191
\rho=0.2191
) and
msi
and
pdq
(
ρ
=
0.2211
\rho=0.2211
) show only modest positive correlation. This suggests that the metrics belong to the same task but capture different aspects of scientific reasoning, so strong fluent reasoning does not automatically imply strong mechanism or alignment. Second, since the benchmark is built from published papers, contamination and memorization can occur. We mitigate this by using reference-free metrics that score outputs against the input problem and internal structure rather than by direct answer matching. Rare-term analysis suggests that highly specific mechanistic detail is uncommon in the corpus: the mean rare-term count is 0.021, 98% of examples contain zero such terms, and only 0.1% contain two or more. This reduces the risk that benchmark performance is dominated by obvious memorization.
6.1
CBS Weight Sensitivity
Table
8
reports system rankings under four alternative
cbs
weight schemes. The top two systems,
Reference
and
ChemDFM-8B
, are stable across all schemes, and the bottom system,
Gemini-Weak
, is also stable. The only instability occurs between
Gemini-Direct
and
Gemini-Retrieval
under the
msi
-heavy scheme. This is interpretable: when mechanistic specificity is weighted at 0.40, the small
msi
advantage of
Gemini-Retrieval
(0.040 vs. 0.038) becomes decisive. Overall, the rankings are stable under reasonable weight perturbations, with Kendall’s
τ
≥
0.905
\tau\geq 0.905
relative to the default ranking.
Table 8:
cbs
scores under alternative weight schemes.
Default:
w
=
[
0.20
,
0.20
,
0.18
,
0.15
,
0.15
,
0.12
]
w=[0.20,0.20,0.18,0.15,0.15,0.12]
for (
rcf
,
hpa
,
msi
,
sns
,
ip
,
pdq
).
Rankings are stable except for the
Gemini-Direct
/
Gemini-Retrieval
swap under
msi
-heavy weighting.
System
Default
Uniform
rcf
-heavy
msi
-heavy
Reference
0.467
0.482
0.561
0.405
ChemDFM-8B
0.427
0.442
0.473
0.366
Gemini-Direct
0.388
0.330
0.446
0.248
Gemini-Retrieval
0.388
0.330
0.446
0.249
AI-Researcher
0.386
0.328
0.444
0.247
Open Co-Scientist
0.379
0.323
0.440
0.245
Gemini-Weak
0.379
0.323
0.434
0.243
Rank correlation with default ranking (Kendall’s
τ
\tau
):
vs. Uniform
—
0.905
—
—
vs.
rcf
-heavy
—
—
1.000
—
vs.
msi
-heavy
—
—
—
0.905
6.2
Additional Validations
We ran three additional checks to clarify potential weaknesses of the benchmark. The reliability of the
ip
evidence-strength field, the quality of automatically extracted instances, and the near-parity between
Gemini-Direct
and
Gemini-Retrieval
.
Evidence-strength field in
ip
.
The
ip
metric includes an evidence-strength subscore extracted from the source paper. Across the 2,645 benchmark instances, 61.3% are labeled strong, 38.4% are labeled moderate, 0.2% are labeled unknown, and 0.1% are labeled weak. These map to evidence subscores of 1.00, 0.65, 0.35, and 0.25, respectively. The mean evidence subscore is 0.864, with only 0.2% of examples receiving the unknown fallback. This suggests that the
ip
evidence component is usually supported by an explicit evidence label rather than dominated by missing-field defaults.
Instance-quality spot check.
We also performed a spot check of 50 randomly sampled instances using GPT-5.5 as the evaluator. We found 31 responses were validly parsed. The pass rates were 96.8% for problem-statement correctness, 100.0% for failure-mode specificity, 96.8% for intervention relevance, and 87.1% for mechanism coherence. Overall, 83.9% of valid instances passed all four criteria, and 87.1% were rated high quality. Because the evaluator is an LLM rather than a human expert, we treat this as a consistency check rather than independent human validation.
Retrieval-direct parity.
Gemini-Retrieval
and
Gemini-Direct
achieve nearly identical
cbs
scores (0.3877 vs. 0.3878). Retrieval slightly increases
msi
(+0.0012) and
ip
(+0.0002), but slightly decreases
rcf
(-0.0006) and
hpa
(-0.0011). This suggests that retrieval adds a small amount of mechanistic context, but does not substantially change the quality of the generated hypotheses. In this benchmark, generic retrieval alone is therefore not sufficient to close the gap to domain-specialized systems such as
ChemDFM-8B
.
Table 9:
Instance-quality spot check on 31 valid randomly sampled instances.
Criterion
Pass rate
Problem statement correct
96.8%
Failure mode specific
100.0%
Intervention relevant
96.8%
Mechanism coherent
87.1%
All four correct
83.9%
Overall high quality
87.1%
7
Acknowledgments
This work was supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research and Office of Basic Energy Sciences, Scientific Discovery through Advanced Computing (SciDAC) program under the FORUM-AI project. Work performed at the Center for Nanoscale Materials, a U.S. Department of Energy Office of Science User Facility, was supported by the U.S. DOE, Office of Basic Energy Sciences, under Contract No. DE-AC02-06CH11357.
References
Alampara et al. [2024]
Nawaf Alampara, Mara Schilling-Wilhelmi, Martiño Ríos-García, Indrajeet Mandal, Pranav Khetarpal, Hargun Singh Grover, N. M. Anoop Krishnan, and Kevin Maik Jablonka.
Probing the limitations of multimodal language models for chemistry and materials research.
arXiv e-prints
, art. arXiv:2411.16955, November 2024.
doi:
10.48550/arXiv.2411.16955
.
Chehbouni et al. [2025]
Khaoula Chehbouni, Mohammed Haddou, Jackie Chi Kit Cheung, and Golnoosh Farnadi.
Neither Valid nor Reliable? Investigating the Use of LLMs as Judges.
arXiv e-prints
, art. arXiv:2508.18076, August 2025.
doi:
10.48550/arXiv.2508.18076
.
Chen et al. [2024]
Ziru Chen, Shijie Chen, Yuting Ning, Qianheng Zhang, Boshi Wang, Botao Yu, Yifei Li, Zeyi Liao, Chen Wei, Zitong Lu, Vishal Dey, Mingyi Xue, Frazier N. Baker, Benjamin Burns, Daniel Adu-Ampratwum, Xuhui Huang, Xia Ning, Song Gao, Yu Su, and Huan Sun.
ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery.
arXiv e-prints
, art. arXiv:2410.05080, October 2024.
doi:
10.48550/arXiv.2410.05080
.
Dehghani et al. [2021]
Mostafa Dehghani, Yi Tay, Alexey A. Gritsenko, Zhe Zhao, Neil Houlsby, Fernando Diaz, Donald Metzler, and Oriol Vinyals.
The Benchmark Lottery.
arXiv e-prints
, art. arXiv:2107.07002, July 2021.
doi:
10.48550/arXiv.2107.07002
.
Ganesan [2018]
Kavita Ganesan.
ROUGE 2.0: Updated and Improved Measures for Evaluation of Summarization Tasks.
arXiv e-prints
, art. arXiv:1803.01937, March 2018.
doi:
10.48550/arXiv.1803.01937
.
Gottweis et al. [2025]
Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Anil Palepu, Petar Sirkovic, Artiom Myaskovsky, Felix Weissenberger, Keran Rong, Ryutaro Tanno, Khaled Saab, Dan Popovici, Jacob Blum, Fan Zhang, Katherine Chou, Avinatan Hassidim, Burak Gokturk, Amin Vahdat, Pushmeet Kohli, Yossi Matias, Andrew Carroll, Kavita Kulkarni, Nenad Tomasev, Yuan Guan, Vikram Dhillon, Eeshit Dhaval Vaishnav, Byron Lee, Tiago R D Costa, José R Penadés, Gary Peltz, Yunhan Xu, Annalisa Pawlosky, Alan Karthikesalingam, and Vivek Natarajan.
Towards an AI co-scientist.
arXiv e-prints
, art. arXiv:2502.18864, February 2025.
doi:
10.48550/arXiv.2502.18864
.
Gu et al. [2024]
Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni, and Jian Guo.
A Survey on LLM-as-a-Judge.
arXiv e-prints
, art. arXiv:2411.15594, November 2024.
doi:
10.48550/arXiv.2411.15594
.
Jiao et al. [2025]
Rui Jiao, Yue Zhang, and Jinku Li.
Trustworthy Reasoning: Evaluating and Enhancing Factual Accuracy in LLM Intermediate Thought Processes.
arXiv e-prints
, art. arXiv:2507.22940, July 2025.
doi:
10.48550/arXiv.2507.22940
.
Kumbhar et al. [2025]
Shrinidhi Kumbhar, Venkatesh Mishra, Kevin Coutinho, Divij Handa, Ashif Iquebal, and Chitta Baral.
Hypothesis Generation for Materials Discovery and Design Using Goal-Driven and Constraint-Guided LLM Agents.
arXiv e-prints
, art. arXiv:2501.13299, January 2025.
doi:
10.48550/arXiv.2501.13299
.
Li et al. [2025]
Qingquan Li, Shaoyu Dou, Kailai Shao, Chao Chen, and Haixiang Hu.
Evaluating Scoring Bias in LLM-as-a-Judge.
arXiv e-prints
, art. arXiv:2506.22316, June 2025.
doi:
10.48550/arXiv.2506.22316
.
Liu et al. [2025a]
Siyu Liu, Bo Hu, Beilin Ye, Jiamin Xu, David J. Srolovitz, and Tongqi Wen.
MatTools: Benchmarking Large Language Models for Materials Science Tools.
arXiv e-prints
, art. arXiv:2505.10852, May 2025a.
doi:
10.48550/arXiv.2505.10852
.
Liu et al. [2025b]
Yujie Liu, Zonglin Yang, Tong Xie, Jinjie Ni, Ben Gao, Yuqiang Li, Shixiang Tang, Wanli Ouyang, Erik Cambria, and Dongzhan Zhou.
ResearchBench: Benchmarking LLMs in Scientific Discovery via Inspiration-Based Task Decomposition.
arXiv e-prints
, art. arXiv:2503.21248, March 2025b.
doi:
10.48550/arXiv.2503.21248
.
Longjohn et al. [2024]
Rachel Longjohn, Markelle Kelly, Sameer Singh, and Padhraic Smyth.
Benchmark Data Repositories for Better Benchmarking.
arXiv e-prints
, art. arXiv:2410.24100, October 2024.
doi:
10.48550/arXiv.2410.24100
.
Mirza et al. [2024]
Adrian Mirza, Nawaf Alampara, Sreekanth Kunchapu, Martiño Ríos-García, Benedict Emoekabu, Aswanth Krishnan, Tanya Gupta, Mara Schilling-Wilhelmi, Macjonathan Okereke, Anagha Aneesh, Amir Mohammad Elahi, Mehrdad Asgari, Juliane Eberhardt, Hani M. Elbeheiry, María Victoria Gil, Maximilian Greiner, Caroline T. Holick, Christina Glaubitz, Tim Hoffmann, Abdelrahman Ibrahim, Lea C. Klepsch, Yannik Köster, Fabian Alexander Kreth, Jakob Meyer, Santiago Miret, Jan Matthias Peschel, Michael Ringleb, Nicole Roesner, Johanna Schreiber, Ulrich S. Schubert, Leanne M. Stafast, Dinga Wonanke, Michael Pieler, Philippe Schwaller, and Kevin Maik Jablonka.
Are large language models superhuman chemists?
arXiv e-prints
, art. arXiv:2404.01475, April 2024.
doi:
10.48550/arXiv.2404.01475
.
Mitchener et al. [2025]
Ludovico Mitchener, Jon M Laurent, Alex Andonian, Benjamin Tenmann, Siddharth Narayanan, Geemi P Wellawatte, Andrew White, Lorenzo Sani, and Samuel G Rodriques.
BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology.
arXiv e-prints
, art. arXiv:2503.00096, February 2025.
doi:
10.48550/arXiv.2503.00096
.
Post [2018]
Matt Post.
A Call for Clarity in Reporting BLEU Scores.
arXiv e-prints
, art. arXiv:1804.08771, April 2018.
doi:
10.48550/arXiv.1804.08771
.
Prasad Majumder et al. [2024]
Bodhisattwa Prasad Majumder, Harshit Surana, Dhruv Agarwal, Bhavana Dalvi Mishra, Abhijeetsingh Meena, Aryan Prakhar, Tirth Vora, Tushar Khot, Ashish Sabharwal, and Peter Clark.
DiscoveryBench: Towards Data-Driven Discovery with Large Language Models.
arXiv e-prints
, art. arXiv:2407.01725, July 2024.
doi:
10.48550/arXiv.2407.01725
.
Raji et al. [2021]
Inioluwa Deborah Raji, Emily M. Bender, Amandalynne Paullada, Emily Denton, and Alex Hanna.
AI and the Everything in the Whole Wide World Benchmark.
arXiv e-prints
, art. arXiv:2111.15366, November 2021.
doi:
10.48550/arXiv.2111.15366
.
Shi et al. [2025]
Lin Shi, Chiyu Ma, Wenhua Liang, Xingjian Diao, Weicheng Ma, and Soroush Vosoughi.
Judging the judges: A systematic study of position bias in LLM-as-a-judge.
In Kentaro Inui, Sakriani Sakti, Haofen Wang, Derek F. Wong, Pushpak Bhattacharyya, Biplab Banerjee, Asif Ekbal, Tanmoy Chakraborty, and Dhirendra Pratap Singh, editors,
Proceedings of the 14th International Joint Conference on Natural Language Processing and the 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics
, pages 292–314, Mumbai, India, December 2025. The Asian Federation of Natural Language Processing and The Association for Computational Linguistics.
ISBN 979-8-89176-298-5.
doi:
10.18653/v1/2025.ijcnlp-long.18
.
URL
https://aclanthology.org/2025.ijcnlp-long.18/
.
Steck et al. [2024]
Harald Steck, Chaitanya Ekanadham, and Nathan Kallus.
Is Cosine-Similarity of Embeddings Really About Similarity?
arXiv e-prints
, art. arXiv:2403.05440, March 2024.
doi:
10.48550/arXiv.2403.05440
.
Stepanov [2015]
Alexei Stepanov.
On the Kendall Correlation Coefficient.
arXiv e-prints
, art. arXiv:1507.01427, July 2015.
doi:
10.48550/arXiv.1507.01427
.
Tang et al. [2025]
Jiabin Tang, Lianghao Xia, Zhonghang Li, and Chao Huang.
AI-Researcher: Autonomous Scientific Innovation.
arXiv e-prints
, art. arXiv:2505.18705, May 2025.
doi:
10.48550/arXiv.2505.18705
.
Tian et al. [2024]
Minyang Tian, Luyu Gao, Shizhuo Dylan Zhang, Xinan Chen, Cunwei Fan, Xuefei Guo, Roland Haas, Pan Ji, Kittithat Krongchon, Yao Li, Shengyan Liu, Di Luo, Yutao Ma, Hao Tong, Kha Trinh, Chenyu Tian, Zihan Wang, Bohao Wu, Yanyu Xiong, Shengzhu Yin, Minhui Zhu, Kilian Lieret, Yanxin Lu, Genglin Liu, Yufeng Du, Tianhua Tao, Ofir Press, Jamie Callan, Eliu Huerta, and Hao Peng.
SciCode: A Research Coding Benchmark Curated by Scientists.
arXiv e-prints
, art. arXiv:2407.13168, July 2024.
doi:
10.48550/arXiv.2407.13168
.
Tran et al. [2019]
Ngoc Tran, Hieu Tran, Son Nguyen, Hoan Nguyen, and Tien N. Nguyen.
Does BLEU Score Work for Code Migration?
arXiv e-prints
, art. arXiv:1906.04903, June 2019.
doi:
10.48550/arXiv.1906.04903
.
Wagstaff [2012]
Kiri Wagstaff.
Machine Learning that Matters.
arXiv e-prints
, art. arXiv:1206.4656, June 2012.
doi:
10.48550/arXiv.1206.4656
.
Yan et al. [2024]
Hanqi Yan, Qinglin Zhu, Xinyu Wang, Lin Gui, and Yulan He.
Mirror: A Multiple-perspective Self-Reflection Method for Knowledge-rich Reasoning.
arXiv e-prints
, art. arXiv:2402.14963, February 2024.
doi:
10.48550/arXiv.2402.14963
.
Ye et al. [2024]
Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer, Chao Huang, Pin-Yu Chen, Nitesh V Chawla, and Xiangliang Zhang.
Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge.
arXiv e-prints
, art. arXiv:2410.02736, October 2024.
doi:
10.48550/arXiv.2410.02736
.
Yuan and Dasgupta [2024]
Jun Yuan and Aritra Dasgupta.
Fooling SHAP with Output Shuffling Attacks.
arXiv e-prints
, art. arXiv:2408.06509, August 2024.
doi:
10.48550/arXiv.2408.06509
.
Zhang et al. [2019]
Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q. Weinberger, and Yoav Artzi.
BERTScore: Evaluating Text Generation with BERT.
arXiv e-prints
, art. arXiv:1904.09675, April 2019.
doi:
10.48550/arXiv.1904.09675
.
Zhao et al. [2025]
Zihan Zhao, Da Ma, Lu Chen, Liangtai Sun, Zihao Li, Yi Xia, Bo Chen, Hongshen Xu, Zichen Zhu, Su Zhu, Shuai Fan, Guodong Shen, Kai Yu, and Xin Chen.
Developing ChemDFM as a large language foundation model for chemistry.
Cell Reports Physical Science
, 6(4):102523, April 2025.
doi:
10.1016/j.xcrp.2025.102523
.
Zou et al. [2023]
Deyu Zou, Shikun Liu, Siqi Miao, Victor Fung, Shiyu Chang, and Pan Li.
GeSS: Benchmarking Geometric Deep Learning under Scientific Applications with Distribution Shifts.
arXiv e-prints
, art. arXiv:2310.08677, October 2023.
doi:
10.48550/arXiv.2310.08677
.
Appendix A
Metrics
A.1
Reasoning Chain Fidelity (
rcf
)
Steps
{
s
1
,
…
,
s
n
}
\{s_{1},\ldots,s_{n}\}
are extracted by parsing
[Begin Step
k
k
]…[End Step
k
k
]
tags from
the
reasoning_process
field.
Progression.
For each adjacent pair
(
s
i
,
s
i
+
1
)
(s_{i},s_{i+1})
:
p
i
=
1
−
|
J
⁡
(
s
i
,
s
i
+
1
)
−
0.25
|
0.75
,
rcf
prog
=
max
⁡
(
0
,
1
n
−
1
​
∑
i
=
1
n
−
1
p
i
)
p_{i}=1-\frac{|J(s_{i},s_{i+1})-0.25|}{0.75},\qquad\textsc{rcf}_{\text{prog}}=\max\!\left(0,\,\frac{1}{n-1}\sum_{i=1}^{n-1}p_{i}\right)
(1)
Target overlap 0.25 reflects the empirical distribution of consecutive-step Jaccard similarities in the reference corpus (
μ
=
0.24
\mu{=}0.24
,
σ
=
0.07
\sigma{=}0.07
,
n
=
500
n{=}500
).
Convergence.
rcf
conv
=
J
⁡
(
s
n
,
H
)
\textsc{rcf}_{\text{conv}}=J(s_{n},H)
, where
H
H
is the generated hypothesis.
Non-redundancy.
rcf
nr
=
max
⁡
(
0
,
1
−
2
n
⁡
(
n
−
1
)
​
∑
i
<
j
J
⁡
(
s
i
,
s
j
)
)
\textsc{rcf}_{\text{nr}}=\max\!\left(0,\,1-\frac{2}{n(n-1)}\sum_{i<j}J(s_{i},s_{j})\right)
(2)
Density.
Let
w
¯
=
1
n
​
∑
k
|
s
k
|
words
\bar{w}=\frac{1}{n}\sum_{k}|s_{k}|_{\text{words}}
.
σ
low
\displaystyle\sigma_{\text{low}}
=
1
1
+
e
−
0.05
​
(
w
¯
−
40
)
,
σ
high
=
1
1
+
e
−
0.02
​
(
w
¯
−
150
)
\displaystyle=\tfrac{1}{1+e^{-0.05(\bar{w}-40)}},\quad\sigma_{\text{high}}=\tfrac{1}{1+e^{-0.02(\bar{w}-150)}}
(3)
rcf
den
\displaystyle\textsc{rcf}_{\text{den}}
=
max
⁡
(
0
,
min
⁡
(
σ
low
,
1
−
σ
high
)
)
\displaystyle=\max\!\left(0,\,\min(\sigma_{\text{low}},\,1-\sigma_{\text{high}})\right)
(4)
The double-sigmoid peaks at
w
¯
≈
80
\bar{w}{\approx}80
words/step
and decays toward 0 for
w
¯
<
20
\bar{w}{<}20
or
w
¯
>
200
\bar{w}{>}200
.
A.2
Hypothesis-Problem Alignment (
hpa
)
Let
P
P
,
H
H
,
F
F
,
I
I
,
M
M
,
T
T
denote the problem statement, hypothesis, failure mode, intervention, mechanism, and target property fields respectively.
Causal language sub-score.
𝒞
\mathcal{C}
is a set of 13 causal connector patterns: {thereby, thus, leading to, resulting in, which enables, by
…
\ldots
increas-, enhancing, reducing, improving, will
…
\ldots
enable, provides, allows, facilitates}.
hpa
causal
=
min
(
1
,
|
{
c
∈
𝒞
:
c
​
matches
​
H
}
|
4
)
\textsc{hpa}_{\text{causal}}=\min\!\left(1,\,\frac{|\{c\in\mathcal{C}:c\text{ matches }H\}|}{4}\right)
(5)
The denominator 4 is calibrated so that
≥
4
\geq 4
distinct
causal connectors in a 2–3 sentence hypothesis indicates
saturated causal expressivity (
≥
95
{\geq}95
th percentile of
reference corpus).
Fallbacks.
If
F
=
∅
F=\varnothing
:
hpa
fail
=
0.8
⋅
J
⁡
(
P
,
H
)
\textsc{hpa}_{\text{fail}}=0.8\cdot J(P,H)
.
If
T
=
∅
T=\varnothing
:
hpa
tgt
=
0.5
\textsc{hpa}_{\text{tgt}}=0.5
.
If
I
=
∅
I=\varnothing
or
M
=
∅
M=\varnothing
:
hpa
coh
=
0.3
\textsc{hpa}_{\text{coh}}=0.3
.
A.3
Mechanistic Specificity Index (
msi
)
Let
C
=
H
⊕
M
⊕
R
C=H\oplus M\oplus R
(concatenation of hypothesis, mechanism, reasoning process).
Vocabulary tiers.
Three curated vocabulary sets, all entries lowercased and matched as substrings in
C
C
:
•
𝒦
H
\mathcal{K}_{H}
(44 terms, weight 3): electrochemical mechanism terms, e.g.Butler-Volmer,
solid electrolyte interphase, tortuosity, operando, Coulombic efficiency, Jahn-Teller, lattice parameter, formation energy.
•
𝒦
M
\mathcal{K}_{M}
(23 terms, weight 1.5): materials/component terms, e.g. doping, porosity, capacity fade, volume expansion, SEI, grain boundary.
•
𝒦
L
\mathcal{K}_{L}
(13 terms, weight 0.5): vague filler terms, e.g. improve, enhance, novel, promising, efficient.
msi
vocab
=
min
⁡
(
1
,
3
​
h
+
1.5
​
m
+
0.5
​
ℓ
3
​
|
𝒦
H
|
+
1.5
​
|
𝒦
M
|
+
0.5
​
|
𝒦
L
|
×
3
)
\textsc{msi}_{\text{vocab}}=\min\!\left(1,\,\frac{3h+1.5m+0.5\ell}{3|\mathcal{K}_{H}|+1.5|\mathcal{K}_{M}|+0.5|\mathcal{K}_{L}|}\times 3\right)
(6)
The
×
3
\times 3
normalization ensures the score spans
[
0
,
1
]
[0,1]
for typical scientific texts; without it, the denominator is too large for any single hypothesis to saturate.
Quantitative grounding.
𝒬
\mathcal{Q}
: 10 regex patterns matching physical quantities with units, including nm/µm/mm,
∘
C/K, eV/kJ, mAh/Wh, mol, V/mV, mA/cm
2
, %, mg/g/cm
3
, and scientific notation (
a
×
10
b
a{\times}10^{b}
).
Saturates at 5 distinct matches.
Characterization anchoring.
𝒳
\mathcal{X}
: 23 techniques—XRD, TEM, SEM, XPS, EIS, NMR, Raman, FTIR, DFT, AIMD, synchrotron, neutron diffraction, operando, cryo-TEM, SAXS, WAXS, DSC, TGA, GITT, PITT, cyclic voltammetry, galvanostatic, impedance spectroscopy. Saturates at 4 distinct matches.
Mechanism depth.
msi
depth
=
min
⁡
(
1
,
|
M
|
w
/
(
3
​
|
H
|
w
)
)
\textsc{msi}_{\text{depth}}=\min(1,\,|M|_{w}/(3|H|_{w}))
. Saturates when the mechanism rationale is
≥
3
×
\geq 3{\times}
the word count of the hypothesis, consistent with the median ratio of 3.2 in the reference corpus.
A.4
Scientific Novelty Score (
sns
)
TF-IDF construction.
For corpus
{
H
1
,
…
,
H
N
}
\{H_{1},\ldots,H_{N}\}
, vocabulary
V
=
2000
V{=}2000
(top terms by document frequency, 3-character minimum):
X
i
​
j
=
c
i
​
j
∑
k
c
i
​
k
×
(
log
⁡
N
+
1
d
​
f
j
+
1
+
1
)
X_{ij}=\frac{c_{ij}}{\sum_{k}c_{ik}}\times\left(\log\frac{N+1}{df_{j}+1}+1\right)
(7)
Rows are
ℓ
2
\ell_{2}
-normalised. The cosine similarity matrix
is
𝐒
=
𝐗𝐗
⊤
\mathbf{S}=\mathbf{X}\mathbf{X}^{\top}
with
S
i
​
i
=
−
1
S_{ii}=-1
to exclude self-similarity.
Corpus novelty.
sns
corp
​
(
i
)
=
1
−
1
5
​
∑
k
=
1
5
S
i
,
π
i
​
(
k
)
\textsc{sns}_{\text{corp}}(i)=1-\frac{1}{5}\sum_{k=1}^{5}S_{i,\pi_{i}(k)}
(8)
where
π
i
​
(
k
)
\pi_{i}(k)
is the
k
k
-th most similar hypothesis index. Top-5 mean (not max) is used for robustness against a single near-duplicate.
Within-system novelty.
For each battery system group
ℬ
\mathcal{B}
, the same pipeline is run on the submatrix
𝐗
ℬ
\mathbf{X}_{\mathcal{B}}
using top-3 neighbors (smaller groups have fewer comparators).
Cross-domain bonus.
𝒟
\mathcal{D}
: 28 terms from adjacent fields biomimetic, aerogel, MOF, COF, zeolite, metamaterial, topology, fractal, quantum, plasma, textile, machine learning, neural network, gasification, wood-derived, bio-inspired, biomass, silk, cellulose, chitin, and 8 others. Saturates at 2 distinct hits.
A.5
Intervention Plausibility (
ip
)
Material compatibility.
System-to-material keyword mapping (6 families):
System
Expected constituent keywords
NMC
li, ni, mn, co, oxide, layered
LFP
fe, phosphate, olivine, iron
NCA
ni, co, al, layered
Silicon
si, silicon, expansion, volume
Solid-state
solid, ceramic, sulfide, oxide, garnet
Li metal
li metal, dendrite, plating
ip
mat
=
min
⁡
(
1
,
0.5
+
0.1
×
hits
)
\textsc{ip}_{\text{mat}}=\min(1,\,0.5+0.1\times\text{hits})
.
Defaults to 0.5 for unrecognised systems.
Scalability.
𝒮
+
\mathcal{S}^{+}
: 14 terms (scalable, cost-effective, low-cost, roll-to-roll, industrial, commercializ-, mass produc-, pilot, kg-scale, ton-scale, solution process, spray coat, simple, facile).
𝒮
−
\mathcal{S}^{-}
: 4 terms (atomic layer deposition [unqualified], CVD without scalability qualifier, extremely expensive, requires ultra-high vacuum).
ip
scale
=
max
⁡
(
0
,
min
⁡
(
1
,
0.3
+
0.15
​
|
𝒮
+
∩
C
|
−
0.2
​
|
𝒮
−
∩
C
|
)
)
\textsc{ip}_{\text{scale}}=\max\!\left(0,\,\min\!\left(1,\,0.3+0.15|\mathcal{S}^{+}\cap C|-0.2|\mathcal{S}^{-}\cap C|\right)\right)
(9)
Evidence grounding.
Mapped from
evidence_strength
field: strong/high
→
1.0
{\to}1.0
; moderate
→
0.65
{\to}0.65
; theoretical
→
0.50
{\to}0.50
; preliminary
→
0.40
{\to}0.40
; unknown
→
0.35
{\to}0.35
; weak
→
0.25
{\to}0.25
.
Outcome specificity.
ip
out
=
0.8
\textsc{ip}_{\text{out}}=0.8
if
O
O
matches a numeric quantity with unit (regex:
\d+%|\d+ mAh|\d+ V
, etc.);
0.6
0.6
if
|
O
|
w
>
10
|O|_{w}>10
; else
0.3
0.3
.
A.6
Problem Decomposition Quality (
pdq
)
Root-cause compression.
Let
r
=
|
P
core
|
w
/
|
P
|
w
r=|P_{\text{core}}|_{w}/|P|_{w}
:
pdq
core
=
{
1.0
0.15
≤
r
≤
0.50
0.7
0.05
≤
r
<
0.15
​
or
​
0.50
<
r
≤
0.80
0.4
r
>
0.80
0.3
r
<
0.05
\textsc{pdq}_{\text{core}}=\begin{cases}1.0&0.15\leq r\leq 0.50\\
0.7&0.05\leq r<0.15\;\text{or}\;0.50<r\leq 0.80\\
0.4&r>0.80\\
0.3&r<0.05\end{cases}
(10)
Failure mode specificity.
f
spec
f_{\text{spec}}
: count of
𝒦
H
\mathcal{K}_{H}
terms in
F
F
.
f
vague
f_{\text{vague}}
: count of {poor, bad, issue, problem,
challenge, difficulty, limitation} in
F
F
.
pdq
fail
=
max
⁡
(
0
,
min
⁡
(
1
,
0.3
+
0.2
​
f
spec
−
0.1
​
f
vague
)
)
\textsc{pdq}_{\text{fail}}=\max(0,\,\min(1,\,0.3+0.2f_{\text{spec}}-0.1f_{\text{vague}}))
.
Abstraction consistency.
pdq
abs
=
max
⁡
(
0.2
,
J
⁡
(
P
broad
,
P
fine
)
)
\textsc{pdq}_{\text{abs}}=\max(0.2,\,J(P_{\text{broad}},P_{\text{fine}}))
. Floor of 0.2 accounts for valid IS-A relationships without shared surface tokens (e.g., “thermal etching” specialises
“mass transport”).
Appendix B
Metric Validity and Remaining Limitations
The six metrics in
Matter to Mechanism
are intended as transparent operational proxies for domain-relevant aspects of hypothesis quality, not as ground-truth measures of scientific discovery. We therefore assess them through converging validity checks rather than a single definitive test.
4.1
shows that the dimensions separate different system behaviors: for example, high
rcf
does not imply high
msi
. Tests in
4.2
checks whether low-scoring regions correspond to interpretable scientific failure modes. Comparisons with BLEU, ROUGE-L, BERTScore, and embedding cosine similarity test whether
cbs
captures signal beyond conventional reference matching.
4.4
provides noisy external evidence, while gaming stress test in
4.5
checks whether the aggregate remains stable under superficial adversarial manipulation. Finally,
6.1
shows that the main ranking is stable under reasonable perturbations of the
cbs
weights. These checks do not prove that the equations perfectly reflect expert scientific judgment, but they support the claim that the metric suite behaves consistently with the intended constructs.
Several limitations remain. First,
ip
uses evidence strength as one subcomponent, but evidence strength is extracted from the source paper and may be noisy when a paper provides incomplete or ambiguous experimental support. Second, instance construction relies on automated extraction from papers, with expert checking of the schema and a subset of instances rather than full manual annotation of all examples. Third, retrieval and direct prompting are nearly tied in overall
cbs
, suggesting that generic retrieval does not automatically improve mechanistic grounding unless the retrieved context contains the right causal details. Fourth, the reference set has lower
hpa
than some generated systems because the literature-derived hypothesis can be narrower, more mechanism-focused, or less lexically aligned with the extracted problem statement than a model-generated answer that mirrors the problem text. We view these as important directions for future validation, especially through larger expert annotation studies and downstream checks against simulation or experimental outcomes.
Component granularity.
𝒢
\mathcal{G}
: 14 specific component terms (cathode, anode, sei, cei, interface, grain boundary, particle, electrode, binder, active material, current collector, separator, nlp, carbon black).
pdq
comp
=
min
(
1
,
0.4
⋅
𝟙
[
|
G
|
w
>
1
]
+
0.4
⋅
|
𝒢
∩
G
|
)
\textsc{pdq}_{\text{comp}}=\min(1,\,0.4\cdot\mathbb{1}[|G|_{w}>1]+0.4\cdot|\mathcal{G}\cap G|)
.
Appendix C
Pairwise LLM-Judge Prompt
LLM Judge Prompt
System:
You are an expert battery materials scientist evaluating two AI-generated research hypotheses.
Input:
PROBLEM
,
BATTERY_SYSTEM
,
FAILURE_MODE
,
HYPOTHESIS A
,
HYPOTHESIS B
Evaluate which hypothesis is better on three criteria:
1.
Problem_Addressed
— which better addresses the stated failure mode?
2.
Mechanistic_Depth
— which is more mechanistically grounded?
3.
Scientific_Utility
— which would be more useful to a researcher?
Respond only with JSON:
{"problem_addressed": "A|B", "mechanistic_depth": "A|B", "scientific_utility": "A|B", "overall": "A|B", "confidence": "high|medium|low"}
Applied twice per pair with swapped order (A
→
\to
B, then B
→
\to
A) to control for position bias.
Appendix D
Scoring Example
Scoring example: reference-free evaluation
Problem.
A disordered-rocksalt cathode has poor Li
+
transport, low electronic conductivity, and capacity fade at elevated C-rates.
Three hypotheses.
Reference:
Fluorination, particle-size reduction, and carbon coating improve Li
+
percolation, shorten diffusion paths, improve electronic transport, and suppress irreversible oxygen loss.
Fluent/vague:
Optimizing composition and microstructure can improve Li-ion transport and conductivity, leading to better rate capability and cycling stability.
Alternative:
Mo
6+
/Nb
5+
co-substitution stabilizes 0-TM Li diffusion channels, lowers Li migration barriers, improves high-rate capacity, and suppresses Mn-dissolution-driven fade.
Metric
Reference
Fluent/vague
Alternative
rcf
0.71
0.74
0.69
hpa
0.34
0.22
0.31
msi
0.42
0.03
0.51
sns
0.78
0.81
0.84
ip
0.82
0.51
0.79
pdq
0.61
0.52
0.61
cbs
0.608
0.403
0.612
Takeaway.
The fluent/vague hypothesis has the highest
rcf
but very low
msi
, showing that coherent reasoning is not the same as mechanistic specificity. The alternative hypothesis scores slightly above the reference even though it does not match the paper’s intervention, illustrating that
Matter to Mechanism
rewards scientific quality rather than overlap with a single reference answer.
Appendix E
Design Rationale: Programmatic vs. LLM-as-Judge
We deliberately avoid LLM-as-judge for the six core metrics. This choice is motivated by three considerations:
(1) Reproducibility.
Programmatic metrics produce identical scores given identical inputs, independent of model version, API availability, or sampling stochasticity. LLM judges are known to exhibit significant score variance across calls and model versions
[
Chehbouni et al. 2025
]
.
(2) Interpretability.
Because the benchmark is intended to diagnose failure modes, we prefer metrics whose inputs and behavior can be inspected directly. Programmatic dimensions make it easier to identify why a system scored poorly, for example due to weak mechanism, weak problem alignment, or poor decomposition, rather than only observing a single opaque judgment.
(3) Cost and accessibility.
Running
Matter to Mechanism
on 2,645 hypotheses with an LLM judge would cost approximately $150-$400 per evaluation run at current API prices, making re-evaluation on new systems prohibitively expensive. The programmatic pipeline runs in less than 90 seconds on a standard CPU node. An optional LLM-judge module (
cge
: Co-Scientist Generation Evaluator) is provided for supplementary deep evaluation of scientific soundness and falsifiability, and is excluded from the main
cbs
computation.