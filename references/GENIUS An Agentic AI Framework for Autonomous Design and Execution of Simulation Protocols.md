GENIUS: An Agentic AI Framework for Autonomous Design and Execution of Simulation Protocols
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY 4.0
arXiv:2512.06404v1 [cs.AI] 06 Dec 2025
GENIUS: An Agentic AI Framework for Autonomous Design and Execution of Simulation Protocols
Mohammad Soleymanibrojeni
Affiliation:
Karlsruhe Institute of Technology,
Institute of Nanotechnology Hermann-von-Helmholtz-Platz,
Karlsruhe, 76021, Germany
Roland Aydin
Affiliation:
Hamburg University of Technology,
Eißendorfer Straße 42, Hamburg, 21073, Germany
Diego Guedes-Sobrinho
Affiliation:
Federal University of Paraná,
Department of Chemistry,
Curitiba,
81531-980,
Brazil
Alexandre C. Dias
Affiliation:
University of Brasília,
Institute of Physics and International Center of Physics,
Brasília,
70919-970,
Brazil
Maurício J. Piotrowski
Affiliation:
Federal University of Pelotas,
Department of Physics,
Pelotas,
96010-900,
Brazil
Wolfgang Wenzel
Affiliation:
Karlsruhe Institute of Technology,
Institute of Nanotechnology Hermann-von-Helmholtz-Platz,
Karlsruhe, 76021, Germany
Celso Ricardo Caldeira Rêgo
Affiliation:
Karlsruhe Institute of Technology,
Institute of Nanotechnology Hermann-von-Helmholtz-Platz,
Karlsruhe, 76021, Germany
Affiliation:
Corresponding author
:
celso.rego@kit.edu
Abstract
Predictive atomistic simulations have propelled materials discovery, yet routine setup and debugging still demand computer specialists. This know-how gap limits Integrated Computational Materials Engineering (ICME), where state-of-the-art codes exist but remain cumbersome for non-experts. We address this bottleneck with GENIUS, an AI-agentic workflow that fuses a smart Quantum ESPRESSO knowledge graph with a tiered hierarchy of large language models supervised by a finite-state error-recovery machine. Here we show that GENIUS translates free-form human-generated prompts into validated input files that run to completion on
≈
80
%
\approx$80\text{\,}\mathrm{\%}$
of
295
295
diverse benchmarks, where
76
%
76\text{\,}\mathrm{\%}
are autonomously repaired, with success decaying exponentially to a
7
%
7\text{\,}\mathrm{\%}
baseline. Compared with LLM-only baselines, GENIUS halves inference costs and virtually eliminates hallucinations. The framework democratizes electronic-structure DFT simulations by intelligently automating protocol generation, validation, and repair, opening large-scale screening and accelerating ICME design loops across academia and industry worldwide.
keywords
Computational materials science, Large language models, Knowledge graphs, Quantum ESPRESSO, Automated error handling, Integrated Computational Materials Engineering
Introduction
Computational simulations have revolutionized materials design, accelerating innovation by allowing researchers to explore material properties and their behaviors virtually before experimental validation
[
15
,
33
,
3
,
6
]
. This shift has led to significant breakthroughs that range from energy storage
[
40
,
27
]
to pharmaceutical development
[
16
,
22
]
. However, a persistent challenge undermines this potential: the technical barriers to effective simulation setup disproportionately burden researchers, particularly those whose expertise lies in experimental rather than computational domains. When scientists identify a promising new compound, understanding its fundamental properties often requires computational validation. Yet, even seemingly straightforward simulations frequently lead to lengthy technical challenges. Even experienced computational scientists (physicists, chemists, engineers) find themselves diverted from scientific inquiry toward navigating complex programming challenges, engaging in trial-and-error attempts, and struggling with computational setup details rather than focusing on the scientific questions
[
32
]
.
Integrated Computational Materials Engineering (ICME) has emerged as a robust framework to accelerate materials development by synergizing experimental data, simulations, and theoretical models across multiple scales. ICME aims to streamline the transition from laboratory discovery to industrial application through predictive modeling
[
2
,
37
]
. However, its full potential remains constrained by what implementation science describes as
know-do gap
, the disparity between available computational tools and their practical application by the broader scientific community. This gap persists despite the availability of a wide range of these tools. The open source community has made remarkable progress in the accuracy and consistency of computational codes. Recent community-wide benchmarks demonstrate that modern DFT codes and pseudopotentials now yield near-identical equations of state for elemental crystals, approaching experimental precision
[
26
,
19
]
. This technical convergence suggests that the tools are mature, yet the human interface to these tools remains a significant bottleneck. The time spent on technical implementation rather than scientific thinking dramatically slows the pace of discovery.
As current approaches to the simulation protocol creation rely on predefined or rigid parameter settings across several programs
[
10
,
4
,
34
]
, the complexity of integrating different computational tools remains challenging. Creating and validating these protocols requires that the user manually interact with the databases to collect relevant data. Furthermore, users must technically master several computational tools’ syntax and possess deep expertise in all of them, practically becoming experts in the documentation by debugging protocols when errors occur. Although state-of-the-art (SOTA) electronic-structure codes are accurate, open, and widely accessible, their routine use still demands technical expertise that many domain scientists find challenging. This expertise barrier narrows the pool of researchers who can exploit computational materials science. It creates barriers that drain time and delay critical discoveries, slowing theory translation into concrete advances in batteries, catalysts, and structural alloys. Implementation science principles
[
28
,
38
]
, the field that studies how evidence-based practices move from the laboratory into everyday use, offer a path forward. By diagnosing and dismantling the educational, cultural, and infrastructural obstacles that restrict the adoption of evidence-based tools, this principle can shrink the
know–do gap
separating mature computational capabilities from the needs of working material scientists. The goal is not to invent another method but to democratize the already powerful methods, freeing researchers to focus on scientific questions rather than software configuration and workflow maintenance. In doing so, we can accelerate how computational insights can become real-world materials innovations, which might otherwise transform industries and address global challenges.
To address this critical interface bottleneck and bridge the
know-do gap
, this paper introduces GENIUS, an AI-driven agentic framework combining large language models (LLMs)
[
20
]
with a smart knowledge graph (KG)
[
39
]
employing reinforcement learning with verifiable rewards
[
24
,
11
,
21
]
, that in our case interprets the schema, enforces constraints, reformulates questions, and surfaces only consistent answers. This framework acts as an intelligent interface to computational tools, specifically designed here for generating and automatically debugging simulation protocols based on Density Functional Theory (DFT), and to validate our approach, we choose the Quantum ESPRESSO (QE) program
[
12
]
. A schematic overview of this framework is presented in Fig.
1
. The mechanisms of the smart KG with the LLMs infer relevant parameters by understanding both explicit and implicit conditions within the user’s request, then critically evaluate the retrieved information to ensure its suitability and context. This process provides accurate and structured knowledge to the LLM, mitigating limitations such as hallucinations
[
29
,
25
]
and enabling reliable protocol generation tailored to user requirements, including material specifics from curated databases. Furthermore, the framework incorporates robust automated error handling capable of debugging and validating protocols when initial attempts fail, overcoming a significant hurdle during the generation of the protocols in practical simulation workflows. This integrated approach addresses the inherent limitations of current AI models when applied to precise scientific tasks.
GENIUS reshapes who can participate in computational materials research by bridging technical computational tasks with the nature of the materials. We connect previously discrete manual tasks into one integrated AI system by evaluating the researcher’s request, generating compliant simulation protocols, validating, and handling errors automatically. This integration improves the reproducibility, re-usability, and transferability of simulation protocols
[
32
,
14
]
while making advanced simulations accessible to researchers regardless of their computational background. Our work advances both in ICME and in the implementation of science objectives: we enhance the ICME paradigm by making its computational tools more accessible, while applying implementation science principles to overcome adoption barriers in computational materials research. By allowing researchers to focus on scientific questions rather than technical implementation, GENIUS delivers incremental efficiency gains while enabling a fundamental shift in how—and by whom—materials discovery can be conducted
[
17
]
. In the following sections, we detail the creation of the smart QE KG and explain the framework’s architecture, including its specialized agents and subsystems, such as recommendation, protocol generation, and automated error handling. We present benchmarks assessing the framework’s performance across several computational tasks.
Figure 1
:
GENIUS framework for autonomous Quantum ESPRESSO simulations. This schematic illustration depicts the end-to-end workflow of the GENIUS framework, designed to overcome technical barriers in DFT simulations. Users’ Natural language prompts are interpreted by a recommendation system powered by a smart knowledge graph that encodes Quantum ESPRESSO parameter details and constraints. Large language models then generate the corresponding simulation protocols. The framework includes automated validation and an Automated Error Handling (
AEH
(
error 1
and
error 2
) loop that utilizes a knowledge graph and Large language models to diagnose and correct failed runs iteratively. This integrated process autonomously translates user intent into validated Quantum ESPRESSO input files, ready for submission to the available computational resources.
Methods
We developed GENIUS to overcome the technical challenges in computational materials science and made the QE code simulation methods more accessible to researchers within the domain-knowledge context. Although we focus here on QE as a representative case, this approach can easily be extended to any atomistic simulation code, including molecular dynamics. This framework combines LLMs with a smart KG, serving as an intelligent interface between users and QE to automate the generation, validation, and debugging of complex simulation protocols. Our system architecture comprises three main components, which are: (
i
i
) a recommendation system, (
i
​
i
ii
) a protocol generation module, and (
i
​
i
​
i
iii
) an automated error handling system (denoted as
error 1
and
error 2
) as shown in Fig.
1
. These components are designed to handle specific aspects of the workflow, from user input to final protocol generation. The framework prioritizes reproducibility, accuracy, and user adaptability, aligning with computational materials research’s best practices and scientific standards. Therefore, references to computational resources, model names, service providers, or other entities are made by name, as these are considered common knowledge within the relevant fields.
System Architecture Overview
In GENIUS, our three-tier QE simulation protocol generation architecture is based on a set of sequential propositions. (
i
i
) Recommendation System: This is the interface between the user and the protocol generation pipeline. It comprises submodules responsible for collecting material-specific information, retrieving relevant QE simulation parameters, and evaluating them. This information is formulated into a template recommended to the protocol generation system. The template includes a collection of parameters with suggested values and data types (
CHARACTER
,
REAL
,
INTEGER
,
LOGICAL
), followed by materials-specific information like atomic positions and appropriate element-specific pseudopotentials. (
i
​
i
ii
) Protocol Generation System: It generates the simulation protocol based on the template provided by the recommendation system. The system may not utilize all suggested parameters, as the final selection occurs during protocol generation, considering the user’s prompt and additional context provided to the LLM. The generated input is syntactically validated by running the QE program. Upon successful validation, the workflow concludes. If validation fails, the automated error handling module is triggered. (
i
​
i
​
i
iii
) Automated Error Handling System: It receives the current generated simulation protocol and the error messages from the QE program, and extracts relevant documentation based on these messages. Using the currently generated protocol and extracted documentation, the error can be resolved, and the protocol can be revalidated. Each LLM is allocated a specific number of attempts to resolve the error. If the error persists, the system switches to the next, presumably more capable LLM in a predefined hierarchy. If all attempts fail, the process terminates with a failure message.
System Components Integration
The framework employs a finite state machine (FSM) architecture to manage component interactions and the workflow progression. Each component operates as a distinct FSM state node, with clearly defined transition conditions depending on the state of the executed process. The FSM implementation has an (
i
i
) Entry Node: to initialize the framework and validate user inputs, (
i
​
i
ii
) State Transitions: defined by the success or failure conditions at each processing step, (
i
​
i
​
i
iii
) Error Recovery States: implementing retry mechanisms (for I/O, network, validation), and (
i
​
V
iV
) Terminal States: indicating either Success (valid protocol generation) or Failure (unresolved error). The overall framework is illustrated in Fig.
2
.
Figure 2
:
State diagram of the AI-driven framework for generating QE simulation protocols. The diagram is organized into four composite states (dashed boxes): RecommendationSystem parses the user’s natural-language request (‘Interface’ → ‘InitializeWorkflow’), retrieves materials data (‘MaterialsDb’) and simulation parameters (via ‘DocumentCollection’ → ‘ConditionExtraction’ → ‘RetrieveCandidateParameters’), and evaluates them (‘EvaluateParameters’) to produce a structured input template. ‘ProtocolGeneration’ uses that template (‘PrepareInputTemplate’) to generate the actual QE input file (‘QeInputGeneration’). ‘ExecutionValidation’ runs the simulation (‘QeRun’), transitioning to ‘Finished’ on success. ‘AutomatedErrorHandling’ detects failures (‘FailureDetected’ → ‘CheckRetries’) and either retries execution (‘AttemptCorrection’), switches to an alternative model (‘SwitchModel’), or terminates at ‘Failure’ if all options are exhausted. Solid arrows show transitions labeled with the triggering action or condition; color and class styling differentiate data sources, main processes, and error-handling loops; more details can be found in the GitHub
repository
.
Smart Knowledge Graph
The user interfaces with the original documentation, as provided, via our developed smart KG, as shown in Fig.
3(a)
, which displays the structure of the QE KG. The user can search the nodes and look for the connectivity between them. Although we performed some manual refinement, it should be noted that the parameter descriptions remain faithful to the original documentation. The KG is the recommendation system’s core component, comprising
247
247
nodes and
330
330
connectivity edges, providing structured and connected information extracted from the QE program documentation. The data source for the QE knowledge graph is the online documentation for the QE
pw.x
code, which can be found at
https://www.quantum-espresso.org/Doc/INPUT_PW.html
. Initially, the documentation was converted into a plain
.txt
version, as QE uses parameters organized into
nameless
sections and
cards
, each with distinct syntax and purposes, which made this format easier to manage than the original
HTML
format. As a result, information was extracted separately for each type. The curated documentation was then transformed into a key-value pair format using
anthropic/claude-3.5-sonnet
[
8
]
language model, followed by manual verification and adjustments. For a complete description of the resulting key-value schema (including all namelist and card entries, their
connections
and
conditions
keys, and illustrative
JSON
examples such as the parameter
nspin
and card
ATOMIC_SPECIES
given in Fig.
3(b)
–Fig.
3(c)
), please refer to our GitHub repository at
https://github.com/KIT-Workflows/agentic-workflow-framework/blob/main/knowledge_graph_schema.md
. Given the specialized expertise required, improving the KG, particularly the
connections
and
conditions
, remains an area for future work and potential community contributions. We refer to this object as
smart
when we name it as
smart
knowledge graph to distinguish it from a plain.
The nodes are retrieved from the KG using two complementary approaches: (
i
i
) direct keyword matching and (
i
​
i
ii
) context-aware retrieval based on graph relationships and inferred logical conditions. A threshold of top
70
%
70\text{\,}\mathrm{\%}
cosine similarity
[
36
]
is used as the cutoff for the retrieval, increasing the number of nodes for evaluation, which means more computational resources are required. A hashing vectorizer is employed for node embedding, since it is robust, reliable, fast, and works well with large corpora. Due to the domain-specific nature of calculation requests, retrieval based on keywords and inferred conditions proved highly effective and efficient compared to denser embedding representations. Additionally, implicit conditions were inferred from the user’s input request. For example, when a calculation mentions the
Cu
surface, bulk, or elemental system, the
Metallic systems
condition is automatically invoked. We extracted
162
162
conditions under nine different categories to facilitate knowledge retrieval. These nine categories are: calculation type, functional and method, cell and material properties, pseudopotential, magnetism (and spin), isolated systems (by including boundary conditions),
k
-point settings, electric field conditions, and occupation types. User input requests are processed under these nine categories, and the explicit and implicit relevant conditions are extracted. Each condition serves as an access key to nodes in the KG. This inference of implicit conditions allows the KG to provide relevant information even when not explicitly requested, significantly enhancing the contextual understanding presented to the user or downstream tasks.
(a)
Screenshot of the web interface for the Quantum ESPRESSO knowledge graph, enabling interactive exploration of nodes and their relationships.
(b)
Example
JSON
structure for a namelist parameter node
’nspin’
in the knowledge graph, showing its attributes and inter-parameter relationships.
(c)
Example
JSON
structure for a card node
’ATOMIC_SPECIES’
, illustrating its complex syntax and conditional options.
Figure 3
:
The three panels illustrate the structure and interface of the QE knowledge graph and how individual QE input parameters are formalized as machine-readable nodes and exposed through an interactive graph that makes their dependencies explicit.
Large Language Model Integration
We employed LLMs to perform various tasks, including user prompt interfacing for material information, keyword extraction for KG retrieval, evaluation of QE parameters, and processing QE error messages. Users choose the LLM based on accuracy, cost, context window length, and runtime availability. For initial interfacing, condition extraction, and parameter evaluation, we used
mistralai/mixtral-8x22b-instruct
[
30
]
. For error keyword extraction,
databricks/dbrx-instruct
[
9
]
was employed. Our core protocol generation involved a hierarchical model structure with two worker models (
databricks/dbrx-instruct
,
meta-llama/llama-3.1-405b-instruct
)
[
1
]
and one referee model
anthropic/claude-3.5-sonnet
[
8
]
. Additionally,
google/gemini-2.0-flash-001
[
13
]
was used for pre-processing user prompts to extract scoring metrics. This framework validates the effectiveness of the knowledge graph and the automated error-handling system, providing insights into LLM capabilities.
We implemented two main prompt engineering strategies. The first aimed to provide contextual scaffolding to the LLM, and the second strategy focused on extracting structured information. The first is used for subsequent LLM inputs and further processing or initiating other framework components; when generating textual responses, the LLM was guided to explain the current context and then expand upon it, making a reasoned conclusion based on incrementally acquired in-context knowledge. Such a technique was crucial for error handling and resolution, but less critical for tasks like keyword extraction. The second strategy, aimed at structured information extraction, employed explicit schema definitions with expected keys and data types, supported by few-shot examples, ensuring that the output was a valid
JSON
object. The LLM’s raw output was extracted using regular expressions and parsed into a Python dictionary. This method helped to secure downstream integration for API calls and system updates.
As displayed in panel Fig.
4(b)
, user calculation prompts are parsed to extract keywords and calculation conditions. This structured output facilitates three parts of access to KG nodes. (
i
i
) The required nodes corresponding to essential QE parameters for any calculation are included. (
i
​
i
ii
) A keyword search is performed using the extracted keywords against the raw text of the knowledge graph. The top
70
%
70\text{\,}\mathrm{\%}
of nodes ranked by relevance (cosine similarity) are selected. This text search utilizes a hashing vectorizer (
scikit-learn
implementation) with
2
17
2^{17}
features to vectorize the raw text in the knowledge graph and the query keywords. (
i
​
i
​
i
iii
) QE-specific conditions are extracted from the user’s prompt. We identified
164
164
unique conditions across nine categories within the QE documentation. The user’s prompt is parsed to identify applicable conditions within these categories. Each matched condition activates relevant KG nodes. The nodes connected to the collected nodes are added to the final set. The nodes from these three parts are concatenated and sent for evaluation. Each selected node (QE parameter) is assessed based on the user’s prompt and calculation conditions to determine an appropriate value. If a parameter is evaluated as non-relevant, it gets
None
as a value and is excluded.
(a)
Schematic of the minimal
JSON
payload accepted by the
POST /workflow/
REST endpoint. The object defines the free-text
calculation_prompt
, the ordered
gen_model_hierarchy
, per-task
model_config
, optional interface-agent kwargs, the target LLM API, and an optional project configuration.
(b)
The browser dashboard wraps the same parameters in a point-and-click interface: users paste an API key, enter their calculation prompt, select a model hierarchy, and launch or abort the run. A live log pane streams Server-Sent Events for real-time monitoring. The two views illustrate parity between programmatic and interactive control of the GENIUS workflow service.
Figure 4
:
Comparison of workflow service JSON payload and the web interface.
Prompt Dataset and Complexity Mapping
As depicted in Fig.
4(b)
, the framework provides a web interface through which users submit free-form calculation prompts. Moreover, since material-structure geometries can be inconsistent when directly extracted from different models, we employ an agent responsible for retrieving and standardizing all structural data from the specified database to ensure the reproducibility of the DFT calculations. Upon submission, the system parses the text, extracts the material formula or structure, and automatically routes the request to the appropriate Materials Cloud database (MC2D or MC3D) based on whether the target compound is two- or three-dimensional
[
18
,
7
]
. To benchmark the interface under realistic conditions, we assembled more than 400 prompts from independent researchers without prior knowledge of the framework’s internal design. After verifying that each requested material was available in MC2D or MC3D, we selected
295
295
prompts for testing the framework. We quantified the prompt complexity with a score-based rubric inspired by Brown
et al.
[
5
]
. Using the
google/gemini-2.0-flash-001
model, we extracted ten linguistic and domain-specific features from every prompt; each feature present assigned
+
1
+1
to the total score. Prompts scoring
0
​
–
​
4
0\text{\textendash}4
,
5
​
–
​
8
5\text{\textendash}8
, and
9
9
or more were labeled basic, standard, and complex, respectively. The complete scoring scripts and prompt dataset are available in our public
repository
[
35
]
for more details.
Automated Error Handling (
AEH
)
The framework incorporates an automated error handling (
AEH
) system designed to mitigate the critical challenge of time-consuming manual debugging when simulations fail. Following the generation of a simulation protocol, the QE program is executed. If the execution fails, QE generates a
CRASH
file containing a descriptive error message. An LLM processes this message to extract relevant keywords, which are then used to query the smart KG for relevant information. The retrieved nodes provide contextual information to the LLM, which then attempts to formulate a solution to the encountered error. Each LLM within the hierarchical architecture is allocated a predefined number of retries. Logs from previous unsuccessful attempts within the same model’s retry cycle are omitted from the LLM input due to their length and potential lack of immediate usefulness. If an LLM uses all its retries without resolving the error, it switches to the next model in the hierarchy. The subsequent model restarts the error resolution process from the beginning, using the initial output from the recommendation module as its starting point. The overall effectiveness of the
AEH
system is thus significantly dependent on the clarity and informational content of the
CRASH
file combined with the KG, operating within a self-consistent feedback loop. The QE
PWSCF v.7.2
package
[
31
]
serves as the execution-level validator for the generated simulation protocols. A protocol is considered valid if the QE simulation completes successfully, as indicated by the absence of a
CRASH
file and a zero exit code. Conversely, an invalid protocol results in a non-zero exit code and the generation of a
CRASH
file that contains a detailed error description.
Logs were collected from executing the
295
295
curated calculation prompts to track the framework’s evolution. Each log file records the terminal status of the workflow (success or failure) and, in the case of successful runs, includes the number of attempts and any model switches that occurred during the automated error-handling phase. The primary metric for assessing the efficiency of protocol generation is the number of attempts and model switches required to achieve a successful outcome. A zero value indicates zero-shot generation, indicating that the initial protocol generated by Model 1, using the recommendation system’s output, was successful on the first attempt, without requiring any intervention from the
AEH
system. The primary requirements are the capability to interact with LLM provider APIs and to execute the QE program for protocol validation. Some tools, such as the Atomic Simulation Environment (ASE),
scikit-learn
, and
networkx
, were also used. Additional dependencies are standard Python libraries. The workflow API is a
RESTful
design written in
FastAPI
, managing the workflow through standardized
HTTP
endpoints. Once the workflow server is initialized, its primary endpoint
POST "/workflow/"
accepts
JSON
payloads that specify calculation parameters, model configurations, and optional project settings, as shown in Fig.
4(a)
. The service provides additional workflow management through other endpoints for: Status monitoring (
GET "/workflow-status/{workflow_id}"
), Result retrieval (
GET "/results/{workflow_id}"
), and Visualization access (
GET "/timeline/{workflow_id}"
). Real-time monitoring is enabled via Server-Sent Events (SSE) at the
/logs
endpoint, as illustrated in Fig.
4(b)
. These approaches facilitate programmatic integration with other AI-driven applications while supporting interactive human user experiences.
Results
We tested GENIUS with multiple LLMs to evaluate our approach, each exhibiting incremental capabilities, to obtain more comprehensive diagnostic insights into the workflow’s performance. By gathering a large dataset of human-generated prompts for DFT calculations through QE and collecting the corresponding workflow logs (see Fig.
7
), we analyzed how many attempts were required to complete each prompt successfully. These prompts were authored by chemists and physicists who routinely perform DFT simulations with electronic-structure packages other than Quantum ESPRESSO, ensuring that the benchmark reflects realistic expert usage while remaining unbiased toward QE-specific syntax.
To understand the diversity of the prompts dataset, we converted the
295
295
prompts into
3072
3072
-dimensional embedding vectors with OpenAI’s
text-embedding-3-large
model. A
10
×
10
10\times 10
self-organizing map (SOM)
[
23
]
was then trained to visualize their semantic landscape. The SOM is an unsupervised neural network for dimensionality reduction and clustering by projecting high-dimensional input data onto a lower-dimensional grid (here
2
2
-dimensional) while preserving topological relationships between the input data. Each of the
100
100
SOM neurons was initialized with a random weight vector of equal dimensionality, and training proceeded for
50 000
50\,000
iterations in mini-batches of
50
50
samples. During each iteration, the neurons compete to best represent the input pattern. The algorithm identifies the Best Matching Unit (BMU) for each input vector, which is defined as the neuron whose weight vector has the smallest Euclidean distance to the input vector. Afterward, the BMU and its neighboring neurons are updated, with the adjustment magnitude decreasing as a function of distance from the BMU, according to a Gaussian neighborhood function. This neighborhood influence, combined with a linearly decreasing learning rate, allows the SOM to form a topologically ordered map of the input space. The convergence and quality of the resulting map were quantitatively validated by calculating standard SOM metrics: the Quantization Error, representing the average distance between input data vectors and their best matching unit’s weight vector, and the Topological Error (TE), measuring the proportion of data points for which the first and second BMUs are not adjacent on the map grid.
(a)
U-matrix visualization of the SOM trained on user prompt embeddings, where regions with more distance indicate cluster boundaries and regions with lower distance denote dense clusters of similar prompts.
(b)
SOM hit map (BMU activation count) showing the distribution of prompts across the neuron grid. Five distinct high-activation and low-activation regions are scattered in between, suggesting a balance of semantic clusters and diverse request types in the input data.
Figure 5
:
Self-Organizing Map (SOM) analysis of user input prompt embeddings.
The SOM and BMU analyses give us information regarding the prompts’ degree of complexity and semantic similarity. The score-based metric evaluation shows that the prompts comprise
44.3
%
44.3\text{\,}\mathrm{\%}
basic,
48.5
%
48.5\text{\,}\mathrm{\%}
standard, and
7.2
%
7.2\text{\,}\mathrm{\%}
complex prompts. This evaluation is performed by an LLM, which means that the language model assigns a numerical value to text data
[
5
]
. The SOM analysis creates a self-organizing map grid of hexagonally packed neurons, Fig.
5
, trained on the embeddings of the prompts, and the prompts are clustered into different groups. The SOM shows the clusters while preserving topological identity. The quality of the SOM representation reinforces the reliability of the observed prompt distribution (Fig.
5
). The low TE (
0.0373
0.0373
) confirms excellent preservation of the original data’s neighborhood structure. The Quantization Error (
0.4970
0.4970
) indicates good representational fidelity; considering that the input vectors were unit-normalized (maximum possible pairwise distance of 2.0), this average distance between data points and their map representatives is low, especially given the significant dimensionality reduction. The U-matrix (Unified distance matrix) in Fig.
5(a)
shows the neuron distances; the hexagonal structure captures six equidistant neighbors, compared to a square grid with only four. To analyze the learned representations, two complementary visualizations were generated. The U-matrix visualizes the average distance between neighboring neurons, where higher values indicate cluster boundaries and lower values suggest dense regions of similar inputs. The BMU activation count plot (hit map) in Fig.
5(b)
shows how frequently each neuron was selected as a BMU, revealing the distribution of input assignments across the SOM grid. Neurons with zero activations indicate they serve as boundary regions or represent semantic areas not covered by the current dataset. These
empty
neurons are crucial for topology preservation, helping maintain proper distance relationships between clusters.
A similar SOM representation can be generated for each component of the embedding vectors, revealing which dimensions contribute most significantly to semantic distinctions and helping identify correlated components that form meaningful semantic features. These visualizations are available in the project’s GitHub
repository
. The figure shows five neurons with the highest activation counts, including their respective BMUs. These neurons are well separated on the SOM grid, indicating that the calculation prompts can be grouped mainly into five semantic clusters, with additional residual prompts that share similarities within the core concepts. Overall, the SOM grid shows how the prompt collection is dispersed, which is a good balance between semantic cohesion within the identified clusters and conceptual diversity across them. Upon manual inspection of prompts, it was found that the prompts are mainly divided into two major categories, namely structural relaxation and a variety of single-shot DFT calculations, using different methodologies available in the QE code, which is further confirmed by a simpler k-means analysis (See GitHub
repository
). Discussing these findings illuminates the framework’s sensitivity to input quality and type, potentially guiding future improvements in user interaction or prompt pre-processing. This analysis uncovers latent structures within the user request space directly relevant to developing automated protocol generation mechanisms.
Figure 6
:
Real simulation protocol example of Quantum Espresso generated by GENIUS. The user’s prompt request is displayed in the upper part, instructing QE code to perform a geometry optimization for 2D
PdS
2
\text{PdS}{\vphantom{\text{X}}}_{\vphantom{\text{2}}\smash[t]{\text{2}}}^{\vphantom{\smash[t]{\text{2}}}\hphantom{\text{2}}\text{}}
in the P21/c space group, using Quantum Espresso with the
B3LYP
exchange-correlation functional. The generated protocol is provided, as presented in two columns for compactness. The framework parses these instructions and automatically generates the valid QE input. The protocol specifies
20
%
20\text{\,}\mathrm{\%}
exact-exchange, a plane-wave basis set, smearing for occupation, a mixing parameter for the SCF cycle, and a
7
×
7
×
2
7\times 7\times 2
k
-points mesh. Additionally, the file includes detailed control parameters for geometry relaxation (via BFGS), pseudopotentials for
Pd
and
S
, and the required settings, such as ecutwfc, ecutrho, occupations, spin polarization, as presented in the output.
Figure 7
:
Live timeline of a self-healing (
AEH
) GENIUS job. Each dot marks a log event (y-axis, newest at top) plotted against wall-clock time (x-axis), colors denote status:
PENDING
(orange),
SUCCESS
(green),
RETRY
(gray),
ERROR
(red). The workflow first parses the user prompt, harvests documentation, builds a parameter graph, and generates a QE input template. After launch, QE crashes once (red); the finite-state loop applies a single retry (gray) within the
AEH
, resolves the issue, and the simulation reaches steady execution and completion (green) in
≈
\approx
3 min. The timeline exposes full provenance and illustrates how GENIUS autonomously recovers from runtime failures while streaming real-time status updates.
An overview of the outcomes for the
295
295
test prompts is presented in Fig.
8
, which depicts the distribution between successful and failed runs, the path to success,
zero-shot
or via specific models in the
AEH
system, as well as a breakdown according to the initial prompt complexity. Additionally, when the prompts are evaluated using only base LLMs without the GENIUS framework, they return negligible contributions to generate valid QE input files containing the correct cards and mutually consistent parameters for a given geometric structure, irrespective of their nominal reasoning enhancements. This limitation is probably because the models do not embed explicit crystallographic information and cannot infer the subtle interdependencies between geometry, namelist keywords, and the card syntax required by QE. We reiterate that Model 1, the first component in the protocol generation hierarchy, produces the initial simulation protocol version. Therefore, a
zero-shot
success corresponds to cases in which the first output generated by Model 1 is valid and does not require any further correction. Within the GENIUS framework, Model 1 proceeds with the first cycle of automated error-handling retries if this initial attempt fails.
In Fig.
6
, the user’s prompt (classified as standard) is shown at the top, specifying a geometry optimization for a
2
D
PdS
2
\text{PdS}{\vphantom{\text{X}}}_{\vphantom{\text{2}}\smash[t]{\text{2}}}^{\vphantom{\smash[t]{\text{2}}}\hphantom{\text{2}}\text{}}
structure using the
B3LYP
functional, whereas the bottom portion highlights the valid QE input file generated by the GENIUS framework. In Fig.
7
, we illustrate the complete timeline log for the same prompt, emphasizing the sequence of events, as indicated by color-coded statuses (
PENDING
,
SUCCESS
,
RETRY
, and
ERROR
), as the system progresses from the interface agent phase to the final solution generation. As evidenced in Fig.
7
, the extended time required to evaluate input parameters is a secondary constraint imposed by LLM API providers, which a self-host service could mitigate; without such limitations, parameters could be processed in parallel, reducing overall latency. The stepwise entries in the log figure demonstrate the framework’s resilience, including how QE crashes (red dots) occur due to some hallucination or confabulation. Our framework automatically detects and resolves these failures, which iteratively refines and validates the input parameters until the final QE calculation is completed.
In Fig.
8
, we present the distribution of successful runs that reached the
FINISHED
state in the workflow after a given number of attempts. The success at zero-shot cases indicates the scenarios where a request was
FINISHED
using only the recommendation system of the workflow, without invoking the automated error handling system. This scenario accounts for
17.9
%
17.9\text{\,}\mathrm{\%}
, comprising
9.4
%
9.4\text{\,}\mathrm{\%}
for basic prompts,
7.2
%
7.2\text{\,}\mathrm{\%}
for standard prompts, and
1.3
%
1.3\text{\,}\mathrm{\%}
for complex prompts. A similar distribution pattern can be observed for subsequent attempts. If the initial execution fails, the GENIUS
AEH
system is triggered. Each retry uses the same model that generated the initial protocol within its designated attempt cycle. After three attempts per model, the process switches to the next model in the hierarchy if no solution is found. Based on the user’s calculation prompt, the workflow resets from the output of the recommendation system, which is a template for generating a simulation protocol. The previous changelog attempts are not provided to the new model in each model exchange. The model receives only the error message, the relevant documentation, the latest version of the simulation protocol, and the original user calculation prompt.
Our results demonstrate that successful cases at each attempt comprise a mixture of basic, standard, and complex calculation prompts. This observation shows that prompt complexity (basic, standard, or complex) is not inherently problematic for the framework’s performance. Complex prompts can contain more distinctive instructions, enhancing the framework’s ability to generate valid protocols. The general trend reveals that after the initial attempts with Model 1, the number of successful attempts stabilizes at a baseline level. This initial high success rate is followed by a plateau, which resembles an exponential decay behavior in the number of cases requiring successive attempts. For the model selection hierarchy, we assume a performance ordering of
Model
​
1
<
Model
​
2
<
Referee
\text{Model }1<\text{Model }2<\text{Referee}
. This can be done with any set of language models, but the predefined order characterizes the framework’s behavior, where the Referee model was chosen as the SOTA model. The Referee model is used to establish the existence of the performance baseline. This outcome indicates that the framework itself, rather than just the power of the strongest model, is responsible for successfully handling most cases, as the Referee model is not utilized disproportionately, which would otherwise suggest a failure in the preceding stages. This demonstrates that the GENIUS framework can be used with any model (it is model-agnostic) and that its overall performance is attributable to its architecture intelligence, not just the underlying language model’s capabilities. The opposite scenario would manifest as a lack of a baseline and, instead, an increase in successful attempts. Specifically indicating that success relied primarily on the more performative model rather than the framework’s architectural design.
From our total dataset of
295
295
calculation requests analyzed,
235
235
successfully produced a valid simulation protocol, with
42
42
of these succeeding in the
zero-shot
scenario, which is defined here as the framework converging to a correct protocol on its very first attempt, without invoking any automated error-handling loops. This yields an overall system success ratio of
P
⁡
(
S
)
=
235
295
≈
0.7966
P(S)=\frac{235}{295}\approx 0.7966
, a
zero-shot
, (
Z
​
S
ZS
), success ratio of
P
⁡
(
Z
​
S
)
=
42
295
≈
0.1424
P(ZS)=\frac{42}{295}\approx 0.1424
, and a ratio of success through automated error handling (given zero-shot fails) of
P
⁡
(
AEH
∣
not
​
Z
​
S
)
=
193
253
≈
0.7628
P(\texttt{AEH}\mid\text{not }ZS)=\frac{193}{253}\approx 0.7628
. To characterize how the success rate evolves as a function of successive attempts, we fitted an exponential decay function to the observed success rates (
S
S
) across multiple attempts, where
x
x
represents the attempt number. The function takes the form, Eq.
1
:
S
⁡
(
x
)
=
A
​
e
−
b
​
x
+
C
,
RMSE
=
1.9
%
,
S(x)=A\,e^{-bx}+C,\quad\mathrm{RMSE}=1.9\%\penalty\ ,
(1)
obtaining
A
=
11.1
%
±
1.0
A=$11.1\text{\,}\mathrm{\%}$\pm 1.0
,
b
=
0.46
​
(
1
/
attempt
)
±
0.1
b=0.46\ (1/\mathrm{attempt})\pm 0.1
, and
C
=
7.0
%
±
0.70
C=$7.0\text{\,}\mathrm{\%}$\pm 0.70
. In this parametrization, the initial amplitude,
A
⁡
(
%
)
A\ ($\mathrm{\%}$)
, represents the maximum influence of the zero-shot attempt; the decay rate,
b
⁡
(
1
/
attempt
)
b\ (1/\mathrm{attempt})
, determines how quickly this initial advantage decreases over successive attempts, and the baseline,
C
(
%
)
C\ (\%)
is the asymptotic success probability reached after many retries.
Fig.
9
delineates three distinct operational regimes within GENIUS:
recommendation-system
,
maximum workflow utilization
, and
shallow workflow utilization
. The opening
recommendation-system
regime coincides with the
zero-shot
pass, highlighting the framework’s ability to successfully generate protocols independently of model switching or fallback mechanisms. Immediately thereafter, the curve plunges through the
maximum workflow utilization
regime: each early retry unlocks deeper cross-model synergies, yielding rapidly diminishing, but still substantive, gains. Once the process reaches roughly six attempts, the trajectory flattens into the
shallow workflow utilization
regime, where the performance asymptotically converges toward the baseline value of
C
≈
7
%
C\!\approx\!7\%
. Within this regime, further retries contribute marginal benefit; success is governed primarily by the workflow’s inherent competence rather than by additional computation. The slight oscillations superimposed on the fitted curve stem from the design choice to reset the context after every third attempt and switch the model. Inter-block influence is shortened because each reset isolates the subsequent block of attempts. Allowing more consecutive attempts per model would amplify these oscillations, which could be quantitatively captured by extending the fitting function to include an explicit periodic component, where finer-grained modeling is required.
Figure 8
:
GENIUS performance benchmark on
295
295
tested prompts.
The stacked bar chart reports the
percentage of successful runs
(y-axis) for the
Zero-Shot
pass (GENIUS without
AEH
) and GENIUS using
AEH
combined with
Model 1
,
Model 2
, and
Referee
models. Shaded vertical panels group the bars that belong to the systems assessed by the same model. Within every bar, colored segments disaggregate the total success rate by prompt complexity: Basic, Standard, and Complex. The cumulative solved percentage (right y-axis) is overlaid in dark blue, showing the total proportion of prompts solved after each successive attempt.
Figure 9
:
Exponential decay fit (red curve) applied to the observed fraction of successful runs per attempt number (black points). A single-parameter exponential,
S
⁡
(
x
)
=
11.1
​
e
−
0.46
​
x
+
7.0
S(x)=11.1\,\mathrm{e}^{-0.46x}+7.0
% (red line), captures the trend. Shaded bands specify the three operating regimes: the opening
Recommendation System
zone (
zero-shot
wins), the steep
Maximum Workflow Utilization
zone where early retries yield rapidly diminishing but still substantive gains, and the long-tail
Shallow Workflow Utilization
zone in which performance plateaus at the
7
%
7\text{\,}\mathrm{\%}
baseline. The fit confirms that most recoverable errors are corrected within the first three attempts, after which additional computation yields marginal returns.
The recommendation system (
R
​
e
​
c
Rec
) includes the smart knowledge graph, extracts boundary conditions, and evaluates key parameters for each user query (
Q
Q
). The workflow is complete if the calculation request is successfully resolved in a
zero-shot
scenario. Otherwise, the request proceeds to the
AEH
subsystem, which can be a successful case. Given an effective recommendation system, we can decompose
S
S
as in Eq.
2
:
P
⁡
(
S
)
=
P
⁡
(
Z
​
S
)
+
(
1
−
P
⁡
(
Z
​
S
)
)
​
P
​
(
A
​
E
​
H
∣
¬
Z
​
S
)
.
P(S)=P(ZS)+\bigl(1-P(ZS)\bigr)\,P\!\left(AEH\mid\neg ZS\right).
(2)
To estimate the system’s performance in the absence of
R
​
e
​
c
Rec
, we introduce the scaling factors
α
\alpha
and
β
\beta
, which quantify how much
R
​
e
​
c
Rec
multiplies the
zero-shot
and
AEH
success probabilities, respectively, assuming
α
,
β
≥
1
\alpha,\beta\geq 1
. Using Eq.
2
the hypothetical
Q
Q
-only success probabilities are then,
P
⁡
(
Z
​
S
∣
Q
​
-only
)
=
0.1424
α
,
P
⁡
(
AEH
∣
¬
Z
​
S
,
Q
​
-only
)
=
0.7628
β
,
P(ZS\mid Q\text{-only})=\frac{0.1424}{\alpha},\qquad P\!\left(\texttt{AEH}\mid\neg ZS,\,Q\text{-only}\right)=\frac{0.7628}{\beta},
(3)
so that
P
⁡
(
S
∣
Q
​
-only
)
=
0.1424
α
+
0.7628
β
−
0.1086
α
​
β
.
P(S\mid Q\text{-only})=\frac{0.1424}{\alpha}+\frac{0.7628}{\beta}-\frac{0.1086}{\alpha\beta}.
(4)
Setting
α
=
β
=
γ
\alpha=\beta=\gamma
gives
P
⁡
(
S
∣
Q
​
-only
)
=
0.9052
γ
−
0.1086
γ
2
.
P(S\mid Q\text{-only})=\frac{0.9052}{\gamma}-\frac{0.1086}{\gamma^{2}}.
(5)
This dependency of the success probability on the effectiveness of the recommendation system can be considered with a few representative examples: In the limiting case where the recommendation system has no effect (
γ
=
1
\gamma=1
), the success probability is
0.7966
0.7966
, which is the same as the overall success probability with the recommendation system. A case where the recommendation system has an effectiveness reduction of
50
%
50\text{\,}\mathrm{\%}
(i.e.,
γ
=
1.50
\gamma=1.50
), the success rate without the recommendation system drops to
0.56
0.56
. In the case of double effectiveness (
γ
=
2
\gamma=2
), the success rate further declines to
0.43
0.43
. The sensitivity of the success rate concerning variations in the recommendation system’s effectiveness is shown in the following Eq. (
6
):
d
d
​
γ
​
P
​
(
S
∣
Q
​
-only
)
=
−
0.9052
γ
2
+
0.2172
γ
3
,
for
​
γ
>
1
.
\frac{d}{d\gamma}P(S\mid Q\text{-only})=-\frac{0.9052}{\gamma^{2}}+\frac{0.2172}{\gamma^{3}},\quad\text{for }\gamma>1.
(6)
This derivative indicates that the reduction in success rate (when the recommendation system is removed) is most sensitive when its effectiveness factor (
γ
\gamma
) is close to
1
1
. These results imply that the recommendation system significantly boosts system performance. As
γ
\gamma
increases (implying that the recommendation system is even slightly effective), the success probability in the
Q
Q
-only regime diminishes sharply. The derivative analysis confirms that the decrease in success probability is steepest when
γ
\gamma
is near 1. Small enhancements due to the recommendation system can lead to substantial differences in overall performance.
Conclusion
Our study demonstrates that the GENIUS framework substantially improves productivity in DFT calculation, streamlining the entire process from typing a query to running the simulations. By marrying a domain-specific knowledge graph with a tiered stack of large language models and an intelligent-automated error-handling loop, the framework converts free-form user requests into validated Quantum ESPRESSO inputs, achieving successful execution on first attempt approximately
80
%
80\text{\,}\mathrm{\%}
of the time. When the initial attempt fails, the agentic loop repairs
>
76
%
>$76\text{\,}\mathrm{\%}$
of crashes, and the attempt-wise success curve follows a fast exponential decay toward a stable
7
%
7\text{\,}\mathrm{\%}
baseline, evidence that most recoverable errors are neutralized in the earliest retries. Three architectural choices underpin this reliability and efficiency.
Smart knowledge graph
: Encapsulating
247
247
parameters and
330
330
dependency edges, the KG supplies the LLMs with grounded, constraint-aware facts, sharply reducing hallucinations and ensuring syntactic and physical consistency.
Model hierarchy
: Lightweight models tackle the bulk of queries, while larger models are invoked only when the workflow stalls, cutting inference cost and latency without sacrificing accuracy.
Finite-state error recovery
. A transparent finite-state machine monitors every run, restarts from a clean template after three failed fixes, and escalates only when the evidence justifies the expense. Together, these elements close the
know–do gap
that separates mature electronic-structure codes from routine, accessible usage. Experimentalists no longer detour into arcane input syntax, and computational specialists can redirect effort from boilerplate scripting to scientific exploration. In the context of ICME, GENIUS removes a critical implementation barrier, allowing predictive simulation to flow unimpeded into design loops and high-throughput campaigns. By automating protocol generation, validation, and repair, GENIUS democratizes access to advanced simulation tools for groups lacking deep computational expertise, enabling wider participation in materials discovery. Its cost-aware orchestration makes large-scale screening feasible on moderate budgets, and its transparent logs assure reproducibility, a prerequisite for FAIR data practice. The present KG covers only
pw.x
; extending it to other Quantum ESPRESSO modules and codes beyond QE will broaden GENIUS’s reach. Community-driven contributions could add more simulation codes, refine edge conditions, and enrich metadata that remain manually curated. Finally, incorporating physics-informed validators (e.g., symmetry checks, charge counting) and adaptive hyperparameter tuning promises an additional jump in first-shot accuracy. GENIUS shows that the long-standing technical drag on computational materials science can be lifted when factual domain knowledge, strategic model selection, and disciplined workflow control are fused into a single agentic system.
Declaration of Competing Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
Data Availability Statement
The authors confirm that the data supporting the study’s findings are available in the article GitHub repository
https://github.com/KIT-Workflows/agentic-workflow-framework
, and upon request.
Acknowledgements
We acknowledge support by the KIT Publication Fund of the Karlsruhe Institute of Technology. The authors are also thankful for financial support from the National Council for Scientific and Technological Development (CNPq, grant numbers 444431/2024-1, and 444069/2024-0). W.W. and C.R.C.R. thank the German Federal Ministry of Education and Research (BMBF) for financial support of the project Innovation-Platform MaterialDigital (
www.materialdigital.de
) through project funding FKZ number 13XP5094A.
References
[1]
M. AI
(2024)
Meta llama 3.1
.
Note:
https://ai.meta.com/blog/meta-llama-3-1/
Accessed: February, 2025
Cited by:
Large Language Model Integration
.
[2]
J. Allison, D. Backman, and L. Christodoulou
(2006)
Integrated computational materials engineering: a new paradigm for the global materials profession
.
Jom
58
,
pp. 25–27
.
External Links:
Document
Cited by:
Introduction
.
[3]
F. E. Bock, R. C. Aydin, C. J. Cyron, N. Huber, S. R. Kalidindi, and B. Klusemann
(2019)
A review of the application of machine learning and data mining approaches in continuum materials mechanics
.
Frontiers in Materials
6
,
pp. 110
.
External Links:
Document
Cited by:
Introduction
.
[4]
M. Bonacci, J. Qiao, N. Spallanzani, A. Marrazzo, G. Pizzi, E. Molinari, D. Varsano, A. Ferretti, and D. Prezzi
(2023)
Towards high-throughput many-body perturbation theory: efficient algorithms and automated workflows
.
npj Computational Materials
9
(
1
).
External Links:
ISSN 2057-3960
,
Link
,
Document
Cited by:
Introduction
.
[5]
T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell,
et al.
(2020)
Language models are few-shot learners
.
Advances in neural information processing systems
33
,
pp. 1877–1901
.
Cited by:
Prompt Dataset and Complexity Mapping
,
Results
.
[6]
C. R. Caldeira Rego, J. Schaarschmidt, T. Schlöder, M. Penaloza-Amion, S. Bag, T. Neumann, T. Strunk, and W. Wenzel
(2022)
SimStack: an intuitive workflow framework
.
Frontiers in Materials
9
.
External Links:
Document
Cited by:
Introduction
.
[7]
D. Campi, N. Mounet, M. Gibertini, G. Pizzi, and N. Marzari
(2023)
Expansion of the materials cloud 2d database
.
ACS nano
17
(
12
),
pp. 11268–11278
.
External Links:
Document
Cited by:
Prompt Dataset and Complexity Mapping
.
[8]
(2024)
Claude 3.5 sonnet
.
Note:
https://www.anthropic.com/news/claude-3-5-sonnet
Accessed: February, 2025
Cited by:
Smart Knowledge Graph
,
Large Language Model Integration
.
[9]
Inc. Databricks
(2024)
Dbrx
.
Note:
https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm
Accessed: February, 2025
Cited by:
Large Language Model Integration
.
[10]
L. O. de Araujo, C. R. Caldeira Rego, W. Wenzel, M. J. Piotrowski, A. C. Dias, and D. Guedes-Sobrinho
(2024)
Automated workflow for analyzing thermodynamic stability in polymorphic perovskite alloys
.
npj Computational Materials
10
(
1
).
External Links:
ISSN 2057-3960
,
Link
,
Document
Cited by:
Introduction
.
[11]
DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, D. Dai, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Bao, H. Xu, H. Wang, H. Ding, H. Xin, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Wang, J. Chen, J. Yuan, J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang, M. Tang, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du, R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen, S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, S. Ye, T. Yun, T. Pei, T. Sun, T. Wang, W. Zeng, W. Zhao, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An, X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su, X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang, X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang, Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X. Zhu, Y. Xu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang
(2025)
DeepSeek-r1: incentivizing reasoning capability in llms via reinforcement learning
.
arXiv
.
External Links:
Document
,
Link
Cited by:
Introduction
.
[12]
P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso, S. de Gironcoli, S. Fabris, G. Fratesi, R. Gebauer, U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri, L. Martin-Samos, N. Marzari, F. Mauri, R. Mazzarello, S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, G. Sclauzero, A. P. Seitsonen, A. Smogunov, P. Umari, and R. M. Wentzcovitch
(2009)
QUANTUM espresso: a modular and open-source software project for quantum simulations of materials
.
Journal of Physics: Condensed Matter
21
(
39
),
pp. 395502
.
External Links:
ISSN 1361-648X
,
Link
,
Document
Cited by:
Introduction
.
[13]
Google AI
(2024)
Gemini 2.0 flash
.
Note:
https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/
Accessed: February, 2025
Cited by:
Large Language Model Integration
.
[14]
O. E. Gundersen
(2021)
The fundamental principles of reproducibility
.
Philosophical Transactions of the Royal Society A
379
(
2197
),
pp. 20200210
.
External Links:
Document
Cited by:
Introduction
.
[15]
J. Hafner, C. Wolverton, and G. Ceder
(2006)
Toward computational materials design: the impact of density functional theory on materials research
.
MRS bulletin
31
(
9
),
pp. 659–668
.
External Links:
Document
Cited by:
Introduction
.
[16]
X. Han, M. Alameh, N. Gong, L. Xue, M. Ghattas, G. Bojja, J. Xu, G. Zhao, C. C. Warzecha, M. S. Padilla, R. El-Mayta, G. Dwivedi, Y. Xu, A. E. Vaughan, J. M. Wilson, D. Weissman, and M. J. Mitchell
(2024)
Fast and facile synthesis of amidine-incorporated degradable lipids for versatile mrna delivery in vivo
.
Nature Chemistry
16
(
10
),
pp. 1687–1697
.
External Links:
ISSN 1755-4349
,
Link
,
Document
Cited by:
Introduction
.
[17]
J. B. Holbrook
(2019)
Open science, open access, and the democratization of knowledge
.
Issues in science and technology
35
(
3
),
pp. 26–28
.
Cited by:
Introduction
.
[18]
S. Huber, M. Bercx, N. Hörmann, M. Uhrin, G. Pizzi, and N. Marzari
(2022)
Materials cloud three-dimensional crystals database (mc3d)
.
Materials Cloud Archive 2022.38
.
External Links:
Document
Cited by:
Prompt Dataset and Complexity Mapping
.
[19]
S. P. Huber, E. Bosoni, M. Bercx, J. Bröder, A. Degomme, V. Dikan, K. Eimre, E. Flage-Larsen, A. Garcia, L. Genovese, D. Gresch, C. Johnston, G. Petretto, S. Poncé, G. Rignanese, C. J. Sewell, B. Smit, V. Tseplyaev, M. Uhrin, D. Wortmann, A. V. Yakutovich, A. Zadoks, P. Zarabadi-Poor, B. Zhu, N. Marzari, and G. Pizzi
(2021)
Common workflows for computing material properties using different quantum engines
.
npj Computational Materials
7
(
1
).
External Links:
ISSN 2057-3960
,
Link
,
Document
Cited by:
Introduction
.
[20]
K. M. Jablonka, Q. Ai, A. Al-Feghali, S. Badhwar, J. D. Bocarsly, A. M. Bran, S. Bringuier, L. C. Brinson, K. Choudhary, D. Circi,
et al.
(2023)
14 examples of how llms can transform materials science and chemistry: a reflection on a large language model hackathon
.
Digital discovery
2
(
5
),
pp. 1233–1250
.
External Links:
Document
Cited by:
Introduction
.
[21]
Kimi Team, A. Du, B. Gao, B. Xing, C. Jiang, C. Chen, C. Li, C. Xiao, C. Du, C. Liao, C. Tang, C. Wang, D. Zhang, E. Yuan, E. Lu, F. Tang, F. Sung, G. Wei, G. Lai, H. Guo, H. Zhu, H. Ding, H. Hu, H. Yang, H. Zhang, H. Yao, H. Zhao, H. Lu, H. Li, H. Yu, H. Gao, H. Zheng, H. Yuan, J. Chen, J. Guo, J. Su, J. Wang, J. Zhao, J. Zhang, J. Liu, J. Yan, J. Wu, L. Shi, L. Ye, L. Yu, M. Dong, N. Zhang, N. Ma, Q. Pan, Q. Gong, S. Liu, S. Ma, S. Wei, S. Cao, S. Huang, T. Jiang, W. Gao, W. Xiong, W. He, W. Huang, W. Wu, W. He, X. Wei, X. Jia, X. Wu, X. Xu, X. Zu, X. Zhou, X. Pan, Y. Charles, Y. Li, Y. Hu, Y. Liu, Y. Chen, Y. Wang, Y. Liu, Y. Qin, Y. Liu, Y. Yang, Y. Bao, Y. Du, Y. Wu, Y. Wang, Z. Zhou, Z. Wang, Z. Li, Z. Zhu, Z. Zhang, Z. Wang, Z. Yang, Z. Huang, Z. Huang, Z. Xu, and Z. Yang
(2025)
Kimi k1.5: scaling reinforcement learning with llms
.
arXiv
.
External Links:
Document
,
Link
Cited by:
Introduction
.
[22]
A. King
(2025)
Four ways to power-up ai for drug discovery
.
Nature
.
External Links:
ISSN 1476-4687
,
Link
,
Document
Cited by:
Introduction
.
[23]
T. Kohonen
(1990)
The self-organizing map
.
Proceedings of the IEEE
78
(
9
),
pp. 1464–1480
.
External Links:
Document
Cited by:
Results
.
[24]
N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, Y. Gu, S. Malik, V. Graf, J. D. Hwang, J. Yang, R. L. Bras, O. Tafjord, C. Wilhelm, L. Soldaini, N. A. Smith, Y. Wang, P. Dasigi, and H. Hajishirzi
(2024)
Tulu 3: pushing frontiers in open language model post-training
.
arXiv
.
External Links:
Document
,
Link
Cited by:
Introduction
.
[25]
G. Ledger and R. Mancinni
(2024)
Detecting llm hallucinations using monte carlo simulations on token probabilities
.
Authorea Preprints
.
External Links:
Document
Cited by:
Introduction
.
[26]
K. Lejaeghere, G. Bihlmayer, T. Björkman, P. Blaha, S. Blügel, V. Blum, D. Caliste, I. E. Castelli, S. J. Clark, A. Dal Corso, S. de Gironcoli, T. Deutsch, J. K. Dewhurst, I. Di Marco, C. Draxl, M. Dułak, O. Eriksson, J. A. Flores-Livas, K. F. Garrity, L. Genovese, P. Giannozzi, M. Giantomassi, S. Goedecker, X. Gonze, O. Grånäs, E. K. U. Gross, A. Gulans, F. Gygi, D. R. Hamann, P. J. Hasnip, N. A. W. Holzwarth, D. Iuşan, D. B. Jochym, F. Jollet, D. Jones, G. Kresse, K. Koepernik, E. Küçükbenli, Y. O. Kvashnin, I. L. M. Locht, S. Lubeck, M. Marsman, N. Marzari, U. Nitzsche, L. Nordström, T. Ozaki, L. Paulatto, C. J. Pickard, W. Poelmans, M. I. J. Probert, K. Refson, M. Richter, G. Rignanese, S. Saha, M. Scheffler, M. Schlipf, K. Schwarz, S. Sharma, F. Tavazza, P. Thunström, A. Tkatchenko, M. Torrent, D. Vanderbilt, M. J. van Setten, V. Van Speybroeck, J. M. Wills, J. R. Yates, G. Zhang, and S. Cottenier
(2016)
Reproducibility in density functional theory calculations of solids
.
Science
351
(
6280
).
External Links:
ISSN 1095-9203
,
Link
,
Document
Cited by:
Introduction
.
[27]
X. Lin, S. Zhang, M. Yang, B. Xiao, Y. Zhao, J. Luo, J. Fu, C. Wang, X. Li, W. Li, F. Yang, H. Duan, J. Liang, B. Fu, H. Abdolvand, J. Guo, G. King, and X. Sun
(2024)
A family of dual-anion-based sodium superionic conductors for all-solid-state sodium-ion batteries
.
Nature Materials
24
(
1
),
pp. 83–91
.
External Links:
ISSN 1476-4660
,
Link
,
Document
Cited by:
Introduction
.
[28]
D. A. Luke, B. J. Powell, and A. Paniagua-Avila
(2024)
Bridges and mechanisms: integrating systems science thinking into implementation research
.
Annual Review of Public Health
45
.
External Links:
Document
Cited by:
Introduction
.
[29]
C. Michelutti, J. Eckert, M. Monecke, J. Klein, and S. Glesner
(2024)
A systematic study on the potentials and limitations of llm-assisted software development
.
In
2024 2nd International Conference on Foundation and Large Language Models (FLLM)
,
pp. 330–338
.
External Links:
Document
Cited by:
Introduction
.
[30]
Mistral AI
(2024)
Mixtral-8x22b instruct
.
Note:
https://mistral.ai/news/mixtral-8x22b
Accessed: February, 2025
Cited by:
Large Language Model Integration
.
[31]
Quantum ESPRESSO Group
(2023)
User’s guide for quantum ESPRESSO (pw.x)
.
Quantum ESPRESSO Foundation
{https://www.quantum-espresso.org/Doc/pw_user_guide/}
.
Note:
Accessed: February, 2025
Cited by:
Automated Error Handling (
AEH
)
.
[32]
J. Schaarschmidt, J. Yuan, T. Strunk, I. Kondov, S. P. Huber, G. Pizzi, L. Kahle, F. T. Bölle, I. E. Castelli, T. Vegge, F. Hanke, T. Hickel, J. Neugebauer, C. R. C. Rêgo, and W. Wenzel
(2021)
Workflow engineering in materials design within the battery 2030+ project
.
Advanced Energy Materials
12
(
17
).
External Links:
ISSN 1614-6840
,
Link
,
Document
Cited by:
Introduction
,
Introduction
.
[33]
S. C. Shen, E. Khare, N. A. Lee, M. K. Saad, D. L. Kaplan, and M. J. Buehler
(2023)
Computational design and manufacturing of sustainable materials through first-principles and materiomics
.
Chemical Reviews
123
(
5
),
pp. 2242–2275
.
External Links:
Document
Cited by:
Introduction
.
[34]
M. Soleymanibrojeni, C. R. Caldeira Rego, M. Esmaeilpour, and W. Wenzel
(2024)
An active learning approach to model solid-electrolyte interphase formation in li-ion batteries
.
Journal of Materials Chemistry A
12
(
4
),
pp. 2249–2266
.
External Links:
ISSN 2050-7496
,
Link
,
Document
Cited by:
Introduction
.
[35]
M. Soleymanibrojeni and C. R. Caldeira Rego
(2025)
Agentic-workflow-framework: AI-driven agentic framework for autonomous simulation protocol generation and execution
.
Note:
https://github.com/KIT-Workflows/agentic-workflow-framework
GitHub repository
Cited by:
Prompt Dataset and Complexity Mapping
.
[36]
H. Steck, C. Ekanadham, and N. Kallus
(2024)
Is cosine-similarity of embeddings really about similarity?
.
External Links:
Document
,
Link
Cited by:
Smart Knowledge Graph
.
[37]
C. D. Taylor, P. Lu, J. Saal, G. Frankel, and J. Scully
(2018)
Integrated computational materials engineering of corrosion resistant alloys
.
npj Materials Degradation
2
(
1
),
pp. 6
.
External Links:
Document
Cited by:
Introduction
.
[38]
A. Toner-Rodgers
(2024)
Artificial intelligence, scientific discovery, and product innovation
.
arXiv preprint arXiv:2412.17866
.
External Links:
Document
Cited by:
Introduction
.
[39]
Q. Wang, Z. Mao, B. Wang, and L. Guo
(2017)
Knowledge graph embedding: a survey of approaches and applications
.
IEEE transactions on knowledge and data engineering
29
(
12
),
pp. 2724–2743
.
External Links:
Document
Cited by:
Introduction
.
[40]
Z. Yu, B. Singh, Y. Yu, and L. F. Nazar
(2025)
Suppressing argyrodite oxidation by tuning the host structure for high-areal-capacity all-solid-state lithium–sulfur batteries
.
Nature Materials
.
External Links:
ISSN 1476-4660
,
Link
,
Document
Cited by:
Introduction
.