TxAgent: An AI Agent for Therapeutic Reasoning
      Across a Universe of Tools
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2503.10970v1 [cs.AI] 14 Mar 2025
TxAgent: An AI Agent for Therapeutic Reasoning
Across a Universe of Tools
Shanghua Gao
1
Richard Zhu
1
Zhenglun Kong
1
Ayush Noori
1
Xiaorui Su
1
Curtis Ginder
1,2
Theodoros Tsiligkaridis
3
and Marinka Zitnik
1,4,5,6,‡
1
Department of Biomedical Informatics, Harvard Medical School, Boston, MA
2
Cardiovascular Division, Department of Medicine, Brigham and Women’s Hospital, Harvard Medical School, Boston, MA
3
MIT Lincoln Laboratory, Lexington, MA
4
Kempner Institute for the Study of Natural and Artificial Intelligence, Harvard University, Cambridge, MA
5
Broad Institute of MIT and Harvard, Cambridge, MA
6
Harvard Data Science Initiative, Cambridge, MA
‡
{\ddagger}
Corresponding author. Email: marinka@hms.harvard.edu
TxAgent
project is at
https://zitniklab.hms.harvard.edu/TxAgent
TxAgent
code and demos are at
https://github.com/mims-harvard/TxAgent
ToolUniverse
is at
https://github.com/mims-harvard/ToolUniverse
Abstract
Precision therapeutics require multimodal adaptive models that generate personalized treatment recommendations. We introduce
TxAgent
, an AI agent that leverages multi-step reasoning and real-time biomedical knowledge retrieval across a toolbox of 211 tools to analyze drug interactions, contraindications, and patient-specific treatment strategies.
TxAgent
evaluates how drugs interact at molecular, pharmacokinetic, and clinical levels, identifies contraindications based on patient comorbidities and concurrent medications, and tailors treatment strategies to individual patient characteristics, including age, genetic factors, and disease progression.
TxAgent
retrieves and synthesizes evidence from multiple biomedical sources, assesses interactions between drugs and patient conditions, and refines treatment recommendations through iterative reasoning. It selects tools based on task objectives and executes structured function calls to solve therapeutic tasks that require clinical reasoning and cross-source validation. The
ToolUniverse
consolidates 211 tools from trusted sources, including all US FDA-approved drugs since 1939 and validated clinical insights from Open Targets.
TxAgent
outperforms leading LLMs, tool-use models, and reasoning agents across five new benchmarks: DrugPC, BrandPC, GenericPC, TreatmentPC, and DescriptionPC, covering 3,168 drug reasoning tasks and 456 personalized treatment scenarios. It achieves 92.1% accuracy in open-ended drug reasoning tasks, surpassing GPT-4o by up to 25.8% and outperforming DeepSeek-R1 (671B) in structured multi-step reasoning.
TxAgent
generalizes across drug name variants and descriptions, maintaining a variance of
<
<
0.01 between brand, generic, and description-based drug references, exceeding existing tool-use LLMs by over 55%.
By integrating multi-step inference, real-time knowledge grounding, and tool-assisted decision-making,
TxAgent
ensures that treatment recommendations align with established clinical guidelines and real-world evidence, reducing the risk of adverse events and improving therapeutic decision-making.
\spacing
1.15
\spacing
1.38
Main
Precision therapy personalizes treatments based on individual patient conditions to maximize efficacy and minimize risks. Prescribing the appropriate drug requires evaluating multiple factors, including patient-specific characteristics, comorbidities, drug interactions, contraindications, current clinical guidelines, drug mechanisms of action, and the underlying biology of the disease
[
1
]
.
Large language models (LLMs) can process therapeutic tasks by large-scale pretraining
[
2
,
3
,
4
,
5
,
6
]
followed by fine-tuning on medical data
[
7
,
8
,
9
]
. While LLMs generate fluent, contextually relevant responses, they lack real-time access to updated biomedical knowledge, frequently hallucinate, and cannot reliably reason over multiple clinical variables. Retraining these models with new medical insights is computationally expensive and impractical due to catastrophic forgetting. Furthermore, LLMs absorb large volumes of open-net data, which may contain unverified or deliberately misleading medical information
[
10
]
.
Tool-augmented LLMs
[
11
,
12
,
13
]
incorporate external knowledge retrieval mechanisms, such as retrieval-augmented generation (RAG)
[
14
]
, to mitigate these issues. These models retrieve drug and disease information from external sources but cannot execute multi-step reasoning required for treatment selection. Precision therapy could benefit from iterative reasoning, where models could retrieve information from verified sources, evaluate interactions, and dynamically refine treatment plans.
We introduce
TxAgent
, an AI agent
[
15
,
16
,
17
,
18
,
19
]
that delivers evidence-grounded treatment recommendations by combining multi-step reasoning with real-time biomedical tool integration.
TxAgent
generates natural language responses alongside a transparent reasoning trace, detailing each step of its decision-making process. It executes goal-driven tool selection, calling external databases and specialized machine learning (ML) models to ensure accuracy. To support complex medical queries,
TxAgent
leverages
ToolUniverse
, a biomedical toolbox consolidating 211 expert-curated tools, spanning drug mechanisms, interactions, clinical guidelines, and disease annotations. These tools integrate trusted sources, including openFDA
[
20
]
, Open Targets
[
21
]
, and the Human Phenotype Ontology
[
22
]
.
TxAgent
further employs
ToolRAG
model, an ML-based retrieval system that dynamically selects the most relevant tools from
ToolUniverse
based on query context.
TxAgent
consists of: (1)
ToolUniverse
, a diverse collection of 211 biomedical tools, (2) a specialized LLM fine-tuned for multi-step reasoning and tool execution, and (3)
ToolRAG
model, an adaptive tool retrieval model. To construct tools compatible with
TxAgent
, we introduce
ToolGen
, a multi-agent tool construction system that generates tools from API documentation.
TxAgent
is fine-tuned using
TxAgent-Instruct
, a dataset of 378,027 instruction-tuning samples that is derived from 85,340 multi-step reasoning traces and encompasses 177,626 reasoning steps and 281,695 function calls. The dataset is generated using
QuestionGen
and
TraceGen
, multi-agent systems that construct diverse therapeutic queries and generate stepwise reasoning traces that cover treatment and drug information in FDA labels since 1939.
We introduce five new benchmarks (DrugPC, BrandPC, GenericPC, DescriptionPC, TreatmentPC, Table
1
). These benchmarks comprehensively assess drug selection, treatment personalization, and reasoning robustness across structured and unstructured queries.
TxAgent
outperforms larger LLMs and existing tool-use models across all five benchmarks, achieving state-of-the-art performance in open-ended drug reasoning and patient-specific therapeutic decision-making. On the DrugPC benchmark, which evaluates 11 common drug reasoning tasks,
TxAgent
attains 92.1% accuracy in the open-ended setting, where the model generates answers without predefined choices. This performance surpasses GPT-4o
[
23
]
, the strongest closed-weight reference model, by 25.8% (GPT-4o: 66.3%) and outperforms Llama-3.1-70B-Instruct
[
2
]
, a model nearly 9× larger, by 39.3% (Llama-3.1-70B-Instruct: 52.8%).
TxAgent
, based on the fine-tuned 8-billion parameter Llama-3.1-8B-Instruct model
[
2
]
, delivers superior accuracy while maintaining computational efficiency. Compared to tool-use LLMs with function-calling capabilities, such as ToolACE and WattTool
[
12
,
13
]
,
TxAgent
significantly outperforms both models in open-ended drug reasoning tasks. Unlike existing tool-augmented LLMs, which struggle with multi-step tool selection and iterative reasoning,
TxAgent
dynamically retrieves and synthesizes knowledge from 211 biomedical tools, achieving more accurate and context-aware therapeutic decisions.
Beyond drug reasoning,
TxAgent
generalizes across drug name variants and descriptions, overcoming a key limitation of LLM-based methods
[
24
,
25
]
. Many models exhibit high variance when drugs are referenced by brand names, generic names, or detailed descriptions
[
24
]
. In contrast,
TxAgent
achieves an exceptionally low accuracy variance of
<
<
0.01 across these variations, whereas GPT-4o exhibits a variance of 9.96, indicating a much higher sensitivity to representation shifts. On DescriptionPC, a benchmark that evaluates drug reasoning when drug names are replaced with descriptive narratives,
TxAgent
attains 56.5% accuracy, outperforming GPT-4o by 8.3% and indicating
TxAgent
’s robustness to infer drug identities from contextual clues.
TxAgent
also excels in personalized treatment recommendations, where it evaluates patient-specific drug selection. On TreatmentPC, which assesses 456 real-world treatment scenarios,
TxAgent
outperforms GPT-4o by 13.6% and Llama-3.1-70B-Instruct by 25.4% in the open-ended setting, establishing its superiority in personalized medicine. Compared to DeepSeek-R1
[
26
]
, a 671-billion parameter model optimized for multi-step reasoning,
TxAgent
achieves 7.5% higher accuracy in open-ended queries, demonstrating that specialized reasoning and tool-use capabilities outweigh model size.
We conduct ablation studies to evaluate
TxAgent
’s toolbox size, tool dependency, and reasoning process. Increasing the number of tools in
ToolUniverse
improves performance, demonstrating that access to external biomedical tools improves therapeutic reasoning. We compare real-world tool usage to an LLM acting as a tool substitute and find that tool-assisted decision-making consistently outperforms LLM-only reasoning, highlighting the need for grounding AI agents in continually updated and verified therapeutic knowledge. We also examine the impact of explicit reasoning steps before function calls and show that structured reasoning improves performance more than multi-round function calls alone. Finally, we analyze the effect of multi-step training traces and find that increasing the number of reasoning steps in fine-tuning and inference significantly improves
TxAgent
’s ability to handle complex drug reasoning and treatment selection.
Results
TxAgent
: Multi-step therapeutic reasoning with a universe of tools
TxAgent
uses multi-step, white-box reasoning and tool-use for solving precision treatment problems (Figure
a). Using a wide array of tools that connect to verified knowledge bases, such as FDA-approved drug labels and the Open Targets
[
20
,
21
]
, as well as machine learning tools for special purposes such as tool retrieval (Figure
b),
TxAgent
performs detailed reasoning on drugs, diseases, and patient populations. This ability to leverage a vast array of biomedical tools ensures
TxAgent
is not limited by the internal knowledge of LLMs, enabling it to generate accurate and reliable answers with transparent reasoning traces. It can handle a variety of patient scenarios, from specific patient populations and complex medical histories to polypharmacy and individual-specific genetic variants.
TxAgent
uses
ToolUniverse
, which is a generalizable toolbox with 211 tools that support real-time retrieval of knowledge from verified data sources, including openFDA
[
20
]
, Open Targets
[
21
]
, and the Human Phenotype Ontology from the Monarch Initiative
[
22
]
. These tools address diverse aspects of drugs and diseases, such as drug indications and usage (Figure
c).
TxAgent
is an LLM trained to use tools. This is achieved by building three training datasets (a tooling dataset, a comprehensive therapeutic question dataset, and a reasoning trace dataset), which we create using three auxiliary agent systems (Figure
a). Given these datasets, we instruction-tune an LLM
[
2
]
to achieve multiple capabilities, including multi-step reasoning and tool call argument generation. For each step in the multi-step reasoning process,
TxAgent
receives either a therapeutic question or tool feedback from the previous round. Based on this input,
TxAgent
generates a language-based thought process and invokes calls to tools. During the reasoning process, to identify and utilize relevant tools,
TxAgent
invokes the
ToolRAG
model, which selects suitable candidates from
ToolUniverse
based on descriptions provided by
TxAgent
. This iterative process continues until
TxAgent
arrives at a final answer and invokes the
Finish
tool to conclude the reasoning process. The output of
TxAgent
includes both the final answer and a multi-step reasoning trace. Each step of the reasoning trace includes a thought process, function calls to utilize tools, and feedback from those tools.
We show the detailed inference process of
TxAgent
in Online Methods Section
and Algorithm
.
Capabilities of
TxAgent
TxAgent
generates reasoning traces, constructs function call arguments, performs multi-step logical reasoning, and searches for, selects, and invokes tools to solve a therapeutic reasoning task. These capabilities are developed through instruction tuning of the LLM (Online Methods Section
). By applying these capabilities,
TxAgent
retrieves verified biomedical knowledge through tool calls, selects tools based on specific objectives, solves problems through multi-step reasoning, and integrates continuously updated knowledge bases.
Knowledge grounding using tool calls.
Treatment decisions require reliable answers with transparent justifications. LLMs lack inherent mechanisms to verify their predictions, requiring users to assess trustworthiness manually.
TxAgent
addresses this by retrieving verified information from trusted sources through function calls. Instead of generating responses directly,
TxAgent
queries tools to obtain accurate data and formulates answers based on verified outputs. In Figure
f,
TxAgent
determines the dosage of Kisunla (donanemab-azbt), an FDA-approved drug from 2024, which is beyond the training data of its base LLMs.
TxAgent
recognizes the knowledge gap, calls
get_dosage
, and retrieves dosage details from FDA records. It then synthesizes the retrieved information into a response. This approach ensures factual accuracy and transparency, allowing users to verify responses through reasoning traces.
Goal-oriented tool selection.
TxAgent
uses
ToolRAG
model to search for, identify, and apply the most relevant tools. Figure
g shows
TxAgent
retrieving adverse reactions for Alyftrek (vanzacaftor, tezacaftor, deutivacaftor). It recognizes the need for external data, generates function call arguments, and queries
ToolUniverse
. From the returned tools,
TxAgent
selects
get_adverse_reactions
to extract relevant information from FDA drug labels. This process enables
TxAgent
to dynamically integrate new tools rather than relying on static, pre-trained knowledge. By first generating a plan and then selecting appropriate tools,
TxAgent
supports adaptive decision-making.
Multi-step therapeutic reasoning.
TxAgent
applies multi-step reasoning to address complex problems that require integrating multiple sources of information or adapting to incomplete data. Single-step approaches fail when problems demand information from multiple perspectives or when function calls return insufficient results. By iteratively generating reasoning steps and function calls,
TxAgent
refines its analysis until it reaches a well-supported answer. In Figure
h,
TxAgent
identifies protein targets for breast cancer, a task no single
ToolUniverse
tool can complete. Therefore,
TxAgent
first retrieves the disease’s EFO ID using
get_disease_id_desc
, then queries
ToolUniverse
for tools that map diseases to protein targets. From the returned options,
TxAgent
selects
get_associated_targets
and ranks the retrieved proteins by score. This iterative process ensures robust reasoning in cases where direct retrieval is insufficient.
Real-time retrieval from continually updated knowledge sources.
LLMs retain only the knowledge available at the time of training and cannot update dynamically. Retraining models to incorporate new biomedical information is computationally expensive and impractical. Retrieval-augmented generation
[
27
]
mitigates this by querying a precomputed vector database, but maintaining high-quality embeddings for frequent updates is resource-intensive.
TxAgent
addresses this limitation by executing function calls to directly query real-time data sources, such as Open Targets and FDA databases. This approach enables
TxAgent
to retrieve current drug approvals, clinical guidelines, and treatment indications without requiring model retraining. Unlike static vector databases, which require periodic reprocessing,
TxAgent
continuously integrates new information from multiple verified sources. Figure
i illustrates this capability. Bizengri (zenocutuzumab-zbco) was approved by the FDA in December 2024, after the knowledge cutoff of
TxAgent
’s base model, Llama3.1-8B (December 2023). Instead of relying on outdated internal knowledge,
TxAgent
calls the
get_indications
tool to query the openFDA API, retrieving the latest drug label information. This allows
TxAgent
to correctly identify Bizengri’s approved indications for non-small cell lung cancer and pancreatic adenocarcinoma. By integrating continuously updated sources,
TxAgent
ensures access to the latest biomedical knowledge, eliminating reliance on static training data and mitigating knowledge obsolescence.
ToolUniverse
: A universe of tools and machine learning models
ToolUniverse
is a suite of 211 biomedical tools that integrate with
TxAgent
. It covers a wide range of categories (Figure
c), including adverse events, risks, and safety; addiction and abuse; drug usage in specific populations; drug administration and handling; pharmacology; drug mechanisms and composition; ID and labeling tools; general clinical annotations; clinical laboratory information; patient and caregiver resources; pairwise disease, phenotype, target, and drug associations; biological annotation tools; publication information; search tools; and target characterization. Tools in
ToolUniverse
are built on APIs from trusted sources, including openFDA
[
20
]
, Open Targets
[
21
]
, and the Monarch Initiative
[
22
]
. Extended Data Figure
provides a detailed breakdown of
ToolUniverse
tools.
ToolGen
agents generate a dataset of tool specifications used to create
ToolUniverse
.
The
ToolGen
system constructs tools in
ToolUniverse
using a multi-agent approach that converts API documentation into structured tool specifications (Extended Data Figure
a). API documentation varies widely in format and content, making direct integration with
TxAgent
challenging.
ToolGen
standardizes this process by organizing API functions into well-defined tools with clear, concise descriptions that
TxAgent
can interpret. The system operates in four stages:
1.
Capability summarization: The
Summarizer
agent extracts and condenses API documentation to identify the API’s core functionalities.
2.
Tool generation: The
Tool Generator
agent translates these capabilities into structured tool specifications. Each tool specification includes a description for
TxAgent
’s function calls and a mapping rule that converts function calls into API requests. The tool description defines the tool’s name, purpose, input arguments, data types, and mandatory parameters (examples in Figure
b and Extended Data Figure
).
3.
Tool validation: The
Tool Checker
agent generates test cases with predefined queries and function calls to verify the tool’s functionality.
4.
Human verification: Experts manually review and refine tools to ensure correctness, meaningful applications, and robustness to unexpected inputs.
The
Summarizer
,
Tool Generator
, and
Tool Checker
agents operate by prompting the LLM with specialized instructions. Online Methods Section
provides additional details about the
ToolGen
system.
TxAgent-Instruct
dataset of therapeutic tasks and reasoning traces
We construct
TxAgent-Instruct
, a multi-step reasoning and function call training dataset (Figure
d).
TxAgent-Instruct
consists of three datasets: a tooling dataset, a therapeutic question dataset, and a reasoning trace dataset, generated by three agent systems (Extended Data Figure
).
The tooling dataset contains augmented versions of 211 tools from
ToolUniverse
. Each tool description is rephrased to introduce variability, ensuring that
TxAgent
learns tool usage rather than memorizing specific descriptions. The therapeutic question dataset includes 85,340 questions and functional instructions generated by the
QuestionGen
agent system to train
TxAgent
’s reasoning capabilities. The reasoning trace dataset comprises 85,340 detailed reasoning traces that contain 177,626 reasoning steps and 281,695 function calls, all generated by the
TraceGen
agent system.
Processing these three datasets (as detailed in Online Methods Section
) results in
TxAgent-Instruct
, which includes 378,027 instruction-tuning samples. The agent systems generate training data by sampling drugs and disease information from verified biomedical sources. Drug data is obtained from FDA drug labeling documents
[
20
]
, while disease information is sourced from PrimeKG
[
28
]
. Drug-disease, phenotype, and target associations are compiled from Open Targets
[
21
]
.
QuestionGen
agents generate a dataset of therapeutic questions.
QuestionGen
constructs therapeutic questions with treatment, disease, and drug-related information. Training
TxAgent
requires a large dataset of questions that address various forms of therapeutic reasoning, including patient populations, drug side effects, and drug interactions. Manually generating these questions is infeasible. Instead,
QuestionGen
, a multi-agent system, generates meaningful questions from verified knowledge bases (Online Methods Section
, Extended Data Figure
b).
QuestionGen
operates in three stages. First, the
Information Extractor
agent identifies and extracts key information from biomedical documents and data sources. Next, the
Question Generator
agent constructs questions using the extracted information and generates corresponding answers with detailed explanations that clarify how the answer addresses the question. Finally,
QuestionGen
evaluates each question based on knowledge grounding, solvability, and reasonableness. Only validated questions proceed to the
TraceGen
system for reasoning trace generation.
TraceGen
agents generate a dataset of therapeutic reasoning traces.
To generate valid reasoning traces that integrate feedback from real-world tools, we design
TraceGen
, a multi-agent system that constructs complex, step-wise reasoning traces (Extended Data Figure
c).
TraceGen
produces training data for each question, including a reasoning trace and the final answer. Generating reasoning traces presents several challenges:
(1) Complexity of questions: Many questions require multi-step reasoning and the analysis of multiple factors, making it difficult to generate a single direct answer.
TraceGen
must generate reasoning traces that effectively handle this complexity.
(2) Integration of external tools: Effective reasoning requires incorporating real-world tools rather than relying solely on the internal knowledge of LLMs.
TraceGen
must integrate tool outputs into reasoning traces while ensuring consistency across sources.
(3) Handling unpredictable tool outputs: External tools often produce unexpected results.
TraceGen
must manage failure cases, filter noisy outputs, and ensure that reasoning progresses toward a valid solution despite deviations in tool responses.
TraceGen
addresses these challenges using a multi-agent system consisting of the
Helper
agent, the
Tool Provider
module, the
Solver
agents, and a reasoning trace evaluation step (Extended Data Figure
c).
•
The
Helper
agent provides the
Solver
with step-by-step hints, guiding the reasoning process based on previous steps. It has access to correct answers and explanations, ensuring alignment with expected outcomes.
•
The
Tool Provider
module identifies relevant tools based on the question and recommendations from
ToolRAG
model, which iteratively improves tool selection accuracy by learning from previously generated data.
•
The
Solver
agent integrates information from the
Tool Provider
,
Helper
, and existing reasoning traces to iteratively generate reasoning steps and function calls until reaching a final answer.
•
The evaluation step verifies the correctness of the answer, function calls, and reasoning process while detecting hallucinations, arbitrary outputs, and repetitive reasoning patterns.
Details of
TraceGen
are provided in Online Methods Section
.
TxAgent
outperforms larger LLMs in multi-step reasoning
We construct the DrugPC (Drug Prescribing Card) benchmark to evaluate
TxAgent
’s performance in drug reasoning. DrugPC includes 3,168 questions spanning 11 tasks: drug overview, ingredients, warnings and safety, dependence and abuse, dosage and administration, use in specific populations, pharmacology, clinical information, nonclinical toxicology, patient-focused information, and storage and supply.
To mitigate data leakage from pretraining, we focus on drugs approved by the FDA in 2024, reducing the likelihood that LLMs have encountered them.
We exclude drugs approved after 2023 from the training set and use drugs approved in 2024 for evaluation. We perform instruction tuning on LLMs, such as the Llama-3.1-8B-Instruct model with 8 billion parameters, using
TxAgent-Instruct
to develop
TxAgent
’s reasoning and tool-use capabilities. Training details are provided in Online Methods Section
.
We evaluate models in two settings: multiple-choice, where the model selects the correct answer from given options, and open-ended, where the model generates responses without predefined choices. By default,
QuestionGen
generates questions with 4-5 options, verified by human experts. To create open-ended versions, we remove answer choices from the input. After generating a response, the model selects the correct option from the original choices based on its generated text.
Table
provides examples of both formats. Further details on benchmark datasets and evaluation are in Online Methods Section
.
TxAgent
is built on the Llama-3.1-8B-Instruct model, which has 8 billion parameters and is fine-tuned for multi-step reasoning and function call execution. We compare
TxAgent
to larger models, including Llama3.1-70B-Instruct (70 billion parameters) and GPT-4o (Figure
d).
Despite its smaller size,
TxAgent
consistently outperforms Llama3.1-70B-Instruct in both multiple-choice and open-ended tasks. In the multiple-choice setting,
TxAgent
achieves 93.8% accuracy, surpassing Llama3.1-70B-Instruct’s 75.1%. In the open-ended setting,
TxAgent
maintains 92.1% accuracy, while Llama3.1-70B-Instruct drops to 52.8%.
Among baseline models, GPT-4o performs best, achieving 76.4% in multiple-choice and 66.3% in open-ended tasks. However,
TxAgent
outperforms GPT-4o by 17.4% in multiple-choice and 25.8% in open-ended settings. By leveraging multi-step reasoning and executing function calls to
ToolUniverse
for verified information,
TxAgent
surpasses larger models in accuracy and reliability.
The open-ended setting is more challenging than the multiple-choice format, as models cannot rely on answer choices. GPT-4o and Llama3.1-70B-Instruct show accuracy drops of 10.1% and 22.3%, respectively, when switching to open-ended tasks. In contrast,
TxAgent
exhibits only a 1.7% decline, highlighting its robustness in open-ended reasoning.
We evaluate performance across all 11 tasks in the DrugPC benchmark (Figure
b,c). Although GPT-4o is the strongest baseline overall, it does not consistently outperform other models. For example, Llama3.1-70B-Instruct achieves higher accuracy than GPT-4o on the Warning and Safety task. In contrast,
TxAgent
surpasses all baselines in all tasks, demonstrating its effectiveness in multitask drug reasoning.
TxAgent
provides reasoning traces supported by verified function call results, allowing users to assess the reliability of the response. In contrast, LLM-generated outputs require manual verification, limiting trust without external validation.
TxAgent
outperforms tool-use LLMs in multi-step reasoning
We compare
TxAgent
with tool-use LLMs that support function calling
[
12
,
13
,
11
]
(Figure
e). Existing models focus on generating accurate function calls based on input questions and tool descriptions but lack the ability to handle complex problems requiring multi-step function calls, reasoning, and diverse tool integration. By incorporating multi-step reasoning and function call capabilities,
TxAgent
provides key advantages over existing tool-use LLMs: (1) Expanded tool support:
TxAgent
employs goal-oriented tool selection, enabling access to a large number of tools in
ToolUniverse
. In contrast, existing methods rely on including all tool descriptions in the context window, limiting the number of tools they can handle. Some tool-use LLMs
[
29
]
cannot support large-scale toolboxes like
ToolUniverse
. (2) Improved problem-solving:
TxAgent
performs multi-round function calls to address complex problems. When a single function call does not provide sufficient information,
TxAgent
reevaluates and selects alternative tools to refine its solution.
We compare
TxAgent
against state-of-the-art tool-use LLMs, including ToolACE-8B
[
13
]
and WattTool-8B
[
12
]
, both fine-tuned on the same Llama-3.1-8B-Instruct model as
TxAgent
. To ensure a fair comparison, we provide all models with full access to
ToolUniverse
and enable multi-step reasoning. Since existing tool-use LLMs do not natively support multi-step reasoning but allow multi-round interactions, we simulate multi-step reasoning by feeding tool results back as user messages, allowing the LLM to continue function calls until reaching a final answer. Additionally, because most tool-use LLMs struggle with switching between function calls and answer generation, we introduce a special
GiveAnswer
tool. This tool requires the model to invoke it with the final answer once problem-solving is complete, ensuring a structured response process.
TxAgent
achieves significantly higher accuracy than existing tool-use LLMs. In the multiple-choice setting,
TxAgent
outperforms ToolACE by 62.5% and WattTool by 59.1%. In the open-ended setting,
TxAgent
surpasses ToolACE by 59.4% and WattTool by 55.0%. This performance gap arises from key limitations in existing tool-use LLMs: (1) Limited tool selection: These models struggle to handle many tools in a single context window and often fail to select the correct tool from hundreds available in
ToolUniverse
. (2) Single-round function calls: They fill in function arguments based only on the input question, without making additional calls to retrieve missing information. (3) Ineffective multi-step reasoning: Lacking adaptive reasoning, they often repeat initial function calls instead of refining their approach based on previous results, leading to failures when reaching the maximum reasoning round limit.
We quantify these failures by tracking invalid answers—cases where the model cannot produce a valid response. WattTool-8B fails on 58.9% of multiple-choice and 56.6% of open-ended questions. ToolACE-8B fails on 63.1% and 60.7% of multiple-choice and open-ended questions, respectively. In contrast,
TxAgent
employs multi-step reasoning, iterative function calls, and goal-oriented tool selection, allowing it to fully use
ToolUniverse
in therapeutic reasoning.
TxAgent
generalizes across drug name variants and descriptions
We evaluate
TxAgent
’s ability to generalize across different drug representations. LLM-based models are sensitive to variations in how drugs are referenced
[
24
]
, such as brand versus generic names. To test generalization, we construct three modified versions of the DrugPC benchmark: BrandPC, GenericPC, and DescriptionPC.
BrandPC and GenericPC systematically replace drug names in DrugPC with their brand or generic equivalents. Questions that do not reference drug names remain unchanged, while those requiring conversion between brand and generic names are modified accordingly. Both datasets maintain the same number of samples as DrugPC. Sample questions are shown in Figure
a.
DescriptionPC replaces drug names with detailed descriptions to assess generalization without explicit drug names, including indications, mechanisms of action, contraindications, and interactions. We removed DrugPC questions that became unanswerable after this transformation, resulting in 626 questions.
Since multiple drugs may share similar descriptions, DescriptionPC introduces a two-step evaluation: (1) drug identification and (2) answer correctness (Figure
b). In the first step, the model identifies the drug based on its description. The ground truth includes all drugs that could match the given description. In the second step, the model selects the correct answer to a multiple-choice question using its predicted drug name. If drug identification is incorrect, the answer is automatically marked incorrect, ensuring that predictions rely on accurate drug recognition.
TxAgent
achieves 93.6% accuracy on BrandPC and 93.7% on GenericPC, outperforming both pure LLMs and tool-use LLMs on both benchmarks (Figure
a).
Among pure LLMs, Llama3.1-70B-Instruct performs best on BrandPC (73.0%), while GPT-4o leads on GenericPC (77.3%).
TxAgent
surpasses these top reference models by 20.6% and 16.4%, respectively.
Among tool-use LLMs, WattTool-8B achieves the highest accuracy, with 40.2% on BrandPC and 31.5% on GenericPC.
TxAgent
outperforms these baselines by 53.4% and 62.2%, respectively.
TxAgent
also exhibits lower performance variance across the original, BrandPC, and GenericPC datasets, with a variance of 0.00667. In contrast, GPT-4o has a variance of 9.96, Llama3.1-70B-Instruct 2.42, WattTool-8B 13.07, and ToolACE-8B 1.05. These results demonstrate
TxAgent
’s superior robustness and generalization across different drug name representations.
On the DescriptionPC benchmark (Figure
b), when evaluating only answer correctness (without considering whether the model identifies the correct drug)
TxAgent
achieves 90.4%, surpassing GPT-4o (85.9%) and Llama3.1-70B-Instruct (85.3%). However, models may be able to “guess” the answer to certain questions in DescriptionPC without first identifying the class of drugs being referenced, which limits model trustworthiness. Specifically, when requiring both correct drug identification and answer selection, accuracy drops significantly for Llama3.1-70B-Instruct to 20.1%, indicating unreliable drug grounding. In contrast,
TxAgent
maintains the highest performance at 56.5%, outperforming GPT-4o by 8.3%.
For drug name identification alone,
TxAgent
achieves the highest accuracy at 60.1%, compared to GPT-4o’s 55.8% and Llama3.1-70B-Instruct’s 23.6%. These results highlight
TxAgent
’s stronger ability to reason over drugs and base decisions on correct information.
TxAgent
for precision treatment recommendation
We evaluate
TxAgent
’s ability to provide personalized treatment recommendations using the TreatmentPC benchmark, which consists of 456 questions focused on specialized treatment scenarios. While multiple drugs may treat a single disease, patient-specific factors (such as pregnancy or comorbidities) require tailored drug selection and dosage adjustments. TreatmentPC assesses these cases by formulating questions that account for varying drug application conditions. We select drugs approved by the FDA in 2024, identify their indicated diseases, and analyze treatment options by comparing drug attributes. For example, among all available treatments, only one drug may be suitable for pregnant patients. This analysis is based on FDA documentation, including indications, usage in specific populations, safety warnings, precautions, and contraindications.
Using these drug-specific properties, we generate multiple-choice questions with 4-5 options, ensuring only one correct choice based on the patient’s condition. Questions also include scenarios where drug interactions must be considered, requiring the model to account for contraindications. We evaluate models in both multiple-choice and open-ended settings. In the multiple-choice format, the model selects the most appropriate drug from the given options. In the open-ended format, the model generates a treatment recommendation and later selects the correct answer from its own response. TreatmentPC measures
TxAgent
’s ability to analyze patient conditions and recommend appropriate treatments. Further details on the benchmark dataset and evaluation methodology are in Online Methods Section
.
TxAgent
outperforms LLMs and tool-use LLMs in TreatmentPC.
TxAgent
achieves significantly higher accuracy than its fine-tuning base model, Llama-3.1-8B-Instruct (Figure
a). In the multiple-choice setting,
TxAgent
reaches 86.8% accuracy, surpassing Llama-3.1-8B-Instruct’s 56.1%. In the open-ended setting,
TxAgent
attains 75.0%, outperforming Llama-3.1-8B-Instruct’s 33.11%. Compared to larger LLMs,
TxAgent
maintains superior performance. In the multiple-choice setting, it outperforms GPT-4o by 12.7% and Llama-3.1-70B-Instruct by 16.4%. The gap widens in the open-ended setting, where
TxAgent
exceeds GPT-4o by 13.6% and Llama-3.1-70B-Instruct by 25.4%. Even in the open-ended setting,
TxAgent
(75.0%) surpasses GPT-4o’s multiple-choice accuracy (74.1%), despite the latter benefiting from predefined answer choices.
TxAgent
also outperforms tool-use LLMs (Figure
b). ToolACE-8B and WattTool-8B, fine-tuned on the same Llama-3.1-8B-Instruct model and given full access to
ToolUniverse
, perform significantly worse. In the multiple-choice setting, WattTool-8B achieves only 18.2%, while
TxAgent
reaches 86.8%. In the open-ended setting, ToolACE-8B scores 13.4%, compared to
TxAgent
’s 75.0%. As observed in DrugPC,
TxAgent
’s advantage stems from its multi-step reasoning capabilities. It integrates information from multiple sources, executes iterative function calls, refines queries when initial tool calls return empty results, and dynamically adjusts its approach. These strengths enable
TxAgent
to solve complex treatment recommendation tasks more effectively than existing tool-use LLMs.
TxAgent
outperforms reasoning LLMs, including DeepSeek-R1.
Recent reasoning LLMs, such as DeepSeek-R1
[
26
]
and GPT-o1
[
30
]
, are designed for long chain-of-thought reasoning and test-time scaling. Since TreatmentPC requires multi-step reasoning over patient conditions and drug effects, we compare
TxAgent
with DeepSeek-R1 models (Figure
c).
To enable multi-step reasoning in DeepSeek-R1, we explicitly prompt it to generate reasoning steps using special tokens <think> and <\think>. Despite DeepSeek-R1’s full model having 671 billion parameters,
TxAgent
outperforms it by 10.3% in the multiple-choice setting (86.8% vs. 76.5%) and by 7.5% in the open-ended setting.
Extended Data Figure
shows the comparison between Deepseek-R1 and TxAgent.
Deepseek-R1 relies on internal knowledge for reasoning, risking hallucinations and misjudgments.
In contrast, TxAgent bases its reasoning on trusted sources, such as FDA drug labels, minimizing the risk of hallucinations and ensuring more reliable conclusions.
TxAgent
also surpasses distilled variants, including DeepSeek-R1-Llama-8B/70B, which are trained on Llama-3.1-8B and Llama-3.1-70B. Against DeepSeek-R1-Llama-8B, which shares the same base model as
TxAgent
,
TxAgent
achieves accuracy gains of 36.1% in multiple-choice and 34.9% in open-ended tasks.
Unlike reasoning LLMs that rely solely on internal knowledge,
TxAgent
integrates multi-step reasoning with verified external information from
ToolUniverse
, making it more effective for specialized treatment recommendation tasks.
Examples of
TxAgent
reasoning traces for specialized treatments
We present detailed
TxAgent
reasoning traces for four personalized treatment questions, evaluating its ability to incorporate drug mechanisms, drug-drug interactions, comorbidities, and clinical guidelines for specific patient groups, including elderly and pediatric patients.
(1) Treatment selection based on drug mechanism and pediatric use.
Figure
d presents a case of a pediatric male patient with Duchenne muscular dystrophy (DMD) seeking treatment. The patient does not want steroid-based therapies due to side effects, including weight gain and mood changes
[
31
]
, and is ineligible for exon-skipping antisense oligonucleotides, which are effective only for specific genetic mutations
[
32
]
.
TxAgent
must identify an appropriate non-steroidal, non-exon-skipping treatment.
TxAgent
first calls
ToolRAG
model to find tools that identify drugs based on indications. It selects
get_drug_names_by_indication
and retrieves ten DMD drugs. Analyzing the results,
TxAgent
determines that Duvyzat is the only drug meeting the patient’s criteria.
To assess pediatric suitability,
TxAgent
calls
get_drug_name_by_pediatric_use
, but this tool does not return relevant information.
TxAgent
then queries
ToolRAG
model again for tools related to pediatric guidelines and selects
get_pediatric_use_by_drug_name
, which confirms that Duvyzat is safe for children over six years old. Based on this reasoning,
TxAgent
confidently recommends Duvyzat for this patient.
This case study highlights
TxAgent
’s ability to distinguish drugs by mechanism despite similar indications and to integrate mechanistic considerations with personalized factors such as pediatric safety.
(2) Treatment selection considering drug-drug interactions.
Figure
e examines a treatment decision that involves drug-drug interactions. The patient is currently taking Prozac (fluoxetine hydrochloride) for Major Depressive Disorder and is considering adding Xolremdi (mavorixafor) for WHIM syndrome.
TxAgent
assesses whether these medications can be taken together.
TxAgent
first queries
ToolRAG
model for tools related to drug indications and contraindications. It simultaneously calls
get_indications
and
get_contraindications
for Xolremdi. The retrieved data confirm that Xolremdi is indicated for WHIM syndrome but is contraindicated with drugs dependent on CYP2D6 for clearance. Xolremdi inhibits CYP2D6, reducing its enzyme activity and prolonging the presence of drugs metabolized by CYP2D6 in the body.
To determine whether this contraindication applies to Prozac,
TxAgent
calls
get_drug_interactions
, which reveals that Prozac is both a substrate and an inhibitor of CYP2D6. This presents two potential drug-drug interactions: (1) Direct contraindication: Prozac is metabolized by CYP2D6, and since Xolremdi inhibits this enzyme, Prozac exposure would increase, potentially leading to adverse effects. (2) Compounded inhibition: Both Prozac and Xolremdi reduce CYP2D6 activity. Their combined effect could further affect the metabolism of CYP2D6, increasing exposure to other drugs metabolized with CYP2D6.
Based on these interactions,
TxAgent
concludes that taking Prozac and Xolremdi together is not suitable for the patient. This case highlights
TxAgent
’s ability to analyze drug-drug interactions through multi-step reasoning and detailed biological insights retrieved from
ToolUniverse
.
(3) Treatment selection considering geriatric use.
Figure
f examines
TxAgent
’s ability to consider geriatric-specific treatment adjustments. A 70-year-old patient with schizophrenia seeks the maximum recommended dosage for Cobenfy (xanomeline and trospium chloride), a recently approved drug. Since the dosage can be adjusted based on patient response,
TxAgent
must determine the appropriate upper limit and provide justification.
TxAgent
first calls
ToolRAG
model to retrieve relevant dosage- and age-related tools from
ToolUniverse
. It then selects and executes
get_dosage_and_storage_info
and
get_geriatric_use_info
. The dosage tool confirms that the maximum recommended dose for elderly patients is 100 mg/20 mg twice daily, lower than the 125 mg/30 mg twice daily recommended for younger patients. The geriatric use tool explains that this adjustment is due to an increased risk of urinary retention in elderly patients.
TxAgent
synthesizes these findings and provides a final answer with supporting evidence. This case study highlights
TxAgent
’s ability to conduct parallel reasoning threads—both identifying and explaining the maximum dosage—by executing multiple tool calls simultaneously. It also demonstrates how
TxAgent
integrates verified external information to deliver patient-specific, evidence-based treatment recommendations.
(4) Treatment selection considering comorbidities.
Figure
g demonstrates
TxAgent
’s ability to incorporate comorbidities into treatment recommendations. The patient has two cardiac conditions: second-degree AV block, which disrupts electrical signaling in the heart, and hypertension.
TxAgent
is tasked with identifying an appropriate hypertension treatment while considering the AV block.
TxAgent
first retrieves indication-related tools using
ToolRAG
model. It calls
get_drug_names_by_indication
to identify ten potential hypertension treatments. Next, it filters these candidates based on contraindications for AV block. Using
get_drug_name_by_contraindication
with the argument “AV block,”
TxAgent
searches FDA-approved drug labels for contraindications. The results show that two of the retrieved hypertension drugs are contraindicated for patients with second-degree AV block.
TxAgent
then summarizes the mechanisms of the non-contraindicated drugs and provides them as the final answer. This case study highlights
TxAgent
’s ability to integrate comorbidity considerations into treatment recommendations and efficiently search and filter drug candidates using FDA drug labels.
Impact of tools in
ToolUniverse
on
TxAgent
’s performance
We evaluate two factors: the reliability of tools compared to language model-based alternatives and the effect of expanding
ToolUniverse
on agent’s performance.
ToolUniverse
tools provide more accurate information than LLMs.
ToolUniverse
improves
TxAgent
’s reasoning accuracy by integrating verified knowledge sources through specialized tools. We compare its effectiveness against an LLM-only approach, where the model mimics tool functionality by receiving structured prompts that describe each tool’s capabilities and arguments (Figure
c, Online Methods Section
). GPT-4o and Llama 3.1-Instruct-8B serve as the backend LLMs in this analysis, with all other settings unchanged.
Replacing real tools in
ToolUniverse
with LLM-based tools significantly reduces accuracy. On DrugPC, using Llama3.1-8B-Instruct as tools lowers accuracy from 93.8% to 68.7% (-25.1%), while using GPT-4o results in 72.7% (-21.1%). Although GPT-4o performs better, both models remain inferior to
ToolUniverse
, demonstrating the limitations of LLM-only approaches in retrieving precise biomedical information.
We observe a similar pattern on TreatmentPC. GPT-4o and Llama3.1-8B-Instruct achieve 67.11% and 74.78% accuracy, respectively, compared to 86.84% with real tools in
ToolUniverse
. While advanced LLMs improve factual consistency, they still underperform compared to real-world tools.
ToolUniverse
ensures verifiable results, allowing users to validate
TxAgent
’s reasoning trace and final outputs.
Scaling
ToolUniverse
improves performance.
We evaluate the effectiveness and scalability of
ToolUniverse
by measuring how performance changes as more tools are added. We construct four subsets containing 10%, 20%, 50%, and 75% of
ToolUniverse
, ensuring each larger subset includes all tools from the smaller ones. This approach allows us to assess the incremental impact of adding tools while maintaining continuity across evaluations. Using
TxAgent
equipped with each subset and the full
ToolUniverse
, we measure accuracy on the DrugPC and TreatmentPC benchmarks (Figure
d). Accuracy on DrugPC increases from 78.4% with 10% of the tools to 93.8% with the full selection. A similar trend is observed on TreatmentPC, where accuracy rises from 71.7% to 86.8%. These results demonstrate that expanding
ToolUniverse
consistently improves
TxAgent
’s ability to handle complex, specialized treatment tasks.
The critical role of reasoning in
TxAgent
This section evaluates the role of reasoning in
TxAgent
through three experiments. First, we assess the impact of thought generation by removing this process. Second, we examine how the number of reasoning steps in training data affects performance by limiting the maximum reasoning traces. Finally, we evaluate the influence of reasoning during inference by imposing a step limit, forcing
TxAgent
to generate a final answer after a predefined number of steps.
Explicit thought generation drives reasoning in
TxAgent
.
We evaluate the impact of thought generation by comparing
TxAgent
with and without this process on the DrugPC and TreatmentPC benchmarks, using accuracy as the metric (Figure
e). Unlike existing tool-use LLMs that generate only function calls,
TxAgent
produces both reasoning thoughts and function calls at each step. To assess the importance of thought generation, we modify
TxAgent
to generate only function calls without intermediate reasoning. At the final step, it directly outputs the answer instead of reasoning through function calls. We implement this by removing the thought process from the
TxAgent-Instruct
dataset (Online Methods Section
). Eliminating thought generation reduces accuracy on DrugPC from 93.8% to 71.5% (-22.3%) and on TreatmentPC from 86.4% to 64.9% (-21.5%). This decline demonstrates the critical role of explicit reasoning in
TxAgent
and its advantage over tool-use LLMs that rely solely on function calls.
Long multi-step training traces improve performance on complex tasks.
We evaluate how the number of reasoning steps in
TxAgent
’s training data affects its performance on the DrugPC and TreatmentPC benchmarks, using accuracy as the metric (Figure
f).
TxAgent
acquires multi-step reasoning through fine-tuning on the
TxAgent-Instruct
dataset. To assess the impact of reasoning depth, we filter training data to retain samples with at most 1, 3, or 5 reasoning steps, or all available steps (Online Methods Section
). During inference,
TxAgent
remains unrestricted in the number of reasoning steps it can take. Reducing reasoning steps in training significantly decreases performance. A model trained with only 1 reasoning step sees accuracy drop from 86.8% to 66.9% on TreatmentPC and from 93.8% to 71.6% on DrugPC. The decline is more pronounced on TreatmentPC, indicating that complex treatment decisions require stronger multi-step reasoning. These results demonstrate that deeper reasoning traces during training improve
TxAgent
’s ability to handle complex therapeutic tasks.
Longer inference traces improve performance.
We assess the impact of reasoning depth during inference by imposing a step limit on
TxAgent
, using the TreatmentPC benchmark and accuracy as the evaluation metric (Figure
g).
TxAgent
is trained on the full
TxAgent-Instruct
dataset but is restricted to a maximum number of reasoning steps at inference. As described in Algorithm
, instead of allowing
TxAgent
to autonomously determine when to generate the special token
[FinalAnswer]
, we enforce this token when
TxAgent
reaches the step limit, instructing it to produce the final answer based on the accumulated reasoning trace. For reasoning traces shorter than the limit, the inference process remains unchanged. Accuracy improves as the reasoning step limit increases. When restricted to a single step—equivalent to conventional LLMs that generate direct answers—
TxAgent
achieves 73.5% accuracy, 13.3% lower than its unrestricted multi-step reasoning configuration. Performance continues to improve with additional steps, showing notable gains up to five steps, after which improvements plateau. The diminishing returns beyond five steps suggest that most essential reasoning occurs within this range, though maintaining full reasoning capacity remains optimal.
As a reference, we present the average number of reasoning steps and tool calls for
TxAgent
in Extended Data Figure
. The TreatmentPC benchmark requires more reasoning steps than the DrugPC benchmarks, suggesting that precise treatment recommendations require more reasoning steps before reaching a conclusion.
Similarly, the TreatmentPC benchmark involves a greater number of tool calls compared to DrugPC. When comparing multiple-choice and open-ended settings, DrugPC shows no significant difference in reasoning steps or tool calls. However, in the open-ended setting, TreatmentPC requires a significantly larger number of reasoning steps and tool calls compared to the multiple-choice setting.
Discussion
TxAgent
is an AI agent that applies multi-step reasoning and tool usage to solve therapeutic problems, including drug prescriptions and disease treatment recommendations, while considering patient-specific factors. Unlike conventional models that produce probability scores without explanations,
TxAgent
generates a reasoning trail along with its answer, making its decision-making process transparent and interpretable.
TxAgent
integrates external tools from
ToolUniverse
to retrieve real-time biomedical knowledge, overcoming the limitations of LLMs that rely solely on static training data. This enables
TxAgent
to recommend newly approved drugs, assess indications, and provide evidence-based prescriptions. By grounding the responses in verified sources,
TxAgent
allows users to trace each decision step in a transparent manner.
Treatment decisions must account for patient-specific factors, including age, comorbidities, pregnancy status, disease severity, and immune function. Existing models predict disease-drug links but fail to consider these variations.
TxAgent
addresses this limitation through dynamic, multi-step reasoning. It identifies the disease based on phenotypes, retrieves potential treatments by considering associated phenotypes and biological targets, and evaluates drug suitability based on patient characteristics. Rather than following a fixed sequence,
TxAgent
adapts its reasoning through iterative function calls to biomedical tools, ensuring decisions are grounded in verified sources such as FDA drug labels. For example,
TxAgent
determines that Xolremdi, a treatment for WHIM syndrome, should not be used with Prozac, a CYP2D6 inhibitor, because it alters Xolremdi’s metabolism. By integrating patient-specific constraints into its reasoning process,
TxAgent
ensures clinically relevant and personalized treatment recommendations.
TxAgent
’s limitations highlight areas for future research. It relies on tool calls for external information, but gaps in
ToolUniverse
restrict access to specific data types, limiting its ability to address a broader range of questions.
Uncertainty quantification in
TxAgent
’s internal knowledge remains a challenge. The current approach grounds reasoning through external tools, improving verifiability. However, integrating internal knowledge with tool feedback could enhance flexibility for exploratory tasks.
TxAgent
processes only natural language inputs and does not yet support other modalities such as pathology images, EHR data, or web-based lab results. Expanding multi-modal support would enable
TxAgent
to handle more complex cases and specialized clinical analyses.
TxAgent
is an AI agent for therapeutic reasoning that leverages a universe of tools to generate transparent reasoning traces grounded in multi-source medical evidence and continuously updated medical knowledge. It integrates verified information from FDA drug labels, Open Targets, and other trusted sources to produce evidence-based therapeutic recommendations. Future advances in integrating clinical modalities and extended memory for patient histories could allow
TxAgent
to analyze multi-modal clinical data
[
33
]
.
TxAgent
establishes a new framework for precision therapeutics by advancing personalized therapy selection and supporting regulatory-compliant clinical decision-making.
Data and code availability.
The project page is available at
https://zitniklab.hms.harvard.edu/TxAgent
.
The code and demo of
TxAgent
are available at
https://github.com/mims-harvard/TxAgent
.
The code of
ToolUniverse
is available at
https://github.com/mims-harvard/ToolUniverse
.
The pre-trained models are available at
https://huggingface.co/collections/mims-harvard/txagent-67c8e54a9d03a429bb0c622c
.
Acknowledgements.
We gratefully acknowledge the support of NIH R01-HD108794, NSF CAREER 2339524, US DoD FA8702-15-D-0001, Harvard Data Science Initiative, Amazon Faculty Research, Google Research Scholar Program, AstraZeneca Research, Roche Alliance with Distinguished Scientists, Sanofi iDEA-iTECH, Pfizer Research, Gates Foundation (INV-079038), Chan Zuckerberg Initiative, John and Virginia Kaneb Fellowship at Harvard Medical School, Biswas Computational Biology Initiative in partnership with the Milken Institute, Harvard Medical School Dean’s Innovation Fund for the Use of Artificial Intelligence, and Kempner Institute for the Study of Natural and Artificial Intelligence at Harvard University. Any opinions, findings, conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the funders.
We thank Owen Queen and Thomas Hartvigsen for their helpful discussion and feedback on our project.
DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited. This material is based upon work supported by the Under Secretary of Defense for Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions, findings, conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Under Secretary of Defense for Research and Engineering.
Competing interests.
The authors declare no competing interests.
\spacing
1
Figure 1:
Figure
:
a
)
TxAgent
processes specialized therapy-related questions, generating detailed step-by-step reasoning and conducting parallel function calls across a vast array of biomedical tools and specialized tools. It delivers solutions supported by clear, rational, and verified reasoning traces.
b
) Examples of tools in
ToolUniverse
and the machine learning tool.
ToolUniverse
consolidates 211 tools linked to trusted sources, including all US FDA-approved drugs since 1939 and validated clinical insights from Open Targets and Monarch Initiative.
The machine learning tool, e.g.,
ToolRAG
model, is based on a machine learning model instead of APIs.
c
)
ToolUniverse
includes 211 biomedical tools that address various aspects of drugs and diseases.
It covers the following categories:
adverse events, risks, safety; addiction and abuse; drug usage in patient populations; drug administration and handling; pharmacology; drug use, mechanism, composition; ID and labeling tools; general clinical annotations; clinical laboratory info; general info for patients and relatives; disease, phenotype, target, drug links; biological annotation tools; publications; search; target characterization.
d
)
TxAgent
demonstrates superior performance compared to LLMs with a larger number of parameters, such as GPT-4o, excelling in both open-ended and multiple-choice questions.
e
)
TxAgent
demonstrates superior performance compared to tool-use LLMs that also have full access to
ToolUniverse
, excelling in both open-ended and multiple-choice questions.
f-i
) Capabilities of
TxAgent
: knowledge grounding using tool calls, goal-oriented tool selection,
problem solving with multi-step reasoning, and leverage constantly updated knowledge base.
f
) Knowledge grounding using tool calls, where
TxAgent
utilizes tools to obtain verified knowledge and provides outputs based on it.
g
) Goal-oriented tool selection, where
TxAgent
proactively requests tools from
ToolUniverse
using the
ToolRAG
model model and selects and applies the most suitable tool from the available candidates.
h
) Problem solving with multi-step reasoning, where
TxAgent
manages complex tasks or unexpected responses from tools through multiple iterations of thought and function calls.
i
) Leveraging constantly updated knowledge bases, where
TxAgent
accesses continuously updated databases via tools to handle problems that go beyond the
TxAgent
’s intrinsic knowledge.
Figure 2:
Figure
:
a
)
TxAgent-Instruct
dataset is a diverse synthetic multi-step reasoning and massive function call training dataset anchored in biomedical knowledge.
To generate
TxAgent-Instruct
, we construct three datasets—a tooling dataset, a comprehensive therapeutic question dataset, and a reasoning trace dataset—using the auxiliary agent systems.
The tooling dataset consists of augmented versions of 211 tools from
ToolUniverse
.
The comprehensive therapeutic question dataset includes 85,340 therapeutic questions and functional instructions designed to train
TxAgent
’s abilities. These are generated by the
QuestionGen
agent system.
The reasoning trace dataset comprises 85,340 detailed reasoning traces for answering therapeutic questions. These traces collectively encompass 177,626 reasoning steps and 281,695 function calls, all generated by the
TraceGen
agent system.
By processing the data from these three datasets, we construct
TxAgent-Instruct
, which comprises 378,027 instruction-tuning data samples.
b
)
TxAgent
outperforms larger open-source LLMs and GPT-4 across 11 tasks from the DrugPC dataset, excelling in both open-ended and multiple-choice questions. These tasks cover various drug-related topics, including drug overview, ingredients, warnings and safety, dependence and abuse, dosage and administration, use in specific populations, pharmacology, clinical information, nonclinical toxicology, patient-focused information, and storage and supply.
c
) Across the 11 tasks of the DrugPC dataset,
TxAgent
demonstrates superior performance compared to existing tool-use LLMs.
Figure 3:
Figure
:
a
)
TxAgent
surpasses both native and tool-use LLMs on the DrugPC benchmark, as well as its Brand and Generic variants, where drug names are replaced with their brand and generic counterparts. Additionally,
TxAgent
demonstrates minimal variance when handling drug names with different representations.
b
)
TxAgent
surpasses LLM in a two-step evaluation on the DescriptionPC benchmark, where drug names are replaced with their descriptions, including indications, mechanisms of action, contraindications, and interactions. In this evaluation, the first step involves identifying the correct drug name based on its description, followed by answering the question using the correctly identified drug name.
c
) Comparison of real-world tools from
ToolUniverse
versus relying on an LLM’s internal knowledge as a substitute for external tools on DrugPC and TreatmentPC benchmarks. When paired with
TxAgent
,
ToolUniverse
tools provide more accurate information than using LLMs ike GPT-4o as tools.
d
) The impact of increasing the number of tools in
ToolUniverse
on the DrugPC and TreatmentPC benchmarks. As more tools are incorporated into
ToolUniverse
, the results consistently demonstrate steady and significant performance improvements.
e
) Explicit thought generation is fundamental to reasoning in
TxAgent
. We evaluate
TxAgent
with and without thought generation on the DrugPC and TreatmentPC benchmarks. The absence of thought generation results in a significant performance decline, underscoring its essential role in
TxAgent
’s reasoning process.
f
) Long multi-step traces in training data enhance
TxAgent
’s ability to handle complex tasks. We examine how the number of reasoning steps in
TxAgent
’s training data affects its performance on the DrugPC and TreatmentPC benchmarks. As the number of reasoning steps decreases, performance gradually declines, suggesting that more complex tasks demand a stronger multi-step reasoning capability from
TxAgent
.
g
) Longer inference traces enhance model performance. To assess the impact of reasoning during inference, we impose a step limit on
TxAgent
and evaluate its performance on the TreatmentPC benchmark. Results show a clear upward trend in accuracy as the number of reasoning steps increases, highlighting the importance of extended reasoning in
TxAgent
’s inference process.
Figure 4:
Figure
:
a
) Performance comparison between
TxAgent
and large-scale LLMs on the TreatmentPC benchmark. Despite being based on an 8-billion-parameter model,
TxAgent
outperforms larger LLMs such as GPT-4o and Llama 3.1-70B-Instruct in both open-ended and multiple-choice settings. Notably, in the open-ended setting,
TxAgent
achieves a higher accuracy (75%) than GPT-4o does in the multiple-choice setting (74.1%), even though the latter benefits from predefined answer options that simplify the task.
b
) Performance comparison between
TxAgent
and tool-use LLMs on the TreatmentPC benchmark.
Although ToolACE-8B and WattTool-8B, like
TxAgent
, are fine-tuned on Llama-3.1-8B-Instruct and have full access to the
ToolUniverse
,
TxAgent
still achieves a significantly higher performance.
c
) Performance comparison between
TxAgent
and reasoning LLMs (e.g., DeepSeek-R1) on the TreatmentPC benchmark.
TxAgent
achieves superior performance compared to the full DeepSeek-R1 model and its two distilled versions based on Llama-3.1-8B and Llama-3.3-70B.
d
)
TxAgent
identifies Duvyzat as the optimal treatment for a pediatric patient with Duchenne muscular dystrophy by evaluating drug mechanisms and pediatric use guidelines.
e
)
TxAgent
evaluates the potential drug-drug interactions between Prozac and Xolremdi, highlighting the risks of combined use due to their effects on the CYP2D6 enzyme.
f
)
TxAgent
provides personalized, evidence-based treatment advice for elderly patients, adjusting the maximum dosage of Cobenfy based on age-specific considerations and the associated risks.
g
)
TxAgent
personalizes treatment recommendations by considering comorbidities, ensuring hypertension drugs are not contraindicated for a patient’s second-degree AV block.
Figure 1:
Examples of tool specifications in
ToolUniverse
.
Each specification includes a tool description, which serves as a reference for
TxAgent
’s function calls, and a mapping rule that translates function calls into API requests. The tool description outlines the tool’s name, purpose, and the arguments it accepts, including details such as each argument’s name, purpose, data type, and whether it is mandatory.
a
) Tool description for the tool from OpenFDA.
b
) Tool description for the tool from Open Targets.
c
) Mapping between Tools in TxAgent and external APIs from from OpenFDA.
d
) Mapping between Tools in TxAgent and external APIs from from Open Targets.
Figure 2:
The multi-agent systems, (i.e.,
ToolGen
,
QuestionGen
, and
TraceGen
) that construct the
TxAgent-Instruct
training dataset for instruction tuning LLM to achieve the capabilities of
TxAgent
.
a
)
ToolGen
: A tool generation multi-agent system that transforms APIs into 211 agent-compatible tools, aggregating them into the
ToolUniverse
.
b
)
QuestionGen
: A question generation multi-agent system designed to extract critical information from documents (e.g., FDA drug documentation) and generate relevant questions.
c
)
TraceGen
: A reasoning trace generation multi-agent system, where a
Helper
agent and a
Tool provider
module assist the
Solver
agent in generating step-by-step reasoning and function calls to solve a problem.
Figure 3:
Categories of biomedical tools in
ToolUniverse
.
ToolUniverse
contains 211 biomedical tools and includes the following categories:
adverse events, risks, safety; addiction and abuse; drug usage in patient populations; drug administration and handling; pharmacology; drug use, mechanism, composition; id and labeling tools; general clinical annotations; clinical laboratory info; general info for patients and relatives; disease, phenotype, target, drug links; biological annotation tools; publications; search; target characterization.
Figure 4:
a
) The average number of reasoning steps for multiple-choice questions and open-ended reasoning in the DrugPC and TreatmentPC benchmarks. The TreatmentPC requires more reasoning steps compared to the DrugPC benchmarks, indicating that precision treatment recommendations require more reasoning steps before reaching a conclusion.
b
) The average number of tool calls for multiple-choice questions and open-ended reasoning in the DrugPC and TreatmentPC benchmarks.
Similarly, the TreatmentPC benchmark requires a greater number of tool calls compared to the DrugPC.
Figure 5:
Comparison between
TxAgent
and Deepseek-R1.
Deepseek-R1 relies on its internal knowledge for reasoning, which can sometimes lead to hallucinated information and misjudgments.
In contrast, TxAgent bases its reasoning on trusted sources, such as FDA drug labels, minimizing the risk of hallucinations and ensuring more reliable conclusions.
Table 1:
Benchmark datasets. These datasets are derived from newly approved FDA drugs in 2024 to minimize the risk of information leakage from LLMs. A human evaluation process is conducted to carefully review and refine the questions and answers, ensuring the exclusion of non-biomedical questions.
Benchmark
Size
Description
DrugPC
3,168
FDA newly approved drugs in 2024
Drug Overview
242
package label principal display panel; description
Drug Ingredients
83
product data elements
Drug Warnings and Safety
515
boxed warning; warnings and cautions; contraindications; adverse reactions; drug interactions
Drug Dependence and Abuse
53
drug abuse and dependence; abuse; controlled substance; overdosage
Dosage and Administration
507
indications and usage; dosage and administration; dosage forms and strengths; instructions for use
Drug use in Specific Populations
333
use in specific populations; pregnancy; pediatric use; geriatric use; nursing mothers
Pharmacology
565
clinical pharmacology; mechanism of action; pharmacodynamics; pharmacokinetics
Clinical Information
146
clinical studies
Nonclinical Toxicology
172
nonclinical toxicology; carcinogenesis and mutagenesis and impairment of fertility; animal pharmacology and or toxicology
Patient-Focused Information
349
information for patients; patient medication guide; patient package insert; patient medication information
Storage and Supply Information
203
how supplied; storage and handling
BrandPC
3,168
Drugs represented with drug brand name
GenericPC
3,168
Drugs represented with drug generic name
DescriptionPC
626
Drugs represented with descriptions instead of names
TreatmentPC
456
Questions regarding specialized treatment recommendations considering patient populations
Variable
Description
Q
Q
A precision therapy question.
A
A
The final answer, including the rationale and the solution.
G
G
The ground truth answer
G
G
.
X
X
The explanation of why
G
G
answers
Q
Q
.
ℱ
\mathcal{F}
The
TxAgent
’s backend LLM.
ℱ
T
​
X
\mathcal{F}_{TX}
ℱ
\mathcal{F}
prompted by the system prompt of being an
TxAgent
.
ℱ
S
\mathcal{F}_{S}
ℱ
\mathcal{F}
prompted by the system prompt of a summarization prompt.
ℛ
i
\mathcal{R}_{i}
The verified reasoning trace
{
R
1
,
R
2
,
…
,
R
i
}
\{R_{1},R_{2},...,R_{i}\}
until the
i
i
th step.
i
i
Index representing the step in the reasoning trace.
T
i
T_{i}
The thought at the
i
i
th step of the reasoning trace.
𝒫
i
\mathcal{P}_{i}
The collection of tools available at step
i
i
.
𝒫
^
0
\mathcal{\hat{P}}_{0}
Tools obtained from the reference information during training data generation process.
𝒫
^
i
RAG
\mathcal{\hat{P}}_{i}^{\text{RAG}}
Tools obtained from the
ToolUniverse
at the
i
i
th step during training data generation process.
𝒞
i
\mathcal{C}_{i}
The set of function calls
{
C
i
,
1
,
C
i
,
2
,
…
,
C
i
,
k
}
\{C_{i,1},C_{i,2},...,C_{i,k}\}
at step
i
i
.
ℰ
i
\mathcal{E}_{i}
Response of the function calls in the
i
i
th step.
R
i
R_{i}
The
i
i
th step in the reasoning trace,
R
i
=
[
T
i
,
𝒞
i
,
ℰ
i
]
R_{i}=[T_{i},\mathcal{C}_{i},\mathcal{E}_{i}]
.
C
i
,
k
C_{i,k}
The
k
k
th function call at the
i
i
th step in the reasoning trace.
ℬ
\mathcal{B}
The tool set containing various tools
{
B
1
,
B
2
,
…
,
B
j
}
\{B_{1},B_{2},...,B_{j}\}
.
B
j
B_{j}
The
j
j
th tool from the tool set.
ℐ
\mathcal{I}
Real-world biomedical information, including FDA documents, disease and drug data.
Table 2:
Additional notation.
Multi-choice setting
Open-ended setting
Question
A 60-year-old female patient with a history of myocardial infarction and hypertension is being evaluated for medication adjustments. She is currently on a beta-blocker and has no known renal or hepatic impairments. Which medication would be most appropriate to add to her regimen to further reduce her cardiovascular risk?
A 60-year-old female patient with a history of myocardial infarction and hypertension is being evaluated for medication adjustments. She is currently on a beta-blocker and has no known renal or hepatic impairments. Which medication would be most appropriate to add to her regimen to further reduce her cardiovascular risk?
Options
A: Sitagliptin B: Altace C: Katerzia D: Aspirin
Answer
B
Ramipril (Altace) is the most appropriate medication to add to the patient’s regimen to further reduce her cardiovascular risk. Ramipril is an ACE inhibitor that is indicated for reducing the risk of myocardial infarction, stroke, and death from cardiovascular causes in patients 55 years or older who are at high risk of developing a major cardiovascular event. This aligns with the patient’s profile, as she is 60 years old with a history of myocardial infarction and hypertension. Additionally, Ramipril is indicated for use in stable patients with signs of congestive heart failure post-myocardial infarction, making it a suitable choice for this patient. Therefore, adding Ramipril to her current regimen of a beta-blocker would provide comprehensive cardiovascular protection.
Table 3:
The examples of questions, options, and answers in open-ended and multi-choice settings.
\spacing
1.4
Online Methods
1
TxAgent
1.1
Overview
We introduce
TxAgent
, an agentic AI model for precision therapy, leveraging an extensive array of biomedical tools and multi-step, white-box drug reasoning grounded with verified real-world knowledge.
TxAgent
interprets user questions written in natural language and generates answers accompanied by detailed rationales and reasoning traces (Figure
b). These traces include multiple thought processes, function calls, and grounded information drawn from tools, enabling users to clearly understand and verify the basis of its conclusions.
To address complex queries,
TxAgent
performs a series of actions such as analyzing user inputs and current contexts, identifying relevant tools, executing function calls on selected tools, synthesizing answers, and coordinating among tools to compile a comprehensive and accurate response.
This functionality is powered by unified multi-step reasoning, where each step involves iterative thinking and tool utilization.
TxAgent
is supported by a
ToolUniverse
and specialized tools, such as machine learning model-based tools. The
ToolUniverse
includes 211 biomedical tools for accessing high-quality knowledge, such as FDA drug information. Specialized tools are created for specific usages, such as the
ToolRAG
model, which is an embedding model that facilitates efficient tool retrieval, and the
Finish
tool, which signals the conclusion of multi-step reasoning.
The multi-step reasoning with function call abilities is achieved through fine-tuning open-source large language models (LLMs) such as Llama-3.1. By utilizing open-source models, our method supports local deployment for private applications, safeguarding patient information and ensuring privacy.
To achieve
TxAgent
, the collection of
ToolUniverse
and the fine-tuning of LLMs for multi-step reasoning and function calls are essential. We introduce three key multi-agent systems: the
ToolGen
system for tool construction, the
QuestionGen
system for training question generation, and the
TraceGen
system for reasoning trace generation.
These multi-agent systems leverage AI agents powered by LLMs through prompting. Drawing on real-world biomedical information and APIs from verified sources—including FDA documents
[
20
]
, the OpenTarget database
[
21
]
, and the PrimeKG graph
[
28
]
—they enable the generation, verification, and filtering of data. Using these systems, we construct the
TxAgent-Instruct
dataset to fine-tune LLMs and achieve
TxAgent
.
Preliminaries.
During the inference process,
given a therapy question
Q
Q
,
TxAgent
generates a verified reasoning trace
ℛ
i
=
{
R
1
,
R
2
,
R
3
,
…
,
R
i
}
\mathcal{R}_{i}=\{R_{1},R_{2},R_{3},...,R_{i}\}
and the final answer
A
A
, which includes the rationale for the answer, such as treatment recommendations.
The
i
i
-th step in the reasoning trace
R
i
R_{i}
consists of a thought
T
i
T_{i}
, a set of function calls
𝒞
i
=
{
C
i
1
,
C
i
2
,
…
​
C
i
k
}
\mathcal{C}_{i}=\{C_{i}^{1},C_{i}^{2},...C_{i}^{k}\}
, and responses from the function calls
ℰ
i
=
{
E
i
1
,
E
i
2
,
…
​
E
i
k
}
\mathcal{E}_{i}=\{E_{i}^{1},E_{i}^{2},...E_{i}^{k}\}
, i.e.,
R
i
=
{
T
i
,
𝒞
i
,
ℰ
i
}
R_{i}=\{T_{i},\mathcal{C}_{i},\mathcal{E}_{i}\}
.
The
ToolUniverse
ℬ
=
{
B
1
,
B
2
,
…
,
B
j
}
\mathcal{B}=\{B_{1},B_{2},...,B_{j}\}
contains a wide array of biomedical tools from
ToolUniverse
.
𝒫
i
\mathcal{P}_{i}
is the collection of tools available at step
i
i
,
which contains the default specialized tools and tools retrieved by the
ToolRAG
model in previous steps.
To aid understanding, Table
provides the complete definitions and explanations of all notations used in this work.
1.2
Skills of
TxAgent
TxAgent
is an LLM-based agentic model designed to address complex drug reasoning problems through its versatile capabilities. These capabilities are enabled by
TxAgent
’s multi-step reasoning processes and its ability to perform function calls, which leverage the combined effects of its diverse skill set.
This section introduces the core skills of
TxAgent
, which are obtained by the instruction finetuning of an LLM as introduced in Section
. Then, we detail the advanced capabilities
TxAgent
can achieve by integrating these skills and describe the inference process of
TxAgent
.
Contextual thought generation.
TxAgent
is capable of generating thoughtful, context-aware, step-by-step reasoning based on prior interactions and user inputs. Given a user query
Q
Q
and a sequence of previous reasoning traces
ℛ
i
−
1
\mathcal{R}_{i-1}
,
TxAgent
produces a new thought
T
i
T_{i}
at step
i
i
, expressed in natural language.
This thought generation process can be represented as:
T
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
𝒫
i
)
,
T_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},\mathcal{P}_{i}),
(1)
where
ℱ
T
​
X
\mathcal{F}_{TX}
is the
TxAgent
’s backend LLM prompted by the system prompt of being an
TxAgent
, which operates in an autoregressive manner
[
34
]
, and
𝒫
i
\mathcal{P}_{i}
is a set of available tools at this step.
The query
Q
Q
along with the reasoning traces
ℛ
i
−
1
\mathcal{R}_{i-1}
is provided as input to
ℱ
T
​
X
\mathcal{F}_{TX}
to generate
T
i
T_{i}
, which incorporates reasoning about the analysis of prior steps and determines the next actions.
Function call arguments generation.
TxAgent
executes tools by generating function call arguments based on the tool descriptions provided in the prompts. Each tool description consists of the tool’s name, its purpose, and the arguments it accepts. For each argument, the description specifies its name, purpose, data type, and whether it is mandatory (Extended Data Figure
).
Following the generated thought
T
i
T_{i}
of reasoning step
R
i
R_{i}
, given a set of tool descriptions
𝒫
i
\mathcal{P}_{i}
available to
TxAgent
,
TxAgent
produces the corresponding function call arguments for tool calls:
𝒞
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
T
i
,
𝒫
i
)
,
\mathcal{C}_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},T_{i},\mathcal{P}_{i}),
(2)
where
𝒞
i
=
{
C
i
1
,
C
i
2
,
…
,
C
i
k
}
\mathcal{C}_{i}=\{C_{i}^{1},C_{i}^{2},\dots,C_{i}^{k}\}
is a list that contains multiple function calls as
TxAgent
supports parallel tool execution by generating multiple function calls across various tools.
The
k
k
-th function call at step
i
i
,
C
i
k
C_{i}^{k}
, is represented as a code snip in JSON format:
C
i
k
=
⟨
name
,
𝒜
i
k
⟩
,
C_{i}^{k}=\left\langle\texttt{name},\mathcal{A}_{i}^{k}\right\rangle,
(3)
where
name
is the name of the tool selected from the set of available tools
𝒫
i
\mathcal{P}_{i}
,
𝒜
i
k
=
{
a
1
,
a
2
,
…
,
a
n
}
\mathcal{A}_{i}^{k}=\{a_{1},a_{2},\dots,a_{n}\}
represents the arguments required by tool
C
i
k
C_{i}^{k}
, where each
a
j
a_{j}
corresponds to a specific argument-value pair corresponding to the description of the selected tool.
The generated function call arguments
𝒞
i
\mathcal{C}_{i}
are sent to the
ToolUniverse
codebase for execution. The results from these function calls
ℰ
i
=
{
E
i
1
,
E
i
2
,
…
​
E
i
k
}
\mathcal{E}_{i}=\{E_{i}^{1},E_{i}^{2},...E_{i}^{k}\}
, where
E
i
k
E_{i}^{k}
is the result of
k
k
-th function call, are then sent back to
TxAgent
as part of the current step of the reasoning trace
R
i
=
{
T
i
,
𝒞
i
,
ℰ
i
}
R_{i}=\{T_{i},\mathcal{C}_{i},\mathcal{E}_{i}\}
.
The reasoning trace
ℛ
i
\mathcal{R}_{i}
is then updated as:
ℛ
i
=
ℛ
i
−
1
∪
R
i
\mathcal{R}_{i}=\mathcal{R}_{i-1}\cup R_{i}
.
Tools used by
TxAgent
involve a variety of types, such as biomedical tools in
ToolUniverse
that gather outputs from multiple verified sources, and the machine learning-based tools (
ToolRAG
model) that use a machine learning model to achieve certain functions.
Moreover, we will explore tool use of
TxAgent
in a broader range,
such as the formation of a multi-agent system where tools represent specialized agents with unique capabilities, or even the creation of a new instance of
TxAgent
. To add new capabilities to
TxAgent
, simply introduce new tools to the framework, and
TxAgent
will automatically incorporate and utilize them when needed.
Logical multi-step reasoning and decision-making.
TxAgent
achieves logical multi-step reasoning by iteratively generating thoughts and formulating tool arguments. At each step,
TxAgent
evaluates whether the reasoning trace up to that point—particularly the outputs from prior function calls—provides sufficient information to answer the user’s query by generating thought
T
i
T_{i}
. Based on this assessment, it decides on the next action, which could involve generating new function calls
𝒞
i
\mathcal{C}_{i}
to use tools for accessing new information or generating the final answer
A
A
, depending on if the special token
[FinalAnswer]
is generated or not:
𝒞
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
T
i
,
𝒫
i
)
,
\displaystyle\mathcal{C}_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},T_{i},\mathcal{P}_{i}),
[FinalAnswer]
∉
T
i
;
\displaystyle\texttt{[FinalAnswer]}\notin T_{i};
(4)
A
,
𝒞
F
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
T
i
,
𝒫
i
)
,
\displaystyle A,\mathcal{C}_{F}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},T_{i},\mathcal{P}_{i}),
[FinalAnswer]
∈
T
i
,
\displaystyle\texttt{[FinalAnswer]}\in T_{i},
where
𝒞
F
\mathcal{C}_{F}
is a final function call to the special
Finish
tool, signifying the end of the reasoning process.
Despite its simplicity, this iterative thought and function call generation process has potential to incorporate complex and dynamic agentic workflows.
Proactive tool search, selection and utilization.
ToolUniverse
includes 211 tools spanning various aspects of the biomedical field. However, due to the limited context window of the LLM (i.e., the number of text tokens it can handle in a prompt), it is impractical to include all tool descriptions within the prompt.
To address this,
TxAgent
employs a proactive tool search strategy by utilizing the
ToolRAG
model. When no suitable tool is available for the next action,
TxAgent
dynamically invokes the
ToolRAG
model by function call to search for tools matching the desired requirement.
Rather than relying on tools memorized during training,
TxAgent
selects and uses tools based on its current requirements and descriptions of tools, ensuring flexibility and scalability.
The
ToolRAG
model is an embedding model designed to retrieve tools based on specific requirements.
During inference, the
ToolRAG
model processes all tool descriptions in
ToolUniverse
to generate their semantic embeddings. For each new function call to
ToolRAG
model, the model encodes the requirement argument obtained from the function call arguments into an embedding and retrieves the top-
k
k
tools whose embeddings have the highest similarity to the requirement’s embedding.
The newly retrieved tools are put into the tool set
𝒫
i
\mathcal{P}_{i}
.
Due to the expansive scope of
ToolUniverse
, imperfection of
ToolRAG
model, and the open-ended reasoning approach of
TxAgent
, not all tools retrieved by
ToolRAG
model are immediately applicable to
TxAgent
’s next action. Drawing from the prior reasoning trace and the descriptions of the retrieved tools,
TxAgent
identifies the most suitable options from
𝒫
i
\mathcal{P}_{i}
, formulates new thoughts, and generates parallel function calls to effectively utilize the selected tools.
Concise summarization.
Tool outputs can often be lengthy, especially in complex cases. This poses a challenge due to the limited context window of the LLM, as lengthy outputs restrict the maximum number of reasoning steps that can be performed. To overcome this limitation,
TxAgent
introduces a mechanism to transform lengthy tool outputs into concise, accurate, and meaningful summaries.
Given a reasoning step
R
i
=
{
T
i
,
𝒞
i
,
ℰ
i
}
R_{i}=\{T_{i},\mathcal{C}_{i},\mathcal{E}_{i}\}
,
TxAgent
generates a summarized version of tool response
ℰ
i
\mathcal{E}_{i}
as follows:
ℰ
^
i
=
ℱ
S
​
(
T
i
,
𝒞
i
,
ℰ
i
)
,
\hat{\mathcal{E}}_{i}=\mathcal{F}_{S}\left(T_{i},\mathcal{C}_{i},\mathcal{E}_{i}\right),
(5)
where
ℱ
S
\mathcal{F}_{S}
is the backend LLM of
TxAgent
prompted with a summarization prompt.
This summary retains the essential information relevant to the thought
T
i
T_{i}
, ensuring that the critical details are preserved. By compressing lengthy outputs into a compact form,
TxAgent
enables a larger number of reasoning steps while avoiding context window overflow.
Structured question responses.
While
TxAgent
generates open-ended answers along with a reasoning trace, it can also be used for evaluating multiple-choice questions. Given a question and the open-ended answer,
TxAgent
can map the answer to the correct option from the provided choices.
Input:
Question
Q
Q
,
ToolUniverse
ℬ
\mathcal{B}
, Initial available tools
𝒫
0
\mathcal{P}_{0}
Output:
Reasoning trace
ℛ
\mathcal{R}
, final answer
A
A
Initialize
ℛ
←
{
}
\mathcal{R}\leftarrow\{\}
, tools
𝒫
←
𝒫
0
\mathcal{P}\leftarrow\mathcal{P}_{0}
, step
i
←
0
i\leftarrow 0
;
while
Reasoning is incomplete
do
i
←
i
+
1
i\leftarrow i+1
;
Generate thought:
T
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
𝒫
i
)
T_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},\mathcal{P}_{i})
;
if
[FinalAnswer]
in
T
i
T_{i}
then
Generate final answer:
A
,
𝒞
F
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
T
i
,
𝒫
i
)
A,\mathcal{C}_{F}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},T_{i},\mathcal{P}_{i})
;
Execute
Finish
tool to end the multi-step reasoning;
Return
ℛ
i
,
A
\mathcal{R}_{i},A
;
else
Generate function calls:
𝒞
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
T
i
,
𝒫
i
)
\mathcal{C}_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},T_{i},\mathcal{P}_{i})
;
if
call to
ToolRAG
in
𝒞
i
\mathcal{C}_{i}
then
Execute
ToolRAG
and update
𝒫
i
\mathcal{P}_{i}
;
else
Execute tools from
𝒞
i
\mathcal{C}_{i}
to get tool response
ℰ
i
\mathcal{E}_{i}
;
Update reasoning trace:
ℛ
i
←
ℛ
i
−
1
∪
{
T
i
,
𝒞
i
,
ℰ
i
}
\mathcal{R}_{i}\leftarrow\mathcal{R}_{i-1}\cup\{T_{i},\mathcal{C}_{i},\mathcal{E}_{i}\}
;
Algorithm 1
TxAgent
multi-step inference process.
1.3
Capabilities of
TxAgent
In Algorithm
, we present the inference process of
TxAgent
, leveraging the skills described above. We highlight the capabilities of
TxAgent
made possible through its diverse skill sets.
Knowledge grounding using tool calls.
The treatment problem demands reliable answers accompanied by transparent explanations to justify decisions. However, a significant concern arises from the inability of machine learning models, such as LLMs, to provide dependable explanations for their predictions. This forces users to invest additional effort in determining whether the model’s predictions can be trusted.
With the function calling skill,
TxAgent
provides answers to user queries grounded in verified information by leveraging tools connected to trusted sources. Instead of generating responses directly like traditional LLMs,
TxAgent
utilizes tools to retrieve accurate information. The answers are then crafted based on the verified outputs of these tools. For instance, it can query the dosage instructions for a medication from official FDA documents.
This knowledge-grounding approach allows users to validate the factual correctness of answers by reviewing the reasoning trace, ensuring transparency and reliability.
Goal-oriented tool selection.
Through the proactive tool search, selection and utilization skills,
TxAgent
leverages
ToolRAG
model to search for tools, identify suitable options, and effectively utilize the most appropriate tools from the candidates provided by
ToolRAG
model.
This approach enables
TxAgent
to access a vast array of tools and seamlessly adapt to new ones.
Instead of relying solely on tools memorized during training, the goal-oriented tool selection process allows
TxAgent
to reason more freely by first generating a plan of action and then identifying the tools necessary to execute it.
Furthermore,
TxAgent
can expand its capabilities by integrating additional tools into the
ToolUniverse
without requiring retraining. When faced with new scenarios where existing tools are insufficient,
TxAgent
can address these cases by incorporating relevant tools into the
ToolUniverse
, showcasing its flexibility and adaptability in handling novel challenges.
Multi-step therapeutic reasoning.
When tackling complex therapeutic problems that cannot be solved in a single step,
TxAgent
employs multi-step therapeutic reasoning to iteratively generate new thoughts and function calls based on the prior reasoning trace.
There are two key scenarios where multi-step reasoning is essential. First, solving complex problems often requires gathering information from multiple perspectives before arriving at a well-founded answer. Second, in real-world applications, interactions with the environment can be unpredictable—such as function calls failing to retrieve necessary information—making it common for a single attempt to fall short.
By leveraging multi-step reasoning,
TxAgent
can effectively address both cases by systematically collecting information, generating new ideas, and making additional function calls to explore alternative solutions. This iterative process continues until the goal is successfully achieved.
Real-time retrieval from continually updated knowledge sources.
Once a model finishes training, its internal knowledge remains static and is no longer updated. Given the high cost and technical challenges associated with continuously training large models, such as LLMs, it is difficult to incorporate new knowledge directly into these models.
Retrieval-augmented generation
[
27
]
, a special form of tool-use model, retrieves relevant text by matching query embeddings with a precomputed vector database. However, maintaining a high-quality vector database is computationally intensive, making frequent updates difficult.
TxAgent
takes a different approach by using function calls to directly access multiple constantly updated data sources, such as the OpenTargets and FDA databases.
By leveraging these dynamic knowledge bases,
TxAgent
can answer questions about newly approved drugs, even when the training data lacks relevant information.
Additionally, it integrates complementary information from multiple sources, eliminating the need to construct and maintain a vector database.
2
ToolUniverse
The
ToolUniverse
consists of 211 biomedical tools that provide real-time, up-to-date information on diseases, drugs, targets, and other essential biomedical data.
Constructing such a vast number of tools manually would be impractical; therefore, we developed
ToolGen
, a tool construction multi-agent system that automates the creation of tool descriptions and the critical mappings between tools and APIs.
This section first presents an overview of
TxAgent
, followed by an introduction to
ToolGen
system.
2.1
Overview of
ToolUniverse
ToolUniverse
has 211 biomedical tools, covering the following categories:
adverse events, risks, safety; addiction and abuse; drug patient populations; drug administration and handling; pharmacology; drug use, mechanism, composition; ID and labeling tools; general clinical annotations; clinical laboratory info; general info for patients and relatives; disease, phenotype, target, drug links; biological annotation tools; publications; search; target characterization.
Tools in
ToolUniverse
are built upon APIs from multiple sources, including OpenFDA, OpenTargets, and the Monarch Initiative.
The complete distribution of tools across these categories is presented in Extended Data Figure
.
Each tool includes a tool description that will be provided to
TxAgent
as the reference for function call, along with backend code that translates function calls into API requests to these external sources.
Tool description consists of the tool’s name, its purpose, and the arguments it accepts. For each argument, the description specifies its name, purpose, data type, and whether it is mandatory (Examples in Extended Data Figure
).
2.2
ToolGen
: a multi-agent system for constructing tools
ToolGen
is a tool construction multi-agent system for constructing tools that are suitable for
TxAgent
, based on API documentation.
API documentation often varies significantly in format and content, presenting challenges for direct integration into
TxAgent
. For instance, OpenTargets utilizes a GraphQL schema to describe its API; OpenFDA employs Elasticsearch as its API backend and includes documentation to explain available fields; The Monarch Initiative provides RESTful APIs.
This diversity in API representation complicates the process of converting them into tools for
TxAgent
.
ToolGen
system addresses this by organizing the API functions into a set of tools, each with a specific purpose and a clear description that is easily understandable to
TxAgent
.
ToolGen
system comprises three agents: the
summarizer
,
tool generator
, and
tool checker
(Extended Data Figure
a). Since their abilities are simple, these agents are implemented by providing specialized instructive prompts to GPT-4o.
After completing the tool construction, a human evaluation process is conducted to assess the generated tools.
API summarization.
The
summarizer
agent serves as the initial step in the system. It extracts API documentation from a given source to summarize the API’s capabilities. The result is a list of potential functions that could be enabled using the APIs, such as “identify the active ingredients for a drug” and “find disease-related phenotypes”.
Tool construction.
For each capability in the list, the
tool generator
agent refers to the API documentation to create detailed tool specifications. These specifications include the tool’s name, description, arguments, and specialized mapping data to translate arguments into API requests.
Each argument includes the name, description, data type, and an indication of whether it is required.
Mappings for OpenTargets and Monarch Initiative correspond to the query string defined in the GraphQL and RESTful schema, with variables in APIs connected to arguments in the tool. Mapping for OpenFDA employs the search and return fields of Elasticsearch, where search fields are tied to arguments in the tool, and return fields are selected to align with the tool’s description (Extended Data Figure
).
Tool check.
The
tool checker
agent evaluates the validity of generated tools by constructing and testing questions and function calls. In this process, we first verify the mapping, ensuring its correctness by checking the validity of the provided mappings. Next, we randomly sample data points linked to either the input or output of the APIs, such as drug names, disease names, target names, and their corresponding IDs, to test the APIs.
If useful information can be retrieved through API requests, the retrieved data and the tool specifications are sent to the
tool checker
agent. The agent then generates test questions and function call arguments for the tool. If the generated function call arguments produce valid outputs, the tool is deemed functional and valid.
However, if any of the steps in this process fail, the tool is marked invalid and subsequently removed.
Human verification.
After the tool construction process, human experts manually verify and refine the tools. This evaluation includes determining whether the tool has meaningful applications, verifying that it functions as described, and ensuring its stability when handling unexpected inputs. Once this process is complete, the validated tools are included in the
ToolUniverse
.
2.3
Tool Graph
The tool graph is a directed graph that connects tools in
ToolUniverse
. It is used to facilitate the construction of training data. In the tool graph, each node represents a tool, and a directed link is established when the output of one tool serves as the input for another. The presence of a link is determined by providing descriptions of the two tools to an LLM, which then decides if a directed link should exist between them.
Sampling a tool chain from a tool graph enables the construction of complex questions that require multiple rounds of tool calls. Further uses of the tool graph are described in Section
.
The tool graph is used solely for constructing the training dataset, not for the inference process in
TxAgent
, due to the challenges in constructing an exceptionally precise tool graph. Unrestricted by the tool graph,
TxAgent
can seamlessly integrate newly added tools during the inference process.
3
Constructing
TxAgent-Instruct
dataset
We perform instruction tuning on open-source LLMs using a collected
TxAgent-Instruct
dataset to achieve the capabilities of
TxAgent
. This section describes the construction process of
TxAgent-Instruct
.
To achieve comprehensive coverage of specialized treatment and drug information, we employ
QuestionGen
, a question construction multi-agent system that produces diverse questions.
Recognizing the challenges in generating valid reasoning traces that effectively integrate feedback from real-world tools, we design
TraceGen
, a multi-agent system that leverages a helper agent to assist in generating complex, step-wise reasoning traces.
3.1
TxAgent-Instruct
Data Sources
The source information of
TxAgent-Instruct
is collected from the following sources.
OpenFDA
is a health informatics database maintained by the FDA, offering public access to FDA data on approved drugs, devices, and foods
[
20
]
. This work utilizes the drug labeling data provided by the platform, which covers more than 67,000 drugs currently on the market
[
35
]
. OpenFDA includes a search API for retrieving information based on specific query fields.
In this study, we use the drug API of OpenFDA to obtain FDA documentation on various drugs. Each drug entry contains numerous fields, such as indications, boxed warnings, and supply information (Table
1
).
Open Targets
is a platform that integrates data from 23 public resources, including Orphanet, Gene2Phenotype, and ChEMBL
[
21
]
, to facilitate target identification and prioritization. As of September 2024, Open Targets includes 63,121 targets, 28,327 diseases, 18,041 drugs, 17,853,184 evidence entries, and 8,155,988 target-disease associations
[
36
]
.
In this study, we utilize the association data from Open Targets to extract drug-disease relationships, drug status, drug-target interactions, and disease-target associations.
Human Phenotype Ontology from the Monarch Initiative
(HPO) is a database that provides an ontology of medically relevant phenotypes and disease-phenotype annotations
[
22
]
. It includes over 18,000 terms and more than 156,000 annotations linked to hereditary diseases. We leverage HPO to establish connections between diseases and phenotypes.
PrimeKG
is a comprehensive medicine-focused knowledge graph designed to offer a holistic view on diseases
[
28
]
. It incorporates data from 20 high-quality biomedical resources, capturing details about 17,080 diseases and their 4,050,249 relationships across ten key biological scales. In this work, PrimeKG provides the disease list and disease-related information for generating disease-related questions.
3.2
QuestionGen
Multi-agent System for Question Construction
While training
TxAgent
requires a large number of diverse questions that cover different aspects regarding treatment, disease, and drugs, and considers specialized cases such as patient populations, drug side effects, and drug interactions, manually writing these questions would be too costly.
To effectively collect questions,
QuestionGen
system is proposed as a question construction multi-agent system that generates meaningful questions from verified knowledge bases such as FDA documents.
QuestionGen
system begins with the information extraction, which identifies and extracts key information relevant to the desired questions from documents and data sources. Using the extracted information, the question construction step creates questions, corresponding answers, and detailed explanations that clarify how the answer addresses the question.
At last, the question evaluation step verifies questions in multiple aspects.
Question types.
We generate questions through three distinct approaches: drug-centered, disease-centered, and tool-chain-centered question construction.
Drug-centered questions focus on common therapeutic aspects of drugs, including their use in specific patient populations, indications, dosage, safety warnings, and potential risks.
Disease-centered questions address specialized treatment scenarios. These questions incorporate detailed patient profiles, such as phenotypes, medical histories, current medications, and characteristics of the patient population.
Tool-chain-centered questions are generated by randomly sampling a sequence of tools from the
ToolUniverse
tool graph, followed by creating questions based on the selected tool chain, which increases the diversity of questions.
Information extraction.
This step identifies and extracts key information relevant to the desired questions from documents and data sources.
Different information extraction strategies are designed to meet the requirements of various question types.
For drug-centered questions, we randomly sample drugs from the FDA database and retrieve their corresponding FDA documents as raw data sources. From each drug’s FDA document, one field is randomly selected and extracted as the reference data for question construction. To enable question construction beyond just related to drug names, descriptive information about the drug—such as its mechanism of action, indications, and contraindications—is also extracted. This allows for the creation of questions that focus on the drug’s characteristics without explicitly mentioning its name.
For disease-centered questions, we begin by randomly sampling a disease and gathering its description, associated phenotypes, targets, and all potential drugs. For each drug in the list, we retrieve its FDA document and extract information on indications, patient populations, contraindications, warnings, and drug interactions.
The extracted data is then categorized by field and passed to the
information extractor
agent, which compares the drugs across these fields and highlights their differences. The generated comparison serves as the reference for question construction, enabling the creation of challenging, specialized questions that account for subtle differences among drugs.
For tool-chain-centered questions, we first sample a tool-chain from the tool graph starting from common tools such as identify drug ID or disease ID based on names.
Then, we obtain information that can be retrieved by tools and the tool descriptions as the reference for question construction.
Question construction.
In this step, the
Question Generator
leverages reference information extracted during the information extraction process to produce the question
Q
Q
, corresponding answer
G
G
, and explanations justifying why the answers are correct
X
X
. For multiple-choice questions, it also generates answer options.
The inclusion of explanations plays a crucial role, as they ensure the meaningfulness of the generated questions and offer solution hints for the
Helper
agent during reasoning trace generation.
The
Question Generator
operates by prompting GPT-4o with instructions for generating questions. It utilizes multiple prompt variations, each designed for specific question types. During the question-construction process, general guidelines for question creation, reference information, and specific requirements for particular question types are provided as contextual input to the
Question Generator
to produce the questions.
Question evaluation.
The generated question undergoes evaluation based on three key aspects: knowledge-based grounding, answerability, and reasonableness. For each aspect, GPT-4o is prompted to perform the evaluation.
For knowledge-based grounding, to ensure the question is generated from the reference information and not from hallucinations by the language model, both the question and reference information are provided to GPT-4o. GPT-4o is tasked with verifying whether the information in the question is directly derived from the reference information.
For the answerability check, GPT-4o is prompted to assess whether the question can be adequately answered using the provided reference information.
For the reasonableness check, the explanation in the generated question is sent to GPT-4o, which evaluates whether the reasoning behind the explanation is logical and makes sense.
If any of the checks fail, the question is discarded. Otherwise, it is retained and sent to
TraceGen
for reasoning trace construction.
3.3
Reasoning Trace Generation
TraceGen
is designed to generate training data consisting of a reasoning trace
ℛ
\mathcal{R}
and the final answer
A
A
based on the question
Q
Q
. However, generating
ℛ
\mathcal{R}
faces several challenges:
1) Complexity of questions: Many questions require multi-step reasoning and analysis of multiple aspects, making it difficult to generate a single straightforward answer. The challenge is to create a reasoning trace that can handle these complexities effectively.
2) Incorporating external tools: To improve reasoning with the help of a massive number of tools, it’s important to incorporate real-world tools into
ℛ
\mathcal{R}
. The challenge here is integrating the outputs of these tools, rather than relying solely on the internal knowledge of LLMs.
3) Handling uncontrollable tool outputs: The results from external tools are often unpredictable. A key challenge is how to manage failure cases and continue progressing toward a solution, even when tool outputs deviate from expectations.
TraceGen
is a multi-agent system designed to address various challenges through its key components: the
Helper
agent, the
Tool Provider
module, and the
Solver
agent.
The
Helper
agent assists the
Solver
by offering step-by-step solution hints. It has access to the answers and explanations for questions and provides guidance for the next steps in the reasoning process based on the prior steps generated by the
Solver
agent.
The
Tool Provider
presents a selection of potential tools for the
Solver
agent to choose from. These tools are identified based on reference information from the current question and a
ToolRAG
model, which is iteratively trained on previously collected data to improve its recommendations.
Armed with tools from the
Tool Provider
module, hints from the
Helper
agent, the current question, and previously generated reasoning traces, the
Solver
agent iteratively solves the problem. It does so by generating subsequent reasoning steps and function calls until arriving at the final answer.
Providing solution hint with
Helper
.
The
Helper
agent plays a crucial role in assisting the
Solver
by providing solution hints, which is achieved by prompting GPT-4o with instructions. At each reasoning step
i
i
, the
Helper
has access to the problem question
Q
Q
, the ground truth answer
G
G
, and its explanation
X
X
. Additionally, it takes as input the current reasoning trace
ℛ
i
=
{
R
1
,
R
2
,
…
,
R
i
}
\mathcal{R}_{i}=\{R_{1},R_{2},...,R_{i}\}
, which represents all steps generated by the
Solver
up to step
i
i
. Using this information, the
Helper
generates a solution hint, denoted as
ℋ
i
+
1
\mathcal{H}_{i+1}
, which guides the
Solver
toward the next step in the reasoning process.
When the
Solver
provides an answer
A
A
, the
Helper
checks whether
A
A
matches the ground truth answer
G
G
. If
A
=
G
A=G
, the reasoning process is deemed complete. If
A
≠
G
A\neq G
, the
Helper
prompts the
Solver
to reflect on its reasoning and continue the reasoning process. In such cases, the
Helper
generates a hint
ℋ
i
+
1
\mathcal{H}_{i+1}
to guide the
Solver
back into the reasoning process and help refine the answer.
Helper
is defined as:
ℋ
i
+
1
=
Helper
​
(
[
Q
,
G
,
X
]
,
ℛ
i
,
A
)
,
\mathcal{H}_{i+1}=\textsc{Helper}([Q,G,X],\mathcal{R}_{i},A),
(6)
where
A
A
is empty if it is not provided to the
Helper
.
By iteratively providing hints
ℋ
i
+
1
\mathcal{H}_{i+1}
, the
Helper
ensures that the
Solver
progresses logically, generating the reasoning trace until the solution
A
A
is fully constructed and consistent with the ground truth answer
G
G
and explanation
X
X
.
Providing tools with the
Tool Provider
.
The
Tool Provider
module supports the
Solver
by supplying relevant tools during the reasoning process. It operates in two stages. First, the module analyzes the reference information attached to the problem question
Q
Q
and identifies an initial set of tools
𝒫
^
0
\mathcal{\hat{P}}_{0}
from the tool set
ℬ
\mathcal{B}
. These initial tools are provided to the
Solver
at the start of the reasoning process. Second, if the
Solver
determines that no suitable tools are available for a specific reasoning step, it invokes the
ToolRAG
model within the
Tool Provider
module. This model retrieves additional tool suggestions, denoted as
𝒫
^
i
RAG
\mathcal{\hat{P}}_{i}^{\text{RAG}}
, based on the tool descriptions provided by the
Solver
.
By combining these two stages, the
Tool Provider
module ensures that the
Solver
has access to the most relevant tools throughout the reasoning process, either by leveraging the initial set of tools
𝒫
^
0
\mathcal{\hat{P}}_{0}
or dynamically adapting to the problem’s demands with tools
𝒫
^
i
RAG
\mathcal{\hat{P}}_{i}^{\text{RAG}}
from the
ToolRAG
model.
Step-wise reasoning trace generation with
Solver
.
The
Solver
serves as the central component for iteratively generating the reasoning trace
ℛ
\mathcal{R}
and deriving the final answer
A
A
, which is achieved by prompting GPT-4o. We provide the algorithm in Algorithm
. At each step
i
i
, the
Solver
integrates the question
Q
Q
, tools from the
Tool Provider
, solution hints
ℋ
i
\mathcal{H}_{i}
provided by the
Helper
, and its prior reasoning
ℛ
i
−
1
\mathcal{R}_{i-1}
. Using this information, it formulates intermediate thoughts
T
i
T_{i}
and function calls
𝒞
i
\mathcal{C}_{i}
, driving the reasoning process toward a complete and accurate solution.
To simulate the inference process, the
Solver
avoids directly utilizing tools available in the initial set
𝒫
^
0
\mathcal{\hat{P}}_{0}
. Instead, it generates virtual
ToolRAG
calls, which simulate accessing these tools. Each virtual call specifies the tool’s name and its rewritten description from
𝒫
^
0
\mathcal{\hat{P}}_{0}
. These virtual calls are later replaced by actual calls to
ToolRAG
.
When the
Solver
identifies that no suitable tools are available for the current reasoning step, it invokes the
ToolRAG
model within the
Tool Provider
to dynamically suggest additional tools. These new tools, denoted as
𝒫
^
i
RAG
\mathcal{\hat{P}}_{i}^{\text{RAG}}
, are retrieved based on descriptions provided by the
Solver
.
Hints
ℋ
i
+
1
\mathcal{H}_{i+1}
from the
Helper
guide the
Solver
through the reasoning trajectory by suggesting logical next steps. This iterative mechanism allows the reasoning trace to evolve through external tool usage, dynamic adjustments based on feedback, and updates to the reasoning trace. The process continues until the
End
tool suggests a candidate answer
A
A
. If validated by the
Helper
, the reasoning trace
ℛ
\mathcal{R}
and the final answer
A
A
are returned. If the answer is deemed incorrect, the
Solver
removes the corresponding reasoning step and continues refining
ℛ
\mathcal{R}
.
Input:
Question
Q
Q
,
ToolUniverse
ℬ
\mathcal{B}
, ground truth
G
G
, explanation
X
X
Output:
Reasoning trace
ℛ
\mathcal{R}
, final answer
A
A
Initialize
ℛ
←
{
}
\mathcal{R}\leftarrow\{\}
, tools
𝒫
←
{
}
\mathcal{P}\leftarrow\{\}
, step
i
←
0
i\leftarrow 0
;
Obtain initial hints
ℋ
0
\mathcal{H}_{0}
from
Helper
;
Obtain initial tools
𝒫
^
0
\mathcal{\hat{P}}_{0}
from
Tool Provider
;
while
Reasoning is incomplete
do
i
←
i
+
1
i\leftarrow i+1
;
if
Suitable tools exist in
𝒫
\mathcal{P}
then
Generate thought
T
i
T_{i}
and call
𝒞
i
\mathcal{C}_{i}
based on
Q
Q
,
ℋ
i
\mathcal{H}_{i}
, and
ℛ
i
−
1
\mathcal{R}_{i-1}
;
if
Suitable tools exist in
𝒫
^
0
\mathcal{\hat{P}}_{0}
then
Generate thought
T
i
T_{i}
and virtual calls
𝒞
i
\mathcal{C}_{i}
;
foreach
Virtual call in
𝒞
i
\mathcal{C}_{i}
do
Replace virtual
ToolRAG
call with real arguments;
if
No suitable tools in
𝒫
\mathcal{P}
then
Generate thought
T
i
T_{i}
and request additional tools
𝒫
^
i
RAG
\mathcal{\hat{P}}_{i}^{\text{RAG}}
by calling
ToolRAG
with desired tool’s descriptions;
Execute tool calls from
𝒞
i
\mathcal{C}_{i}
and update reasoning trace:
ℛ
←
ℛ
∪
{
R
i
}
\mathcal{R}\leftarrow\mathcal{R}\cup\{R_{i}\}
;
Obtain the next hint
ℋ
i
+
1
\mathcal{H}_{i+1}
from
Helper
;
if
End
tool provides candidate answer
A
A
then
if
Helper
confirms correctness
then
Return
ℛ
,
A
\mathcal{R},A
;
else
Remove the
R
i
R_{i}
from
ℛ
\mathcal{R}
;
Return
ℛ
,
A
\mathcal{R},A
;
Algorithm 2
Step-wise reasoning trace generation with
Solver
Reasoning trace evaluation.
We consider the quality of the reasoning trace to be essential for the performance of
TxAgent
. Evaluating the reasoning trace ensures both its reliability and correctness. This evaluation focuses on two main aspects: correctness and behavior.
For correctness, we examine the correctness of the answer, reasoning trace, and function calls. For answer correctness, in the case of multiple-choice questions, we compare the predicted option with the correct one. For open-ended reasoning questions, GPT-4 is prompted as a judge to determine if the prediction aligns with the correct answer.
For the reasoning trace, we use GPT-4 as a judge, with the question and the ground truth answer serving as references to assess the quality of the reasoning process.
For function calls, we verify that the correct tool is used, and we check the correctness of the argument names, argument value types, and the inclusion of any required arguments.
Even if the generated reasoning trace passes the correctness check, undesired behaviors may still occur, leading to incorrect reasoning during inference. In the behavior check, we examine issues such as hallucinations, arbitrary results, and repeated reasoning.
For hallucinations, we look for hallucinated placeholders in object names and IDs, such as drug names, disease names, and target IDs in function calls. Since IDs for drugs or diseases are not general knowledge, we eliminate reasoning traces where IDs appear without being shown earlier in the context.
The goal of
TxAgent
is to generate verified reasoning traces, meaning the answers should be based on feedback from function calls. However, arbitrary results can arise when answers are derived from the model’s unverified internal knowledge rather than tool feedback. We remove reasoning traces that are based on general knowledge instead of the feedback from the tools.
In more complex cases,
Solver
may generate reasoning traces that include repeated thoughts or function calls.
For repeated thoughts, we assess the similarity between them, and for repeated function calls, we identify steps with identical function calls using the same arguments.
We remove reasoning traces that involve repeated thoughts and function calls.
If the reasoning trace passes all checks, it is retained. However, if it fails due to errors in correctness or undesired behaviors, it is discarded. This evaluation ensures that only high-quality reasoning traces are considered in training data.
3.4
Iterative Training for
ToolRAG
model
ToolRAG
model is used in both
TxAgent
inference process and the training data collection phase.
It utilizes gte-Qwen2-1.5B-instruct
[
37
]
as the base model, which is fine-tuned on pairs of requirements and tool descriptions using the multiple negatives ranking loss.
In the
Tool Provider
module, we use the
ToolRAG
model to identify tools beyond the initial list retrieved from the reference information of the question. While the
ToolRAG
model requires training data from reasoning traces, we propose an iterative training process for
ToolRAG
model, where it is trained on the generated reasoning traces, which in turn helps improve the generation of future reasoning traces.
In the first stage, since the
ToolRAG
model is not yet available, we rely solely on the initial set of tools
𝒫
^
0
\mathcal{\hat{P}}_{0}
that are obtained from the reference information of the question, to generate the reasoning trace. From this trace, we extract pairs of tool requirements and tool descriptions, which are then used to train the
ToolRAG
model.
In the second stage, after the initial training of
ToolRAG
model, we use it to select tools instead of relying exclusively on
𝒫
^
0
\mathcal{\hat{P}}_{0}
. This approach allows the reasoning trace to better reflect real-world use cases, as tools are now retrieved directly by the
ToolRAG
model. Using the data collected from this stage, we continue to gather new pairs for further training of the
ToolRAG
model.
This process is repeated iteratively, continually refining both the
ToolRAG
model and the quality of reasoning trace generation.
4
Training
TxAgent
model
To enable the multi-step reasoning and function call capabilities of
TxAgent
, we fine-tune LLMs using the
TxAgent-Instruct
dataset designed to encompass the diverse behaviors required by
TxAgent
.
This section introduces the training dataset
TxAgent-Instruct
and the training strategies.
4.1
TxAgent
Training Dataset:
TxAgent-Instruct
dataset
We use three agent systems to generate
three training datasets, including a tooling dataset, a therapeutic question dataset, and a reasoning trace dataset.
The question dataset comprises 85,340 therapeutic questions, while the reasoning trace dataset includes 177,626 reasoning steps and 281,695 function calls.
Then, we begin by integrating the question with a reasoning trace and incorporating augmented tools. Next, we break down the complete reasoning trace into step-wise training data.
This process results in the creation of the
TxAgent-Instruct
dataset that contains 378,027 instruction tuning data samples.
The
TxAgent-Instruct
dataset is generated by randomly sampling from drugs in the FDA drug label database and disease phenotypes from the PrimeKG database.
To prevent any leakage of evaluation data through the training data, we remove all drugs approved after 2023.
Constructing step-wise training data.
During supervised fine-tuning, in order to enable
TxAgent
to have step-wise reasoning and function call abilities, we apply step-wise supervision on the thoughts and function calls at each reasoning step. Given a question
Q
Q
, a reasoning trace
ℛ
=
{
R
1
,
R
2
,
R
3
,
…
,
R
M
}
\mathcal{R}=\{R_{1},R_{2},R_{3},\dots,R_{M}\}
consisting of
M
M
reasoning steps, and the final answer
A
A
, where each reasoning step
R
i
R_{i}
is represented as a tuple
R
i
=
{
T
i
,
𝒞
i
,
ℰ
i
}
R_{i}=\{T_{i},\mathcal{C}_{i},\mathcal{E}_{i}\}
— with
T
i
T_{i}
and
𝒞
i
\mathcal{C}_{i}
being the thought and function calls at the
i
i
-th step, and
ℰ
i
\mathcal{E}_{i}
results of function calls — we decompose the reasoning trace into
M
M
step-wise samples for supervision. Each of these step-wise samples consists of an input and an output for the fine-tuned LLM.
For each
i
∈
{
1
,
2
,
…
,
M
−
1
}
i\in\{1,2,\dots,M-1\}
, the input to the model consists of the
system prompt
S
S
, question
Q
Q
, a set of available tools at step
i
i
denoted as
𝒫
i
\mathcal{P}_{i}
, and the reasoning trace up to the previous step, denoted as
ℛ
1
:
i
−
1
\mathcal{R}_{1:i-1}
, which represents the reasoning steps from
R
1
R_{1}
to
R
i
−
1
R_{i-1}
.
The output of the model is the components
[
T
i
,
𝒞
i
]
[T_{i},\mathcal{C}_{i}]
, which correspond to the thought and function calls at step
i
i
.
At the final step
M
M
, the input consists of the system prompt
S
S
, question
Q
Q
and the reasoning trace up to the
M
−
1
M-1
-th step, i.e.,
ℛ
1
:
M
−
1
=
{
R
1
,
R
2
,
…
,
R
M
−
1
}
\mathcal{R}_{1:M-1}=\{R_{1},R_{2},\dots,R_{M-1}\}
, as well as the tools available up to that step,
𝒫
M
\mathcal{P}_{M}
. The output consists of the thought
T
M
T_{M}
, the final function call to the
Finish
tool
𝒞
M
\mathcal{C}_{M}
, and the final answer
A
A
.
Thus, for each
i
∈
{
1
,
2
,
…
,
M
}
i\in\{1,2,\dots,M\}
, the
i
i
-th step-wise sample is:
Input:
\displaystyle\text{Input: }
[
S
,
Q
,
ℛ
1
:
i
−
1
,
𝒫
i
]
,
Output:
[
T
i
,
𝒞
i
]
for
i
∈
{
1
,
2
,
…
,
M
−
1
}
,
\displaystyle\left[S,Q,\mathcal{R}_{1:i-1},\mathcal{P}_{i}\right],\hskip 9.24994pt\text{Output: }\left[T_{i},\mathcal{C}_{i}\right]\hskip 9.24994pt\text{for}\hskip 9.24994pti\in\{1,2,\dots,M-1\},
(7)
Input:
\displaystyle\text{Input: }
[
S
,
Q
,
ℛ
1
:
M
−
1
,
𝒫
M
]
,
Output:
[
T
M
,
𝒞
M
,
A
]
for
i
=
M
.
\displaystyle\left[S,Q,\mathcal{R}_{1:M-1},\mathcal{P}_{M}\right],\hskip 9.24994pt\text{Output: }\left[T_{M},\mathcal{C}_{M},A\right]\hskip 9.24994pt\text{for}\hskip 9.24994pti=M.
While each step in the reasoning trace may involve multiple function calls, we introduce an argument,
id
, which is a randomly generated string, to uniquely identify each function call. This
id
is added to both the function call arguments
𝒞
i
,
k
\mathcal{C}_{i,k}
, and the corresponding results returned by the function
ℰ
i
,
k
\mathcal{E}_{i,k}
.
The
id
is added to the input reasoning trace
ℛ
1
:
M
−
1
\mathcal{R}_{1:M-1}
and is removed in model output as it’s random unpredictable string.
This step-wise decomposition allows for effective supervision of the reasoning process, with each sample providing contextual information about the model’s reasoning at every intermediate step. At the final step, both the reasoning components and the final answer are output together, marking the completion of the reasoning process.
4.2
Training data augmentation
We design several training data augmentation strategies to ensure that
TxAgent
is trained to perform function calls based on contextual information and can generalize to new tools.
Augmenting tools.
To prevent over-fitting to the tools in
ToolUniverse
, we apply augmentation to the tool descriptions by randomly rephrasing all fields of a tool.
For each tool in
ToolUniverse
, we prompt the LLM to rewrite the original description and generate 20 distinct versions of the tool’s name, function description, argument names, and argument descriptions.
For each training sample in
TxAgent-Instruct
, we randomly select from these rewritten fields to create a new, augmented tool description. Then, we replace the tool name and argument names in the function call arguments to generate the augmented training sample.
This strategy enables
TxAgent
to learn how to call functions based on the tool names and arguments, rather than memorizing the specific functions encountered during training.
As a result, the model can generalize to new and unseen tools during inference, enabling flexible scaling of
ToolUniverse
.
Extending the available tool set.
The available tool set
𝒫
\mathcal{P}
(index note of
i
i
-th step is omitted here for simplicity) in each sample of
TxAgent-Instruct
consists of tools used in the reasoning traces. However, during inference, the tools retrieved by the imperfect
ToolRAG
model may include additional candidates, making it challenging for
TxAgent
to select the most suitable tools from the returned set.
To address this, we enhance the tool set
𝒫
\mathcal{P}
by including all tools retrieved by
ToolRAG
model, not just those explicitly used in the reasoning traces. Additionally, we randomly sample several tools from
ToolUniverse
and add them to
𝒫
\mathcal{P}
.
This approach ensures that
TxAgent
learns to effectively select the correct tool from a broader set of candidate tools.
Shuffling the tool list.
To mitigate any potential bias introduced by the position of tools in the tool list
𝒫
\mathcal{P}
, we shuffle the tools in
𝒫
\mathcal{P}
. This ensures that the order in which tools appear does not influence the ability of
TxAgent
to select the correct tool. By randomizing the positions of the tools, we encourage
TxAgent
to focus on the context and descriptions of the tools, rather than their position in the list.
This strategy helps the model learn to make tool selections based on the contextual information rather than relying on the order of the tools in the tool set.
Replacing long results to results summary.
To ensure the training data fits within the context window while preserving the overall reasoning trace, we shorten samples that exceed the maximum context limit by replacing the full tool results with summarized versions. This process begins with the earliest step in the reasoning trace and continues until the total length of the sample is within the context limit.
4.3
Training design
Model.
We use pre-trained LLMs, such as Llama3.1-8B-Instruct, as the base models for fine-tuning on the
TxAgent-Instruct
. The Llama3 series is built on the Transformer architecture
[
38
]
, which leverages self-attention mechanisms to process input sequences in parallel. This enables efficient learning of contextual relationships between tokens.
Our model initialization begins with loading the pre-trained weights from the instruction-tuned version of the Llama3 series, specifically fine-tuned on question-and-answer data. To further adapt the model to our specific task, we apply Low-Rank Adaptation (LoRA) fine-tuning
[
39
]
. LoRA enhances the fine-tuning process by introducing low-rank updates to the pre-trained weights, reducing computational costs and the number of parameters trained. This allows us to efficiently fine-tune the model while preserving the knowledge from the pre-trained LLM.
Training process.
During the training process, the input of one training sample
[
S
,
Q
,
ℛ
1
:
i
−
1
,
𝒫
1
:
i
−
1
]
\left[S,Q,\mathcal{R}_{1:i-1},\mathcal{P}_{1:i-1}\right]
and the corresponding output
[
T
i
,
𝒞
i
]
\left[T_{i},\mathcal{C}_{i}\right]
are formatted according to the instruction-following format of the LLM (e.g., the chat template of Llama).
The formatted text is then processed by the LLM tokenizer to generate a sequence of tokens
𝐱
=
{
x
1
,
x
2
,
…
,
x
N
}
\mathbf{x}=\{x_{1},x_{2},\dots,x_{N}\}
,
where
N
N
is the total number of tokens. These tokens are embedded and passed through the model for autoregressive prediction. The model predicts the next token
x
t
x_{t}
based on all previously generated tokens
{
x
1
,
x
2
,
…
,
x
t
−
1
}
\{x_{1},x_{2},\dots,x_{t-1}\}
, producing a conditional probability distribution
p
⁡
(
x
t
∣
x
1
,
x
2
,
…
,
x
t
−
1
)
p(x_{t}\mid x_{1},x_{2},\dots,x_{t-1})
.
The training objective is to minimize the autoregressive loss, but only for the tokens corresponding to the output sequence
𝐱
⊆
𝐱
out
\mathbf{x}\subseteq\mathbf{x}_{\text{out}}
. The loss is defined as:
ℒ
=
−
∑
t
∈
Idx
out
log
p
(
x
t
∣
x
1
,
x
2
,
…
,
x
t
−
1
)
,
\mathcal{L}=-\sum_{t\in\text{Idx}_{\text{out}}}\log p(x_{t}\mid x_{1},x_{2},\dots,x_{t-1}),
(8)
where
Idx
out
\text{Idx}_{\text{out}}
represents the indices of tokens in
𝐱
\mathbf{x}
corresponding to the output sequence
𝐱
out
\mathbf{x}_{\text{out}}
. By focusing on the output tokens, this loss ensures that the model learns to generate thought and function calls instead of over-fitting to the results from tools.
4.4
Training implementation
Training resources.
We use the Nvidia H100 GPU cluster provided by the Kempner Institute for the Study of Natural and Artificial Intelligence at Harvard University to train
TxAgent
.
For training the
TxAgent
-8B model, we utilize 4 GPUs, totaling 320GB of GPU memory.
Training
TxAgent
-8B requires 9.93 GPU days.
Training infrastructure.
The training infrastructure of
TxAgent
is modified based on several key libraries, including TRL
[
40
]
, Alignment Handbook
[
41
]
, Transformers
[
42
]
, Deepspeed
[
43
]
, and PyTorch
[
44
]
. The fully sharded data parallel (FSDP) technique is employed as the multi-GPU distributed training method. In this setup, the model’s parameters are split across multiple GPUs to reduce memory usage, enabling the training of
TxAgent
with large backend LLMs and long context windows. This approach efficiently distributes both computation and model weights, allowing for better scalability while minimizing communication overhead.
For multi-node training, we leverage the PyTorch implementation of FSDP. For single-node training, the Deepspeed implementation of FSDP is utilized, which is also referred to as Deepspeed Stage 3.
5
Benchmarking
TxAgent
5.1
Benchmarks
We constructed five evaluation benchmarks, including DrugPC, BrandPC, GenericPC, DescriptionPC, and TreatmentPC.
Given that LLMs have been pretrained on vast amounts of publicly available internet data, there is a risk of potential data leakage, meaning that LLMs may have previously encountered similar questions. To mitigate this risk in our evaluation datasets, we focused on creating new datasets centered around drugs approved by the FDA in 2024, reducing the likelihood that the LLMs have been exposed to this specific information. Statistics of all benchmarks are shown in Table
1
.
DrugPC: A comprehensive benchmark covering 11 common therapeutic tasks.
We created the DrugPC dataset, which includes 3,168 questions covering 11 common tasks related to therapy. These sub-tasks include drug overview, drug ingredients, drug warnings and safety, drug dependence and abuse, dosage and administration, use in specific populations, pharmacology, clinical information, nonclinical toxicology, patient-focused information, and storage and supply (as detailed in Table
1
).
To facilitate evaluation, the dataset is formatted as multiple-choice questions, with each question followed by several options (most having 4 options, with some having 2 or 5). The dataset construction process follows these steps:
1) We classify the sections within FDA documents and map them to 11 tasks. The specific fields for each task are outlined in Table
1
.
2) For question construction, we use the text from relevant sections of FDA documents as context. Using the question construction multi-agent system
QuestionGen
, we create questions, multiple-choice options, and corresponding answers that can be answered using the provided context.
The evaluation process checks whether the questions are answerable based on the context provided and ensures that the answers are accurate according to the given information.
3) After construction, a human evaluation process is conducted to carefully review and refine the questions and answers, ensuring that non-biomedical content, such as information about drug manufacturers, is excluded.
BrandPC/GenericPC: Datasets representing drug name in brand and generic forms.
LLM-based methods have been shown to be sensitive to variations, such as representing drugs by either their brand or generic names. To assess the robustness of
TxAgent
, we transform the DrugPC dataset into two versions: BrandPC and GenericPC. In these versions, drug names are systematically replaced with their respective brand or generic names. Problems that do not involve drug names in the questions or options remain unchanged, while those requiring conversion between brand and generic names are also kept as is.
DescriptionPC: A benchmark representing drugs with detailed descriptions.
The drug name plays a crucial role in enabling LLM-based methods to effectively answer questions. However, to evaluate the models’ generalization capabilities in the absence of explicit drug names, we introduce the DescriptionPC benchmark. In this benchmark, drug names are replaced with detailed descriptions that include information such as indications, mechanisms of action, contraindications, and drug interactions.
To ensure the validity of the dataset, we manually remove questions in the DrugPC benchmark that cannot be answered after replacing the drug name with its description. This process results in 626 questions, forming the DescriptionPC benchmark.
While a model might infer an answer without explicitly identifying the drug name from its description, ensuring that the prediction is based on the correct drug rather than exploiting patterns is critical.
To address this, the DescriptionPC benchmark incorporates a two-step evaluation process: drug identification and answer correctness evaluation.
Drug identification
: The model must identify the drug name based on the provided description. Since multiple drugs can share similar descriptions, we construct the ground truth for this step by first collecting drug descriptions corresponding to their original names. We then identify similar drugs that can be described in the same way and include them in the ground truth.
Answer correctness evaluation
: Using the drug names predicted in the first step, the model is tasked with selecting the correct answer from multiple-choice questions.
During the two-step evaluation process, if the drug identification in the first step is incorrect, the second step is automatically marked as incorrect, regardless of the answer’s correctness in that step. This approach ensures that the evaluation rigorously tests the model’s reasoning based on the intended drug descriptions.
TreatmentPC: A specialized treatment benchmark for precision therapy in targeted conditions.
While multiple indications can be applied to a single disease, patients with specific conditions, such as pregnancy or comorbidities, require specialized treatment approaches, such as customized drug selection and dosage adjustments.
The TreatmentPC benchmark is designed to address such specialized treatment scenarios by generating questions based on the varying application conditions of drugs. This is achieved using the question construction system
QuestionGen
.
We first select drugs approved by the FDA in 2024, identifying their indicated diseases.
For each disease, we compile all associated treatments and analyze the unique attributes of each drug.
This analysis is conducted by examining FDA documents, including information on indications, usage in specific populations, safety warnings, precautions, and contraindications.
Next, we generate multi-choice questions that specifically account for differences among drugs. The answer options represent treatments for the disease, but only one is suitable based on the patient’s specific condition. For instance, we include scenarios where a patient is taking other medications that are contraindicated for certain treatments.
The TreatmentPC benchmark requires the model to do a thorough analysis of the patient’s condition before determining an appropriate solution.
5.2
Evaluation strategy
To assess performance on the aforementioned benchmarks, we employ two evaluation strategies: multiple-choice evaluation and open-ended evaluation. Examples of both multiple-choice and open-ended questions can be found in Table
.
Multi-choice evaluation.
In this approach, the question is accompanied by multiple options, and the model must select the correct answer from these options. Accuracy across the dataset is reported as the evaluation metric.
Open-ended evaluation.
The model is presented with only the question, without any options, and is required to generate an open-ended answer. Evaluating such answers is inherently challenging. To address this, we introduce an additional step: the generated open-ended answer is provided as context, and the model is tasked with selecting the correct answer from multiple options based on this context. This allows for the evaluation of open-ended questions by producing quantitative results.
Performance metrics.
For both multi-choice evaluation and open-ended evaluation, we report the accuracy on the benchmark dataset as the performance metrics.
6
Settings for analysis of
TxAgent
6.1
ToolUniverse
vs. LLM-as-tools
In the experiments comparing
ToolUniverse
with LLM-as-tools, we prompt the LLM with the following instruction to make it function as tools:
You are a function that answers the questions based on your given description and given input. Do not answer questions that you don’t have knowledge about.
Here is your definition: {tool description}.
Here is the input to the function:{function call arguments}.
The tool response:
In this instruction, the function call arguments generated by
TxAgent
serve as the input, while the tool description obtained from the
ToolUniverse
is used as a reference. The LLM is then prompted to simulate the tool’s outputs.
6.2
Limit
TxAgent
to function calls only, no thoughts
To verify the role of reasoning thoughts in
TxAgent
, we build a modified version of
TxAgent
that does not generate reasoning thoughts (Algorithm
).
This modified version of
TxAgent
follows a multi-step inference process where, at each step, instead of explicitly reasoning through generating intermediate thoughts, the model directly produces function calls. The process starts with the initialization of the reasoning trace
ℛ
←
{
}
\mathcal{R}\leftarrow\{\}
, the set of available tools
𝒫
←
𝒫
0
\mathcal{P}\leftarrow\mathcal{P}_{0}
, and a step counter
i
←
0
i\leftarrow 0
. In each iteration, the model generates function calls or the final answer:
U
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
𝒫
i
)
.
U_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},\mathcal{P}_{i}).
(9)
If
U
i
U_{i}
contains textual content, it is assigned as the final answer
A
A
, and the
Finish
tool is executed to terminate the reasoning process, returning
ℛ
i
\mathcal{R}_{i}
and
A
A
. Otherwise,
U
i
U_{i}
is the function calls arguments
𝒞
i
\mathcal{C}_{i}
, which are executed. If
𝒞
i
\mathcal{C}_{i}
includes a call to
ToolRAG
, the available tools
𝒫
i
\mathcal{P}_{i}
are updated accordingly. The reasoning trace is iteratively updated as:
ℛ
i
←
ℛ
i
−
1
∪
{
𝒞
i
,
ℰ
i
}
.
\mathcal{R}_{i}\leftarrow\mathcal{R}_{i-1}\cup\{\mathcal{C}_{i},\mathcal{E}_{i}\}.
(10)
Input:
Question
Q
Q
,
ToolUniverse
ℬ
\mathcal{B}
, Initial available tools
𝒫
0
\mathcal{P}_{0}
Output:
Reasoning trace
ℛ
\mathcal{R}
, final answer
A
A
Initialize
ℛ
←
{
}
\mathcal{R}\leftarrow\{\}
, tools
𝒫
←
𝒫
0
\mathcal{P}\leftarrow\mathcal{P}_{0}
, step
i
←
0
i\leftarrow 0
;
while
Reasoning is incomplete
do
i
←
i
+
1
i\leftarrow i+1
;
Generate function calls or final answer:
U
i
=
ℱ
T
​
X
​
(
Q
,
ℛ
i
−
1
,
T
i
,
𝒫
i
)
U_{i}=\mathcal{F}_{TX}(Q,\mathcal{R}_{i-1},T_{i},\mathcal{P}_{i})
if
U
i
U_{i}
contains text
then
Split the text as the final answer:
A
A
;
Execute
Finish
tool to end the multi-step reasoning;
Return
ℛ
i
,
A
\mathcal{R}_{i},A
;
else
𝒞
i
=
U
i
\mathcal{C}_{i}=U_{i}
;
if
call to
ToolRAG
in
𝒞
i
\mathcal{C}_{i}
then
Execute
ToolRAG
and update
𝒫
i
\mathcal{P}_{i}
;
else
Execute tools from
𝒞
i
\mathcal{C}_{i}
;
Update reasoning trace:
ℛ
i
←
ℛ
i
−
1
∪
{
𝒞
i
,
ℰ
i
}
\mathcal{R}_{i}\leftarrow\mathcal{R}_{i-1}\cup\{\mathcal{C}_{i},\mathcal{E}_{i}\}
;
Return
ℛ
,
A
\mathcal{R},A
;
Algorithm 3
TxAgent
multi-step inference process without thoughts.
7
Prompt sketches
This section shows the prompts used to build agents in the data generation multi-agent systems.
For simplicity, we provide prompt sketches that contain an outline of the full prompt that summarizes key points and omits unnecessary details.
7.1
System prompt for
TxAgent
You are a helpful assistant that will solve problems through detailed, step-by-step reasoning and actions based on your reasoning. Typically, your actions will use the provided functions. You have access to the following functions. {functions}
7.2
Prompts for
ToolGen
{API schema}
Using the provided {database name} API Schema, generate all possible specific functional commands in words with no code. Output them in a list.
You are a helpful assistant for generating functions based on the field descriptions and API schema of openFDA:
{API schema, field descriptions, and example functions}
Guidelines:
•
Generate
two functions
: one function retrieves the drug name based on the field information, and the other function retrieves information for that field based on drug names.
•
Align the function with the expected fields and descriptions.
•
Each function must be unique and different from existing examples.
•
Fields should contain search_fields and return_fields:
–
search_fields is a
dict
, where the keys are the function input parameters and the values are the fields to be searched.
–
return_fields is a
list
of field names from which information must be returned.
The capabilities of the functions should be related to the given capabilities: {capabilities}
You are a helpful assistant for generating functions based on the OpenTarget API schema:
{API schema and example functions}
Guidelines for the generated function:
•
The function should align with the schema’s functional and structural requirements.
•
The function’s name, description, input parameters, and schema should be unique and different from the existing example functions.
•
The function capabilities should be related to the given capabilities: {capabilities}
You are a helpful assistant who generates test queries based on a given function. You are provided the following:
•
Function: {generated tool}
•
Related keywords and information for questions and queries:{additional information}
Based on the provided function, you must generate {number} different questions in natural language that require using the function.
Guidelines:
•
The questions should be specific and diverse; avoid general questions
•
Function calls must include “name” and “arguments” arguments
•
Question examples: {examples}
7.3
Prompt for
QuestionGen
You are provided the following information:
•
Disease Information:
These phenotypes or symptoms in the following disease-related information will be used to construct a patient profile.  {disease desc info}
•
Paired Drug Information:
Here is a side-by-side comparison of multiple drug options that help in designing design patient conditions. Consider the side effects, drug interactions, contraindications, and other aspects of these drugs in deciding which patient-specific factors would require someone to take one drug instead of the other options. For example, one drug may be a better option than the others given specific adverse drug-drug interactions, warnings, age restrictions, patient population restrictions, pregnancy considerations, and contraindications. Include such factors in the constructed patient profile to make one drug the definitive correct answer.  {drug information}
Generate a comparison analysis of the selected drugs based on the provided information. Show the differences between the drugs and provide evidence for the differences.
You are an assistant specializing in creating advanced biomedical multiple-choice questions focused on drug treatments given various patient-specific information like diseases, phenotypes, and genetic variation.
Guidelines:
•
Frame questions around patient case scenarios, where a patient is diagnosed with a disease or exhibits specific phenotypes, and the goal is to identify the most suitable treatment. You may also provide protein targets or genes. If additional info is given in the Personalized Information section below, incorporate this info into the profile being constructed.
•
Construct questions and answer choices that compare multiple similar drug treatments and select the most suitable one given the patient’s particular conditions. Incorrect answer choices could be drugs indicated for the disease but unsuitable for this particular patient due to factors like age, comorbidities, or dosage considerations. The correct answer should be the most appropriate drug for the patient’s specific profile.
•
Selected Tools:
Generate questions related to these functions. {selected tools}
•
Disease Information:
Use phenotypes or symptoms in the following disease-related information to construct the patient profile.  {disease desc information}
•
Personalized Information:
When constructing the patient profile, use the following analysis of the side-by-side drug comparison. Consider the side effects, drug interactions, contraindications, and other aspects of these drugs in deciding which patient-specific factors would require someone to take one drug instead of the other options. For example, one drug may be a better option than the others given specific adverse drug-drug interactions, warnings, age restrictions, patient population restrictions, pregnancy considerations, and contraindications. Include such factors in the constructed patient profile to make one drug the definitive correct answer.
Drug information:  { drug information }
Drug comparison analysis:  {side by side drug comparison from Information Extractor agent}
Generate a question, answer, and explanation according to this format:
 {format outline}
