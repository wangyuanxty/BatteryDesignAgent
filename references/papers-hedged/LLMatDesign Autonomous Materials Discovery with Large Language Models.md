LLMatDesign: Autonomous Materials Discovery with Large Language Models
Title:
Content selection saved. Describe the issue below:
Description:
arXiv is now an independent nonprofit!
Learn more
×
License: CC BY-NC-ND 4.0
arXiv:2406.13163v1 [cond-mat.mtrl-sci] 19 Jun 2024
Abstract
Discovering new materials can have significant scientific and technological implications but remains a challenging problem today due to the enormity of the chemical space. Recent advances in machine learning have enabled data-driven methods to rapidly screen or generate promising materials, but these methods still depend heavily on very large quantities of training data and often lack the flexibility and chemical understanding often desired in materials discovery. We introduce LLMatDesign, a novel language-based framework for interpretable materials design powered by large language models (LLMs). LLMatDesign utilizes LLM agents to translate human instructions, apply modifications to materials, and evaluate outcomes using provided tools. By incorporating self-reflection on its previous decisions, LLMatDesign adapts rapidly to new tasks and conditions in a zero-shot manner. A systematic evaluation of LLMatDesign on several materials design tasks,
in silico
, validates LLMatDesign’s effectiveness in developing new materials with user-defined target properties in the small data regime. Our framework demonstrates the remarkable potential of autonomous LLM-guided materials discovery in the computational setting and towards self-driving laboratories in the future.
1
Introduction
Discovering novel materials with useful functional properties is a longstanding challenge in materials science due to the vast and diverse composition and structure space these materials can inhabit
[
1
,
2
]
. Traditional approaches to materials discovery often involve exhaustively screening materials via lab-based experiments or
in silico
simulations, which can be time-consuming and resource-intensive
[
3
,
4
,
5
]
. Recent advancements have introduced machine learning surrogate models to predict material structures and properties
[
6
,
7
]
, as well as generative modeling techniques to propose novel materials
[
8
,
9
,
10
,
11
,
12
,
13
,
14
]
. However, these data-driven methods rely heavily on extensive training datasets, generally derived from density functional theory (DFT) calculations. These methods are less useful in most instances where such data is unavailable, or when only a limited budget exists to perform experiments or high fidelity simulations. In contrast, a human expert would be far more effective here by being able to draw from domain knowledge and prior experiences, and reason from limited examples. Therefore, a different materials design paradigm is needed in these situations where models should be developed to exhibit similar proficiencies as human experts.
Fueled by ever-expanding textual datasets and significant increases in computing power, large language models (LLMs) have witnessed a meteoric rise in capabilities and usage in recent years. More broadly, the remarkable performance of LLMs across diverse tasks they have not been explicitly trained on has sparked a burgeoning interest in developing and utilizing LLM-based agents capable of reasoning, self-reflection, and decision-making
[
15
,
16
,
17
]
. These autonomous agents are typically augmented with tools or action modules, empowering them to go beyond conventional text processing and directly interact with the physical world, such as robotic manipulation
[
18
,
19
]
and scientific experimentation
[
20
,
21
]
. As the capabilities of LLMs and LLM-based autonomous agents continue to expand, they are increasingly being recognized for their potential in scientific domains, particularly in chemistry
[
22
]
. This surge in interest stems from the fact that the majority of information in chemistry exists as text, aligning closely with the text-centric nature of LLMs
[
23
]
. For instance, recent studies have demonstrated the use of LLMs to extract chemical reaction information
[
24
,
25
]
, predict chemical properties
[
26
,
27
,
28
,
29
]
, and generate crystal structures
[
30
,
31
,
32
]
, among many other applications. In particular, chemical research, such as materials discovery, traditionally hinges on human expertise and experience encapsulated in scientific publications. LLMs, capable of ingesting vast quantities of these publications beyond human capacity, have the potential to act as intelligent copilots that might be able to extract key insights, uncover hidden patterns, and propose novel methodologies, thereby accelerating scientific progress
[
23
]
.
Figure 1
:
Overview of LLMatDesign. The discovery process with LLMatDesign begins with user-provided inputs of chemical composition and target property. It recommends modifications (addition, removal, substitution, or exchange), and uses machine learning tools for structure relaxation and property prediction. Driven by an LLM, this iterative process continues until the target property is achieved, with self-reflection on past modifications fed back into the decision-making process at each step.
In this work, we present LLMatDesign (Fig.
1
), a language-based framework for materials design powered by state-of-the-art LLMs. LLMatDesign is capable of interpreting human-provided instructions and design constraints, using computational tools for materials evaluation, and leveraging existing chemical knowledge and feedback to act as a highly effective autonomous materials design agent.
Unlike traditional methods that rely on explicit mathematical formulations and programmed solvers, LLMatDesign as an autonomous agent works with natural language directly, allowing it to quickly adapt to a diverse set of tasks, materials and target properties by simply modifying the prompt. In each step, LLMatDesign generates new designs of a material by choosing a modification of a starting material along with a corresponding hypothesis. It then applies the modification to the material and validates its property. Here, we use surrogate models as a stand-in for DFT to perform property validation, which can be readily replaced with any other computational or, potentially, experimental validation method. Following this, LLMatDesign reflects on the applied modification and its outcome. This reflection, along with the modified material and hypothesis, is then incorporated into the prompt in an iterative process. Moreover, LLMatDesign’s flexibility allows incorporation of the entire modification history or user-defined requirements, offering even finer control over the discovery process.
By utilizing state-of-the-art LLMs as chemical reasoning engines, LLMatDesign represents a novel framework for materials discovery which, unlike many current data-driven generative methods, eliminates the need for large training datasets derived from ab initio calculations. LLMatDesign’s ability to interpret human instructions and incorporate design constraints enables rapid adaptation to new conditions, tasks, materials, and target properties via prompt modification—a flexibility that is often very difficult for current materials discovery methods such as those using generative models. More importantly, LLMatDesign’s ability to generate hypothesis, evaluate outcomes, and self-reflect on past decisions in a closed-loop manner showcases the potential for a fully automated artificial intelligence (AI) agent for materials design in both a computational setting or towards robotic laboratories in the future.
2
Results
2.1
LLMatDesign Framework
LLMatDesign is a flexible framework powered by an LLM and empowered with the necessary tools to perform materials discovery. The discovery process with LLMatDesign begins by taking the chemical composition and property of a starting material, along with a target property value, as user-provided inputs. If a chemical composition is specified without an initial structure, LLMatDesign will automatically query the Materials Project
[
33
]
database to retrieve the corresponding structure. If multiple candidates match the query, the structure with the lowest formation energy per atom is selected. LLMatDesign then intelligently recommends one of four possible modifications—addition, removal, substitution, or exchange—to the material’s composition and structure to achieve the target value.
Specifically, “exchange” refers to swapping two elements within the material, while “substitution” involves replacing one type of element with another. “Removal” means eliminating a specific element from the material. In the case of “addition,” an atom of the suggested element is added to the unit cell of the material, with its position randomly determined. These four choices act as a proxy to physical processes in materials modification, such as doping or creating defects, and additional modification choices can also be readily added or removed as desired within the framework.
LLMatDesign Prompt Template (GPT-4o)
I have a material and its
<property>
.
<definition of property>
.
(
<chemical composition>
,
<property value>
)
Please propose a modification to the material that results in
<objective>
. You can choose one of the four following modifications:
1.
exchange: exchange two elements in the material
2.
substitute: substitute one element in the material with another
3.
remove: remove an element from the material
4.
add: add an element to the material
<additional constraints>
Your output should be a python dictionary of the following the format:
{Hypothesis: $HYPOTHESIS, Modification: [$TYPE, $ELEMENT_1, $ELEMENT_2]}.
Here are the requirements:
1.
$HYPOTHESIS should be your analysis and reason for choosing a modification
2.
$TYPE should be the modification type; one of “exchange”, “substitute”, “remove”, “add”
3.
$ELEMENT should be the selected element type to be modified. For “exchange” and “substitute”, two $ELEMENT placeholders are needed. For “remove” and “add”, one $ELEMENT placeholder is needed.
<modification history>
Figure 2
:
Prompt template for LLMatDesign with GPT-4o. Text placeholders in red angular brackets are specific to the task given to LLMatDesign. Text placeholders in blue angular brackets are optional and can be omitted if not needed. For Gemini-1.0-pro’s prompt template, see Appendix
A
.
Self-reflection Prompt Template
After completing the following modification on
<previous composition>
, we obtained
<current composition>
and the
<property>
changed from
<previous value>
to
<current value>
. Please write a brief post-action reflection on the modification, explaining how successful it was in achieving the
<objective>
and the reasons for its success or failure:
<hypothesis>, <modification>
Figure 3
:
Prompt template for self-reflection. Text placeholders in red angular brackets are specific to the task given to LLMatDesign.
Alongside the proposed modification, LLMatDesign provides a hypothesis explaining why the suggested change could be beneficial. This hypothesis generated by the LLM provides a window into the reasoning behind its choices and provides a degree of interpretability which is not possible with traditional optimization algorithms. Next, LLMatDesign modifies the material based on the given suggestion, relaxes the structure using a machine learning force field (MLFF), and predicts its properties using a machine learning property predictor (MLPP). If the predicted property of the new material does not match the target value within a defined threshold, LLMatDesign then evaluates the effectiveness of the modification through a process called self-reflection where commentary is provided on the success of failure of the chosen modification.
After self-reflection, a modification history message is created. This message includes the modified chemical composition, the modification itself, the hypothesis behind the modification, and the self-reflection results. This history is then fed back into LLMatDesign, which enters the next design decision-making phase towards the goal of achieving the target property. The entire process repeats in a loop until termination conditions are met. Optionally, density functional theory (DFT) calculations can be performed on the final material.
At the core of the entire workflow, LLMatDesign utilizes an LLM engine or agent which translates user-defined objectives into appropriate Materials Project API calls, drives the design decision-making process, and conducts self-reflection on previous decisions to enhance performance. In this work, we demonstrate the capabilities of LLMatDesign using two state-of-the-art LLMs: GPT-4o
[
34
]
and Gemini-1.0-pro
[
35
]
. However, the framework is model-agnostic and should function effectively with any capable LLMs. The overall architecture and algorithm of LLMatDesign is depicted in Fig.
1
and Algo.
1
respectively. The modification and self-reflection prompt templates are shown in Fig.
2
and
3
respectively.
Algorithm 1
LLMatDesign Algorithm
Input:
(
x
0
,
y
0
)
(x_{0},y_{0})
: chemical composition and property of the starting material.
y
target
y_{\text{target}}
: target property value to achieve.
ℳ
:=
∅
\mathcal{M}:=\varnothing
: set of history messages, if any.
Output:
(
x
i
,
y
i
)
(x_{i},y_{i})
: chemical composition and property of the new material.
for
i
=
1
:
N
i=1:N
do
⊳
\triangleright
N
N
: maximum number of modifications
s
i
,
h
i
←
LLM
⁡
(
x
i
−
1
,
y
i
−
1
,
y
target
,
ℳ
)
s_{i},h_{i}\leftarrow\operatorname{LLM}(x_{i-1},y_{i-1},y_{\text{target}},\mathcal{M})
⊳
\triangleright
s
s
: modification;
h
h
: hypothesis
x
~
i
←
perform_modification
​
(
x
i
−
1
,
s
i
)
\tilde{x}_{i}\leftarrow\texttt{perform\_modification}(x_{i-1},s_{i})
x
i
←
MLFF
⁡
(
x
~
i
)
x_{i}\leftarrow\operatorname{MLFF}(\tilde{x}_{i})
y
i
←
MLPP
⁡
(
x
i
)
y_{i}\leftarrow\operatorname{MLPP}(x_{i})
if
|
y
i
−
y
target
|
/
|
y
target
|
≤
ε
|y_{i}-y_{\text{target}}|/|y_{\text{target}}|\leq\varepsilon
then
⊳
\triangleright
ε
\varepsilon
: error tolerance
return
(
x
i
,
y
i
)
(x_{i},y_{i})
end
if
r
i
←
LLM
⁡
(
x
i
−
1
,
x
i
,
y
i
−
1
,
y
i
,
s
i
,
h
i
)
r_{i}\leftarrow\operatorname{LLM}\left(x_{i-1},x_{i},y_{i-1},y_{i},s_{i},h_{i}\right)
⊳
\triangleright
r
r
: self-reflection
m
i
←
create_history_message
​
(
s
i
,
h
i
,
r
i
)
m_{i}\leftarrow\texttt{create\_history\_message}\left(s_{i},h_{i},r_{i}\right)
⊳
\triangleright
m
m
: history message
ℳ
←
ℳ
∪
{
m
i
}
\mathcal{M}\leftarrow\mathcal{M}\cup\{m_{i}\}
end
for
2.2
Evaluation
To evaluate the effectiveness of LLMatDesign, we performed a set of experiments with 10 starting materials randomly selected from the Materials Project
[
6
]
. Specifically, we focus on designing materials targeting two material properties and their corresponding objectives:
•
Band gap
(eV): design a new material with a band gap of 1.4 eV.
•
Formation energy per atom
(eV/atom): design a new material with the most negative formation energy possible.
The objective of achieving a band gap value of 1.4 eV is chosen as an example of designing an ideal photovoltaic material with a band gap within the range of 1–1.8 eV
[
36
]
, and the aim of obtaining the most negative formation energy requires LLMatDesign to suggest modifications that could result in more stable materials.
For the band gap experiments, we record the average number of modifications taken by LLMatDesign, with a maximum budget of up to 50 modifications. A 10% tolerance of error to the target is used as the convergence criterion. For the formation energy experiments, a fixed budget of 50 modifications is used, and both the average and minimum formation energies are recorded. The experiment is then repeated 30 times for each starting material. We present results for two different LLM engines: Gemini-1.0-pro and GPT-4o. Within each LLM engine, two variants of experiments—
history
and
historyless
—are conducted to evaluate the impact of including the knowledge of prior modification history. All results are compared against a random baseline, where modifications to materials are randomly selected. The results for band gap and formation energy per atom are shown in Table
1
and Table
2
respectively. Note that self-reflection is included only for GPT-4o and not for Gemini-1.0-pro.
Table 1
:
LLMatDesign’s performance in achieving a new material with a target band gap of 1.4 eV. Each experiment is repeated 30 times, and the average number of modifications taken to reach the target value is recorded.
Starting Material
Average # of Modifications
Average Final Band Gap (eV)
Gemini-1.0-pro
GPT-4o
Random
Gemini-1.0-pro
GPT-4o
Random
History
Historyless
History
Historyless
History
Historyless
History
Historyless
BaV
2
​
Ni
2
​
O
8
\text{BaV}_{2}\text{Ni}_{2}\text{O}_{8}
17.7
14.4
17.7
30.4
22.4
1.23
1.42
1.39
1.89
1.12
CdCu
2
​
GeS
4
\text{CdCu}_{2}\text{GeS}_{4}
11.1
13.4
3.3
9.5
28.7
1.41
1.39
1.44
1.38
1.01
CeAlO
3
\text{CeAlO}_{3}
14.3
15.1
7.4
16.9
26.7
1.42
1.39
1.41
1.68
1.21
Co
2
​
TiO
4
\text{Co}_{2}\text{TiO}_{4}
8.8
13.1
5.5
1.6
29.7
1.40
1.30
1.36
1.42
1.02
ErNi
2
​
Ge
2
\text{ErNi}_{2}\text{Ge}_{2}
26.8
24.8
19.3
47.6
31.8
1.18
1.26
1.36
0.43
0.90
Ga
2
​
O
3
\text{Ga}_{2}\text{O}_{3}
10.3
12.3
12.7
37.7
32.8
1.34
1.38
1.36
1.76
0.87
Li
2
​
CaSiO
4
\text{Li}_{2}\text{CaSiO}_{4}
15.7
20.5
14.3
29.3
27.4
1.36
1.37
1.41
1.81
1.09
LiSiNO
12.4
10.4
4.1
2.8
27.4
1.38
1.39
1.39
1.50
1.09
Na
2
​
ZnGeO
4
\text{Na}_{2}\text{ZnGeO}_{4}
13.0
15.0
11.5
49.4
22.9
1.40
1.39
1.39
2.35
1.15
SrTiO
3
\text{SrTiO}_{3}
7.2
8.8
12.0
40.6
24.3
1.42
1.41
1.45
1.64
1.11
Avg.
13.7
14.8
10.8
26.6
27.4
1.35
1.37
1.39
1.59
1.06
Table 2
:
LLMatDesign’s performance in achieving a new material with a as low as possible formation energy per atom. Each experiment consists of 50 modifications, and is repeated 30 times.
Starting Material
Average Formation Energy (eV/atom)
Minimum Formation Energy (eV/atom)
Gemini-1.0-pro
GPT-4o
Random
Gemini-1.0-pro
GPT-4o
Random
History
Historyless
History
Historyless
History
Historyless
History
Historyless
BaV
2
​
Ni
2
​
O
8
\text{BaV}_{2}\text{Ni}_{2}\text{O}_{8}
-0.80
-0.20
-2.45
-2.50
-0.12
-2.69
-2.30
-2.91
-2.74
-1.99
CdCu
2
​
GeS
4
\text{CdCu}_{2}\text{GeS}_{4}
-0.19
0.11
-1.05
-0.61
0.29
-1.31
-1.59
-1.61
-0.72
-1.37
CeAlO
3
\text{CeAlO}_{3}
-0.77
-0.28
-2.79
-2.24
-0.04
-3.44
-3.22
-3.73
-3.73
-2.50
TiO
4
\text{}\text{TiO}_{4}
-0.39
0.03
-1.57
-1.49
0.0
-2.64
-2.08
-2.48
-2.10
-1.80
ErNi
2
​
Ge
2
\text{ErNi}_{2}\text{Ge}_{2}
-0.02
-0.19
-0.54
-0.74
-0.11
-0.96
-1.71
-0.94
-1.57
-1.40
Ga
2
​
O
3
\text{Ga}_{2}\text{O}_{3}
-0.19
-0.12
-1.61
-2.07
-0.16
-2.05
-1.82
-3.31
-3.29
-1.67
Li
2
​
CaSiO
4
\text{Li}_{2}\text{CaSiO}_{4}
-0.77
-0.41
-2.30
-2.69
-0.20
-2.94
-2.60
-3.13
-2.98
-2.27
LiSiNO
-0.38
-0.19
-1.75
-1.54
-0.15
-2.01
-2.01
-2.60
-1.72
-1.75
Na
2
​
ZnGeO
4
\text{Na}_{2}\text{ZnGeO}_{4}
-0.79
-0.25
-2.62
-2.52
0.05
-2.48
-2.34
-2.87
-2.55
-1.85
SrTiO
3
\text{SrTiO}_{3}
-1.26
-0.23
-3.01
-3.54
-0.02
-3.40
-3.09
-3.65
-3.57
-2.38
Avg.
-0.56
-0.17
-1.97
-1.99
-0.05
-2.39
-2.28
-2.72
-2.50
-1.90
We observe that GPT-4o with past modification history performs the best in achieving the target band gap value of 1.4 eV, requiring an average of 10.8 modifications (Table
1
). In comparison, Gemini-1.0-pro with history takes an average of 13.7 modifications. Both methods signifcantly outperform the baseline, whic requires 27.4 modifications. Adding modification history to subsequent prompts allows the LLMs to converge to the target more quickly, as both Gemini-1.0-pro and GPT-4o with modification history outperform their historyless counterparts. Notably, the performance gap between the history and historyless variants is smaller for Gemini-1.0-pro than for GPT-4o. From a closer inspection of the modification paths of GPT-4o without history, we find that GPT-4o often alternates between a few of the same modifications until reaching the maximum number of allowed iterations (see Fig.
4
). For the two starting materials where GPT-4o without history performs the best (
Co
2
​
TiO
4
\text{Co}_{2}\text{TiO}_{4}
and
SrTiO
3
\text{SrTiO}_{3}
), the final materials frequently converge to identical composition by following the same modification sequence. This indicates a lack of diversity in the newly generated materials when no history is included in LLMatDesign’s iterative loop. In addition, GPT-4o with history achieves the best final band gap value, averaging 1.39 eV, followed by Gemini-1.0-pro at 1.35 eV, and random at 1.06 eV.
LLMatDesign’s superior performance is also apparent when finding new materials with the lowest formation energy per atom (Table
2
), consistently outperforming the random baseline. Specifically, both the history and historyless variants of GPT-4o achieve the lowest average formation energies, with
−
1.97
-1.97
eV/atom and
−
1.99
-1.99
eV/atom, respectively. GPT-4o with history also achieves the lowest minimum formation energy per atom at
−
2.72
-2.72
eV/atom. Interestingly, while the minimum formation energy per atom values achieved by Gemini-1.0-pro are close to that of GPT-4o, its average formation energy per atom values are significantly higher, indicating that it struggles to consistently suggest chemically stable modifications for the materials. Nonetheless, Gemini-1.0-pro still noticeably outperforms the baseline. In Fig.
D.1
and
D.2
, we visualize 20 materials discovered by LLMatDesign for the band gap and formation energy tasks, respectively. These materials are obtained from the first run of all 10 starting materials. For the band gap task, the final materials are selected. For the formation energy task, the materials with the lowest formation energy per atom are chosen.
Figure 4
:
Average band gaps and formation energies over 50 modifications. The grey horizontal line indicates the target band gap of 1.4 eV. The colored dots on the x-axis indicate the average number of modifications taken for each method to reach the target. For formation energy, the goal is to achieve the lowest possible value.
In Fig.
4
, we plot the band gaps and formation energies per atom over 50 modifications, averaged across 10 starting materials. The target band gap of 1.4 eV is indicated by the grey horizontal line. Both history and historyless variants of Gemini-1.0-pro and GPT-4o demonstrate quick convergence to the target band gap. However, the GPT-4o historyless variant exhibits zig-zag oscillations in band gap values as modifications increase. This occurs because, without historical information, GPT-4o tends to oscillate between a few of the same moves, causing the band gap to fluctuate without improving. In contrast, the random baseline fails to converge to 1.4 eV within the maximum allowed 50 modifications. For formation energy, our findings indicate that GPT-4o is consistently able to suggest modifications which keep formation energy low on average around
−
2
-2
eV/atom, though Gemini-1.0-pro struggles to do so despite being able to obtain a low minimum formation energy. Notably, neither GPT-4o nor Gemini-1.0-pro are able to beat the formation energy of the starting materials, likely due to the the fact that these materials are already at or near the lowest energy states.
BG: Gemini-1.0-pro with history
BG: GPT-4o with history
BG: Random
FE: Gemini-1.0-pro with history
FE: GPT-4o with history
FE: Random
Figure 5
:
Heatmaps of element frequencies in band gap (BG) and formation energy (FE) tasks. The periodic table is color-coded to indicate the frequency of each element’s occurrence in all modified materials (both intermediate and final) across all runs and starting materials. Darker colors represent higher frequencies, while lighter colors denote lower frequencies or absence. The visualization employs log-scaling to effectively highlight the distribution and prevalence of elements.
Fig.
5
presents heatmaps over the periodic table displaying the element occurrences in the modifications for both the band gap and formation energy tasks, which reveal additional insights into the reason for the good performance for LLM-driven design. The number of occurrences of each element is collected across all runs and starting materials. In the heatmaps for the random baseline, all elements are chosen at nearly uniform frequencies. This result is to be expected, as the random algorithm samples elements with atomic numbers up to 99 uniformly. Meanwhile, in the heatmaps for the LLM cases, there is a clear distribution towards certain elements, mostly focusing on elements within the first four rows of the periodic table and avoiding noble metals and Actinides. Both LLM models share similar distributions, such as a preference for elements like oxygen, however Gemini-1.0-pro’s suggestions appear to exhibit a greater element diversity compared to GPT-4o, including some of the transition metals. With Gemini-1.0-pro, we also occasionally observe modifications suggested by the LLM that include noble gases, which is not chemically feasible due to their inert nature. With GPT-4o, this does not occur (see Fig.
C.1
). Regardless, both LLM models are able to consistently suggest chemically viable elements for modification, which is akin to how a human expert would make similar choices based on chemical intuition or from past examples in the literature.
In Fig.
6
, we present an example of the full process whereby LLMatDesign successfully completes a design task to achieve a band gap of 1.40 eV. In the first step, LLMatDesign suggests modifying the starting material
CdCu
2
​
GeS
4
\text{CdCu}_{2}\text{GeS}_{4}
by substituting S with Se, given the hypothesis that increasing atomic radius and changing the electronegativity can alter the band gap. Upon modification, the new material
CdCu
2
​
GeSe
4
\text{CdCu}_{2}\text{GeSe}_{4}
was found to have an even smaller band gap, which is contrary to the desired effect as noted by the reflection. This history is included in the second step of modification, whereby LLMatDesign suggests a subsequent modification of Ge with Si, which increases the gap. The reflection notes a partial success is achieved, but is still not enough to reach the target, whereupon a third step is taken. In the third step, Cu is substituted with Zn, which finally achieves the desired band gap within an acceptable threshold, ending the process. From this example, we can observe the LLM is successful at 1) recognizing differences in element properties (i.e. Se having a larger atomic radius than S), 2) highlighting these properties as being relevant to the design task (i.e. atomic radius, electronegativity, and electronic configuration affecting the band hap), 3) and recognizing whether a modification is successful and the degree of success in the reflection. We will show in the subsequent section that it is this reasoning and reflection process which has a significant impact on its success.
In the final step of the design process, a DFT calculation is performed to validate the material’s properties which were obtained from a ML surrogate model. Here, we use DFT to compute the formation energy of the minimum energy structures in all 30 runs for each 10 starting materials obtained with GPT-4o and random sampling. On average, structures generated by LLMatDesign using GPT-4o with history achieved a formation energy of -2.32 eV/atom with a job completion rate of 73.3%. In comparison, the random baseline obtained an average formation energy of -1.51 eV/atom, with a significantly lower job completion rate of 40.0% (see Fig.
E.1
). The lower completion rate is likely due to a much higher likelihood of unreasonable compositions and configurations obtained from random sampling which cause the DFT calculations to fail. These results also follow the same relative trends in Table
2
. In a situation where DFT is directly used in each iteration rather than a surrogate model, this step can be omitted, or potentially the materials can be validated further with experiments.
Figure 6
:
Example of LLMatDesign with GPT-4o on the task of modifying the starting material
CdCu
2
​
GeS
4
\text{CdCu}_{2}\text{GeS}_{4}
to achieve a band gap of 1.40 eV. The starting material is retrieved from the Materials Project with chemical formula
Cd
2
​
Cu
4
​
Ge
2
​
S
8
\text{Cd}_{2}\text{Cu}_{4}\text{Ge}_{2}\text{S}_{8}
.
2.3
Self-reflection
To quantify the effect of self-reflection on the performance of LLMatDesign, we conduct band gap experiments using GPT-4o and the same set of 10 starting materials, where we aim to find a new material with a target band gap of 1.4 eV. Like with the history variant, past modifications are incorporated into the prompting loop. However, in this case, self-reflection is omitted completely. In other words, the history message only includes the modification and hypothesis pairs (see Algo.
1
). The results from these experiments are shown in Table
3
. As previously discussed, GPT-4o with history achieves an average of 10.8 modifications, while GPT-4o without history requires 26.6 modifications. In comparison, GPT-4o with history but without self-reflection now needs an average of 23.4 modifications, which is over twice as many compared to including self-reflection. These results suggest that self-reflection, which involves the LLM evaluating and reasoning through its previous design choices, plays a crucial role in enhancing the efficiency of LLMatDesign in achieving the given objective.
Table 3
:
LLMatDesign with and without self-reflection. GPT-4o is used as the LLM engine.
Starting Material
Average # of Modifications
History
Historyless
History without reflection
BaV
2
​
Ni
2
​
O
8
\text{BaV}_{2}\text{Ni}_{2}\text{O}_{8}
17.7
30.4
45.1
CdCu
2
​
GeS
4
\text{CdCu}_{2}\text{GeS}_{4}
3.3
9.5
5.0
CeAlO
3
\text{CeAlO}_{3}
7.4
16.9
27.6
Co
2
​
TiO
4
\text{Co}_{2}\text{TiO}_{4}
5.5
1.6
7.9
ErNi
2
​
Ge
2
\text{ErNi}_{2}\text{Ge}_{2}
19.3
47.6
31.0
Ga
2
​
O
3
\text{Ga}_{2}\text{O}_{3}
12.7
37.7
13.1
Li
2
​
CaSiO
4
\text{Li}_{2}\text{CaSiO}_{4}
14.3
29.3
31.4
LiSiNO
4.1
2.8
5.1
Na
2
​
ZnGeO
4
\text{Na}_{2}\text{ZnGeO}_{4}
11.5
49.4
31.5
SrTiO
3
\text{SrTiO}_{3}
12.0
40.6
36.7
Avg.
10.8
26.6
23.4
2.4
Prompting
Well-crafted prompts are essential for eliciting accurate and useful responses from LLMs. While the base prompt template, shown in Fig.
2
, works as intended, we subsequently show that optimizing this prompt can improve the performance of LLMatDesign even further. To this end, we develop two additional prompt templates in a non-exhaustive demonstration. The first template, termed
GPT-4o Refined
, is an enhancement of the original prompt (Fig.
2
) created by GPT-4o itself. This refinement includes rephrasing and reformatting parts of the original prompt and appending the following sentence: “Take a deep breath and work on this problem step-by-step. Your thoughtful and detailed analysis is highly appreciated.” The second template, named
Persona
, mirrors the original prompt but incorporates the persona of a materials specialist. Specifically, it begins with a declaration that the LLM is a materials design expert working on developing new materials with specific properties. Detailed descriptions of these prompt templates are provided in Appendix
A
.
We conduct the same experiments on the band gap task using GPT-4o as the LLM engine for LLMatDesign across all 10 starting materials. The results, shown in Table
4
, indicate that both the GPT-4o Refined and Persona prompt templates outperform the GPT-4o with history, with the GPT-4o Refined template achieving the best performance, requiring an average of only 8.69 modifications to complete the task. The improvement over the original prompt template indicates that careful prompt optimization can positively enhance the efficiency and accuracy of LLM-directed materials discovery frameworks, and that this process can even be performed by the LLM itself. This is a particularly intriguing discovery as it hints towards an unprecedented level of autonomy which can be enabled by LLMs, whereby the prompts and instructions in the framework can be continuously tuned in an automated manner with minimal human intervention.
Table 4
:
LLMatDesign with different prompts. GPT-4o is used as the LLM engine.
Starting Material
Average # of Modifications
History
GPT-4o Refined
Persona
BaV
2
​
Ni
2
​
O
8
\text{BaV}_{2}\text{Ni}_{2}\text{O}_{8}
17.7
13.4
9.6
CdCu
2
​
GeS
4
\text{CdCu}_{2}\text{GeS}_{4}
3.3
3.1
5.3
CeAlO
3
\text{CeAlO}_{3}
7.4
7.2
8.7
Co
2
​
TiO
4
\text{Co}_{2}\text{TiO}_{4}
5.5
8.9
11.9
ErNi
2
​
Ge
2
\text{ErNi}_{2}\text{Ge}_{2}
19.3
11.9
11.7
Ga
2
​
O
3
\text{Ga}_{2}\text{O}_{3}
12.7
8.4
8.3
Li
2
​
CaSiO
4
\text{Li}_{2}\text{CaSiO}_{4}
14.3
11.6
11.9
LiSiNO
4.1
5.6
1.0
Na
2
​
ZnGeO
4
\text{Na}_{2}\text{ZnGeO}_{4}
11.5
6.9
8.8
SrTiO
3
\text{SrTiO}_{3}
12.0
9.9
13.9
Avg.
10.8
8.69
9.11
2.5
Constrained Materials Design
Materials discovery with constraints ensures scientific, economic, and political viability. For instance, avoiding the use of rare earth metals can reduce dependency on limited and expensive resources, mitigate supply chain risks, and align with environmental and ethical standards. To this end, we evaluate LLMatDesign under three constraints limiting its action space. Experiments are conducted on the band gap task using the starting material
SrTiO
3
\text{SrTiO}_{3}
with GPT-4o to test whether these constraints are obeyed. Like before, each experiment is repeated 30 times, and the percentage of modifications adhering strictly to the constraints is calculated across all runs. As shown in Table
5
, LLMatDesign perfectly adheres to the constraints of “do not use Ba or Ca” and “do not modify Sr,” achieving 100% compliant modifications. For the constraint “do not have more than 4 distinct elements,” only 4 out of 509 modifications by LLMatDesign include 5 distinct elements, resulting in a high compliance rate of 99.02%. These results demonstrate LLMatDesign’s robust capability in adhering to predefined constraints as described by natural language, an advantage unique to LLM-driven design.
Table 5
:
LLMatDesign with different constraints on
SrTiO
3
\text{SrTiO}_{3}
.
Constraint
% compliant modifications
Do not use Ba or Ca
100
Do not modify Sr
100
Do not have more than 4 distinct elements
99.02
2.6
Further Discussion
Through extensive experiments, we find LLMatDesign consistently outperforms baselines by a significant margin, demonstrating the viability of using LLM-based autonomous agents for materials discovery tasks under a limited budget. While the random baseline uniformly samples from a set of elements for modification (see Fig.
5
), LLMatDesign, whether utilizing GPT-4o or Gemini-1.0-pro, exhibits inherent chemical knowledge, enabling it to provide chemically meaningful suggestions. Furthermore, GPT-4o accurately recognizes periodic trends such as atomic radius and electronegativity in its hypotheses and self-reflections in guiding its decisions. In contrast, Gemini-1.0-pro is more prone to errors in this regard, likely due to it being a less robust LLM. Further experiments also show the critical role of self-reflection in the performance of the LLM. This indicates that by reviewing and learning from its previous decisions, LLMatDesign can refine its future suggestions more effectively. This iterative learning process helps the model understand the implications of its modifications better, leading to quicker convergence. In general, it is evident that there are more complex underpinnings behind the remarkable effectiveness of LLM-driven design than simply predicting most likely outcomes.
This work also demonstrates the
lower-bound
capabilities of LLM-based design, which is performed without further fine-tuning in a zero-shot manner. A natural extension of this approach would be to further train LLMs on chemical and materials knowledge, such as those obtained from literature articles. In the future, it would be highly desirable for a chemically fine-tuned to provide more insightful hypotheses and explanations, and even refer to specific references of prior published experiments to support them. These capabilities can potentially be within reach given the growing prevalence of powerful open-source LLMs and parameter-efficient fine-tuning.
In the current examples, LLMatDesign comes up with new materials designs from a limited set of modifications on the composition of a material. Nonetheless, this framework is general and can include more complex modifications which act not only on the composition space but also the structure space. Future work in this direction will focus on incorporating structural information when describing the material being modified, and also suggest modifications which directly act on the positions and lattice of the crystal structure. To this end, recent advances in multimodal LLMs can be applied here, where the atomic structure is considered to be an additional modality to be encoded in addition to the text modality.
3
Conclusion
In this work, we present LLMatDesign, a novel materials design framework powered by state-of-the-art LLMs that works directly with user-defined design requirements and constraints in natural language. It integrates computational tools for structure relaxation and property evaluation, incorporates internal chemical knowledge, and learns from previous iterations to function as an automated material design framework with high efficiency.
Additionally, LLMatDesign quickly adapt to different tasks, target properties and design constraints by simply modifying the prompt. In our experiments, LLMatDesign consistently outperforms the baseline, demonstrating the effectiveness of the framework in developing new materials. Our work highlights the potential for fully automated AI-driven materials discovery that can be seamlessly integrated into autonomous laboratories in the future.
4
Methods
4.1
Large Language Models
Large language models (LLMs) are a class of machine learning models built on the transformer architecture
[
37
]
. By training on vast amounts of text data, these models can understand and generate text in a human-like manner. In this work, GPT-4o
[
34
]
refers to OpenAI’s
gpt-4o
model, which has a context length of 128K and a knowledge cutoff date of October 2023. Gemini-1.0-pro
[
35
]
refers to Google’s LLM with the same name, featuring a context length of 32K.
4.2
Machine Learning Force Field
Machine learning force fields (MLFFs) represent a significant advancement in computational chemistry and materials science. By utilizing state-of-the-art machine learning models and training on extensive datasets of atomic structures with energies, forces, and stresses, MLFFs can achieve high accuracy in predicting these properties, often rivaling ab initio methods such as density functional theory (DFT)
[
38
]
. More importantly, MLFFs provide these high-accuracy predictions with unprecedented computational efficiency, enabling the simulation of larger systems and longer timescales. In this study, we train a TorchMD-Net model
[
39
]
using the MatDeepLearn framework
[
40
,
41
]
. The training dataset, curated from the Materials Project
[
6
]
, comprises 187,687 crystal structures with associated energies, forces, and stresses. The model is trained for 400 epochs on a single Nvidia A100 80GB GPU.
4.3
Machine Learning Property Predictor
Similar to machine learning force fields (MLFFs), machine learning property predictors (MLPPs) leverage advanced machine learning models trained on large datasets to make fast and accurate predictions for specific target properties. In this study, we train TorchMD-Net models to predict two separate properties: band gap and formation energy per atom. The datasets used are the
mp_gap
and
mp_form
datasets from the MatBench benchmark
[
42
]
, containing 106,113 and 132,752 structures from the Materials Project
[
6
]
, respectively. Each model is trained for 200 epochs on a single Nvidia A100 80GB GPU.
4.4
Modification of Material
Once LLMatDesign suggests a modification to achieve the user’s target objective, the material is modified accordingly. Specifically, as illustrated in Fig.
1
, there are four types of modifications:
exchange
,
substitute
,
remove
, and
add
. Each modification is applied directly to an
ase.Atoms
object representing the material. For example, given the modification
[‘exchange’, ‘Sr’, ‘Ti’]
, all Sr atoms in the material are replaced with Ti atoms and vice versa. After applying the modification, the structure undergoes relaxation using a machine learning force field (MLFF).
4.5
Modification of Material
The DFT calculations were performed using the Vienna Ab Initio Simulation Package (VASP)
[
43
,
44
]
. All calculations followed the same settings specified by the ”MPRelaxSet” in the Pymatgen library
[
45
]
used in Materials Project.
5
Data Availability
The authors declare that the data, materials and code supporting the results reported in this study are available upon the publication of this manuscript.
6
Acknowledgements
We thank Lingkai Kong and Rui Feng for helpful discussions.
This research used resources of the National Energy Research Scientific Computing Center (NERSC), a U.S. Department of Energy Office of Science User Facility located at Lawrence Berkeley National Laboratory, operated under Contract No. DE-AC02-05CH11231 using NERSC award BES-ERCAP0022842.
References
[1]
Davies, D. W.
et al.
Computational screening of all stoichiometric inorganic materials.
Chem
1
, 617–627 (2016).
[2]
Oganov, A. R., Pickard, C. J., Zhu, Q. & Needs, R. J.
Structure prediction drives materials discovery.
Nature Reviews Materials
4
, 331–348 (2019).
[3]
Liu, Y., Zhao, T., Ju, W. & Shi, S.
Materials discovery and design using machine learning.
Journal of Materiomics
3
, 159–177 (2017).
[4]
Hautier, G., Jain, A. & Ong, S. P.
From the computer to the laboratory: materials discovery and design using first-principles calculations.
Journal of Materials Science
47
, 7317–7340 (2012).
[5]
Pyzer-Knapp, E. O., Suh, C., Gómez-Bombarelli, R., Aguilera-Iparraguirre, J. & Aspuru-Guzik, A.
What is high-throughput virtual screening? a perspective from organic materials discovery.
Annual Review of Materials Research
45
, 195–216 (2015).
[6]
Chen, C. & Ong, S. P.
A universal graph deep learning interatomic potential for the periodic table.
Nature Computational Science
2
, 718–728 (2022).
[7]
Merchant, A.
et al.
Scaling deep learning for materials discovery.
Nature
624
, 80–85 (2023).
[8]
Hoffmann, J.
et al.
Data-driven approach to encoding and decoding 3-d crystal structures.
arXiv preprint arXiv:1909.00949
(2019).
[9]
Court, C. J., Yildirim, B., Jain, A. & Cole, J. M.
3-d inorganic crystal structure generation and property prediction via representation learning.
Journal of Chemical Information and Modeling
60
, 4518–4535 (2020).
[10]
Xie, T., Fu, X., Ganea, O.-E., Barzilay, R. & Jaakkola, T.
Crystal diffusion variational autoencoder for periodic material generation.
arXiv preprint arXiv:2110.06197
(2021).
[11]
Long, T.
et al.
Constrained crystals deep convolutional generative adversarial network for the inverse design of crystal structures.
npj Computational Materials
7
, 66 (2021).
[12]
Ren, Z.
et al.
An invertible crystallographic representation for general inverse design of inorganic crystals with targeted properties.
Matter
5
, 314–335 (2022).
[13]
Fung, V.
et al.
Atomic structure generation from reconstructing structural fingerprints.
Machine Learning: Science and Technology
3
, 045018 (2022).
[14]
Zeni, C.
et al.
Mattergen: a generative model for inorganic materials design.
arXiv preprint arXiv:2312.03687
(2023).
[15]
Wei, J.
et al.
Chain-of-thought prompting elicits reasoning in large language models.
Advances in neural information processing systems
35
, 24824–24837 (2022).
[16]
Huang, J. & Chang, K. C.-C.
Towards reasoning in large language models: A survey.
arXiv preprint arXiv:2212.10403
(2022).
[17]
Li, S.
et al.
Pre-trained language models for interactive decision-making.
Advances in Neural Information Processing Systems
35
, 31199–31212 (2022).
[18]
Ahn, M.
et al.
Do as i can, not as i say: Grounding language in robotic affordances.
arXiv preprint arXiv:2204.01691
(2022).
[19]
Huang, W.
et al.
Voxposer: Composable 3d value maps for robotic manipulation with language models.
arXiv preprint arXiv:2307.05973
(2023).
[20]
Boiko, D. A., MacKnight, R., Kline, B. & Gomes, G.
Autonomous chemical research with large language models.
Nature
624
, 570–578 (2023).
[21]
Bran, A. M.
et al.
Chemcrow: Augmenting large-language models with chemistry tools.
arXiv preprint arXiv:2304.05376
(2023).
[22]
AI4Science, M. R. & Quantum, M. A.
The impact of large language models on scientific discovery: a preliminary study using gpt-4.
arXiv preprint arXiv:2311.07361
(2023).
[23]
Mirza, A.
et al.
Are large language models superhuman chemists?
arXiv preprint arXiv:2404.01475
(2024).
[24]
Fan, V.
et al.
Openchemie: An information extraction toolkit for chemistry literature.
arXiv preprint arXiv:2404.01462
(2024).
[25]
Ai, Q., Meng, F., Shi, J., Pelkie, B. & Coley, C. W.
Extracting structured data from organic synthesis procedures using a fine-tuned large language model.
ChemRxiv preprint 10.26434/chemrxiv-2024-979fz
(2024).
[26]
Zhong, Z., Zhou, K. & Mottin, D.
Benchmarking large language models for molecule prediction tasks.
arXiv preprint arXiv:2403.05075
(2024).
[27]
Xie, Z.
et al.
Fine-tuning gpt-3 for machine learning electronic and functional properties of organic molecules.
Chemical science
15
, 500–510 (2024).
[28]
Jablonka, K. M., Schwaller, P., Ortega-Guerrero, A. & Smit, B.
Leveraging large language models for predictive chemistry.
Nature Machine Intelligence
1–9 (2024).
[29]
Ock, J., Guntuboina, C. & Barati Farimani, A.
Catalyst energy prediction with catberta: Unveiling feature exploration strategies through large language models.
ACS Catalysis
13
, 16032–16044 (2023).
[30]
Flam-Shepherd, D. & Aspuru-Guzik, A.
Language models can generate molecules, materials, and protein binding sites directly in three dimensions as xyz, cif, and pdb files.
arXiv preprint arXiv:2305.05708
(2023).
[31]
Antunes, L. M., Butler, K. T. & Grau-Crespo, R.
Crystal structure generation with autoregressive large language modeling.
arXiv preprint arXiv:2307.04340
(2023).
[32]
Gruver, N.
et al.
Fine-tuned language models generate stable inorganic materials as text.
arXiv preprint arXiv:2402.04379
(2024).
[33]
Jain, A.
et al.
Commentary: The materials project: A materials genome approach to accelerating materials innovation.
APL materials
1
(2013).
[34]
Achiam, J.
et al.
Gpt-4 technical report.
arXiv preprint arXiv:2303.08774
(2023).
[35]
Team, G.
et al.
Gemini: a family of highly capable multimodal models.
arXiv preprint arXiv:2312.11805
(2023).
[36]
Sutherland, B. R.
Solar materials find their band gap.
Joule
4
, 984–985 (2020).
[37]
Vaswani, A.
et al.
Attention is all you need.
Advances in neural information processing systems
30
(2017).
[38]
Ko, T. W. & Ong, S. P.
Recent advances and outstanding challenges for machine learning interatomic potentials.
Nature Computational Science
3
, 998–1000 (2023).
[39]
Thölke, P. & De Fabritiis, G.
Torchmd-net: Equivariant transformers for neural network based molecular potentials.
arXiv preprint arXiv:2202.02541
(2022).
[40]
Fung, V., Zhang, J., Juarez, E. & Sumpter, B. G.
Benchmarking graph neural networks for materials chemistry.
npj Computational Materials
7
, 84 (2021).
[41]
Jia, S.
et al.
Derivative-based pre-training of graph neural networks for materials property predictions.
Digital Discovery
3
, 586–593 (2024).
[42]
Dunn, A., Wang, Q., Ganose, A., Dopp, D. & Jain, A.
Benchmarking materials property prediction methods: the matbench test set and automatminer reference algorithm.
npj Computational Materials
6
, 138 (2020).
[43]
Kresse, G. & Furthmüller, J.
Efficient iterative schemes for ab initio total-energy calculations using a plane-wave basis set.
Physical review B
54
, 11169 (1996).
[44]
Kresse, G. & Furthmüller, J.
Efficiency of ab-initio total energy calculations for metals and semiconductors using a plane-wave basis set.
Computational materials science
6
, 15–50 (1996).
[45]
Ong, S. P.
et al.
Python materials genomics (pymatgen): A robust, open-source python library for materials analysis.
Computational Materials Science
68
, 314–319 (2013).
Supplementary Information
Appendix A
Prompt Templates for LLMatDesign
A slightly different prompt template to Fig.
2
is designed for Gemini-1.0-pro due to its inconsistency in generating standardized output.
LLMatDesign Prompt Template (Gemini-1.0-pro)
I have a material and its
<property>
.
<definition of property>
.
(
<chemical composition>
,
<property value>
)
You will be given a starting material to be modified. Try to achieve
<objective>
. Make an informed choice of modification based on the given material and past modifications and property values obtained after those modifications. Output a list for the suggested modification, and a string of the reason why you think it is a good modification to take to achieve
<objective>
. Make sure the modification is physically meaningful.
Material to be modified:
<chemical composition>
Current property value:
<property value>
<modification history>
Available modifications:
1.
exchange: exchange two elements in the material
2.
substitute: substitute one element in the material with another
3.
remove: remove an element from the material
4.
add: add an element to the material
Example output format:
1.
["exchange", "O", "N"], "some reason here"
2.
["substitute", "Ti", "Fe"], "some reason here"
3.
["add", "O"], "some reason here"
4.
["remove", "O"], "some reason here"
Figure A.1
:
Prompt template for LLMatDesign with Gemini-1.0-pro. Text placeholders in red angular brackets are specific to the task given to LLMatDesign. Text placeholders in blue angular brackets are optional and can be omitted if not needed.
GPT-4o Refined Prompt Template for LLMatDesign
I have a material with a known
<property>
.
<definition of property>
.
Material information:
•
Chemical formula:
<chemical composition>
•
<property>
:
<property value>
Objective:
Propose a modification to this material to achieve
<objective>
. You can choose one of the following modification types:
1.
exchange: exchange two elements in the material
2.
substitute: substitute one element in the material with another
3.
remove: remove an element from the material
4.
add: add an element to the material
Your response should be a Python dictionary in the following format:
‘‘‘
{Hypothesis: $HYPOTHESIS, Modification: [$TYPE, $ELEMENT_1, $ELEMENT_2]}.
‘‘‘
Requirements:
1.
$HYPOTHESIS: Provide a detailed analysis and rationale for your proposed modification.
2.
$TYPE:Specify the type of modification (“exchange”, “substitute”, “remove”, “add”).
3.
$Identify the element(s) involved in the modification. For ”exchange” and ”substitute”, include two elements ($ELEMENT_1 and $ELEMENT_2). For “remove” and “add”, include one element ($ELEMENT_1).
<modification history>
Take a deep breath and work on this problem step-by-step. Your thoughtful and detailed analysis is highly appreciated.
Figure A.2
:
GPT-4o refined prompt template for LLMatDesign. Text placeholders in red angular brackets are specific to the task given to LLMatDesign. Text placeholders in blue angular brackets are optional and can be omitted if not needed.
Persona Prompt Template for LLMatDesign
You are a materials design expert working on the development of new materials with specific properties. You will be given a composition (chemical formula) and its corresponding
<property>
. You will be asked to propose a modification to the material to achieve a target
<property>
.
Material information:
•
Chemical formula:
<chemical composition>
•
<property>
:
<property value>
Objective:
Propose a modification to this material to achieve
<objective>
. You can choose one of the following modification types:
1.
exchange: exchange two elements in the material
2.
substitute: substitute one element in the material with another
3.
remove: remove an element from the material
4.
add: add an element to the material
Your response should be a Python dictionary in the following format:
‘‘‘
{Hypothesis: $HYPOTHESIS, Modification: [$TYPE, $ELEMENT_1, $ELEMENT_2]}.
‘‘‘
Requirements:
1.
$HYPOTHESIS: Provide a detailed analysis and rationale for your proposed modification.
2.
$TYPE:Specify the type of modification (“exchange”, “substitute”, “remove”, “add”).
3.
$Identify the element(s) involved in the modification. For ”exchange” and ”substitute”, include two elements ($ELEMENT_1 and $ELEMENT_2). For “remove” and “add”, include one element ($ELEMENT_1).
<modification history>
Take a deep breath and work on this problem step-by-step. Your thoughtful and detailed analysis is highly appreciated.
Figure A.3
:
Prompt template with materials design expert persona for LLMatDesign. Text placeholders in red angular brackets are specific to the task given to LLMatDesign. Text placeholders in blue angular brackets are optional and can be omitted if not needed.
Appendix B
Convergence Plots
Figure B.1
:
Average band gaps over 50 modifications for all 10 starting materials using GPT-4o. The grey horizontal line indicates the target band gap of 1.4 eV. The colored dots on the x-axis indicate the average number of modifications taken for each method to reach the target.
Figure B.2
:
Average band gaps over 50 modifications for all 10 starting materials using Gemini-1.0-pro. The grey horizontal line indicates the target band gap of 1.4 eV. The colored dots on the x-axis indicate the average number of modifications taken for each method to reach the target.
Figure B.3
:
Average formation energies over 50 modifications for all 10 starting materials using GPT-4o. The goal is to achieve the lowest possible formation energy per atom.
Figure B.4
:
Average formation energies over 50 modifications for all 10 starting materials using Gemini-1.0-pro. The goal is to achieve the lowest possible formation energy per atom.
Appendix C
Heatmaps
BG: Gemini-1.0-pro without history
BG: GPT-4o without history
FE: Gemini-1.0-pro without history
FE: GPT-4o without history
Figure C.1
:
Heatmaps of element frequencies in band gap (BG) and formation energy (FE) tasks for Gemini-1.0-pro and GPT-4o without history. The periodic table is color-coded to indicate the frequency of each element’s occurrence in all modified materials (both intermediate and final) across all runs and starting materials. Darker colors represent higher frequencies, while lighter colors denote lower frequencies or absence. The visualization employs log-scaling to effectively highlight the distribution and prevalence of elements.
Appendix D
Visualization of Selected Structures
\begin{overpic}[structure_vis/band_gap.pdf]
\put(10.0,73.0){{\color[rgb]{1,0,0}SrTiO${}_{3}$}}
\put(10.0,70.0){{Ba${}_{2}$Tl${}_{2}$PNO${}_{6}$}}
\put(10.0,67.0){1.51 eV}
\par\put(40.0,73.0){{\color[rgb]{1,0,0}BaV${}_{2}$Ni${}_{2}$O${}_{8}$}}
\put(40.0,70.0){BaCd${}_{2}$(MoO${}_{5}$)${}_{2}$}
\put(40.0,67.0){1.30 eV}
\par\put(72.0,73.0){{\color[rgb]{1,0,0}Co${}_{2}$TiO${}_{4}$}}
\put(72.0,70.0){Co${}_{2}$SO${}_{4}$}
\put(72.0,67.0){1.42 eV}
\par\put(10.0,41.0){{\color[rgb]{1,0,0}ErNi${}_{2}$Ge${}_{2}$}}
\put(10.0,38.0){ErGa${}_{2}$S${}_{2}$O}
\put(10.0,35.0){1.39 eV}
\par\put(40.0,41.0){{\color[rgb]{1,0,0}CeAlO${}_{3}$}}
\put(40.0,38.0){FeGeO${}_{3}$}
\put(40.0,35.0){1.49 eV}
\par\put(72.0,41.0){{\color[rgb]{1,0,0}Li${}_{2}$CaSiO${}_{4}$}}
\put(72.0,38.0){LiSnO${}_{2}$}
\put(72.0,35.0){1.29 eV}
\par\put(7.0,10.0){{\color[rgb]{1,0,0}CdCu$2$GeS$4$}}
\put(7.0,7.0){Zn${}_{2}$CdSiSe${}_{4}$}
\put(7.0,4.0){1.42 eV}
\par\put(30.0,10.0){{\color[rgb]{1,0,0}Na${}_{2}$ZnGeO${}_{4}$}}
\put(30.0,7.0){Na${}_{4}$MnFe${}_{2}$(GeO${}_{4}$)${}_{2}$}
\put(30.0,4.0){1.41 eV}
\par\put(59.0,10.0){{\color[rgb]{1,0,0}LiSiNO}}
\put(59.0,7.0){LiGePS}
\put(59.0,4.0){1.30 eV}
\par\put(84.0,10.0){{\color[rgb]{1,0,0}Ga${}_{2}$O${}_{3}$}}
\put(84.0,7.0){Ga${}_{4}$SnO${}_{6}$}
\put(84.0,4.0){1.33 eV}
\par\end{overpic}
Figure D.1
:
Visualization of the final structures obtained by LLMatDesign for the band gap task. These structures are obtained from the first run of all 10 starting materials. The chemical formulae in red represent the starting materials, followed by the formulae of the final structures and their corresponding band gaps. GPT-4o with history is utilized as the LLM engine.
\begin{overpic}[structure_vis/formation_energy.pdf]
\put(10.0,73.0){{\color[rgb]{1,0,0}BaV${}_{2}$Ni${}_{2}$O${}_{8}$}}
\put(10.0,70.0){{BaTi${}_{2}$V${}_{2}$O${}_{8}$}}
\put(10.0,67.0){$-3.09$ eV/atom}
\par\put(40.0,73.0){{\color[rgb]{1,0,0}SrTiO${}_{3}$}}
\put(40.0,70.0){BaTiO${}_{3}$}
\put(40.0,67.0){$-3.56$ eV/atom}
\par\put(72.0,73.0){{\color[rgb]{1,0,0}Li${}_{2}$CaSiO${}_{4}$}}
\put(72.0,70.0){Li${}_{2}$CaSiO${}_{4}$}
\put(72.0,67.0){$-3.03$ eV/atom}
\par\put(10.0,41.0){{\color[rgb]{1,0,0}Co${}_{2}$TiO${}_{4}$}}
\put(10.0,38.0){TiMnO${}_{3}$}
\put(10.0,35.0){$-2.38$ eV/atom}
\par\put(40.0,41.0){{\color[rgb]{1,0,0}ErNi${}_{2}$Ge${}_{2}$}}
\put(40.0,38.0){LaAl(NiS)${}_{2}$}
\put(40.0,35.0){$-1.19$ eV/atom}
\par\put(72.0,41.0){{\color[rgb]{1,0,0}Na${}_{2}$ZnGeO${}_{4}$}}
\put(72.0,38.0){Li${}_{2}$AlSiO${}_{4}$}
\put(72.0,35.0){$-2.85$ eV/atom}
\par\put(7.0,10.0){{\color[rgb]{1,0,0}LiSiNO}}
\put(7.0,7.0){Li${}_{2}$Si${}_{2}$N${}_{2}$O${}_{2}$F}
\put(7.0,4.0){$-2.21$ eV/atom}
\par\put(32.0,10.0){{\color[rgb]{1,0,0}CdCu$2$GeS$4$}}
\put(32.0,7.0){MgAl${}_{6}$O${}_{10}$}
\put(32.0,4.0){$-2.87$ eV/atom}
\par\put(58.0,10.0){{\color[rgb]{1,0,0}CeAlO${}_{3}$}}
\put(58.0,7.0){YScO${}_{3}$}
\put(58.0,4.0){$-3.75$ eV/atom}
\par\put(84.0,10.0){{\color[rgb]{1,0,0}Ga${}_{2}$O${}_{3}$}}
\put(84.0,7.0){Al${}_{2}$O${}_{3}$}
\put(84.0,4.0){$-3.29$ eV/atom}
\par\end{overpic}
Figure D.2
:
Visualization of the final structures obtained by LLMatDesign for the formation energy task. These structures represent the ones with the minimum formation energy per atom from the first run of all 10 starting materials. The chemical formulae in red represent the starting materials, followed by the formulae of the structures with the lowest formation energies and their corresponding formation energy per atom values. GPT-4o with history is utilized as the LLM engine.
Appendix E
DFT Calculations
Table E.1
:
DFT results for lowest-energy structures obtained from the formation energy task, averaged across all starting materials and runs.
GPT-4o with history
Random
Formation energy per atom (eV/atom)
−
2.31
-2.31
−
1.51
-1.51
Job success rate (%)
73.3
40.0