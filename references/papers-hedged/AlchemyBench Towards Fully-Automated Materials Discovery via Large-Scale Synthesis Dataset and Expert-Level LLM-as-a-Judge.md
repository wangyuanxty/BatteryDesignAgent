Towards Fully-Automated Materials Discovery via Large-Scale Synthesis Dataset and Expert-Level LLM-as-a-Judge
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY-SA 4.0
arXiv:2502.16457v4 [cs.CL] 19 Mar 2025
Towards Fully-Automated Materials Discovery via Large-Scale Synthesis Dataset and Expert-Level LLM-as-a-Judge
Heegyu Kim
Taeyang Jeon
Seungtaek Choi
Ji Hoon Hong
Affiliation:
Department of Energy Systems Research,
 Department of Materials Science and Engineering,Ajou University, Suwon 16499, Republic of Korea
Dong Won Jeon
Affiliation:
Department of Energy Systems Research,
 Department of Materials Science and Engineering,Ajou University, Suwon 16499, Republic of Korea
Ga-Yeon Baek
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Gyeong-Won Kwak
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Dong-Hee Lee
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Jisu Bae
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Chihoon Lee
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Yunseo Kim
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Seon-Jin Choi
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Jin-Seong Park
Affiliation:
Division of Materials Science and Engineering, Hanyang University, Seoul 04763, Republic of Korea
Correspondence:
hyunsouk@ajou.ac.kr
Sung Beom Cho
Affiliation:
Department of Energy Systems Research,
 Department of Materials Science and Engineering,Ajou University, Suwon 16499, Republic of Korea