You are a helpful assistant for generating expert-level biomedical questions. Based on the given functions, generate a single independent question that focuses on the given drug. The question should be specific, diverse, and framed in multiple ways, requiring the use of as many functions as possible. Do not write a long question; break up the question into multiple sentences if needed. Do not include details that a scientist, physician, or patient would not know (
e.g.,
ontology IDs like MONDO, EFO, CHEMBL, Ensembl/ENS).
Use only the following information:
1.
Functions that can retrieve information related to the drug:  {tool descriptions in the sampled tool chain}
2.
Related information from functions:  {information obtained from tools}
3.
Related information from PrimeKG interactions:  {drug or disease related information from the PrimeKG knowledge graph}
Generate a question, answer, and explanation according to this format:
 {format outline}
You are a helpful assistant to generate meaningful and challenging multi-choice questions for expert biomedical researchers. Formulate biomedical questions and generate answers using only the drug name and field information provided below:
•
Drug generic name: {generic name}
•
Drug brand name: {brand name}
•
Specific field of information for the drug (
e.g.,
contraindications): {field information}
Other guidelines:
•
Generate multiple, different questions to utilize all of the provided information. Make sure the questions do not overlap in content.
•
Formulate questions that can be answered without needing additional information beyond the field information provided.
•
Ask questions in different ways. Don’t always start with “What” and “Which”.
Generate a question, answer, and explanation according to this format:
 {format outline}
