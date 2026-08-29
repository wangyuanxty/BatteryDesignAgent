DrugPilot: LLM-based Parameterized Reasoning Agent for Drug Discovery
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: arXiv.org perpetual non-exclusive license
arXiv:2505.13940v2 [cs.AI] 28 Jul 2025
Large language models (LLMs) integrated with autonomous agents hold significant potential for advancing scientific discovery through automated reasoning and task execution. However, applying LLM agents to drug discovery is still constrained by challenges such as large-scale multimodal data processing, limited task automation, and poor support for domain-specific tools. To overcome these limitations, we introduce
DrugPilot
, a LLM-based agent system with a parameterized reasoning architecture designed for end-to-end scientific workflows in drug discovery. DrugPilot enables multi-stage research processes by integrating structured tool use with a novel parameterized memory pool. The memory pool converts heterogeneous data from both public sources and user-defined inputs into standardized representations. This design supports efficient multi-turn dialogue, reduces information loss during data exchange, and enhances complex scientific decision-making. To support training and benchmarking, we construct a drug instruction dataset covering eight core drug discovery tasks. Under the Berkeley function-calling benchmark, DrugPilot significantly outperforms state-of-the-art agents such as ReAct and LoT, achieving task completion rates of 98.0%, 93.5%, and 64.0% for simple, multi-tool, and multi-turn scenarios, respectively. These results highlight DrugPilot’s potential as a versatile agent framework for computational science domains requiring automated, interactive, and data-integrated reasoning.
DrugPilot: LLM-based Parameterized Reasoning Agent for Drug Discovery
Kun Li
Email:
likun98@whu.edu.cn
Affiliation:
School of Computer Science, Wuhan University, Wuhan, China
Zhennan Wu
Email:
wuzhennan@whu.edu.cn
Affiliation:
School of Computer Science, Wuhan University, Wuhan, China
Shoupeng Wang
Email:
wangshoupeng@whu.edu.cn
Affiliation:
School of Mathematics and Statistics, Wuhan University, Wuhan, China
Jia Wu
Email:
jia.wu@mq.edu.au
Affiliation:
Department of Computing, Macquarie University, Sydney, Australia
Shirui Pan
Email:
s.pan@griffith.edu.au
Affiliation:
School of Information and Communication Technology, Griffith University, Brisbane, Australia
Wenbin Hu
Email:
hwb@whu.edu.cn
Affiliation:
School of Computer Science, Wuhan University, Wuhan, China
keywords
large language model, agent, tool calling, parameterized reasoning, drug discovery
†
†
equal-contributors:
These authors contributed equally to this work.
†
†
equal-contributors:
These authors contributed equally to this work.
†
†
equal-contributors:
These authors contributed equally to this work.
With the rapid development of deep learning, artificial intelligence (AI)-assisted drug discovery is emerging as a revolutionary way to significantly enhance the efficiency and accuracy of key phases of complex drug discovery tasks
Liu et al. 2024
;
Catacutan et al. 2024
. For example, Chemistry42
Ivanenkov et al. 2023
, a generative AI tool, MolProphet
Yang et al. 2024
, a drug screening system, and DrugFlow
Shen et al. 2024
, an AI platform, have demonstrated excellent prediction performance and dramatically shortened the drug development period. Recent studies, based on these, have applied large language models (LLMs) to automating drug discovery tasks
Chakraborty et al. 2025
;
Ye et al. 2025
;
AbuNasser et al. 2024
. The DrugAgent
Liu et al. 2024
, for example, demonstrated the potential of LLMs for drug R&D automation by setting up two intelligent body roles, the mentor and the planner, and constructing an end-to-end machine learning process from data acquisition to model evaluation. Another study with the same name
Inoue et al. 2025
developed an agent system for drug repositioning by combining knowledge graphs and literature mining techniques. These Agents can leverage the reasoning capabilities of LLMs and perform well in handling multi-source heterogeneous data, demonstrating that LLMs not only facilitate cross-domain knowledge fusion, but also hold the promise of automating the whole process of drug discovery through intelligent decision-making
Zheng et al. 2025
.
Although fine-tuning and reinforcement learning can effectively improve the task performance of LLMs, leveraging their reasoning capabilities for automated drug discovery and accurate prediction still faces significant challenges (Fig.
1
a)
de Thé et al. 2023
;
Tiwari et al. 2023
. The primary challenge is to offer convenient usage for non-computer science users. Drug discovery is a multi-stage, time-consuming process involving a series of complex tasks
Lorente et al. 2025
, including drug generation and optimization
Du et al. 2024
, target affinity prediction
Wu et al. 2024
, and molecular property prediction
Chen et al. 2025
;
Li et al. 2025
and so on. However, researchers in pharmacy, biology, and other related fields often lack the technical expertise to operate state-of-the-art (SOTA) deep learning models
Sadybekov and Katritch 2023
;
Mak and Pichika 2019
. These models have stringent input format requirements, and researchers need to spend a lot of time pre-processing real-world data and converting data formats between different platforms
Niazi and Mariam 2023
;
Chen et al. 2021
. Lack of knowledge of programming, computer hardware, and system operation significantly increases the cost for researchers to use SOTA models effectively, and in some cases hinders their use completely
Zhavoronkov et al. 2019
;
Stokes et al. 2020
.
In addition, there are various challenges in designing LLM-based agents, such as multi-task collaboration, large-scale multimodal data management, and predictive performance requirements during complex task computation. Most existing platforms operate as standalone tools and lack automated task planning and execution capabilities
Liu et al. 2024
;
Inoue et al. 2025
;
Ren et al. 2025
, while drug discovery usually involves more than one phase and requires the seamless integration between tasks
Zhang et al. 2025
. This limitation forces researchers to manually switch between tools and integrate intermediate outputs, significantly reducing the efficiency of human–computer collaboration
Chakraborty et al. 2025
;
AbuNasser et al. 2024
. More critically, the natural language output format of LLMs inherently restricts their ability to precisely represent domain-specific entities (e.g., drug compounds, cell lines, and targets) or to reliably predict their interactions. This often results in hallucinations and fragmented multimodal reasoning
Chakraborty et al. 2025
;
AbuNasser et al. 2024
;
Zheng et al. 2025
, as evidenced by failed semantic alignment across molecular graphs, bioactivity data (numerical matrices), and literature-based evidence (natural language). As data volume increases, the text-based memory paradigm of LLMs tends to lose critical information, leading to task interruptions and failures. Moreover, currently, LLMs perform poorly when dealing with complex tasks, particularly in terms of tool calling accuracy and multi-turn conversation capabilities. As a result, users are unable to carry out sustained practical research. These real-world challenges substantially hinder the ability of LLM-based agents to complete tasks accurately and efficiently (Fig.
1
a).
Figure 1
:
Application scenarios and advantages of DrugPilot. a,
Four application scenarios of DrugPilot: zero-code integration of AI models, scalable data acquisition, coordinated multi-task processing, and accurate execution of 8 essential drug discovery tasks.
b,
Comparison of LLMs or agents for drug discovery with our DrugPilot across three aspects.
Figure 2
:
Architecture of DrugPilot framework. a,
The framework of DrugPilot. DrugPilot comprises four components: the LLM backbones, the PMP, the AI models tailored to 8 stages of drug discovery with tool calling support, and the Fe-Fo mechanism.
b,
The PMP’s structure. In PMP, the memory is stored as key-value pairs, where LLMs interact only with concise keys, while tools directly interact with the structured values.
To address these challenges, we propose DrugPilot, an LLM-based agent with parameterized reasoning for drug discovery (Fig.
2
). DrugPilot comprehensively supports the entire drug research and development pipeline and can autonomously plan and execute multi-stage research tasks based on user queries (Fig.
1
b). To meet the critical demands for accurate extraction and analysis of multimodal drug data, including both public datasets and user-provided inputs, we propose an interactive parameterized memory pool (PMP). As a highly flexible component, PMP converts real-world drug data into standardized parametric representations. This design enables efficient knowledge retrieval during multi-turn interactions and mitigates the information loss commonly associated with text-based transmission. To overcome common reasoning errors encountered by LLMs when interpreting PMP and invoking tools, as well as their tendency to lose track of the original task in extended dialogues, we further introduce a feedback-focus mechanism, called Fe-Fo. Meanwhile, We propose the first tool-calling benchmark for drug discovery, which includes a high-quality instruction dataset, TCDD, and an evaluation method. TCDD consists of 2,800 annotated samples spanning 8 representative drug discovery tasks. On this benchmark, DrugPilot demonstrates superior performance compared to existing approaches including ReAct
Yao et al. 2023
, CoT
Wei et al. 2022
, and Lot
Liu et al. 2024
, as evaluated against the Berkeley function-calling leaderboard. Specifically, DrugPilot achieves task completion rates of 98.0%, 93.5%, and 64.0% across three evaluation categories, increasing by 13.2%, 66.1%, and 80.3%, respectively, over the SOTA agent ReAct.
Results
DrugPilot’s Framework
We propose DrugPilot, an LLM-based agent with parameterized reasoning for drug discovery. DrugPilot comprehensively supports the entire drug research and development pipeline, which can autonomously plan and execute multi-stage research tasks based on user queries. The DrugPilot system comprises four key components: the LLMs, the PMP, the Fe-Fo mechanism, and the AI model zoo. DrugPilot operates through a collaborative framework combining natural language interaction and the PMP (Fig.
2
). The PMP is proposed for extracting textual information and processing large-scale multimodal data, and Fe-Fo mechanism could perform real-time monitoring of the LLMs’ outputs. Fe-Fo targets errors that occur when LLMs read PMP and call tools, providing specific error feedback to help LLMs correct their mistakes, and restating the original question to help LLMs maintain focus. The AI model zoo encompasses a collection of state-of-the-art deep learning models that support core tasks in drug discovery (see Fig.
5
e for task details). This paper focuses on the design of LLM-based agents to enable more efficient tool invocation and task-data coordination. Each task-specific model can be seamlessly integrated into the DrugPilot framework. Additional implementation details and performance benchmarks for task-specific models are available in the Supplementary Materials.
DrugPilot enables users to complete preclinical drug research in real time through natural language conversations. In addition, DrugPilot supports large-scale file uploads, automatically parses and saves file data to the PMP, and the parameters and prediction results during the dialogue process are also saved to the PMP, supporting operations such as downloading, modifying, and deleting. The DrugPilot delivers outputs in two formats: providing conclusions through natural language dialogue while presenting data visualizations via the PMP. For example, in molecular optimization tasks, user’s input is:
⬇
Please
generate
some
optimized
molecules
based
on
the
molecule
CC
(
C
)
C1
=
CC
=
CC
=
C1CC2
=
C
(
C
(=
C
(
C
(=
C2
)
C
(=
O
)
NC3
=
CC
=
C
(
C
=
C3
)
S
(=
O
)(=
O
)
C4
=
CC
=
CC
=
C4C
(
C
)(
C
)
C
)
O
)
O
)
O
,
the
Z
-
score
of
cell
line
MOLT
-13
is
required
to
be
less
than
-0.47.
DrugPilot first interprets the user’s input requirements, identifies the task type and key parameters, including the molecules to be optimized and the optimization conditions, and then stores this information in the PMP. DrugPilot then invokes the conditional molecular optimization model and passes the parameters from the PMP to the model. Once DrugPilot completes execution, it generates a specified number of optimized molecules. These molecules have been stored in the PMP, enabling users to download them or proceed to in-depth analysis. Therefore, this parameterized data management mode accurately records molecular SMILES, enabling seamless integration with other tasks such as molecular property prediction. Compared to traditional LLM-based methods, DrugPilot significantly advances molecular optimization by generating hundreds to thousands of precise SMILES candidates per cycle (vs. dozens) and dynamically integrating SOTA algorithms, overcoming the limitations of fixed AI models and stagnant SOTA performance.
Superior Performance over SOTA LLMs and Agents
To comprehensively assess the performance of DrugPilot, we conducted an overall experiment assessing combinations of different LLMs and various agent paradigms. These agent paradigms serve as baseline methods for comparison with DrugPilot, while the different LLMs are used to examine the overall performance of these methods when paired with different models. DrugPilot can be directly used with pretrained LLMs; however, to further enhance its performance, we also fine-tuned the pretrained LLMs specifically for scenarios involving drug-related tool usage. In this experiment, we treat using DrugPilot with pretrained LLMs and with fine-tuned LLMs as two separate methods for comparison.
Table
1
reports the experimental results. DrugPilot achieves the highest accuracy on the three categories over all agents. For the simple function category, mainstream LLMs including Llama3.1
Vavekanand and Sam 2024
, Llama3
Dubey et al. 2024
, Mistral-NeMo
Sreenivas et al. 2024
, Gemma2
Team et al. 2024
, and Qwen2
Yang et al. 2024
all exceed 97% on Acc.F and 95% on Acc.P.
In the multi-function category, DrugPilot continues to dominate. Across Llama3.1, Llama3, Mistral-NeMo, and Gemma2, Acc.F stays above 98% and Acc.P stays above 92%.
Even in the most complex category, multi-turn function, DrugPilot achieves superior performance, attaining accuracy rates exceeding 70% and 60% compared to the SOTA methods.
As the difficulty of tool calling scenarios increases, the accuracy declines overall. But on all three categories, DrugPilot outperforms the SOTA agent ReAct by 13.6% and 13.2% in simple function, 29.4% and 66.1% in multi-function, 61.2% and 80.3% in multi-turn function on Acc.F and Acc.P. Notably, though less capable LLM like deepseek-llm-7b-chat performs poor, especially in the category of multi-turn function, it still gains improvement compared to baseline methods. Besides, after removing SFT, the performance of DrugPilot declines obviously, but it still surpasses the baseline methods in most scenarios. Compared with the second-best method, DrugPilot still has considerable improvement, with 6.3% and 10.9% in simple function, 24.3% and 60.6% in multi-function, 46.9% and 67.5% in multi-turn function on Acc.F and Acc.P.
In addition to measuring accuracy, we also recorded the average execution time for each query in the multi-turn function category. As shown in Fig.
3
c, the average latency of DrugPilot has been reduced to under 20s, and for models including Qwen2, DeepSeek-R1, Llama3, and Llama3.1, this means more than a twofold improvement over baseline methods. The decrease is particularly striking given that the multi-turn tasks require sequential reasoning based on former results. In practice, this means that DrugPilot not only delivers substantially
higher parameter accuracy but does so with a runtime that is less than half of what SOTA agents require. The combination of SFT and an optimized tool-calling procedure allows DrugPilot to maintain fast response times even as task complexity grows, demonstrating that accuracy and efficiency gains can be achieved simultaneously.
Figure 3
:
Visualization of the experimental results. a,
Function accuracy of different agent methods under varying molecule quantities.
b,
Parameter accuracy of different agent methods under varying molecule quantities.
c,
The parameter accuracy and latency of LLMs and agents on category multi-turn function.
d,
Ablation studies about the effects of SFT, Fe-Fo, and PMP components on multi-task performance metrics in DrugPilot’s Llama3.1-8B framework.
e,
Evaluating the capacity boundaries of ChatGPT-4o and DrugPilot for drug discovery tasks.
Parameterized Memory Pool enables High-volume Drug Data Processing
The excessive scale of parameters is a key challenge in utilizing LLM-based agents for drug discovery tasks. To evaluate the upper limit of the parameter scale that existing methods can handle when processing drug-related parameters, we conducted a parameter scale experiment. We tested ChatGPT-4o
OpenAI et al. 2024
, one of the most powerful closed-source large-scale LLMs, in a drug tool-calling scenario. We compared its performance with DrugPilot by invoking ChatGPT-4o’s tool-calling API. The evaluation task involved calling a drug property prediction tool to predict the water solubility of molecules. By adjusting the number of drug molecules and their average string length in the input, we investigated its capability to handle large-scale drug parameters.
The capacity boundaries of LLMs are shown in Fig.
3
e. When the number of input molecules was
≤
\leq
51 and the average molecular length was
≤
\leq
90, ChatGPT-4o could stably select the correct tool, accurately pass the parameters, and ensure successful task execution. However, when these thresholds were exceeded, constrained by the model’s context length, ChatGPT-4o failed to extract and output such large-scale parameters. These results indicate that ChatGPT-4o’s performance in drug property prediction tasks is limited by the scale of input drug molecules, which must be considered in practical applications involving large-scale parameters in drug discovery.
In contrast, DrugPilot has no upper limit on parameter scale. Even with 91 molecules and an average length of 52, it could still accurately pass the parameters to the tool. Since the PMP employs a key-value pair conversion mechanism to remove large-scale parameters from the LLM’s context, DrugPilot can theoretically handle parameters of any scale. This effectively solves the critical issue of large-scale parameter transfer in drug discovery agents.
Figure 4
:
Case study. a-b,
A case of using the DrugPilot platform to predict BACEi classes.
a,
Data upload process on DrugPilot.
b,
Prediction result display of DrugPilot.
c-d
Prediction results of DrugPilot on BACEi classification task.
c,
Predicted probabilities for 10 SMILES as BACEi. The compound IDs (CIDs) of known molecules and molecular formula (MF) expressions of unknown molecules are shown.
d,
Distribution of BACEi molecules in the t-SNE space.
e,
Comparative analysis of cross-cell-line drug efficacy prediction and experimental validation for five classes of anticancer drugs.
Case Studies on Two Classical Drug Discovery Tasks
This section presents the systematic case studies to evaluate the actual effect of the DrugPilot platform on drug discovery tasks. We select two core tasks as evaluation targets: drug response prediction (DRP) and molecular property prediction (MPP). The successful application of DrugPilot relies on two fundamental capabilities: (1) accurately selecting functional modules and extracting task-specific parameters; and (2) correctly invoking embedded models to produce reliable predictions. As demonstrated in Section
Superior Performance over SOTA LLMs and Agents
, the platform’s capability 1 has been thoroughly verified. In this study, we construct a testing framework on the basis of the Genomics of Drug Sensitivity in Cancer (GDSC) v2
Yang et al. 2012
and BACE
Wu et al. 2018
dataset, simulating realistic drug development scenarios to assess the platform’s predictive accuracy, specifically its capability 2.
Model Capabilities for the DRP Task.
The DRP task evaluates drug sensitivity or efficacy for specific cell lines using quantitative metrics such as IC50, AUC, or cell viability. The model takes drug molecular features (e.g., molecular structures or fingerprints) and cell line characteristics (e.g., gene expression profiles or mutation information) as input, and outputs continuous predictive values representing drug response effects.
In this case study, the DrugPilot platform employs the CLDR method
Li et al. 2024
as its core predictive engine. As illustrated in Fig.
4
, the DrugPilot platform provides a comprehensive DRP implementation solution. Users can submit drug-cell line pairs for analysis through an intuitive file upload interface. This study utilizes test datasets from the GDSCv2, with careful selection of five drug-cell line combinations (4, 4, 7, 6, and 5 samples per group, respectively, totaling 26 test samples) that were excluded from model training for validation purposes. Fig.
4
c presents the performance evaluation results of the DrugPilot platform. Analytical results demonstrate that across five independent drug-cell line tests, the platform’s predicted values exhibit highly consistent monotonically increasing trends when aligned with the ascending order of actual measurements. Notably, the stable distribution of prediction errors around zero robustly validates the superior precision and reliability of the DrugPilot platform.
Model Capabilities for the MPP Task.
The MPP task aims to infer essential molecular-level characteristics. Depending on the type of property, the model outputs either classification probabilities or regression values. MPP plays a critical role in early-stage drug screening and compound prioritization.
DrugPilot employs KCHML
Chen et al. 2025
as the core engine for MPP. In this case study, we evaluate its predictive capabilities on a binary classification task that determines whether a molecule functions as a BACE inhibitor. As shown in Fig.
4
c, we select the top five and bottom five molecules from the BACE dataset and predict their likelihood of being BACE-1 inhibitors (BACEi) using DrugPilot. The results show that most predicted probabilities are highly consistent with the ground truth labels. Fig.
4
d further demonstrates the classification performance by visualizing the top 20 and bottom 20 molecules from the BACE dataset. We apply t-SNE to project their fingerprint features into a two-dimensional space. The resulting distribution reveals a strong alignment between the true BACEi and those predicted BACEi with high probability, indicating the model’s ability to effectively distinguish molecular classes. Together, these findings validate the high accuracy and reliability of DrugPilot in molecular property prediction tasks.
Study of key components
To comprehensively evaluate the impact of each component within DrugPilot on overall system performance, we conducted ablation studies from three perspectives: SFT, the feedback-focus (Fe-Fo) mechanism, and the PMP (Parameterized Memory Pool). These experiments aim to analyze the individual contribution and interplay of each module. All experiments used Llama3.1-8B as the foundation LLM under a simplified tool-calling scenario.
Effect of SFT and Fe-Fo Mechanism.
To investigate the role of SFT and Fe-Fo, we removed each module separately while keeping all other conditions unchanged. We then evaluated the accuracy of tool selection and parameter extraction across multi-functional tasks. As shown in Fig.
3
d, both modules have a significant positive effect on performance.
With the addition of SFT and Fe-Fo, tool-selection accuracy achieves 95.0% and parameter-extraction accuracy achieves 93.7%, increasing by 28.7% and 44.9% respectively. Notably, the latency has also been greatly improved, from the original 30.91s to 15.18s. Compared to the baseline results in Table.
1
, either component results in a notable accuracy improvement.
In comparison with the baseline method, the addition of SFT and Fe-Fo increase tool-selection accuracy to 73.8% (+7.5%) and 82.1% (+15.8%), parameter-extraction accuracy to 59.2% (+10.4%) and 70.0% (+21.2%). Furthermore, when PMP is enabled, the performance improvement brought by SFT is greater, with parameter-extraction accuracy to 88.3% (+37.9%). Meanwhile, when the model undergoes SFT, Fe-Fo also increases the parameter-extraction accuracy more significantly, reaching 93.7% (+26.2%).
Specifically, SFT effectively enhances the model’s understanding of domain-specific text, while the Fe-Fo mechanism significantly improves the agent’s error handling ability.
Effect of PMP.
This study highlights the introduction of PMP, designed to handle large-scale molecular data. To validate the effectiveness of PMP, we gradually increased the number of molecules processed per query and tested the boundary of parameter recognition and extraction capability for different agent methods. To simulate real-world usage, an equivalent number of molecules were loaded into the memory pool. Under the same test data and model settings, we recorded the accuracy and latency of various agents. Fig.
3
a and Fig.
3
b show that the performance of traditional approaches degrades as the number of molecules increases—accuracy drops continuously while latency rises sharply. In particular, when the number of molecules exceeds 15, other methods’ accuracy drops significantly. When the number of molecules reaches 20, the CoT method essentially fails to extract valid parameters. Similarly, DrugPilot without PMP, as well as ReAct and LoT, become nonfunctional when handling around 30 molecules. In contrast, real-world applications often require processing tens of thousands of molecules at once. DrugPilot equipped with PMP, however, maintains stable accuracy and response time throughout. The incorporation of PMP enables the model to focus on understanding user intent, effectively overcoming the challenge of extracting task-relevant parameters from lengthy and complex molecular descriptions.
Notations:
\raisebox{-0.9pt}{1}⃝ There are different formalized parameters corresponding to keys in the memory pool, this sample takes
(user_smiles)
for an example.
\raisebox{-0.9pt}{2}⃝
Function Call
is the proper key in ShareGPT format, and we identify function calling and tool calling in this paper.
\raisebox{-0.9pt}{3}⃝ The capital letters denote the types of corresponding parameters, with
ℒ
\mathcal{L}
standing for list and
𝒮
\mathcal{S}
standing for string. Tools
drug_generation
and
drug_optimization
integrate multiple models trained on different datasets, and they are suitable for different conditions. We represent their parameters with
𝒞
∗
\mathcal{C}^{*}
uniformly.
\raisebox{-0.9pt}{4}⃝ Dataset:
⚫
BACE,
⚫
BBBP,
⚫
ESOL,
⚫
FreeSolv,
⚫
LIPO,
⚫
GDSCv2
Yang et al. 2012
,
◼
DAVIS
Davis et al. 2011
,
◼
KIBA
Tang et al. 2014
,
◼
BindingDB
Liu et al. 2007
,
⚫
DrugBank
Wishart et al. 2018
,
⚫
TWOSIDES
Zitnik et al. 2018
,
▲
ZINC
Sterling and Irwin 2015
,
▲
QM9
Ramakrishnan et al. 2014
;
Ruddigkeit et al. 2012
⚫
USPTO
Suzgun et al. 2023
.
Figure 5
:
Format and information of TCDD. a-d,
Sample structure with ShareGPT format for simple-turn dialogue. The dataset samples following the ShareGPT format comprise conversations, system, and tools.
e,
Basic information of drug discovery tools including names, input/output parameter structures, data sources, and the specific quantities of samples in training set.
Discussion
Recent advances in AI-assisted drug discovery have resulted in the development of transformative platforms such as Chemistry42
Ivanenkov et al. 2023
, DrugFlow
Shen et al. 2024
, and large language model (LLM)-based agents, such as DrugAgent
Liu et al. 2024
;
Inoue et al. 2025
, DrugAssist
Ye et al. 2025
, and MolecularGPT
Liu et al. 2024
. However, three critical limitations persist: (1) non-expert researchers struggle with the technical demands of SOTA models
Sadybekov and Katritch 2023
;
Zhavoronkov et al. 2019
;
Talevi 2023
;
Morgnanesi et al. 2015
, (2) existing tools fail to align multimodal data, and (3) workflow fragmentation necessitates manual task integration
Zhang et al. 2025
;
Paul et al. 2010
.
This paper proposes DrugPilot, an end-to-end LLM-based parameterized reasoning agent for drug discovery to address these challenges. To represent multimodal data structurally and parametrically, as well as to break through the traditional text-based context length limitation, we innovatively propose PMP. The PMP solves the problem of multimodal data fragmentation by converting drug-related entities (e.g., SMILES expressions, protein sequences, etc.) into executable key-value pairs. The PMP solves the multimodal data problem by converting drug-related entities (e.g. SMILES expressions, protein sequences, etc.) into actionable key-value pairs. Unlike the text-based memory mechanism relied on by mainstream LLMs (e.g., ChatGPT, DeepSeek) and agents (e.g., CoT
Wei et al. 2022
, ReAct
Yao et al. 2023
), PMP saves parameters structured in unstructured text as key-value pairs (Fig.
2
b), which achieves lossless transfer of information and effectively improves the efficiency and accuracy of collaborative processing of multimodal data
Zhou et al. 2024
. Under the same task settings, DrugPilot keeps the task completion rate above 95% when processing inputs of different scales (1
∼
\sim
30 SMILES strings) compared to other agents (Fig.
3
b). In addition, we also conducted a maximum parameter handling capacity test. The results show that compared with the GPT-4o
OpenAI et al. 2024
, which supports 51 parameters at maximum, DrugPilot has a theoretically unlimited parameter processing capability (Fig.
3
e).
To further improve the robustness of tool calling, we design the Fe-Fo mechanism. In the multiple-function category, adding only the Fe-Fo mechanism, DrugPilot improves the functional accuracy (Acc. F) and parameter accuracy (Acc. P) by 5.8% and 13.7%, respectively, which is significantly better than the ReAct (Table
1
). Meanwhile, we constructed the TCDD, a drug discovery tool calling dataset for drug discovery tasks, which covers 8 core tasks with a total of 2,800 high-quality annotated samples, and supports SFT and evaluation. On the TCDD dataset, DrugPilot achieved superior task completion rates, reaching 98.0% for simple function, 93.5% for multiple function, and 64.0% for multi-turn function, significantly outperforming all baseline methods in each category. Even without fine-tuning, DrugPilot significantly outperforms mainstream agents that have been fine-tuned (e.g., CoT
Wei et al. 2022
, ToT
Yao et al. 2023
, ReAct
Yao et al. 2023
, etc.).
In summary, DrugPilot breaks down the key barriers between AI and the actual drug discovery process through a parametric reasoning structure, and a robust error correction mechanism. Its superior accuracy and efficient workflow automation in multi-tasking scenarios effectively alleviate the long-standing inefficiencies in the drug discovery process. While data construction and task extensibility remain future challenges, this study lays the groundwork for future research, such as incorporating reinforcement learning for dynamic task planning and enabling broader intelligent assists for drug discovery. DrugPilot demonstrates the transformative potential of LLM Agents in accelerating drug discovery by reducing technical barriers and enhancing cross-domain collaboration efficiency.
Methods
To optimize the performance of LLM agents in executing drug discovery tasks through tool-calling, we design DrugPilot. First, we constructed the TCDD dataset and used it to fine-tune LLMs, aiming to enhance the models’ domain-specific knowledge in drug discovery and their understanding of drug-related tools. Second, we propose the parameterized memory pool mechanism to handle large-scale, multimodal data and multi-turn conversations. Finally, we propose a feedback-focus mechanism to help LLMs correct common errors when calling drug-related tools and to maintain focus on the original task.
The DrugPilot framework, depicted in Fig.
2
a. The user’s drug discovery task is first provided as input to the LLM backbones. These LLMs will have the reason to make decisions on reading the PMP and calling tools. After verification by the Fe-Fo mechanism, the tool calls are executed, and results are returned. If errors are detected during verification, feedback is provided to the LLMs through the Fe-Fo mechanism. Throughout this process, users can view or update parameters in the PMP at any time to oversee the task execution. The LLMs will continuously reason based on the above information until the final answer is produced.
Tool-Calling Dataset for Drug Discovery
LLMs have achieved strong performance in general tool calling tasks, but given the lack of knowledge in relevant fields
Holstein 2024
, complex data forms, and the need for batch processing of data
Zhu 2020
, LLMs still struggle to correctly infer tool names and parameters of drug discovery tasks. To address these challenges, we built TCDD, a tool-calling dataset for drug discovery to fine-tune and test LLMs. Specifically, TCDD is used to validate the three key capabilities of LLMs:
1.
Tool selection: comprehending natural language queries of drug discovery tasks and selecting corresponding drug discovery tools;
2.
Parameter extraction: identifying and extracting required parameters of unique data forms from the context.
3.
Interaction with PMP: retrieving parameterized data in PMP and saving execution results.
The TCDD simulates real-world conversations between users and AI systems in the area of drug discovery, comprising various scenarios such as single-turn, multi-turn, error correction, and memory pool updates. It has a total of 2,800 instruction samples, 2500 for training and 300 for testing, with the ShareGPT format, which is originally designed for multi-turn dialogue.
This format supports LLMs in interacting with external services and thus is particularly suitable for drug discovery tasks characterized by multi-turn workflows and tool calling. Fig.
5
e shows the basic information of the eight drug discovery tools in the TCDD, containing their names, input/output parameter structures, data sources, and the specific quantities of samples for different dialogue patterns in the training set.
Since the interaction with the memory pool requires formalized parameters, the samples are categorized into two types based on whether the memory pool mechanism is employed. Fig.
5
a and Fig.
5
b illustrates examples of both types of dialogues using the
drug_property
tool to predict the aqueous solubility of a given drug. Each sample consists of three components: conversation, system instructions, and tools, with variations in the conversation portion between the two sample types. The conversation segment includes:
1.
Human: The user inputs a natural language description of the drug discovery task;
2.
Function Call: The LLM generates the tool calling information in JSON format, specifying the tool name and corresponding parameters;
3.
Observation: The tool is called and the execution result is returned;
4.
LLM: The LLM generates a response integrating the observation and task objectives.
The system section guides the LLM to execute tool calling and return results in a standardized format. The tools section provides essential information about the available tools, including: function names and descriptions, acceptable parameters with types and descriptions, and required parameters.
During the development of TCDD, we designed single-turn/multi-turn dialogue patterns, diversified user query expressions, and varied drug molecule types to enhance performance. Approximately 50% of the samples consist of single-turn dialogues with complete instructions, establishing fundamental tool calling rules and memory pool retrieval mechanisms. The remaining samples simulate complex multi-turn dialogues reflecting real-world workflows, including multi-turn tasks (30%) and parameter error scenarios (20%). For instance, in a typical drug optimization workflow, the system first generates molecular candidates based on inhibitory concentrations against specific cell types, then predicts drug properties (e.g., solubility), evaluates drug-target binding affinity, and finally refines the candidates. Such workflows require the model to integrate intermediate results from prior steps, efficiently extract parameters using the memory pool, and handle error propagation when tool failures occur. For common user input issues such as missing or misspelled parameters, the tool calling returns observations containing specific error messages. Corresponding samples in the dataset train the LLM to accurately discern user intent and interact appropriately based on tool specifications and observations.
The distribution of samples across different tools and patterns was determined considering their usage scenarios, parameter complexity, and frequency of application. In a complete workflow, tools such as
drug_optimization
and
drug_generation
are more likely to be used in combination with others. Hence, their ratios of multi-turn to single-turn samples are relatively higher. Since
drug_target_affinity
and
drug_target_interaction
require target protein sequences as parameters, which are typically long and complex, these tools have more error-correction samples. Similarly, given that
drug_optimization
involves significantly more parameters than other tools, it also includes a higher proportion of error-handling samples.
Figure 6
:
Process of evalution and parameter management in DrugPilot.
a,
The step by step evaluation process.
b,
An example of PMP. PMP automatically saves parameters from conversations and performs key-value mapping, allowing users to modify them anytime.
Parameterized Memory Pool
To address the limitations of traditional memory modules in transmitting large-scale, multimodal drug-related parameters, we propose a novel memory module: the parameterized memory pool (PMP). PMP does not store unstructured text but instead maintains structured key-value pairs. Its purpose is to optimize parameter passing efficiency within the agent, thereby reducing the reasoning burden on LLMs, improving the controllability of reasoning results, and ultimately enhancing the performance of LLMs in drug-related tool calling. We conducted prompt engineering to help LLMs better understand PMP. The memory pool prompt explicitly defines the purpose, usage scenarios, and usage method of PMP, as detailed in Appendix
1
.
The Structure of PMP
In traditional memory modules, memory takes the form of a series of conversation text fragments, with drug-related parameters embedded within the text. While the PMP is a key-value store, where each key-value pair maintains a parameter related to drug discovery. Each key is unique and is a short string representing the name of a drug-related parameter, designed to convey its meaning as clearly as possible for interaction with LLMs. The value is the actual content of the parameter, structured in a format that can be directly used as input for drug-related tools, enabling seamless interaction between PMP and external tools. When there are multiple parameters of the same type, they share one key, and their corresponding values are stored as a list containing all the parameters of that type.
As shown in Fig.
2
b, when storing a large-scale list of drug molecules, the key could be
"generated_drug_smiles"
, indicating that it represents a user-provided list of molecular expressions. Such drug-related parameters can be of considerable scale, for example, they may consist of lists with tens of thousands of entries and be embedded within complex textual contexts. This large-scale, multimodal context poses significant challenges for both storage and reasoning. The PMP extracts these large-scale parameters from complex text and converts them into concise keys, allowing LLMs to interact only with these short keys. This greatly reduces the length of context required for the task. Furthermore, PMP maintains the parameters in a structured manner, enabling subsequent tool invocations to directly use these parameters without requiring LLMs to repeatedly infer their complete content.
Parameter Reading and Updating
In traditional memory modules, the stored memory content is typically text fragments from the conversation. When performing reasoning with the LLMs, the user inputs a piece of text, and memory modules will also retrieve a piece of text from the stored historical information. These two parts of the text are concatenated and fed into the LLMs together for reasoning. This parameter extraction process can be formulated as:
v
=
ℛ
L
​
L
​
M
​
(
T
u
+
T
m
)
,
where
​
T
m
⊆
ℳ
v=\mathcal{R}_{LLM}(T_{u}+T_{m}),\quad\text{where }T_{m}\subseteq\mathcal{M}
(1)
where,
ℳ
\mathcal{M}
denotes the entire stored memory,
T
m
T_{m}
denotes the retrieved memory text,
T
u
T_{u}
denotes the user input text,
ℛ
L
​
L
​
M
\mathcal{R}_{LLM}
denotes the function for retrieving parameters from text using LLMs and
v
v
denotes the final parameter passed to the tool. In this method, the large-scale complex texts bring a tremendous inference burden for LLMs
Fig.
6
b illustrates the workflow of the PMP. First, before the conversation begins, users can upload their own datasets or public datasets into DrugPilot. It is important to note that users are not limited to uploading parameters only at the beginning. They can add, delete, modify, and query parameters in the PMP at any time. This ability to dynamically control and adjust the task direction at any stage enhances the flexibility of the memory module. Compared to disorganized large blocks of text, the structured memory format enables users to operate on memory content. This feature allows humans to efficiently interact with the memory of large models and significantly improves the flexibility of the memory module.
Next, after the drug discovery task and the current keys stored in PMP are input into the LLM, the LLM analyzes the input text, selects the tool to call, and considers how to obtain the parameters required by that tool. If the required parameters are included in the input text, the LLM will identify and extract them directly from the text. Meanwhile, PMP saves the parameter as a key-value pair by assigning a key to the parameter and storing its content in the corresponding value for use in the next step. If the key already exists, PMP will use a list as the value for that key and append the current parameter to the list.
If the user’s input text does not contain the required parameter, the LLM will select a key corresponding to the required parameter from the list of keys in the PMP. The PMP will then map the selected key to its corresponding value and pass that value as a parameter to the tool. If the value is a list containing multiple parameters, the PMP will take the last element of the list, which is the most recently added parameter. Through the key-value conversion mechanism of PMP, LLMs’ reasoning task becomes selecting the key to use. It makes LLMs no longer interact directly with large-scale data, effectively reducing the burden on various components of the LLM-based agent system, including LLM inference, memory storage, and memory retrieval. The parameter extraction process of DruPilot can be formulated as:
v
\displaystyle v
=
𝒢
⁡
(
arg
⁡
max
k
∈
ℳ
𝒦
​
𝒫
L
​
L
​
M
​
(
ℳ
𝒦
)
)
\displaystyle=\mathcal{G}(\underset{k\in\mathcal{M_{K}}}{\arg\max}\ \mathcal{P}_{LLM}(\mathcal{M_{K}}))
(2)
where,
ℳ
𝒦
\mathcal{M_{K}}
denotes the key set in the memory pool,
k
k
denotes a key from
ℳ
𝒦
\mathcal{M_{K}}
,
𝒫
L
​
L
​
M
\mathcal{P}_{LLM}
denotes the function using LLMs to get the probability of using
k
k
, and
𝒢
\mathcal{G}
denotes the predefined mapping function. The PMP provides the LLMs with a series of selectable parameter keys.
After a successful tool calling, PMP will save the result returned by the tool as a key-value pair. It assigns a key to the result and stores the entire result as the value. In the next step, this result will be added to PMP’s key list and passed as input to the LLM. At this point, the LLM can choose this execution result as the input parameter for the next tool invocation.
Feedback-focus Mechanism
LLMs cannot always perfectly select tools and pass parameters with complete correctness in both content and format. Additionally, LLMs tend to forget the initial task during long conversations. To address these issues, we propose a feedback-focus mechanism, named Fe-Fo, to help LLMs correct errors and maintain focus, making their output more controllable.
In the feedback mechanism, we alleviate common reasoning issues by feeding error information back to LLMs. When calling drug-related tools, the reasoning output of LLMs exhibits a series of common issues, as illustrated in Appendix
2
. We have verified these issues and designed corresponding feedback prompts for each error type. These prompts describe the type and cause of the error in detail and explicitly instruct the LLMs to regenerate the output according to the requirements based on this information.
In the focus mechanism, we help LLMs stay focused by reiterating the original task. If LLMs are unable to resolve the issue in one attempt, the length of the conversation will inevitably increase. At this point, LLMs often forget the initial task, leading to a loss of focus and resulting in aimless attempts, such as randomly changing the selected tool or passing parameters based on hallucinations. To address this issue, when LLMs make a reasoning error, DrugPilot will repeat the original task to the LLMs, ensuring that they remain focused on the required drug discovery task.
Fe-Fo integrates the above two types of information and provides a clear instruction: regenerate the output according to the formatting requirements based on the given information. When any error from the types shown in Appendix
2
is detected, the Fe-Fo mechanism will feed the Fe-Fo prompt into the LLMs, which can be formulated as:
O
t
+
1
\displaystyle O_{t+1}
=
L
​
L
​
M
​
(
ℰ
⁡
(
O
t
)
+
T
+
I
)
\displaystyle=LLM(\mathcal{E}(O_{t})+T+I)
(3)
where,
I
{I}
denotes the instruction to guide the reasoning,
T
{T}
denotes the original task description,
ℰ
\mathcal{E}
denotes the error detection function applied to the output of LLMs which returns the feedback information corresponding to the error and
O
t
{O_{t}}
denotes the output of LLMs at step
t
t
.
Evaluation Metrics
Drawing on the Berkeley function-calling leaderboard
Patil et al. 2024
, we designed a custom evaluation framework for DrugPilot and other agents. A valid tool calling requires correct tool selection, accurate parameter extraction, and effective self-correction across multiple turns. Therefore, we divide the evaluation into three categories, with 100 queries in each category, which together constitute the test set.
•
Simple function: This category contains the simplest situation with one and only one function supplied.
•
Multiple function: This category contains a user query that requires the invocation of only one function among eight available tools.
•
Multi-turn function: This category contains multi-turn queries, where different queries may correspond to different tool callings.
Baselines
DrugPilot integrates multiple drug discovery tools, and it mainly focuses on accurate tool calling to complete a full workflow of drug discovery tasks. However, some existing methods, like DrugAgent
Inoue et al. 2025
, are dedicated to improving performance on individual tasks, concentrating on text understanding and result interpretation. These methods do not align well with our task objectives.
Therefore, we select four representative agents with tool-calling capabilities in recent times for comparison, and these four baseline agents are based on pre-trained LLMs:
•
CoT
Wei et al. 2022
is a simple baseline where the agent generates a solution by breaking the problem into substeps.
•
LoT
Liu et al. 2024
is a self-improvement prompting framework where the agent verifies and refines its intermediate reasoning steps by embedding symbolic logic principles.
•
ReAct
Yao et al. 2023
interleaves reasoning traces with actions to enable LLMs to iteratively plan, gather information, and adjust strategies.
•
ChatGPT-4o
OpenAI et al. 2024
Function Calling API is a structured tool-calling interface provided by OpenAI, built on the closed-source LLM and tool-calling method.
Fine-Tuning
We fine-tuned a series of small-scale LLMs on TCDD using LoRA
Hu et al. 2021
, including Meta-Llama-3.1-8B-Instruct
Vavekanand and Sam 2024
, Meta-Llama-3-8B-Instruct
Dubey et al. 2024
, Mistral-Nemo-Instruct-2407
Sreenivas et al. 2024
, Gemma-2-9B-it
Team et al. 2024
, Qwen2-7B-Instruct
Yang et al. 2024
, DeepSeek-LLM-7B-Chat
Bi et al. 2024
, DeepSeek-R1-Distill-Llama-8B
DeepSeek-AI et al. 2025
and Llama-3-Groq-8B-Tool-Use (
https://groq.com/introducing-llama-3-groq-tool-use-models.
). We use the open-source dataset glaive_toolcall (
https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2.
) to improve the general tool-calling capabilities of the LLMs. And we divided our TCDD into training, validation, and testing subsets at a ratio of 8:1:1 to enhance LLMs’ specialized capabilities in drug-related tool calling and evaluated their performance. Details of the hyperparameter settings employed during fine-tuning is recorded in Appendix
3
.
Evaluation Process
For each task, the LLM generates an action input, information required to call the tools, in JSON format. Given that hallucination remains a challenge for LLMs, especially in tool calling, we evaluate their responses in two aspects: tool selection and parameter extraction. According to this, we report two accuracy metrics: function accuracy (
Acc.F
) and parameter accuracy (
Acc.P
). Additionally, detailed calculation formulas are shown in Appendix
4
.
Fig.
6
a shows the step-by-step evaluation process of the LLM response, namely the action input. First, the action input undergoes function evaluation, where the tool name is extracted and verified. Once the tool name is correct, the function parameters are parsed and undergo parameter evaluation. This step verifies whether all required parameters are present and that no unexpected parameter is included. Finally, each parameter value is inspected to confirm its correctness and integrity. Only when all these checks are completed is the tool calling deemed valid. The two parts of the evaluation correspond respectively to function accuracy and parameter accuracy in the final results. In addition, the maximum allowable execution time for an individual query is set to 120s; any response that exceeds this threshold is directly determined erroneous.
Data availability
The tool-calling dataset for drug discovery (TCDD), which includes data for both fine-tuning and evaluation, is available at
https://drive.google.com/file/d/1JthOkIAzuuaajZhgH03e9TfM9KwBHmni/view?usp=sharing.
Code availability
The source code of DrugPilot is freely available and can be found on the GitHub at
https://github.com/wzn99/DrugPilot
.
DrugPilot (ours)
DrugPilot w.o. SFT
CoT
LoT
ReAct
Category
Model
Scale
Acc.F
b
Acc.P
b
Acc.F
Acc.P
Acc.F
Acc.P
Acc.F
Acc.P
Acc.F
Acc.P
Simple Function
Llama3.1
8B
98.4
1.2
\textbf{98.4}_{~1.2}
cd
98.0
1.3
\textbf{98.0}_{~1.3}
89.4
0.4
89.4_{~0.4}
88.4
1.0
88.4_{~1.0}
d
92.6
2.9
92.6_{~2.9}
63.4
3.4
63.4_{~3.4}
81.2
5.1
81.2_{~5.1}
46.4
4.6
46.4_{~4.6}
86.6
4.4
86.6_{~4.4}
86.6
4.4
86.6_{~4.4}
Llama3
8B
99.2
0.8
\textbf{99.2}_{~0.8}
97.6
2.1
\textbf{97.6}_{~2.1}
73.0
3.9
73.0_{~3.9}
73.0
3.9
73.0_{~3.9}
81.0
3.5
81.0_{~3.5}
75.0
3.2
75.0_{~3.2}
43.4
4.5
43.4_{~4.5}
38.8
5.3
38.8_{~5.3}
71.0
4.2
71.0_{~4.2}
71.0
4.2
71.0_{~4.2}
Mistral-NeMo
7B
97.4
0.5
\textbf{97.4}_{~0.5}
97.0
1.0
\textbf{97.0}_{~1.0}
89.2
1.8
89.2_{~1.8}
89.2
1.8
89.2_{~1.8}
90.8
4.9
90.8_{~4.9}
89.0
5.4
89.0_{~5.4}
93.4
2.8
93.4_{~2.8}
89.4
4.2
89.4_{~4.2}
88.6
4.8
88.6_{~4.8}
88.6
4.8
88.6_{~4.8}
Gemma2
9B
97.8
1.1
\textbf{97.8}_{~1.1}
97.4
1.1
\textbf{97.4}_{~1.1}
90.2
0.1
90.2_{~0.1}
90.2
0.1
90.2_{~0.1}
87.0
0.1
87.0_{~0.1}
86.4
1.1
86.4_{~1.1}
85.8
1.8
85.8_{~1.8}
80.6
1.1
80.6_{~1.1}
88.0
0.1
88.0_{~0.1}
87.6
0.5
87.6_{~0.5}
Qwen2
7B
99.3
0.1
\textbf{99.3}_{~0.1}
95.9
1.8
\textbf{95.9}_{~1.8}
98.6
0.1
98.6_{~0.1}
89.2
3.9
89.2_{~3.9}
98.2
1.1
98.2_{~1.1}
87.8
1.5
87.8_{~1.5}
97.0
1.6
97.0_{~1.6}
83.2
3.1
83.2_{~3.1}
97.4
0.5
97.4_{~0.5}
88.4
2.3
88.4_{~2.3}
DeepSeek-LLM
7B
47.6
2.6
\textbf{47.6}_{~2.6}
41.2
4.0
\textbf{41.2}_{~4.0}
33.9
4.7
33.9_{~4.7}
33.6
4.1
33.6_{~4.1}
17.2
4.7
17.2_{~4.7}
13.6
2.7
13.6_{~2.7}
19.6
3.6
19.6_{~3.6}
11.2
4.0
11.2_{~4.0}
40.4
3.4
40.4_{~3.4}
27.4
3.6
27.4_{~3.6}
DeepSeek-R1
a
8B
97.2
0.8
\textbf{97.2}_{~0.8}
73.6
6.2
\textbf{73.6}_{~6.2}
66.2
0.1
66.2_{~0.1}
61.8
1.3
61.8_{~1.3}
48.2
5.4
48.2_{~5.4}
43.6
4.2
43.6_{~4.2}
61.0
3.3
61.0_{~3.3}
54.8
2.6
54.8_{~2.6}
58.0
4.6
58.0_{~4.6}
56.6
4.3
56.6_{~4.3}
Llama3-Groq
8B
99.8
0.4
\textbf{99.8}_{~0.4}
90.6
2.4
\textbf{90.6}_{~2.4}
44.0
5.6
44.0_{~5.6}
43.0
5.4
43.0_{~5.4}
15.8
1.9
15.8_{~1.9}
15.2
2.3
15.2_{~2.3}
23.2
2.9
23.2_{~2.9}
22.6
3.2
22.6_{~3.2}
38.6
4.5
38.6_{~4.5}
38.6
4.5
38.6_{~4.5}
Multiple Function
Llama3.1
8B
98.7
0.6
\textbf{98.7}_{~0.6}
93.5
2.3
\textbf{93.5}_{~2.3}
79.4
2.9
79.4_{~2.9}
58.2
1.2
58.2_{~1.2}
55.8
3.3
55.8_{~3.3}
50.5
3.4
50.5_{~3.4}
53.5
2.7
53.5_{~2.7}
43.0
3.6
43.0_{~3.6}
76.3
5.1
76.3_{~5.1}
56.3
5.6
56.3_{~5.6}
Llama3
8B
98.0
2.3
\textbf{98.0}_{~2.3}
92.8
4.6
\textbf{92.8}_{~4.6}
65.0
1.7
65.0_{~1.7}
54.3
2.0
54.3_{~2.0}
46.3
5.4
46.3_{~5.4}
43.3
5.6
43.3_{~5.6}
35.8
4.6
35.8_{~4.6}
32.8
4.2
32.8_{~4.2}
59.8
2.1
59.8_{~2.1}
53.5
2.7
53.5_{~2.7}
Mistral-NeMo
7B
98.4
2.1
\textbf{98.4}_{~2.1}
96.3
2.5
\textbf{96.3}_{~2.5}
86.8
4.8
86.8_{~4.8}
83.7
3.8
83.7_{~3.8}
82.0
2.7
82.0_{~2.7}
68.3
3.4
68.3_{~3.4}
76.0
3.8
76.0_{~3.8}
70.8
3.0
70.8_{~3.0}
92.3
3.5
92.3_{~3.5}
77.8
3.4
77.8_{~3.4}
Gemma2
9B
99.5
0.7
\textbf{99.5}_{~0.7}
92.2
2.4
\textbf{92.2}_{~2.4}
91.0
2.2
91.0_{~2.2}
72.4
3.1
72.4_{~3.1}
92.5
2.7
92.5_{~2.7}
79.8
1.9
79.8_{~1.9}
86.8
2.9
86.8_{~2.9}
76.3
4.2
76.3_{~4.2}
93.0
1.4
93.0_{~1.4}
73.8
2.3
73.8_{~2.3}
Qwen2
7B
93.7
2.9
\textbf{93.7}_{~2.9}
87.2
2.3
\textbf{87.2}_{~2.3}
93.2
2.9
93.2_{~2.9}
76.0
5.7
76.0_{~5.7}
87.5
2.5
87.5_{~2.5}
77.8
4.5
77.8_{~4.5}
83.3
4.6
83.3_{~4.6}
71.5
3.0
71.5_{~3.0}
92.5
1.1
92.5_{~1.1}
74.5
1.9
74.5_{~1.9}
DeepSeek-LLM
7B
39.5
2.7
\textbf{39.5}_{~2.7}
18.8
1.6
\textbf{18.8}_{~1.6}
26.5
6.5
26.5_{~6.5}
13.0
2.1
13.0_{~2.1}
11.0
2.1
11.0_{~2.1}
5.3
2.1
\ \ 5.3_{~2.1}
9.5
3.3
\ \ 9.5_{~3.3}
5.0
3.5
\ \ 5.0_{~3.5}
20.5
2.4
20.5_{~2.4}
8.5
2.2
\ \ 8.5_{~2.2}
DeepSeek-R1
8B
93.9
2.0
\textbf{93.9}_{~2.0}
72.2
4.1
\textbf{72.2}_{~4.1}
60.3
5.3
60.3_{~5.3}
49.0
2.2
49.0_{~2.2}
51.8
3.4
51.8_{~3.4}
34.3
3.3
34.3_{~3.3}
39.0
3.6
39.0_{~3.6}
29.0
3.8
29.0_{~3.8}
60.3
4.8
60.3_{~4.8}
43.3
4.0
43.3_{~4.0}
Llama3-Groq
8B
96.2
0.9
\textbf{96.2}_{~0.9}
78.5
2.1
\textbf{78.5}_{~2.1}
39.5
4.2
39.5_{~4.2}
30.5
3.2
30.5_{~3.2}
17.5
3.5
17.5_{~3.5}
17.0
3.1
17.0_{~3.1}
10.3
1.9
10.3_{~1.9}
9.3
1.4
\ \ 9.3_{~1.4}
40.3
7.4
40.3_{~7.4}
28.8
4.6
28.8_{~4.6}
Multi-turn Function
e
Llama3.1
8B
72.7
6.7
\textbf{72.7}_{~6.7}
64.0
5.7
\textbf{64.0}_{~5.7}
49.5
2.4
49.5_{~2.4}
38.2
2.3
38.2_{~2.3}
43.0
3.6
43.0_{~3.6}
31.8
2.9
31.8_{~2.9}
30.1
5.4
30.1_{~5.4}
24.5
4.8
24.5_{~4.8}
45.1
5.2
45.1_{~5.2}
35.5
3.7
35.5_{~3.7}
Llama3
8B
74.2
4.1
\textbf{74.2}_{~4.1}
61.9
4.7
\textbf{61.9}_{~4.7}
34.8
4.7
34.8_{~4.7}
25.1
5.4
25.1_{~5.4}
25.8
5.9
25.8_{~5.9}
17.3
3.8
17.3_{~3.8}
20.7
3.3
20.7_{~3.3}
14.7
2.6
14.7_{~2.6}
32.6
1.4
32.6_{~1.4}
18.0
2.6
18.0_{~2.6}
Mistral-NeMo
7B
70.0
6.1
\textbf{70.0}_{~6.1}
56.9
4.1
\textbf{56.9}_{~4.1}
54.9
5.1
54.9_{~5.1}
37.2
2.9
37.2_{~2.9}
44.4
3.2
44.4_{~3.2}
33.2
3.1
33.2_{~3.1}
38.9
3.8
38.9_{~3.8}
31.3
1.6
31.3_{~1.6}
50.9
2.9
50.9_{~2.9}
39.5
3.0
39.5_{~3.0}
Gemma2
9B
84.9
1.9
\textbf{84.9}_{~1.9}
61.8
4.1
\textbf{61.8}_{~4.1}
44.3
1.8
44.3_{~1.8}
34.4
2.1
34.4_{~2.1}
54.3
2.3
54.3_{~2.3}
43.1
2.6
43.1_{~2.6}
35.3
3.4
35.3_{~3.4}
27.6
3.1
27.6_{~3.1}
34.5
2.1
34.5_{~2.1}
32.8
1.9
32.8_{~1.9}
Qwen2
7B
73.9
3.2
\textbf{73.9}_{~3.2}
57.3
3.3
\textbf{57.3}_{~3.3}
38.2
4.0
38.2_{~4.0}
22.7
2.6
22.7_{~2.6}
34.2
3.9
34.2_{~3.9}
20.1
2.6
20.1_{~2.6}
35.2
3.8
35.2_{~3.8}
20.2
3.9
20.2_{~3.9}
21.4
1.1
21.4_{~1.1}
18.7
1.2
18.7_{~1.2}
DeepSeek-LLM
7B
19.9
4.5
\textbf{19.9}_{~4.5}
9.0
2.3
\ \ \textbf{9.0}_{~2.3}
4.1
1.0
\ \ 4.1_{~1.0}
2.4
0.3
2.4_{~0.3}
1.8
0.8
\ \ 1.8_{~0.8}
0.4
0.5
\ \ 0.4_{~0.5}
1.7
0.5
\ \ 1.7_{~0.5}
0.5
0.7
\ \ 0.5_{~0.7}
9.7
2.0
9.7_{~2.0}
1.9
0.3
\ \ 1.9_{~0.3}
DeepSeek-R1
8B
71.5
1.8
\textbf{71.5}_{~1.8}
51.4
3.8
\textbf{51.4}_{~3.8}
25.6
2.3
25.6_{~2.3}
19.1
2.5
19.1_{~2.5}
27.4
4.2
27.4_{~4.2}
17.9
2.2
17.9_{~2.2}
7.4
1.9
\ \ 7.4_{~1.9}
6.8
2.3
\ \ 6.8_{~2.3}
16.3
3.9
16.3_{~3.9}
15.2
4.3
15.2_{~4.3}
Llama3-Groq
8B
79.6
3.4
\textbf{79.6}_{~3.4}
49.0
5.1
\textbf{49.0}_{~5.1}
24.4
1.9
24.4_{~1.9}
19.4
2.2
19.4_{~2.2}
8.9
1.2
\ \ 8.9_{~1.2}
7.1
1.0
\ \ 7.1_{~1.0}
8.5
2.5
\ \ 8.5_{~2.5}
5.6
1.5
\ \ 5.6_{~1.5}
12.4
3.0
12.4_{~3.0}
11.8
3.4
11.8_{~3.4}
a
a
footnotetext:
The model Deepseek-R1 with 8B parameters stands for DeepSeek-R1-Distill-Llama-8B.
b
b
footnotetext:
The two accuracy rates, Acc.F and Acc.P are the average results of repeat evaluation experiments with the standard deviation attached as a corner mark.
c
c
footnotetext:
The subscript of each accuracy rate indicates the standard deviation over five measurements.
d
d
footnotetext:
Bolded
entries denote the highest accuracy rates, and
underlined
entries denote the second-highest.
e
e
footnotetext:
In the multi-turn category, more weight is put on the later queries and thus its accuracy, or score, is more suitable, reflecting more authentic performance on multi-stage tasks.
Table 1
:
Overall results of experiments.
The tool calling performance on three categories of different LLMs and agents are measured by two accuracy metrics. CoT, LoT, and ReAct are baseline methods, and DrugPilot is combined with SFT and pre-trained LLMs.
References
Liu et al. (2024)
Liu, M.,
Li, C.,
Chen, R.,
Cao, D.,
Zeng, X.:
Geometric deep learning for drug discovery.
Expert Systems with Applications
240
,
122498
(2024)
Catacutan et al. (2024)
Catacutan, D.B.,
Alexander, J.,
Arnold, A.,
Stokes, J.M.:
Machine learning in preclinical drug discovery.
Nature Chemical Biology
20
(8),
960–973
(2024)
Ivanenkov et al. (2023)
Ivanenkov, Y.A.,
Polykovskiy, D.,
Bezrukov, D.,
Zagribelnyy, B.,
Aladinskiy, V.,
et al.
:
Chemistry42: an ai-driven platform for molecular design and optimization.
Journal of chemical information and modeling
63
(3),
695–701
(2023)
Yang et al. (2024)
Yang, K.,
Xie, Z.,
Li, Z.,
Qian, X.,
Sun, N.,
et al.
:
Molprophet: a one-stop, general purpose, and ai-based platform for the early stages of drug discovery.
Journal of Chemical Information and Modeling
64
(8),
2941–2947
(2024)
Shen et al. (2024)
Shen, C.,
Song, J.,
Hsieh, C.-Y.,
Cao, D.,
Kang, Y.,
et al.
:
Drugflow: an ai-driven one-stop platform for innovative drug discovery.
Journal of Chemical Information and Modeling
64
(14),
5381–5391
(2024)
Chakraborty et al. (2025)
Chakraborty, C.,
Bhattacharya, M.,
Pal, S.,
Chatterjee, S.,
Das, A.,
et al.
:
Ai-enabled language models (lms) to large language models (llms) and multimodal large language models (mllms) in drug discovery and development.
Journal of Advanced Research
(2025)
https://doi.org/10.1016/j.jare.2025.02.011
Ye et al. (2025)
Ye, G.,
Cai, X.,
Lai, H.,
Wang, X.,
Huang, J.,
et al.
:
Drugassist: a large language model for molecule optimization.
Briefings in Bioinformatics
26
(1),
693
(2025)
AbuNasser et al. (2024)
AbuNasser, R.J.,
Ali, M.Z.,
Jararweh, Y.,
Daraghmeh, M.,
Ali, T.Z.:
Large language models in drug discovery: A comprehensive analysis of drug-target interaction prediction.
In: 2024 2nd International Conference on Foundation and Large Language Models (FLLM),
pp. 417–431
(2024).
https://doi.org/10.1109/FLLM63129.2024.10852448
Liu et al. (2024)
Liu, S.,
Lu, Y.,
Chen, S.,
Hu, X.,
Zhao, J.,
et al.
:
Drugagent: Automating ai-aided drug discovery programming through llm multi-agent collaboration.
In: 2nd AI4Research Workshop: Towards a Knowledge-grounded Scientific Research Lifecycle
(2024)
Inoue et al. (2025)
Inoue, Y.,
Song, T.,
Wang, X.,
Luna, A.,
Fu, T.:
Drugagent: Multi-agent large language model-based reasoning for drug-target interaction prediction.
In: ICLR 2025 Workshop on Machine Learning for Genomics Explorations
(2025).
https://openreview.net/forum?id=QcujughqCJ
Zheng et al. (2025)
Zheng, Y.,
Koh, H.Y.,
Ju, J.,
Nguyen, A.T.N.,
May, L.T.,
Webb, G.I.,
Pan, S.:
Large language models for scientific discovery in molecular property prediction.
Nature Machine Intelligence
7
(3),
437–447
(2025)
de Thé et al. (2023)
Thé, F.-X.B.,
Baudier, C.,
Pereira, R.A.,
Lefebvre, C.,
Moingeon, P.,
et al.
:
Transforming drug discovery with a high-throughput ai-powered platform: A 5-year experience with patrimony.
Drug Discovery Today
28
(11),
103772
(2023)
Tiwari et al. (2023)
Tiwari, P.C.,
Pal, R.,
Chaudhary, M.J.,
Nath, R.:
Artificial intelligence revolutionizing drug development: Exploring opportunities and challenges.
Drug Development Research
84
(8),
1652–1663
(2023)
Lorente et al. (2025)
Lorente, J.S.,
Sokolov, A.V.,
Ferguson, G.,
Schiöth, H.B.,
Hauser, A.S., et al.:
Gpcr drug discovery: new agents, targets and indications.
Nature Reviews Drug Discovery,
1–22
(2025)
Du et al. (2024)
Du, Y.,
Jamasb, A.R.,
Guo, J.,
Fu, T.,
Harris, C.,
et al.
:
Machine learning-aided generative molecular design.
Nature Machine Intelligence
6
(6),
589–604
(2024)
Wu et al. (2024)
Wu, H.,
Liu, J.,
Jiang, T.,
Zou, Q.,
Qi, S.,
et al.
:
Attentionmgt-dta: A multi-modal drug-target affinity prediction using graph transformer and attention mechanism.
Neural Networks
169
,
623–636
(2024)
Chen et al. (2025)
Chen, M.,
Wu, J.,
Pan, S.,
Lin, F.,
Du, B., et al.:
Knowledge-aware contrastive heterogeneous molecular graph learning.
arXiv preprint arXiv:2502.11711
(2025)
Li et al. (2025)
Li, K.,
Hu, L.,
Cai, X.,
Wu, J.,
Hu, W.:
Can molecular evolution mechanism enhance molecular representation?
arXiv preprint arXiv:2501.15799
(2025)
Sadybekov and Katritch (2023)
Sadybekov, A.V.,
Katritch, V.:
Computational approaches streamlining drug discovery.
Nature
616
(7958),
673–685
(2023)
Mak and Pichika (2019)
Mak, K.-K.,
Pichika, M.R.:
Artificial intelligence in drug development: present status and future prospects.
Drug discovery today
24
(3),
773–780
(2019)
Niazi and Mariam (2023)
Niazi, S.K.,
Mariam, Z.:
Computer-aided drug design and drug discovery: a prospective analysis.
Pharmaceuticals
17
(1),
22
(2023)
Chen et al. (2021)
Chen, Z.,
Liu, X.,
Hogan, W.,
Shenkman, E.,
Bian, J.:
Applications of artificial intelligence in drug development using real-world data.
Drug discovery today
26
(5),
1256–1264
(2021)
Zhavoronkov et al. (2019)
Zhavoronkov, A.,
Ivanenkov, Y.A.,
Aliper, A.,
Veselov, M.S.,
Aladinskiy, V.A.,
et al.
:
Deep learning enables rapid identification of potent ddr1 kinase inhibitors.
Nature biotechnology
37
(9),
1038–1040
(2019)
Stokes et al. (2020)
Stokes, J.M.,
Yang, K.,
Swanson, K.,
Jin, W.,
Cubillos-Ruiz, A.,
et al.
:
A deep learning approach to antibiotic discovery.
Cell
180
(4),
688–702
(2020)
Ren et al. (2025)
Ren, F.,
Aliper, A.,
Chen, J.,
Zhao, H.,
Rao, S.,
et al.
:
A small-molecule tnik inhibitor targets fibrosis in preclinical and clinical models.
Nature Biotechnology
43
(1),
63–75
(2025)
Zhang et al. (2025)
Zhang, K.,
Yang, X.,
Wang, Y.,
Yu, Y.,
Huang, N., et al.:
Artificial intelligence in drug development.
Nature Medicine,
1–15
(2025)
Yao et al. (2023)
Yao, S.,
Zhao, J.,
Yu, D.,
Du, N.,
Shafran, I.,
et al.
:
React: Synergizing reasoning and acting in language models.
In: The Eleventh International Conference on Learning Representations
(2023)
Wei et al. (2022)
Wei, J.,
Wang, X.,
Schuurmans, D.,
Bosma, M.,
Xia, F.,
et al.
:
Chain-of-thought prompting elicits reasoning in large language models.
Advances in neural information processing systems
35
,
24824–24837
(2022)
Liu et al. (2024)
Liu, T.,
Xu, W.,
Huang, W.,
Zeng, Y.,
Wang, J., et al.:
Logic-of-thought: Injecting logic into contexts for full reasoning in large language models.
arXiv preprint arXiv:2409.17539
(2024)
Vavekanand and Sam (2024)
Vavekanand, R.,
Sam, K.:
Llama 3.1: An in-depth analysis of the next-generation large language model.
ResearchGate
(2024)
Dubey et al. (2024)
Dubey, A.,
Jauhri, A.,
Pandey, A.,
Kadian, A.,
Al-Dahle, A., et al.:
The llama 3 herd of models.
CoRR
abs/2407.21783
(2024)
https://doi.org/10.48550/ARXIV.2407.21783
2407.21783
Sreenivas et al. (2024)
Sreenivas, S.T.,
Muralidharan, S.,
Joshi, R.,
Chochowski, M.,
Mahabaleshwarkar, A.S., et al.:
Llm pruning and distillation in practice: The minitron approach.
arXiv preprint arXiv:2408.11796
(2024)
Team et al. (2024)
Team, G.,
Riviere, M.,
Pathak, S.,
Sessa, P.G.,
Hardin, C., et al.:
Gemma 2: Improving open language models at a practical size.
arXiv preprint arXiv:2408.00118
(2024)
Yang et al. (2024)
Yang, A.,
Yang, B.,
Hui, B.,
Zheng, B.,
Yu, B., et al.:
Qwen2 technical report.
CoRR
abs/2407.10671
(2024)
https://doi.org/10.48550/ARXIV.2407.10671
2407.10671
OpenAI et al. (2024)
OpenAI,
Hurst, A.,
Lerer, A.,
Goucher, A.P.,
Perelman, A., et al.:
Gpt-4o: A multimodal large language model.
arXiv
(2024)
Yang et al. (2012)
Yang, W.,
Soares, J.,
Greninger, P.,
Edelman, E.J.,
Lightfoot, H.,
et al.
:
Genomics of drug sensitivity in cancer (gdsc): a resource for therapeutic biomarker discovery in cancer cells.
Nucleic acids research
41
(D1),
955–961
(2012)
Wu et al. (2018)
Wu, Z.,
Ramsundar, B.,
Feinberg, E.N.,
Gomes, J.,
Geniesse, C.,
Pappu, A.S.,
Leswing, K.,
Pande, V.:
Moleculenet: A benchmark for molecular machine learning.
Chemical Science
9
(2),
513–530
(2018)
https://doi.org/10.1039/C7SC02664A
Li et al. (2024)
Li, K.,
Gong, X.,
Wu, J.,
Hu, W.:
Contrastive learning drug response models from natural language supervision.
In: Larson, K. (ed.)
Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24,
pp. 2126–2134.
International Joint Conferences on Artificial Intelligence Organization
(2024).
https://doi.org/10.24963/ijcai.2024/235
.
Main Track.
https://doi.org/10.24963/ijcai.2024/235
Chen et al. (2025)
Chen, M.,
Wu, J.,
Pan, S.,
Lin, F.,
Du, B.,
Gong, X.,
Hu, W.:
Knowledge-aware contrastive heterogeneous molecular graph learning.
PLoS Computational Biology
21
(5),
1013008
(2025)
https://doi.org/10.1371/journal.pcbi.1013008
Davis et al. (2011)
Davis, M.I.,
Hunt, J.P.,
Herrgard, S.,
Ciceri, P.,
Wodicka, L.M.,
et al.
:
Comprehensive analysis of kinase inhibitor selectivity.
Nature biotechnology
29
(11),
1046–1051
(2011)
Tang et al. (2014)
Tang, J.,
Szwajda, A.,
Shakyawar, S.,
Xu, T.,
Hintsanen, P.,
et al.
:
Making sense of large-scale kinase inhibitor bioactivity data sets: a comparative and integrative analysis.
Journal of chemical information and modeling
54
(3),
735–743
(2014)
Liu et al. (2007)
Liu, T.,
Lin, Y.,
Wen, X.,
Jorissen, R.N.,
Gilson, M.K.:
Bindingdb: a web-accessible database of experimentally determined protein–ligand binding affinities.
Nucleic acids research
35
(suppl_1),
198–201
(2007)
Wishart et al. (2018)
Wishart, D.S.,
Feunang, Y.D.,
Guo, A.C.,
Lo, E.J.,
Marcu, A.,
et al.
:
Drugbank 5.0: a major update to the drugbank database for 2018.
Nucleic acids research
46
(D1),
1074–1082
(2018)
Zitnik et al. (2018)
Zitnik, M.,
Agrawal, M.,
Leskovec, J.:
Modeling polypharmacy side effects with graph convolutional networks.
Bioinformatics
34
(13),
457–466
(2018)
Sterling and Irwin (2015)
Sterling, T.,
Irwin, J.J.:
Zinc 15–ligand discovery for everyone.
Journal of chemical information and modeling
55
(11),
2324–2337
(2015)
Ramakrishnan et al. (2014)
Ramakrishnan, R.,
Dral, P.O.,
Rupp, M.,
Von Lilienfeld, O.A.:
Quantum chemistry structures and properties of 134 kilo molecules.
Scientific data
1
(1),
1–7
(2014)
Ruddigkeit et al. (2012)
Ruddigkeit, L.,
Van Deursen, R.,
Blum, L.C.,
Reymond, J.-L.:
Enumeration of 166 billion organic small molecules in the chemical universe database gdb-17.
Journal of chemical information and modeling
52
(11),
2864–2875
(2012)
Suzgun et al. (2023)
Suzgun, M.,
Melas-Kyriazi, L.,
Sarkar, S.,
Kominers, S.D.,
Shieber, S.:
The harvard uspto patent dataset: A large-scale, well-structured, and multi-purpose corpus of patent applications.
Advances in neural information processing systems
36
,
57908–57946
(2023)
Ye et al. (2025)
Ye, G.,
Cai, X.,
Lai, H.,
Wang, X.,
Huang, J.,
et al.
:
Drugassist: A large language model for molecule optimization.
Briefings in Bioinformatics
26
(1),
693
(2025)
Liu et al. (2024)
Liu, Y.,
Ding, S.,
Zhou, S.,
Fan, W.,
Tan, Q.:
Moleculargpt: Open large language model (llm) for few-shot molecular property prediction.
arXiv preprint arXiv:2406.12950
(2024)
Talevi (2023)
Talevi, A.:
Computer-aided drug discovery and design: recent advances and future prospects.
Computational Drug Discovery and Design,
1–20
(2023)
Morgnanesi et al. (2015)
Morgnanesi, D.,
Heinrichs, E.J.,
Mele, A.R.,
Wilkinson, S.,
Zhou, S.,
et al.
:
A computational chemistry perspective on the current status and future direction of hepatitis b antiviral drug discovery.
Antiviral research
123
,
204–215
(2015)
Paul et al. (2010)
Paul, S.M.,
Mytelka, D.S.,
Dunwiddie, C.T.,
Persinger, C.C.,
Munos, B.H.,
et al.
:
How to improve r&d productivity: the pharmaceutical industry’s grand challenge.
Nature reviews Drug discovery
9
(3),
203–214
(2010)
Zhou et al. (2024)
Zhou, H.,
Zhou, F.,
Zhao, C.,
Xu, Y.,
Luo, L., et al.:
Multimodal data integration for precision oncology: Challenges and future directions.
arXiv preprint arXiv:2406.19611
(2024)
Yao et al. (2023)
Yao, S.,
Yu, D.,
Zhao, J.,
Shafran, I.,
Griffiths, T.,
et al.
:
Tree of thoughts: Deliberate problem solving with large language models.
Advances in neural information processing systems
36
,
11809–11822
(2023)
Holstein (2024)
Holstein, J.:
Bridging domain expertise and ai through data understanding.
In: Companion Proceedings of the 29th International Conference on Intelligent User Interfaces,
pp. 163–165
(2024)
Zhu (2020)
Zhu, H.:
Big data and artificial intelligence modeling for drug discovery.
Annual review of pharmacology and toxicology
60
(1),
573–589
(2020)
Patil et al. (2024)
Patil, S.G.,
Zhang, T.,
Wang, X.,
Gonzalez, J.E.:
Gorilla: Large language model connected with massive apis.
Advances in Neural Information Processing Systems
37
,
126544–126565
(2024)
Hu et al. (2021)
Hu, E.J.,
Shen, Y.,
Wallis, P.,
Allen-Zhu, Z.,
Li, Y., et al.:
Lora: Low-rank adaptation of large language models.
arXiv preprint arXiv:2106.09685
(2021)
Bi et al. (2024)
Bi, X.,
Chen, D.,
Chen, G.,
Chen, S.,
Dai, D., et al.:
Deepseek LLM: scaling open-source language models with longtermism.
CoRR
abs/2401.02954
(2024)
https://doi.org/10.48550/ARXIV.2401.02954
2401.02954
DeepSeek-AI et al. (2025)
DeepSeek-AI,
Guo, D.,
Yang, D.,
Zhang, H.,
Song, J., et al.:
Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
CoRR
abs/2501.12948
(2025)
https://doi.org/10.48550/ARXIV.2501.12948
2501.12948
1
Memory Pool Prompt
Figure 7
:
Memory pool prompt.
To help LLMs better understand the PMP in DrugPilot, we have incorporated a memory pool prompt into the system prompt. The full memory pool prompt is shown in Fig.
7
.
The memory pool prompt first clarifies the existence of PMP and the responsibilities of the LLMs, namely the correct transmission of parameters to the tools. It then defines the input format received by the LLMs, comprising two parts: the user’s question or the tool’s output, and a description of the current state of PMP, which includes the list of currently stored keys. LLMs can select a key from this pool and map it to its corresponding value. It then explains in detail how the LLMs should interact with PMP. First, it defines scenarios where PMP should not be used: if the required parameters are already present in the question, the LLMs should extract them directly. Next, it specifies when and how to use PMP: if the question lacks the necessary parameters, the LLMs must retrieve the corresponding key from the memory pool and enclose it in parentheses to indicate retrieval. Finally, the prompt provides both a correct and an incorrect example, demonstrating proper memory pool usage and helping LLMs avoid retrieving non-existent keys, thereby mitigating hallucination.
2
DrugPilot’s Reasoning Errors
In tool calling, LLMs are required to generate an action input in JSON format, containing the tool name to be called and required parameters. And in actual tasks, there will be frequent interactions with PMP. Therefore, problems will inevitably arise both in content and format. Based on the real output of LLMs, we summarized the common reasoning errors as shown in Fig.
8
.
Figure 8
:
Common reasoning errors of LLMs. The common types of reasoning errors when LLMs call drug-related tools, and the Fe-Fo mechanism will provide feedback to LLMs regarding these issues.
3
Fine-Tuning Configuration
We conducted LoRA fine-tuning on the LLMs used in DrugPilot to enhance their domain knowledge in drug discovery and improve their ability to call drug-related tools. Batch size of 4 was used for smaller models, and 8 for larger ones. We deployed the final inference-stage LLMs on the Ollama
1
1
1
https://github.com/ollama/ollama
.
platform. The hyperparameter settings used during the fine-tuning process are detailed in Table
2
.
Hyperparameter
Value / Strategy
Batch size
4-8
Cutoff length
1024
Optimizer
AdamW
Initial learning rate
5e-5
Learning rate scheduler
Cosine decay
Precision
BF16
Number of epochs
3
Deployment platform
Ollama
Table 2
:
Hyperparameter Settings for Fine-tuning
4
Accuracy Calculation
Acc.F and Acc.P represent the accuracy of tool selection and parameter extraction, and they are defined by:
A
​
c
​
c
.
F
=
1
N
c
​
∑
i
=
1
N
c
F
⁡
(
s
​
a
​
m
​
p
​
l
​
e
i
)
\displaystyle Acc.F=\frac{1}{N_{c}}\sum_{i=1}^{N_{c}}F(sample_{i})
A
​
c
​
c
.
P
=
1
N
c
​
∑
i
=
1
N
c
P
⁡
(
s
​
a
​
m
​
p
​
l
​
e
i
)
\displaystyle Acc.P=\frac{1}{N_{c}}\sum_{i=1}^{N_{c}}P(sample_{i})
where
N
c
N_{c}
is the number of samples in a category,
F
⁡
(
⋅
)
F(\cdot)
and
P
⁡
(
⋅
)
P(\cdot)
are indicator functions denote whether the current sample has correctly selected the function and extracted the parameters.