Hyunsouk Cho
Affiliation:
Department of Artificial Intelligence,
Department of Software and Computer Engineering,
Abstract
Materials synthesis is vital for innovations such as energy storage, catalysis, electronics, and biomedical devices. Yet, the process relies heavily on empirical, trial-and-error methods guided by expert intuition. Our work aims to support the materials science community by providing a practical, data-driven resource. We have curated a comprehensive dataset of 17K expert-verified synthesis recipes from open-access literature, which forms the basis of our newly developed benchmark, AlchemyBench.
AlchemyBench offers an end-to-end framework that supports research in large language models applied to synthesis prediction. It encompasses key tasks, including raw materials and equipment prediction, synthesis procedure generation, and characterization outcome forecasting. We propose an LLM-as-a-Judge framework that leverages large language models for automated evaluation, demonstrating strong statistical agreement with expert assessments.
Overall, our contributions offer a supportive foundation for exploring the capabilities of LLMs in predicting and guiding materials synthesis, ultimately paving the way for more efficient experimental design and accelerated innovation in materials science.
*
*
footnotetext:
These authors contributed equally to this work
1
Introduction
Materials synthesis underpins advances in energy storage, catalysis, electronics, and biomedical devices
Olivetti et al. 2020
. Despite its importance, synthesis processes remain largely empirical, relying on trial-and-error approaches guided by expert intuition
Merchant et al. 2023
. This inefficiency highlights the need for systematic, data-driven approaches to predict synthesis workflows and optimize experimental design
Huang et al. 2023
.
Figure 1:
An overview of our contributions, featuring the Open Materials Guide Dataset for large-scale synthesis recipes and AlchemyBench for scalable, expert-level evaluation.
(a)
The periodic table of logarithmic frequency of elements.
(b)
The distribution of synthesis techniques.
Figure 2:
The periodic table (left) demonstrates that
OMG
covers diverse elements used in target materials, with darker colors indicating higher usage frequencies. A pie chart (right) illustrates the diversity of synthesis methods, highlighting the contributions of prior studies (white) and our dataset (white + green).
Recent progress in machine learning and large language models has opened new avenues for extracting and generating synthesis procedures from unstructured scientific literature
Song et al. 2023
;
Dunn et al. 2020
. However, practical adoption is hampered by several challenges. Existing datasets are often small, domain-specific, and noisy, limiting model generalizability. Moreover, the absence of comprehensive benchmarks makes it difficult to assess the performance of synthesis prediction methods, while expert evaluations remain too costly and time-consuming for large-scale use.
To address these challenges, we introduce
Open Materials Guide
(
OMG
), a dataset comprising 17K high-quality, expert-verified synthesis recipes curated from open-access literature. This dataset is the foundation for our benchmark,
AlchemyBench
, which evaluates synthesis prediction across multiple facets—from inferring raw materials and recommending appropriate synthesis equipment to generating detailed procedural steps and forecasting suitable characterization techniques.
Additionally, we investigate an LLM-as-a-Judge framework to automate the evaluation process. Our systematic comparisons reveal a strong statistical agreement between LLM-based assessments and expert judgments, underscoring the potential of LLMs to serve as scalable, automated evaluators.
Our work makes the following key contributions:
•
Open Materials Guide
(
OMG
), the most significant materials synthesis dataset, comprises 17K high-quality recipes from open-access literature. We demonstrated that various models can improve their performance with the proposed data-driven Retrieval-Augmented Generation (RAG)
Lewis et al. 2020
experiments. From the improvement, we validate the applicability of our data.
•
AlchemyBench
, the first end-to-end benchmark for ML-driven synthesis prediction utilizing LLM-as-a-Judge, a scalable framework for evaluating synthesis predictions, demonstrating strong alignment with expert assessments. This framework enables automated benchmarking of synthesis prediction models, significantly reducing the reliance on costly and time-intensive expert evaluations while maintaining high evaluation reliability.
•
Extensive experimental insights
into model performance, identifying key challenges, potential capabilities, and future directions to utilize LLM for fully-automated materials synthesis.
To enhance reproducibility and accessibility, we release the dataset and code as an open-source resource for the research community
1
1
1
https://github.com/HeegyuKim/AlchemyBench
.
2
Data Collection and Preparation
2.1
Motivation
Figure 3:
An example of extracted recipe from
Zhao et al. 2020
demonstrates structured annotation of materials, equipment, procedures, and characterization methods.
Previous large-scale datasets for extracting synthesis procedures from materials science literature have faced several critical challenges
Kononova et al. 2019
;
Wang et al. 2022
. The most significant limitation involves common extraction errors—such as missing reagent concentrations, incorrect reaction temperatures, and misordered procedural steps—which have rendered many outputs unreliable for downstream synthesis prediction
Sun and David 2025
. We analyzed existing datasets and revealed that over 92% of records in
Kononova et al. 2019
and 98% in
Wang et al. 2022
lacked essential synthesis parameters (e.g., heating temperature, duration, mixing media). Additionally, these datasets are narrowly focused on a few synthesis techniques (such as solid-state and solution-based). At the same time, real-world materials innovation employs a broader range of specialized techniques
Xu et al. 2023
. Finally, copyright restrictions from commercial journals have limited the legal redistribution of textual synthesis procedures
Authors Alliance 2024
.
To overcome these limitations, we propose
OMG
with three innovations: an LLM-driven parsing approach that improves extraction accuracy, a systematic collection covering more than ten distinct synthesis techniques (including vapor deposition, hydrothermal, and hybrid material systems), and the exclusive use of open-access publications to enable legal distribution of the dataset.
2.2
Dataset Construction
Our pipeline begins by retrieving 28,685 open-access articles from a pool of 400K search results using the Semantic Scholar API with 60 domain-specific search terms (e.g., “solid state sintering process”, “metal organic CVD”) recommended by domain experts. We convert PDFs to structured Markdown using
PyMuPDFLLM
Artifex Software 2024
and then employ GPT-4o in a multi-stage annotation process. First, articles are categorized based on whether they contain synthesis protocols, target materials, synthesis techniques, and applications. For articles confirmed to include synthesis procedures, the text is segmented into five key components, as illustrated in Figure
3
:
•
X
: A summary of the target material, synthesis method, and application.
•
𝐘
𝐌
\mathbf{Y_{M}}
: Raw materials, including quantitative details.
•
𝐘
𝐄
\mathbf{Y_{E}}
: Equipment specifications.
•
𝐘
𝐏
\mathbf{Y_{P}}
: Step-by-step procedural instructions.
•
𝐘
𝐂
\mathbf{Y_{C}}
: Characterization methods and results.
This systematic extraction yielded a dataset of 17,667 high-quality recipes (approximately a 62% yield) covering 10 diverse synthesis methods. Figure
2
demonstrates our dataset’s broad coverage of materials systems and synthesis techniques. Detailed LLM prompts and search keywords are provided in Appendix
A
.
2.3
Quality Verification
To ensure the accuracy of our automatically extracted recipes, we assembled a panel of eight domain experts from three institutions
2
2
2
Appendix
B
describes the details about domain experts
. The experts manually reviewed a representative sample of ten recipes, evaluating them based on the following criteria:
•
Completeness:
Capturing the full scope of the reported recipe (
X
,
𝐘
𝐌
\mathbf{Y_{M}}
,
𝐘
𝐄
\mathbf{Y_{E}}
,
𝐘
𝐏
\mathbf{Y_{P}}
, and
𝐘
𝐂
\mathbf{Y_{C}}
).
•
Correctness:
Extracting critical details such as temperature values and reagent amounts accurately.
•
Coherence:
Retaining a logical, consistent narrative without contradictions or abrupt transitions.
Table
1
presents our expert evaluation results using a five-point Likert scale (1 = poor, 5 = excellent). To measure expert agreement, we computed the
Intraclass Correlation Coefficient (ICC)
Shrout and Fleiss 1979
, utilizing a two-way mixed-effects model (ICC (3,k)) that quantifies agreement among evaluators, ensuring reliability in subjective scoring.
The extracted data exhibited high mean scores, but inter-rater reliability varied across criteria, particularly for articles with well-structured experimental sections.
Table 1:
Data verification by eight domain experts.
Criteria
Mean
σ
{}_{~\sigma}
ICC (3,k)
p
−
value
{}_{p-\text{value}}
Completeness
4.2
0.81
{}_{~0.81}
0.695
0.00
{}_{~0.00}
Correctness
4.7
0.58
{}_{~0.58}
0.258
0.23
{}_{~0.23}
Coherence
4.8
0.46
{}_{~0.46}
0.429
0.10
{}_{~0.10}
Completeness showed moderate agreement (ICC = 0.695), while correctness (ICC = 0.258) and coherence (ICC = 0.429) had lower agreement due to variations in naming conventions and missing characterization details.
Although the completeness score (4.2/5.0) was slightly lower than those for correctness (4.7/5.0) and coherence (4.8/5.0), correctness and coherence exhibited lower inter-rater reliability (ICC = 0.258 and 0.429, respectively), suggesting inconsistencies in how evaluators interpreted minor details.
Variability in scores for correctness and coherence arose from differences in how evaluators weighted minor inconsistencies, such as variations in equipment naming or missing characterization information. Some considered these negligible, while others applied stricter criteria, underscoring the need for refined annotation guidelines.
While manual verification confirms the effectiveness of our extraction process, it cannot fully ensure consistent performance across the diverse range of synthesis procedures. In the following section (Section
3
), we present a structured evaluation framework for tasks such as raw materials and equipment inference, procedure generation, and characterization outcome forecasting.
3
AlchemyBench
We present
AlchemyBench
, a comprehensive benchmark for evaluating materials synthesis prediction models. This framework addresses key challenges in synthesis recipe evaluation through structured tasks, expert-aligned metrics, and scalable assessment strategies.
3.1
Motivation
Evaluating synthesis predictions presents several fundamental challenges:
•
Lack of Benchmarks:
No standardized evaluation framework exists, making it challenging to compare synthesis models systematically. Prior datasets lack critical synthesis parameters and structured ground truth labels, making meaningful comparisons difficult.
•
Limitations of Traditional Metrics:
Traditional metrics, such as BLEU
Papineni et al. 2002
and ROUGE
Lin 2004
prioritize lexical overlap but fail to capture the procedural correctness of synthesis recipes.
Na 2023
et al. introduced the Jaccard score to measure set overlap in synthesis procedures, yet it lacks sensitivity to sequential dependencies critical in procedural texts. BERTScore
Zhang et al. 2019
improves contextual similarity measurement but struggles with domain-specific dependencies unique to materials synthesis. Moreover, these metrics do not account for experimental feasibility, limiting their applicability in real-world synthesis.
•
High Cost of Human Evaluation:
Expert-based assessments require significant time and resources, averaging 23 minutes per prediction (
σ
=
7.57
\sigma=7.57
) in our experiment. This cost makes large-scale benchmarking impractical, requiring an automated evaluation system.
•
Scalability Requirements:
Large-scale benchmarking necessitates an automated yet reliable evaluation system, which LLMs can provide
Gu et al. 2025
. However, prior attempts to use LLMs for evaluation lacked systematic validation against human expert assessments in materials science, raising concerns about reliability.
3.2
Task Definition
AlchemyBench
simulates real-world synthesis workflows, where models must predict the following components given input
𝐗
\mathbf{X}
(target material, synthesis method, application domain):
•
𝐏
𝐌
\mathbf{P_{M}}
: Raw materials (e.g., reagents, solvents) with quantities.
•
𝐏
𝐄
\mathbf{P_{E}}
: Required equipment (e.g., furnace, autoclave).
•
𝐏
𝐏
\mathbf{P_{P}}
: Synthesis procedures (e.g., reaction steps, temperatures).
•
𝐏
𝐂
\mathbf{P_{C}}
: Characterization methods and expected outcomes.
Table 2:
Seven evaluation criteria used to evaluate synthesis recipes, categorized into materials, equipment, procedure, characterization, and overall score. Each criterion is rated on a 1–5 scale to reflect the quality and practicality of the predicted recipes.
Category
Criteria
Description
Materials
Appropriateness
Are the selected materials suitable for the target synthesis?
Equipment
Appropriateness
Is the selected equipment suitable?
Procedure
Completeness
Is the procedure well-organized and logically structured?
Similarity
How closely does it match the ground truth procedure?
Feasibility
Can this procedure be realistically executed in a lab?
Characterization
Appropriateness
Are the methods and metrics suitable for validating the success of the synthesized material?
Similarity
How well do predicted properties match actual results?
Overall Score
-
Average score considering the recipe’s overall quality and practicality.
Predictions
𝐏
𝐗
=
{
𝐏
𝐌
,
𝐏
𝐄
,
𝐏
𝐏
,
𝐏
𝐂
}
\mathbf{P_{X}}=\{\mathbf{P_{M},P_{E},P_{P},P_{C}}\}
are evaluated against ground truth
𝐘
𝐗
=
{
𝐘
𝐌
,
𝐘
𝐄
,
𝐘
𝐏
,
𝐘
𝐂
}
\mathbf{Y_{X}}=\{\mathbf{Y_{M},Y_{E},Y_{P},Y_{C}}\}
using the LLM-as-a-Judge framework. Unlike prior benchmarks that rely on lexical similarity,
AlchemyBench
assesses procedural correctness and experimental feasibility. The evaluation criteria are described in Table
2
.
The scoring function is computed as:
Score
​
(
P
X
,
Y
X
)
=
∑
i
=
1
N
C
C
i
N
C
\text{Score}(P_{X},Y_{X})=\frac{\sum_{i=1}^{N_{C}}C_{i}}{N_{C}}
where
C
i
C_{i}
represents the score for criterion
i
i
, and
N
C
N_{C}
is the total number of evaluation criteria. These criteria were developed in collaboration with domain experts to ensure alignment with real-world synthesis evaluation.
3.3
Dataset Splits and Distribution
We divided
OMG
to three splits to ensure robust evaluation:
•
Training Set:
16,026 articles published before 2024.
•
Test - Standard Impact:
1,472 articles (2024 and beyond) from journals with Impact Factor (IF)
<
<
10.
•
Test - High Impact:
169 articles (2024 and beyond) from journals with IF
≥
\geq
10.
The
temporal split
ensures that models are evaluated on
unseen future research
, mitigating data contamination. Additionally, stratification by
journal impact
allows assessment of a model’s ability to process high-impact findings, often introducing novel and complex synthesis techniques. This split design evaluates both
generalizability
and the ability to meet the rigorous standards of top-tier journals
3
3
3
Table
6
describes the detailed list of high-impact journals utilized for our test-set split.
.
4
LLM as a Judge
A reliable evaluation framework is essential for benchmarking synthesis prediction models. This section examines the alignment between LLM-based and human expert judgments, evaluating inter-rater agreement and assessing the effectiveness of LLMs as automated evaluators.
4.1
Evaluation Metrics
We employ two metrics for evaluating the reliability of metrics: BLEU, ROUGE-L, BERTScore, and our LLM-as-a-Judge approach.
Pearson Correlation Coefficient
measures how closely LLM scores align with expert ratings on a continuous scale, capturing linear relationships. Finally, the
Spearman’s Rank Correlation
assesses rank-order consistency, beneficial when the relative ranking of recipes is more informative than absolute scores.
4.2
Human Expert Evaluation Setup
Before evaluating whether the reliability of
AlchemyBench
assessment aligns with expert evaluations, we enlisted eight materials science researchers from three institutions to establish reliable ground truth. Each evaluator had prior experience in experimental synthesis and was selected based on their publication record and domain expertise. Experts independently assessed model-generated recipes using seven criteria (Table
2
) on a 1–5 scale. To ensure high-quality assessments, we collected expert confidence scores and highlighted the agreement of one organization of three experts with the highest confidence levels on average (denoted as ‘High’). ICC(3,k) ensures the annotators’ consensus’s reliability.
The dataset for evaluation included ten representative synthesis workflows selected by a senior materials scientist to ensure diversity. Prediction recipes were generated using two models (GPT-4o-mini and o1-mini), resulting in 20 unique predictions evaluated by human experts and LLM judges. Appendix
B.2
and
C
describe the experts annotation details and hyperparameters.
4.3
Inter-Expert Agreement Analysis
Table 3:
ICC (3,k) for each criterion. High denotes the highest confidence organization on average, and subscripts denote the
p
p
-value.
Criteria
High (3)
All (8)
Material Appropriateness
0.61
0.01
{}_{~0.01}
0.80
0.00
{}_{~0.00}
Equipment Appropriateness
0.63
0.00
{}_{~0.00}
0.63
0.00
{}_{~0.00}
Procedure Completeness
0.46
0.05
{}_{~0.05}
0.23
0.19
{}_{~0.19}
Procedure Similarity
0.34
0.14
{}_{~0.14}
0.13
0.31
{}_{~0.31}
Procedure Feasibility
0.70
0.00
{}_{~0.00}
−
0.58
0.88
-0.58_{~0.88}
Characterization Appropriateness
0.45
0.06
{}_{~0.06}
0.78
0.00
{}_{~0.00}
Characterization Similarity
0.37
0.11
{}_{~0.11}
0.45
0.03
{}_{~0.03}
Overall Score (Average)
0.75
0.00
{}_{~0.00}
0.68
0.00
{}_{~0.00}
The comparison between the High Confidence group and the All group in Table
3
highlights key differences in inter-rater reliability. The All group achieves higher ICC values for “Material Appropriateness” (0.80) and “Characterization Appropriateness” (0.78) compared to the High group (0.61 and 0.45, respectively), indicating better consensus among the broader panel for these criteria. However, the High group shows significantly stronger agreement on “Procedure Feasibility” (ICC = 0.70) than the All group, which exhibits a negative ICC value (-0.58), suggesting inconsistencies in feasibility evaluations within the larger group. Both groups display similar reliability for “Equipment Appropriateness” (ICC = 0.63). Overall, while larger panels may enhance agreement on straightforward criteria, smaller high-confidence subgroups provide more consistent evaluations for complex aspects like procedural feasibility.
4.4
LLM-Expert Agreement Analysis
Table 4:
Pearson correlation coefficients between evaluation metrics and domain expert consensus for overall score. Subscripts denote the
p
p
-values. We set reasoning_effort to high for o3-mini.
Model
High (3)
All (8)
BLEU
−
0.16
0.50
-0.16_{~0.50}
−
0.23
0.34
-0.23_{~0.34}
ROUGE-L
0.06
0.80
~0.06_{~0.80}
−
0.12
0.60
-0.12_{~0.60}
BERTScore
−
0.30
0.19
-0.30_{~0.19}
−
0.24
0.31
-0.24_{~0.31}
GPT-4o-mini
0.61
0.00
~0.61_{~0.00}
0.45
0.05
~0.45_{~0.05}
GPT-4o-Aug
0.80
0.00
{}_{~0.00}
0.61
0.01
~0.61_{~0.01}
GPT-4o-Nov
0.63
0.00
~0.63_{~0.00}
0.75
0.00
{}_{~0.00}
o3-mini (high)
0.62
0.02
{}_{~0.02}
0.47
0.03
~0.47_{~0.03}
In Table
4
, the traditional metrics (BLEU, ROUGE-L, and BERTScore) exhibit low or even negative correlations with the domain expert consensus regardless of the evaluator group, whereas the LLM-based scores consistently yield higher and statistically significant correlations. The values obtained for GPT-4o-mini, GPT-4o-Aug, and o3-mini (high) are notably higher in the high confidence subgroup—0.61, 0.80, and 0.62 respectively—compared to 0.45, 0.61, and 0.47 for the full panel, suggesting that evaluations from the more confident experts are more tightly aligned with these models. In contrast, GPT-4o-Nov shows a higher correlation with all eight experts (0.75) than with the high confidence subset (0.63), indicating that its performance remains robust even when considering a broader range of expert opinions. Overall, the comparison underscores the influence of expert group composition on evaluation outcomes and highlights the superior alignment of advanced LLM evaluators with expert assessments over traditional similarity metrics
4
4
4
Spearman correlation scores are described in Appendix
B.3
.
.
Our experiment confirms that LLM-generated scores correlate significantly better with expert assessments, supporting their use as scalable synthesis evaluators.
4.5
Summary and Implications
Our findings demonstrate that LLM-based evaluation provides a scalable and effective alternative to traditional synthesis assessment methods. GPT-4o-Aug exhibits strong agreement with expert ratings, outperforming traditional NLP metrics.
However, challenges remain, as LLMs can be sensitive to ambiguous phrasing and domain-specific biases, affecting evaluation consistency. Future work should explore hybrid approaches integrating expert feedback with LLM scoring. Reinforcement learning from human feedback
Ouyang et al. 2022
(RLHF) and domain-specific fine-tuning
Anisuzzaman et al. 2025
may improve alignment with expert reasoning.
Future work should investigate methods for mitigating biases and inconsistencies to enhance reliability, such as integrating expert validation into LLM-based evaluation pipelines. This study highlights the potential of LLMs as automated evaluators, paving the way for AI-driven, context-aware benchmarking frameworks in materials science.
5
Experiments
This section evaluates five LLMs on our benchmark using the LLM-as-a-Judge framework based on GPT-4o-Aug, analyzing performance across multiple metrics and the impact of retrieval-augmented generation (RAG).
5.1
Experiment Setup
To comprehensively evaluate the models, we conducted experiments with the following setup:
Base LLMs
We evaluated four LLMs, including reasoning-based models (o3-mini) and general-purpose models (GPT-4o variants). The knowledge cutoff of these models is October 2023, minimizing potential data contamination in our test sets, which contain 2024 and beyond
5
5
5
The knowledge cutoff of OpenAI’s models is described in
this documentation
.
. We prompt the LLM with a fixed one-shot example from our train set to predict all components (
𝐏
𝐗
\mathbf{P_{X}}
) well
6
6
6
Details about LLM prompt and hyperparameters are described in Appendix
C
.
. Moreover, we varied the reasoning_effort of o3-mini to ensure the effectiveness of reasoning effort in materials synthesis.
Evaluation Framework
Each model generated synthesis recipes for both the
High Impact set
and
Standard Impact set
. Recipes were evaluated using our LLM-as-a-Judge method based on GPT-4o-Aug. The evaluation criteria focused on material appropriateness, procedural feasibility, and overall recipe quality.
Retrieval-Augmented Generation (RAG)
To evaluate the impact of retrieval on recipe generation, we implemented a RAG pipeline using OpenAI’s text-embedding-3-large model
OpenAI 2022
. For each input
X
X
, we retrieved the top-
K
K
most similar recipes from the train set based on cosine similarity and included them as references in LLM prompts. We evaluated
K
=
{
0
,
1
,
5
,
10
,
25
}
K=\{0,1,5,10,25\}
to assess the effect of contextual information.
This experimental setup ensures a thorough evaluation of both baseline performance and improvements achieved through retrieval augmentation. Due to computational constraints, RAG experiments were conducted on three representative models (GPT-4o-Nov, GPT-4o-mini, and o3-mini) using only the
High Impact set
.
5.2
Insights from Experimental Results
Table 5:
Base LLMs’ overall score evaluated by LLM-as-a-judge. Subscripts denote the standard deviation.
High Impact
Standard Impact
Model
Mean
σ
{}_{~\sigma}
Max
Mean
σ
{}_{~\sigma}
Max
GPT-4o-mini
3.238
0.432
{}_{~0.432}
4.50
3.412
0.412
{}_{~0.412}
4.71
GPT-4o-Aug
3.362
0.405
{}_{~0.405}
4.50
3.508
0.397
{}_{~0.397}
4.71
GPT-4o-Nov
3.709
0.410
{}_{~0.410}
4.71
3.398
0.397
{}_{~0.397}
4.71
o3-mini (medium)
3.714
0.411
{}_{~0.411}
4.64
3.822
0.387
{}_{~0.387}
4.80
o3-mini (high)
3.759
0.407
{}_{~0.407}
4.71
3.885
0.377
{}_{~0.377}
4.80
The experimental results provide valuable insights into the challenges and opportunities in materials synthesis prediction, structured around the following research questions:
RQ1: Is High-Impact Set More Challenging than Standard-Impact Set?
The results confirm that
High Impact set
is indeed more challenging than
Standard Impact set
. Across models without GPT-4o-Nov, average scores on the
High Impact set
were generally lower than those on the
Standard Impact set
. For example, o3-mini (high) achieved an average score of
3.759
±
0.407
3.759\pm 0.407
on
High Impact set
compared to
3.885
±
0.377
3.885\pm 0.377
on
Standard Impact set
(Table 5). This discrepancy highlights the increased complexity of High-Impact synthesis workflows, which often involve novel materials or cutting-edge techniques requiring greater reasoning and contextual understanding.
RQ2: Does Increasing Reasoning Effort Improve Recipe Quality in Materials Science?
Materials science relies heavily on trial-and-error experimentation, making reasoning-based approaches particularly relevant for complex synthesis tasks. To explore this, we evaluated the o3-mini model using low, medium, and high reasoning efforts. As shown in Table
5
, o3-mini (high) achieved the highest mean scores across both
High-Impact
(
3.759
3.759
) and
Standard-Impact
(
3.885
3.885
) sets, outperforming both its low and medium reasoning efforts and general-purpose models like GPT-4o-Nov. o3-mini (high) exhibited superior performane in step-by-step instructions compared to GPT-4o-Nov, which achieved a lower mean score (
3.709
3.709
) on the
High Impact set
despite matching o3-mini (high)’s maximum score (
4.71
4.71
). These findings demonstrate the importance of structured problem-solving capabilities in materials synthesis tasks.
Figure 4:
Impact of the Retrieval Augmented Generation (RAG) in
High Impact set
.
RQ3: Does Recipes of Similar Contributions Improve Prediction Performance?
RAG with similar recipes significantly enhances model performance through domain-relevant examples. As shown in Figure
4
, increasing
K
K
improves scores across all models, with different patterns between reasoning-based and general-purpose models.
For o3-mini (high), performance diminish after
K
=
5
K=5
, reaching a maximum score of
4.0
4.0
. In contrast, GPT-4o-Nov shows continuous improvement up to
K
=
25
K=25
, achieving
3.98
3.98
. The close performance between GPT-4o-Nov and o3-mini (high) suggests RAG can effectively bridge the gap between general-purpose and reasoning-based models.
These results highlight two key points: (1) RAG benefits general-purpose models that rely on external context, and (2) retrieval effectiveness depends on model architecture and training data quality. Our findings suggest that
K
=
5
K=5
provides the best trade-off between context enrichment and cognitive load, as additional references beyond this point yield minimal improvements.
6
Related Work
Materials Synthesis Datasets
Existing materials synthesis datasets, such as those focusing on solid-state
Kononova et al. 2019
and solution-based
Wang et al. 2022
methods, have provided valuable resources for machine learning applications. However, these datasets often suffer from issues of incompleteness and low quality, with many synthesis procedures lacking critical parameters necessary for reproducibility or predictive modeling. For instance, only 28% of solid-state synthesis paragraphs yield complete reactions, and over 90% of recipes are missing key parameters. These limitations hinder their utility in guiding novel synthesis workflows.
LLM-based Generation for Materials Science
Large language models (LLMs) have shown promise in accelerating materials discovery by automating hypothesis generation
Kumbhar et al. 2025
, property prediction
Chiang et al. 2024
, and evaluation
Mishra et al.
. However, their effectiveness is constrained by the lack of high-quality domain-specific datasets and the need for retrieving or fine-tuning to handle complex synthesis workflows. Our work addresses these gaps and introduces a large-scale dataset and benchmark tailored to the real-world synthesis workflow, enabling rigorous evaluation of LLM capabilities in materials science.
7
Conclusion
This study presents a comprehensive benchmark for evaluating LLMs in materials synthesis prediction, addressing key challenges in data-driven materials science. By curating a large-scale dataset and designing tasks that mirror real-world synthesis workflows, we provide a robust framework to assess model capabilities in raw materials selection, equipment inference, procedure generation, and characterization prediction. Our experiments reveal the potential of reasoning-based models, such as o3-mini, outperforming general-purpose models like GPT-4o variants in generating coherent and feasible synthesis recipes. Furthermore, integrating retrieval-augmented generation (RAG) enhances recipe quality by grounding predictions in domain-relevant examples, with optimal performance gains observed at
K
=
5
K=5
. These findings underscore the importance of combining advanced reasoning architectures with adaptive retrieval strategies for materials science tasks, laying the foundation for interdisciplinary innovation and accelerating progress in data-driven and fully-automated materials discovery.
8
Limitations
While our benchmark represents a significant step toward integrating LLMs into materials synthesis, several limitations remain. First, the dataset, derived from open-access articles, may exhibit biases in domain coverage, overrepresenting fields like battery materials while underrepresenting others like biomaterials. Second, GPT-4o for recipe extraction and evaluation introduces potential inaccuracies and biases, particularly in complex or ambiguous texts. Third, while practical, reliance on LLM-based scoring may oversimplify the nuanced requirements of tasks like procedure generation and characterization prediction. Additionally, the sequential dependencies between tasks (e.g., precursor prediction influencing procedure generation) pose challenges for current models, which may overfit dataset-specific patterns rather than learning generalizable principles. Finally, the lack of interpretability in model outputs limits their applicability in critical experimental workflows. Addressing these issues through improved data curation, expanded evaluation frameworks, and developing more interpretable models will be vital for future progress in this domain.
References
Anisuzzaman et al. (2025)
DM Anisuzzaman, Jeffrey G Malins, Paul A Friedman, and Zachi I Attia. 2025.
Fine-tuning large language models for specialized use cases.
Mayo Clinic Proceedings: Digital Health
, 3(1).
Artifex Software (2024)
Artifex Software. 2024.
Pymupdf4llm: Pdf text extraction library for llm applications.
https://github.com/artifex-com/pymupdf4llm
.
Accessed: January 2024.
Authors Alliance (2024)
Authors Alliance. 2024.
Text and data mining under u.s. copyright law: Landscape, flaws & recommendations
.
Technical report.
(4)
BerriAI.
Litellm.
https://github.com/BerriAI/litellm
.
Chiang et al. (2024)
Yuan Chiang, Elvis Hsieh, Chia-Hong Chou, and Janosh Riebesell. 2024.
Llamp: Large language model made powerful for high-fidelity materials knowledge retrieval and distillation
.
Preprint
, arXiv:2401.17244.
Douze et al. (2024)
Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, Pierre-Emmanuel Mazaré, Maria Lomeli, Lucas Hosseini, and Hervé Jégou. 2024.
The faiss library
.
Dunn et al. (2020)
Alexander Dunn, Qi Wang, Alex Ganose, Daniel Dopp, and Anubhav Jain. 2020.
Benchmarking materials property prediction methods: the matbench test set and automatminer reference algorithm.
npj Computational Materials
, 6(1):138.
Gu et al. (2025)
Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni, and Jian Guo. 2025.
A survey on llm-as-a-judge
.
Preprint
, arXiv:2411.15594.
Huang et al. (2023)
Guannan Huang, Yani Guo, Ye Chen, and Zhengwei Nie. 2023.
Application of machine learning in material synthesis and property prediction.
Materials
, 16(17):5977.
Kononova et al. (2019)
Olga Kononova, Haoyan Huo, Tanjin He, Ziqin Rong, Tiago Botari, Wenhao Sun, Vahe Tshitoyan, and Gerbrand Ceder. 2019.
Text-mined dataset of inorganic materials synthesis recipes.
Scientific data
, 6(1):203.
Kumbhar et al. (2025)
Shrinidhi Kumbhar, Venkatesh Mishra, Kevin Coutinho, Divij Handa, Ashif Iquebal, and Chitta Baral. 2025.
Hypothesis generation for materials discovery and design using goal-driven and constraint-guided llm agents
.
Preprint
, arXiv:2501.13299.
Lewis et al. (2020)
Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020.
Retrieval-augmented generation for knowledge-intensive nlp tasks.
Advances in Neural Information Processing Systems
, 33:9459–9474.
Lhoest et al. (2021)
Quentin Lhoest, Albert Villanova del Moral, Yacine Jernite, Abhishek Thakur, Patrick von Platen, Suraj Patil, Julien Chaumond, Mariama Drame, Julien Plu, Lewis Tunstall, Joe Davison, Mario Šaško, Gunjan Chhablani, Bhavitvya Malik, Simon Brandeis, Teven Le Scao, Victor Sanh, Canwen Xu, Nicolas Patry, Angelina McMillan-Major, Philipp Schmid, Sylvain Gugger, Clément Delangue, Théo Matussière, Lysandre Debut, Stas Bekman, Pierric Cistac, Thibault Goehringer, Victor Mustar, François Lagunas, Alexander Rush, and Thomas Wolf. 2021.
Datasets: A community library for natural language processing
.
In
Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: System Demonstrations
, pages 175–184, Online and Punta Cana, Dominican Republic. Association for Computational Linguistics.
Lin (2004)
Chin-Yew Lin. 2004.
Rouge: A package for automatic evaluation of summaries.
In
Text summarization branches out
, pages 74–81.
Merchant et al. (2023)
Amil Merchant, Simon Batzner, Samuel S Schoenholz, Muratahan Aykol, Gowoon Cheon, and Ekin Dogus Cubuk. 2023.
Scaling deep learning for materials discovery.
Nature
, 624(7990):80–85.
(16)
Vaibhav Mishra, Somaditya Singh, Mohd Zaki, Hargun Singh Grover, Santiago Miret, NM Anoop Krishnan, et al.
Llamat: Large language models for materials science.
In
AI for Accelerated Materials Design-Vienna 2024
.
Na (2023)
Gyoung S Na. 2023.
Artificial intelligence for learning material synthesis processes of thermoelectric materials.
Chemistry of Materials
, 35(19):8272–8280.
Olivetti et al. (2020)
Elsa A Olivetti, Jacqueline M Cole, Edward Kim, Olga Kononova, Gerbrand Ceder, Thomas Yong-Jin Han, and Anna M Hiszpanski. 2020.
Data-driven materials research enabled by natural language processing and information extraction.
Applied Physics Reviews
, 7(4).
OpenAI (2022)
OpenAI. 2022.
Introducing text and code embeddings.
https://openai.com/index/introducing-text-and-code-embeddings/
.
[Accessed 11-02-2025].
Ouyang et al. (2022)
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022.
Training language models to follow instructions with human feedback.
Advances in neural information processing systems
, 35:27730–27744.
Papineni et al. (2002)
Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002.
Bleu: a method for automatic evaluation of machine translation.
In
Proceedings of the 40th annual meeting of the Association for Computational Linguistics
, pages 311–318.
Semantic Scholar (2023)
Semantic Scholar. 2023.
Semantic scholar academic graph api.
https://www.semanticscholar.org/product/api
.
Accessed: January 2025.
Shrout and Fleiss (1979)
Patrick E Shrout and Joseph L Fleiss. 1979.
Intraclass correlations: uses in assessing rater reliability.
Psychological bulletin
, 86(2):420.
Song et al. (2023)
Yu Song, Santiago Miret, and Bang Liu. 2023.
Matsci-nlp: Evaluating scientific language models on materials science language tasks using text-to-schema modeling.
arXiv preprint arXiv:2305.08264
.
Sun and David (2025)
Wenhao Sun and Nicholas David. 2025.
A critical reflection on attempts to machine-learn materials synthesis insights from text-mined literature recipes.
Faraday Discussions
.
Wang et al. (2022)
Zheren Wang, Olga Kononova, Kevin Cruse, Tanjin He, Haoyan Huo, Yuxing Fei, Yan Zeng, Yingzhi Sun, Zijian Cai, Wenhao Sun, et al. 2022.
Dataset of solution-based inorganic materials synthesis procedures extracted from the scientific literature.
Scientific data
, 9(1):231.
Xu et al. (2023)
Pengcheng Xu, Xiaobo Ji, Minjie Li, and Wencong Lu. 2023.
Small data machine learning in materials science.
npj Computational Materials
, 9(1):42.
Zhang et al. (2019)
Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q Weinberger, and Yoav Artzi. 2019.
Bertscore: Evaluating text generation with bert.
arXiv preprint arXiv:1904.09675
.
Zhao et al. (2020)
Yu Zhao, Dongru Gao, Ruxin Guan, Hongwei Li, Ning Li, Guixian Li, and Shiyou Li. 2020.
Synthesis of a three-dimensional cross-linked ni–v 2 o 5 nanomaterial in an ionic liquid for lithium-ion batteries.
RSC advances
, 10(64):39137–39145.
Table 6:
A list of high-impact journals (IF
≥
10
\geq 10
) that at least ten papers are included in
OMG
.
Publisher
Journals
ACS
ACS Applied Materials and Interfaces, ACS Nano, ACS Energy Letters, Journal of the American Chemical Society, ACS Catalysis
RSC
Journal of Materials Chemistry A, Chemical Society Reviews, Energy Environmental Science
Nature
Nature Communications, Nature Materials, Nature Nanotechnology, Nature Energy, Nature Reviews Materials, Nature Catalysis,
Nature, Nature Electronics, Nature Methods, Nature Chemistry, Nature Physics, Light: Science Applications
Wiley
Advanced Materials, Advanced Energy Materials, Small, Angewandte Chemie, Advanced Science, ChemSusChem,
Advanced Functional Materials
Springer
Nano-Micro Letters, Journal of Advanced Ceramics, Advanced Composites and Hybrid Materials
Figure 5:
Yearly distribution of collected material synthesis papers
Appendix A
Additional Dataset Information
This section provides extended details on dataset statistics and collection methodology that were not included in the main text for brevity.
A.1
Keyword Selection Rationale
Figure
9
describes the search keywords to retrieve 400K articles using Semantic Scholar API
Semantic Scholar 2023
. We collect these keywords guided by our eight domain experts.
A.2
Downloading PDFs
We downloaded open-access papers exclusively from the following six publishers, most frequent in our retrieval result:
pubs.rsc.org
,
mdpi.com
,
nature.com
,
link.springer.com
,
pubs.acs.org
,
onlinelibrary.wiley.com
.
A.3
Dataset Details
Figure
6(a)
,
6(c)
, and
6(b)
demonstrate the distributions of venue for train, test-standard-impact, and test-high-impact respectively. Table
6
describes the high-impact venues (IF
≥
10
\geq 10
) that at least ten papers are included in
OMG
. Figure
5
demonstrates the dataset distribution of the published year, indicating the latest data, 2020 and beyond, accounts for a large percentage.
(a)
A venue distribution of the train set
(b)
A venue distribution of the test high-impact set
(c)
A venue distribution of the test standard impact set
Figure 6:
Venue distributions across datasets: (a) training set, (b) test high-impact set, and (c) test standard impact set. The distributions illustrate the diversity and focus of venues in each subset.
Appendix B
Annotation Pipeline and Quality Checks
Here, we elaborate on the annotation workflow and the validation methods used to ensure the reliability of extracted recipes.
B.1
GPT-4 Prompts for Classification and Extraction
Figure
10
demonstrates the prompt to categorize the literature and Figure
11
demonstrates the prompt to extract the synthesis recipe from the literature.
B.2
Expert Review Protocol
Table
7
describes the anonymized details about the eight domain experts in materials science. They participated as volunteers and received no evaluation fees.
Figure
7
and
8
demonstrate the web UI screenshots for evaluating LLM predictions by domain experts. Domain experts evaluated 20 LLM predictions with seven criteria in Table
2
and recorded the results in a spreadsheet. We aggregated those eight spreadsheets and calculated the agreement.
Table 7:
Anonymized details for the domain experts in our study. Conf. denotes the average confidence for evaluating LLM predictions in Section
4
. Group C is the highest confidence group.
Group
Expertise
Conf.
A
One master and two PhD candidates
specialized in:
- Thin film transistors
- 3D nano-semiconductor thin films
- atomic layer deposition
1.90
B
Two master’s student
specialized in:
- Materials modeling
- DFT & MD simulations
- NLP for materials science
3.15
C
Three master’s student
specialized in:
- Transparent electrodes
- electrospinning
- 2D materials
4.47
B.3
LLM-Expert Agreement Details
The agreement analysis between expert groups (entire 8-member panel vs. 3-member high-confidence group) and GPT-4o-Nov reveals distinct patterns across evaluation criteria, as shown in Tables
8
and
9
.
These results highlight the critical influence of expert group composition on LLM alignment assessment. Compared to the entire panel, the high-impact subgroup demonstrates enhanced agreement on procedural elements but reduced consensus on characterization tasks, suggesting domain-specific expertise differentially weights evaluation criteria. The stability of non-significant results across both groups for equipment and feasibility judgments implies fundamental challenges in consistently operationalizing these metrics.
Table 8:
A agreement between entire expert consensus and GPT-4o-Nov for each criterion. Subscripts denote the
p
−
p-
value.
Category
Pearson
Spearman
Material Appropriateness
0.59
0.01
{}_{~0.01}
0.59
0.01
{}_{~0.01}
Equipment Appropriateness
-0.25
0.29
{}_{~0.29}
-0.25
0.28
{}_{~0.28}
Procedure Completeness
0.05
0.83
{}_{~0.83}
0.09
0.71
{}_{~0.71}
Procedure Similarity
0.41
0.07
{}_{~0.07}
0.40
0.08
{}_{~0.08}
Procedure Feasibility
-0.04
0.86
{}_{~0.86}
-0.04
0.86
{}_{~0.86}
Characterization Appropriateness
0.43
0.06
{}_{~0.06}
0.42
0.07
{}_{~0.07}
Characterization Similarity
0.45
0.05
{}_{~0.05}
0.47
0.04
{}_{~0.04}
Table 9:
A agreement between the expert consensus of the high-confidence group and GPT-4o-Nov for each criterion. Subscripts denote the
p
−
p-
value.
Category
Pearson
Spearman
Material Appropriateness
0.44
0.05
{}_{~0.05}
0.41
0.07
{}_{~0.07}
Equipment Appropriateness
0.10
0.68
{}_{~0.68}
0.13
0.58
{}_{~0.58}
Procedure Completeness
0.23
0.33
{}_{~0.33}
0.20
0.39
{}_{~0.39}
Procedure Similarity
0.56
0.01
{}_{~0.01}
0.50
0.02
{}_{~0.02}
Procedure Feasibility
-0.04
0.86
{}_{~0.86}
-0.04
0.86
{}_{~0.86}
Characterization Appropriateness
0.43
0.06
{}_{~0.06}
0.42
0.07
{}_{~0.07}
Characterization Similarity
0.09
0.72
{}_{~0.72}
0.16
0.50
{}_{~0.50}
Appendix C
Experimental and Implementation Details
This section thoroughly describes the LLM prompts and hyperparameter settings to facilitate reproducibility.
C.1
Hyperparameters
We use a temperature of zero, top-p of 1.0, and max_tokens of 4096 for GPT-4o-mini and GPT-4o variants. o3-mini variants use max_completion_tokens of 16384, and OpenAI does not allow to set temperature and top-p hyperparameters for o3-mini models.
C.2
LLM Prompt
Figure
14
describes the LLM-as-a-Judge prompt. The LLM outputs the JSON-formatted judgment of seven criteria and an overall score for extraction.
C.3
Other Artifacts
We utilized LiteLLM
BerriAI
and FAISS
Douze et al. 2024
, Huggingface Datasets
Lhoest et al. 2021
.
We confirmed that all models, datasets, and frameworks are allowed for research use.
Appendix D
Additional Results and Analysis
Table
10
describes the detailed result of RAG experiments in Figure
4
for four base LLMs.
Appendix E
Ethical Considerations and Potential Risks
Our data collection approach exclusively utilized open-access publications from six major publishers to ensure copyright compliance.
Additionally, we verified the 12958 articles through keyword-based content filtering and selenium-confirmed articles of CC-BY licensing status, supplemented by a manual sampling of 100 randomly selected articles to validate redistribution rights.
While this strategy mitigates legal risks, two potential limitations warrant consideration: First, the open-access corpus may exhibit selection bias toward well-funded research domains (e.g., energy materials) versus proprietary industrial methods. Second, automated extraction via GPT-4o risks propagating subtle errors from source documents, particularly in stoichiometric ratios and procedural sequencing, despite our expert validation protocol. All dataset derivatives will be distributed under original CC-BY licenses.
Appendix F
AI Assitant
We use
Microsoft Copilot
as a coding assistant and
Grammarly
and
Writefull
as a writing assistant.
Table 10:
A full experiment result of RAG prediction in Section
5
Model
K
Mean
σ
\sigma
Min
Max
o3-mini-high
0
3.759
0.407
2.86
4.71
1
3.937
0.401
2.80
4.86
5
4.001
0.384
3.00
4.80
10
3.939
0.359
3.00
4.80
25
3.986
0.383
3.00
4.71
o3-mini-medium
0
3.714
0.411
2.86
4.64
1
3.867
0.381
3.00
4.80
5
3.934
0.349
2.86
4.80
10
3.937
0.390
2.57
4.80
25
3.975
0.413
2.50
4.80
o3-mini-low
0
3.676
0.407
2.50
4.57
1
3.848
0.411
2.90
4.80
5
3.904
0.393
2.93
4.86
10
3.917
0.397
2.86
4.86
25
3.961
0.388
3.00
4.80
GPT-4o Nov
0
3.709
0.410
2.75
4.71
1
3.824
0.417
2.57
4.80
5
3.949
0.391
2.93
4.80
10
3.954
0.366
3.00
4.80
25
3.976
0.375
2.93
4.86
Figure 7:
A web UI screenshot for domain experts annotation (1/2).
Figure 8:
A web UI screenshot for domain experts annotation (2/2).
Figure 9:
60 search keywords to retrieve the literature, including materials synthesis recipes using Semantic Scholar API.
⬇
1
#
Solid
-
State
Processing
2
solid
state
sintering
process
,
reactive
sintering
synthesis
,
3
pressure
-
assisted
sintering
,
spark
plasma
sintering
,
4
hot
pressing
synthesis
,
hot
isostatic
pressing
,
5
cold
isostatic
pressing
,
flash
sintering
technique
,
6
field
-
assisted
sintering
,
microwave
sintering
process
,
7
8
#
Mechanochemical
Methods
9
high
energy
ball
milling
,
mechanical
alloying
synthesis
,
10
mechanochemical
activation
,
planetary
ball
milling
,
11
cryogenic
milling
process
,
attrition
milling
synthesis
,
12
mechanical
grinding
method
,
mechanofusion
process
,
13
mechano
-
chemical
reaction
,
solid
-
state
mechanical
synthesis
,
14
15
#
Vapor
Deposition
Techniques
16
atomic
layer
deposition
,
plasma
enhanced
CVD
,
17
metal
organic
CVD
,
low
pressure
CVD
,
18
atmospheric
pressure
CVD
,
electron
beam
PVD
,
19
magnetron
sputtering
deposition
,
pulsed
laser
deposition
,
20
thermal
evaporation
method
,
molecular
beam
epitaxy
,
21
22
#
Advanced
Thermal
Methods
23
combustion
synthesis
process
,
self
-
propagating
synthesis
,
24
plasma
spray
synthesis
,
flame
spray
pyrolysis
,
25
laser
ablation
synthesis
,
thermal
plasma
synthesis
,
26
microwave
-
assisted
synthesis
,
ultrasonic
spray
pyrolysis
,
27
radio
frequency
thermal
plasma
,
arc
discharge
synthesis
,
28
29
#
Electrochemical
Approaches
30
electrochemical
co
-
deposition
,
pulse
electrodeposition
,
31
electroless
deposition
method
,
anodic
oxidation
synthesis
,
32
cathodic
reduction
process
,
electrochemical
etching
,
33
electrochemical
polymerization
,
electrophoretic
deposition
,
34
galvanic
replacement
reaction
,
electrochemical
exfoliation
,
35
36
#
Novel
Processing
Methods
37
freeze
drying
synthesis
,
spray
freeze
drying
,
38
supercritical
fluid
process
,
template
-
assisted
synthesis
,
39
biomimetic
processing
method
,
sol
-
gel
electrospinning
,
40
ionothermal
synthesis
route
,
microemulsion
technique
,
41
sonochemical
processing
,
continuous
flow
synthesis
Figure 10:
System prompt to categorize the literature converted to markdown format.
⬇
1
Analyze
the
given
scientific
text
and
provide
classifications
in
the
following
order
:
2
3
1.
Synthesis
Recipe
Classification
:
4
Determine
if
the
text
contains
detailed
synthesis
procedures
.
5
Return
only
"
YES
"
or
"
NO
".
6
If
"
NO
",
stop
here
.
If
"
YES
",
continue
with
the
following
classifications
.
7
8
2.
Target
Classification
:
9
Classify
the
synthesized
target
as
one
of
:
10
-
Material
(
e
.
g
.,
nanoparticles
,
compounds
,
composites
)
11
-
Device
(
e
.
g
.,
sensors
,
batteries
,
transistors
)
12
-
Molecule
(
e
.
g
.,
organic
compounds
,
polymers
)
13
14
3.
Material
Identification
:
15
Provide
:
16
-
Chemical
formula
(
if
applicable
)
17
-
Material
name
18
-
Material
class
(
e
.
g
.,
metal
oxide
,
polymer
,
semiconductor
)
19
20
4.
Application
Domain
:
21
List
the
primary
applications
mentioned
in
the
text
:
22
-
Energy
(
e
.
g
.,
batteries
,
solar
cells
)
23
-
Electronics
(
e
.
g
.,
transistors
,
sensors
)
24
-
Healthcare
(
e
.
g
.,
drug
delivery
,
imaging
)
25
-
Environmental
(
e
.
g
.,
catalysis
,
filtration
)
26
-
Others
(
specify
)
27
28
5.
Synthesis
Process
Classification
:
29
Classify
the
given
synthesis
method
into
one
of
these
categories
.
If
it
combines
multiple
methods
,
label
it
as
"
Hybrid
".
If
it
doesn
’
t
fit
any
category
,
label
it
as
"
Others
".
30
31
Categories
:
32
1.
Solid
-
State
:
solid
-
state
reaction
,
ceramic
method
,
sintering
33
2.
Vapor
Deposition
:
CVD
,
PVD
,
sputtering
,
evaporation
34
3.
Mechanochemical
:
ball
milling
,
mechanical
alloying
35
4.
Hydrothermal
:
solvothermal
,
pressurized
solution
36
5.
Pyrolysis
:
thermal
decomposition
,
spray
pyrolysis
37
6.
Melt
Quenching
:
rapid
solidification
,
glass
formation
38
7.
Electrochemical
:
electrodeposition
,
anodization
39
8.
Self
-
Assembly
:
molecular
assembly
,
biomineralization
40
9.
Solution
-
Based
:
precipitation
,
sol
-
gel
,
wet
chemical
synthesis
41
10.
Biological
:
biomimetic
,
enzyme
-
mediated
,
microbial
synthesis
42
11.
Hybrid
:
combination
of
multiple
methods
43
12.
Others
:
novel
or
unconventional
methods
44
45
46
Format
the
output
as
a
structured
list
only
if
Step
1
is
"
YES
".
47
For
not
available
,
use
"
N
/
A
".
48
Do
not
provide
explanations
or
additional
commentary
.
49
50
Example
Output
:
51
For
a
paper
titled
"
Hydrothermal
Synthesis
of
LiFePO4
/
C
Composites
for
High
-
Performance
Lithium
-
Ion
Batteries
":
52
53
1.
Synthesis
Recipe
:
YES
54
2.
Target
:
Material
55
3.
Material
Identification
:
56
-
Chemical
Formula
:
LiFePO4
/
C
57
-
Material
Name
:
Carbon
-
coated
lithium
iron
phosphate
58
-
Material
Class
:
Phosphate
composite
59
4.
Application
Domain
:
Energy
(
lithium
-
ion
batteries
)
60
5.
Synthesis
Process
:
Hydrothermal
(
solvothermal
)
61
62
63
Scientific
Paper
:
64
{
text
}
Figure 11:
System prompt to extract the recipe from literature converted to markdown format.
⬇
1
You
are
a
materials
science
expert
.
Your
task
is
to
extract
ONLY
the
explicitly
stated
synthesis
information
from
the
provided
research
paper
.
Do
not
generate
,
assume
,
or
infer
any
information
not
directly
presented
in
the
paper
.
2
If
the
provided
paper
does
not
contain
any
synthesis
information
,
please
indicate
"
NOT
A
MATERIAL
SYNTHESIS
PAPER
"
and
do
not
provide
any
further
details
.
3
4
##
Key
Contributions
5
Summarize
the
key
contributions
of
the
paper
:
6
-
Novel
materials
or
compounds
:
<
summary
>
7
-
Unique
synthesis
methods
:
<
summary
>
8
-
Specific
applications
or
domains
:
<
summary
>
9
10
##
Materials
11
Extract
and
list
:
12
-
All
precursor
materials
with
:
13
*
Exact
quantities
and
concentrations
14
*
Molar
ratios
or
stoichiometric
proportions
15
*
Purity
grades
and
specifications
16
*
Supplier
information
if
provided
17
-
Solvents
,
reagents
,
catalysts
,
and
any
other
materials
such
as
carrier
gases
.
18
19
##
Synthesis
Equipment
20
-
All
equipment
and
apparatus
with
:
21
*
Model
numbers
if
specified
22
*
Operating
parameters
23
*
Special
configurations
or
modifications
24
25
##
Synthesis
Procedure
26
Extract
and
organize
:
27
-
Chronological
step
-
by
-
step
synthesis
method
28
-
All
processing
parameters
:
29
*
Temperature
ranges
and
ramp
rates
30
*
Time
durations
for
each
step
31
*
Pressure
conditions
32
*
pH
values
if
applicable
33
*
Mixing
speeds
and
durations
34
-
Critical
control
points
and
special
conditions
35
36
##
Characterization
Methods
and
Equipment
37
List
all
:
38
-
Analytical
techniques
used
39
-
Specific
measurement
conditions
40
-
Sample
preparation
methods
41
-
Equipment
models
and
settings
42
-
Standards
or
references
used
43
44
##
Product
Characteristics
45
Document
:
46
-
Final
product
properties
and
specifications
(
include
both
numerical
values
and
literal
descriptions
if
provided
)
47
-
Yield
calculations
and
actual
yields
48
-
Purity
levels
and
impurity
content
49
-
Performance
metrics
with
measured
values
50
-
Morphological
characteristics
51
52
IMPORTANT
RULES
:
53
1.
DO
NOT
generate
or
assume
any
missing
information
54
2.
If
specific
details
are
not
mentioned
in
the
paper
,
indicate
"
N
/
A
"
55
3.
Use
exact
numbers
and
units
as
presented
in
the
paper
56
4.
Maintain
original
measurement
units
57
5.
Quote
unusual
or
specific
procedures
directly
when
necessary
58
6.
Format
all
information
using
proper
markdown
with
headers
(##)
and
bullet
points
59
60
Remember
:
Accuracy
and
authenticity
are
crucial
.
Only
include
information
explicitly
stated
in
the
paper
.
61
62
Scientific
Paper
:
63
{
text
}
Figure 12:
A prompt to predict the recipe with a one-shot example.
⬇
1
You
are
a
materials
science
expert
.
Your
task
is
to
extract
ONLY
the
explicitly
stated
synthesis
information
from
the
provided
research
paper
.
Do
not
generate
,
assume
,
or
infer
any
information
not
directly
presented
in
the
paper
.
2
If
the
provided
paper
does
not
contain
any
synthesis
information
,
please
indicate
"
NOT
A
MATERIAL
SYNTHESIS
PAPER
"
and
do
not
provide
any
further
details
.
3
4
##
Key
Contributions
5
Summarize
the
key
contributions
of
the
paper
:
6
-
Novel
materials
or
compounds
:
<
summary
>
7
-
Unique
synthesis
methods
:
<
summary
>
8
-
Specific
applications
or
domains
:
<
summary
>
9
10
##
Materials
11
Extract
and
list
:
12
-
All
precursor
materials
with
:
13
*
Exact
quantities
and
concentrations
14
*
Molar
ratios
or
stoichiometric
proportions
15
*
Purity
grades
and
specifications
16
*
Supplier
information
if
provided
17
-
Solvents
,
reagents
,
catalysts
,
and
any
other
materials
such
as
carrier
gases
.
18
19
##
Synthesis
Equipment
20
-
All
equipment
and
apparatus
with
:
21
*
Model
numbers
if
specified
22
*
Operating
parameters
23
*
Special
configurations
or
modifications
24
25
##
Synthesis
Procedure
26
Extract
and
organize
:
27
-
Chronological
step
-
by
-
step
synthesis
method
28
-
All
processing
parameters
:
29
*
Temperature
ranges
and
ramp
rates
30
*
Time
durations
for
each
step
31
*
Pressure
conditions
32
*
pH
values
if
applicable
33
*
Mixing
speeds
and
durations
34
-
Critical
control
points
and
special
conditions
35
36
##
Characterization
Methods
and
Equipment
37
List
all
:
38
-
Analytical
techniques
used
39
-
Specific
measurement
conditions
40
-
Sample
preparation
methods
41
-
Equipment
models
and
settings
42
-
Standards
or
references
used
43
44
##
Product
Characteristics
45
Document
:
46
-
Final
product
properties
and
specifications
(
include
both
numerical
values
and
literal
descriptions
if
provided
)
47
-
Yield
calculations
and
actual
yields
48
-
Purity
levels
and
impurity
content
49
-
Performance
metrics
with
measured
values
50
-
Morphological
characteristics
51
52
IMPORTANT
RULES
:
53
1.
DO
NOT
generate
or
assume
any
missing
information
54
2.
If
specific
details
are
not
mentioned
in
the
paper
,
indicate
"
N
/
A
"
55
3.
Use
exact
numbers
and
units
as
presented
in
the
paper
56
4.
Maintain
original
measurement
units
57
5.
Quote
unusual
or
specific
procedures
directly
when
necessary
58
6.
Format
all
information
using
proper
markdown
with
headers
(##)
and
bullet
points
59
60
Remember
:
Accuracy
and
authenticity
are
crucial
.
Only
include
information
explicitly
stated
in
the
paper
.
61
62
Scientific
Paper
:
63
{
text
}
Figure 13:
A prompt to predict the recipe using retrieval-augmented generation
⬇
1
You
are
an
expert
in
material
science
and
chemical
synthesis
.
Your
task
is
to
design
a
detailed
material
synthesis
recipe
,
considering
the
following
**
key
contributions
**:
2
Your
output
should
follow
the
exact
structure
and
format
of
the
below
references
.
Provide
precise
details
for
each
section
,
including
materials
,
equipment
,
and
step
-
by
-
step
procedures
.
3
4
Here
are
recipes
from
research
papers
with
similar
contributions
.
5
--
References
--
6
{
references
}
7
8
--
Prediction
Input
--
9
Based
on
these
references
,
predict
the
synthesis
recipe
for
the
given
key
contributions
:
10
{
contributions
}
Figure 14:
A prompt to judge the prediction recipe using LLM-as-a-Judge
⬇
1
You
are
an
expert
materials
scientist
tasked
with
evaluating
an
AI
-
generated
synthesis
recipe
.
You
will
be
provided
with
:
2
1.
Target
material
description
3
2.
AI
-
generated
recipe
4
3.
Ground
truth
recipe
from
literature
5
6
Please
evaluate
the
AI
-
generated
recipe
according
to
the
following
criteria
on
a
scale
of
1-5
(1.0:
poor
,
5.0:
excellent
,
0.5
step
).
Provide
detailed
justification
for
each
score
.
7
8
Guidelines
for
evaluation
:
9
10
1.
Materials
11
-
Appropriateness
:
Are
the
selected
materials
suitable
for
the
target
synthesis
?
12
13
2.
Equipment
14
-
Appropriateness
:
Is
the
selected
equipment
suitable
?
15
16
3.
Procedure
17
-
Completeness
:
Are
all
necessary
steps
included
with
sufficient
detail
?
18
-
Similarity
:
How
closely
does
it
match
the
ground
truth
procedure
?
19
-
Feasibility
:
Can
this
procedure
be
realistically
executed
in
a
lab
?
20
21
4.
Characterization
22
-
Appropriateness
:
Are
the
metrics
suitable
for
validating
success
?
23
-
Similarity
:
How
well
do
predicted
properties
match
actual
results
?
24
25
Your
Output
format
must
be
as
following
:
26
1.
Step
-
by
-
step
reasoning
first
27
2.
JSON
score
result
28
‘‘‘
json
29
{
30
"
materials_appropriateness_score
":
float
,
31
"
equipment_appropriateness_score
":
float
,
32
"
procedure_completeness_score
":
float
,
33
"
procedure_similarity_score
":
float
,
34
"
procedure_feasibility_score
":
float
,
35
"
characterization_appropriateness_score
":
float
,
36
"
characterization_similarity_score
":
float
,
37
"
overall_score
":
float
38
}
39
‘‘‘