7.4
Prompts for
TraceGen
Please act as a helper to provide solution hints for the next step in solving the question. Give some suggestions about what to do next, but never give the final answer or information that directly leads to the final answer. Only provide hints for one reasoning step.
Also, make sure the user’s final answer contains the correct answer. If not, let the user do self-reflection and continue reasoning until the correct answer is found.
•
Question:{question}
•
Correct final answer:{answer}
•
Explanation of correct answer:{explanation}
•
Previous reasoning steps:{reasoning trace}
You must fully understand and solve a question through reasoning and function calls.
Guidelines:
•
For each step, you must generate a reasoning thought and correct function call. If needed, call multiple functions.
•
If you think you have answered the question, thoroughly reflect on your reasoning to verify you have in fact answered the question. If not, continue reasoning. If so, call the ‘Finish’ function and provide your final answer, which should be 1) comprehensive, 2) explain how you arrived at the answer, and 3) why the answer addresses the question.
•
If the result from the last function call is empty or not useful, you must continue reasoning and call ToolRAG (or simulate a virtual ToolRAG call) to retrieve more tools.
–
If the tool you need is in the Function List below, you must retrieve them using a virtual ToolRAG call that simulates obtaining the tool through ToolRAG.
–
If the tool you need is not in the Function List below, you need to call ToolRAG.
–
{Description of ToolRAG and virtual ToolRAG tools}
•
Do not answer the question based on general knowledge. You must answer the question based on the information returned by the tools.
•
If all previous solution attempts have failed, do not repeat the same thoughts and function calls. Instead, come up with new solution approaches.
Function List:  {available tools description of the initial set of tools
𝒫
^
0
\mathcal{\hat{P}}_{0}
}
For each reasoning step, respond in this JSON format:  {reasoning step format}
For the final step, respond in this JSON format, providing the final answer and a detailed explanation:
 {final reasoning step format}
Previous reasoning steps:  {previous multi-step reasoning trace}
Hint for next step:  {solution hint from Helper agent}
References
\spacing
0.85
References
[1]
Huang, K.
et al.
A foundation model for clinician-centered drug repurposing.
Nature Medicine
30
, 3601–3613 (2024).
[2]
Dubey, A.
et al.
The llama 3 herd of models.
arXiv preprint arXiv:2407.21783
(2024).
[3]
Radford, A., Narasimhan, K., Salimans, T., Sutskever, I.
et al.
Improving language understanding by generative pre-training (2018).
[4]
Jiang, A. Q.
et al.
Mistral 7b.
arXiv preprint arXiv:2310.06825
(2023).
[5]
Touvron, H.
et al.
Llama: Open and efficient foundation language models.
arXiv preprint arXiv:2302.13971
(2023).
[6]
Bai, J.
et al.
Qwen technical report.
arXiv preprint arXiv:2309.16609
(2023).
[7]
Singhal, K.
et al.
Large language models encode clinical knowledge.
Nature
620
, 172–180 (2023).
[8]
Singhal, K.
et al.
Toward expert-level medical question answering with large language models.
Nature Medicine
1–8 (2025).
[9]
Chen, Z.
et al.
Meditron-70b: Scaling medical pretraining for large language models.
arXiv preprint arXiv:2311.16079
(2023).
[10]
Alber, D. A.
et al.
Medical large language models are vulnerable to data-poisoning attacks.
Nature Medicine
1–9 (2025).
[11]
Yan, F.
et al.
Berkeley function calling leaderboard.
https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html
(2024).
[12]
Dadao, I.
watt-tool-8b: A fine-tuned language model for tool usage and multi-turn dialogue.
https://huggingface.co/watt-ai/watt-tool-8B
(2025).
[13]
Liu, W.
et al.
Toolace: Winning the points of llm function calling.
arXiv preprint arXiv:2409.00920
(2024).
[14]
Gao, Y.
et al.
Retrieval-augmented generation for large language models: A survey.
arXiv preprint arXiv:2312.10997
(2023).
[15]
Gao, S.
et al.
Empowering biomedical discovery with ai agents.
Cell
187
, 6125–6151 (2024).
[16]
Boiko, D. A., MacKnight, R., Kline, B. & Gomes, G.
Autonomous chemical research with large language models.
Nature
624
, 570–578 (2023).
[17]
Yao, S.
et al.
React: Synergizing reasoning and acting in language models.
In
International Conference on Learning Representations (ICLR)
(2023).
[18]
Bran, A. M.
et al.
Chemcrow: Augmenting large-language models with chemistry tools.
arXiv preprint arXiv:2304.05376
(2023).
[19]
Swanson, K., Wu, W., Bulaong, N. L., Pak, J. E. & Zou, J.
The virtual lab: Ai agents design new sars-cov-2 nanobodies with experimental validation.
bioRxiv
2024–11 (2024).
[20]
Kass-Hout, T. A.
et al.
Openfda: an innovative platform providing access to a wealth of fda’s publicly available data.
Journal of the American Medical Informatics Association
23
, 596–600 (2016).
[21]
Ochoa, D.
et al.
The next-generation open targets platform: reimagined, redesigned, rebuilt.
Nucleic acids research
51
, D1353–D1359 (2023).
[22]
Castellanos, F.
et al.
The human phenotype ontology in 2024: phenotypes around the world.
Nucleic Acids Research
52
(2024).
[23]
OpenAI.
Gpt-4o (2024).
[24]
Gallifant, J.
et al.
Language models are surprisingly fragile to drug names in biomedical benchmarks.
arXiv preprint arXiv:2406.12066
(2024).
[25]
Chen, C.
et al.
Clinicalbench: Can llms beat traditional ml models in clinical prediction?
arXiv preprint arXiv:2411.06469
(2024).
[26]
Guo, D.
et al.
Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
arXiv preprint arXiv:2501.12948
(2025).
[27]
Lewis, P.
et al.
Retrieval-augmented generation for knowledge-intensive nlp tasks.
Advances in Neural Information Processing Systems
33
, 9459–9474 (2020).
[28]
Chandak, P., Huang, K. & Zitnik, M.
Building a knowledge graph to enable precision medicine.
Nature Scientific Data
(2023).
[29]
Ji, C. C.-J.
et al.
Gorilla openfunctions v2 (2024).
[30]
OpenAI.
Introducing openai o1-preview (2024).
[31]
Gloss, D., Moxley, R. T. I., Ashwal, S. & Oskoui, M.
Practice guideline update summary: Corticosteroid treatment of duchenne muscular dystrophy.
Neurology
86
, 465–472 (2016).
[32]
Matsuo, M.
Antisense oligonucleotide-mediated exon-skipping therapies: precision medicine spreading from duchenne muscular dystrophy.
JMA journal
4
, 232–240 (2021).
[33]
Su, X.
et al.
Multimodal medical code tokenizer.
arXiv:2502.04397
(2025).
[34]
Brown, T.
et al.
Language models are few-shot learners.
Advances in neural information processing systems
33
, 1877–1901 (2020).
[35]
U.S. Food and Drug Administration.
openfda (2024).
[36]
Targets, O.
24.09 platform release now live.
https://community.opentargets.org/t/24-09-platform-release-now-live/1556?ref=blog.opentargets.org
(2024).
[37]
Li, Z.
et al.
Towards general text embeddings with multi-stage contrastive learning.
arXiv preprint arXiv:2308.03281
(2023).
[38]
Vaswani, A.
Attention is all you need.
Advances in Neural Information Processing Systems
(2017).
[39]
Hu, E. J.
et al.
Lora: Low-rank adaptation of large language models.
arXiv preprint arXiv:2106.09685
(2021).
[40]
von Werra, L.
et al.
Trl: Transformer reinforcement learning.
https://github.com/huggingface/trl
(2020).
[41]
Tunstall, L.
et al.
The Alignment Handbook.
[42]
Wolf, T.
et al.
Transformers: State-of-the-art natural language processing.
In
Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations
, 38–45 (Association for Computational Linguistics, Online, 2020).
[43]
Rasley, J., Rajbhandari, S., Ruwase, O. & He, Y.
Deepspeed: System optimizations enable training deep learning models with over 100 billion parameters.
In
Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining
, 3505–3506 (2020).
[44]
Paszke, A.
et al.
Automatic differentiation in pytorch.
In
NIPS-W
(2017).