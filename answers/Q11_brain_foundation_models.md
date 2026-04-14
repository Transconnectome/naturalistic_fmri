# Q11: Brain_Foundation_Models

Based on the provided sources, here is a detailed synthesis addressing your query regarding the progression toward a "Brain Foundation Model." 

*Please note: The provided sources do not contain specific information regarding the "SwiFT," "BrainLM," or "Thomas et al." spatiotemporal transformer architectures, nor do they explicitly detail AI "scaling laws" or "masked reconstruction" pretraining objectives. The response below strictly synthesizes the relevant information available in the sources regarding large-scale datasets, state-space/dynamic modeling, hyperalignment, cross-subject consistency, and current deep neural network (DNN) modeling of brain activity.*

### (a) Corpus-Level Progress Toward a Brain Foundation Model

The development of models capable of generalizing across subjects, stimuli, and tasks requires massive amounts of high-quality, ecologically valid data and robust alignment techniques. 

**Large-Scale Datasets**
The field has amassed increasingly large datasets to capture vast inter-subject and intra-subject variance:
*   **Human Connectome Project (HCP):** The HCP provides a uniquely rich repository of high-quality, multimodal magnetic resonance imaging (MRI) data [1]. Data are acquired at high spatial and temporal resolutions on both customized 3T and 7T scanners, utilizing slice-accelerated "multiband" sequences for resting-state and task fMRI [2-5].
*   **UK Biobank:** Representing a population-based cohort, the UK Biobank has recruited over 500,000 participants, with neuroimaging data available for over 10,000 individuals, providing immense statistical power for brain-behavior modeling and classification [6].
*   **Naturalistic Neuroimaging Database:** Open-science initiatives like this database provide preprocessed fMRI data from participants watching full-length movies (e.g., 86 participants), facilitating open-ended, data-driven modeling of complex, real-world stimulus processing [7].

**Hyperalignment as Pretraining / Data Harmonization**
A major challenge in creating generalized brain models is inter-subject anatomical and functional variability [8]. Traditional models rely on structural alignment, but sources point to **"hyperalignment"** as a vital step forward. By aligning data using the functional signals themselves—such as the evoked BOLD-signal time courses during naturalistic movie-watching—researchers can align participants in a shared representational space [8]. Hyperalignment has been shown to significantly boost classification accuracies of individual subjects and conditions, providing a powerful harmonization step for generalized foundation models [8].

### (b) Architectural and Data Requirements

To capture the brain's complex spatial and temporal dynamics, models require specific architectural frameworks and pretraining objectives. 

**Architectural Approaches: Graph Networks vs. State-Space Models**
*   **Graph Theoretical Networks:** Functional connectivity is often modeled as a graph comprising nodes (regions) and edges (connections). Graph metrics (like degree centrality and clustering coefficients) map brain network topology and dynamic functional connectivity [9, 10]. However, these approaches often rely on discrete sliding windows and can struggle to capture continuous temporal evolution [11, 12].
*   **State-Space Models & Dynamical Systems:** To overcome these limitations, research is pivoting to **voxel-based state space modeling** and **Hidden Markov Models (HMM)**. State-space models embed the high-dimensional population activity of the entire cortex into a low-dimensional "task-related subspace" that recovers task variables continuously over time [13-16]. Similarly, individualized dynamical systems models mathematically define the rate of change in neural activity by decomposing it into intrinsic regional interactions, local self-decay (autocorrelation), and extrinsic (stimulus-driven) perturbations [17-19]. HMMs provide a generative probabilistic model to capture "metastates"—hierarchically organized sets of brain networks that the brain cycles through dynamically during naturalistic processing [20-22].

**Pretraining Objectives: Contrastive Alignment and Cross-Subject Consistency**
*   **Contrastive Alignment:** Neural models trained on naturalistic stimuli (e.g., AudioSet videos) are increasingly utilizing **contrastive learning frameworks**. For example, in a dual-branch Deep Neural Network (DNN) designed to mimic the brain's separate visual and auditory pathways, the model outputs are trained to match video and audio representations for the *same* stimulus while repelling representations of *different* stimuli [23-25].
*   **Cross-Subject Consistency (ISC/ISFC):** Because raw fMRI contains substantial intrinsic noise, models benefit from objectives that enforce cross-subject consistency. **Inter-subject functional correlation (ISFC)** and **Inter-subject correlation (ISC)** filter out spontaneous, non-stimulus-related physiological noise by correlating time courses *across* different brains exposed to the same naturalistic narrative [26-28]. Training a model to prioritize ISFC representations allows for superior decoding of stimulus conditions and captures robust network states that are locked to the temporal coherence of external events [29-31].

### (c) Closest Current Work, Gaps, and the Roadmap to a Brain Foundation Model

**Closest Current Work**
The closest analogues to a true Brain Foundation Model currently involve mapping state-of-the-art Artificial Intelligence models directly onto brain activity:
1.  **Language Models as Brain Predictors:** Researchers have demonstrated that the activations of deep language algorithms like GPT-2 linearly map onto human fMRI responses to spoken stories [32-34].
2.  **Contrastive Audiovisual DNNs:** Two-branch DNNs pre-trained on audiovisual events exhibit a hierarchical progression that closely matches the human brain, where early model layers correlate with early sensory cortices, and higher layers correlate with multisensory association areas [23, 35].

**The Gap in Current Models**
Despite this progress, current architectures lack true biological plausibility in two fundamental ways:
1.  **Lack of Early Cross-Modal Fusion:** While the human brain features direct projections between early visual and auditory cortices that allow for asymmetrical, low-level cross-modal interaction, standard two-branch DNNs isolate these streams until the very end [23, 35, 36]. Consequently, current AI models fail to capture the brain's early cross-modal interactions [36]. 
2.  **Myopic Timescales:** Current deep language models are predominantly optimized to predict the immediate next word (short-range). Predictive coding theory, however, shows that the human brain continuously generates a hierarchy of predictions spanning multiple timescales—with temporal cortices predicting short-term features and frontoparietal cortices forecasting long-range, high-level semantic contexts [37-39].

**The Roadmap to Achievement**
To bridge the gap between current approaches and a unified Brain Foundation Model, the literature suggests the following roadmap:
1.  **Implement Early Multisensory Integration:** Future architectures must move beyond strictly separated sensory pathways and incorporate "early fusion" components or unified branches that allow low-level sensory information (e.g., acoustic features) to interact with early visual networks, mirroring human neurobiology [36, 40].
2.  **Fine-Tune for Hierarchical, Multi-Timescale Forecasting:** Models should be trained with mixed objective functions. For instance, fine-tuning an AI model to simultaneously predict immediate outputs *and* distant, high-level latent representations drastically improves its ability to map onto the brain's frontoparietal networks [39, 41, 42].
3.  **Leverage Naturalistic Data for Dynamic Reconfiguration:** The brain's large-scale networks dynamically reconfigure in response to continuous real-life stimuli, transitioning between "metastates" [43-45]. A true Brain Foundation Model must use dynamic, time-resolved mathematical frameworks (like generative HMMs or voxel-based state-space models) applied to massive naturalistic datasets to capture the complex, multithreaded nature of continuous human experience [20, 46-48].

---

## References

**[1]** (src:f12ffd8a) using new or refined methods applied to the uniquely rich repository of exceptionally high- quality magnetic resonance imaging (MRI) data provided by the Human Connectome Project (HCP), which benefited from major advances in image acquisition and preprocessing5–8. Architectural measures of relative ...

**[2]** (src:f12ffd8a) in 210V (versus 96.6% using all features). Hence, we anticipate that the areal classifier will generalize to other studies that acquire the following core set of MRI images: high- resolution T1w and T2w; spin echo-based b0 field map; and extensive fMRI data acquired using ‘multiband’ pulse sequences...

**[3]** (src:f12ffd8a) Methods Subjects and acquisition A total of 449 young adult twins and non-twin siblings (ages 22–35) from the Human Connectome Project (HCP) were scanned according to the HCP’s acquisition protocol5–7. The MRI acquisition included collecting T1w and T2w structural images, task-based and resting stat...

**[4]** (src:175566f1) Materials and Methods Subjects and Data Acquisitions Data from40healthy, unrelated adults (age: 22–35, 17males)were obtained from the Q3 data release from the Human Connectome Project (HCP) database. The multimodal MRI data consisted of structural MRI, resting-state functional MRI (rfMRI), and diffu...

**[5]** (src:3fa91849) fMRI data acquisition and preprocessing Functional neuroimaging data were collected using a 7T Siemens MAGNETOMTerraMRI scanner equippedwith a 32-channel Nova head coil, located at Sungkyunkwan University and the Institute for Basic Science, Center for Neuroscience Imaging Research. Blood oxygena-ti...

**[6]** (src:0334945f) Materials and Methods Participants We used the following datasets to cover different age groups (Table 1): The UK Biobank (UKB) study (Miller et al. 2016)—a population-based cohort—recruited >500 000 participants in the United Kingdom, and 10 000 of them had neuroimaging data available. After the qu...

**[7]** (src:67a91294) It is important to acknowledge that conducting research that can be open-ended, data-driven, with multi-level data collection either outside the laboratory or in the laboratory with close-to-real-world conditions, is still very challenging. There are however ways in which the scientific community ca...

**[8]** (src:43b9cbf0) 13.4. Hyperalignment A significant challenge when working with developmental fMRI is to align accurately across participants. Typically, this is accomplished using structural features to align each subject to a pediatric atlas. Multiple groups have worked on ways to align data using functional signa...

**[9]** (src:bffb7be6) Using Brain Connectivity Toolbox [Rubinov et al., 2009] and GRETNA Toolbox [Wang et al., 2015], graph metrics were derived from the weighted adjacency matrices, including degree centrality, clustering coefficient, efficien-cy, betweenness centrality, and an alternative centrality metric, eigenvector...

**[10]** (src:86696ce1) The DTI data used in this study was acquired at a resolution of 2.73 × 2.73 × 2.7 mm and reconstructed as 1.37 × 1.37 × 2.7 mm, which is the resolution of the data in the ADNI database. After converting to NIfTI, FLIRT v6.0 [52,53] in FSL v5.0.8 was used to reslice each DTI dataset to its original, ...

**[11]** (src:901d683f) based on their time series and a 200  200 whole-brain sFC matrix was generated. In this experiment, one resting-state sFC matrix and one natural viewing sFC matrix was separately obtained for each sub- ject during each session. 2.3.2 | dFC The sliding-window strategy was adopted to assess the dFC t...

**[12]** (src:4d15b35c) tioned whether observed changes in dynamical functional connectivity in resting-state fMRI are due to genuine brain transitions or, rather, are mostly explained by sampling variability (14–17). However, these valid concerns are specific to techniques that measure dynamic function connectivity using ...

**[13]** (src:557496fe) Published: 06 May 2021 Citation: Zhang T, Gao JS, Çukur T and Gallant JL (2021) Voxel-Based State Space Modeling Recovers Task-Related Cognitive States in Naturalistic fMRI Experiments. Front. Neurosci. 14:565976. doi: 10.3389/fnins.2020.565976 Voxel-Based State Space Modeling Recovers Task-Related ...

**[14]** (src:557496fe) Here we develop a voxel-based state space modeling method for analyzing fMRI data under naturalistic conditions. Our framework is inspired by methods developed originally to model primate electrophysiology data (Mante et al., 2013). The framework is based on the idea that task variables, such as sti...

**[15]** (src:557496fe) Voxel-Based State Space Modeling To recover task-related state spaces from preprocessed BOLD responses, we adopt targeted dimensionality reduction, a modeling framework originally devised for primate electrophysiology experiments (Mante et al., 2013). This framework assumes that task variables are r...

**[16]** (src:557496fe) The voxel-based state space method consists of two steps. First, a set of task variables that are assumed to capture the underlying structure of the task are operationally defined (see section “Task Variables”). Then a low-dimensional task-related state space that is hypothesized to represent these ...

**[17]** (src:40b3e36e) A dynamical systems model of large-scale cortical activity We applied a large-scale parametric dynamical systems model, devel-oped and validated by Singh et al.9 and Chen et al.19, to fit the time series of BOLD activity measured in human cortex with fMRI. The model defines the rate of change in neu...

**[18]** (src:40b3e36e) q  ffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi α2 + ðbxt  0:5Þ2 q ð2Þ Given that Δt equals to 1 TR in our data, the equation canbe simplified as follows. x̂t + 1 = xt +Wψα xt   D xt + βut ð3Þ The goal of the model is to predict neur...

**[19]** (src:40b3e36e) The dynamical systems model used in this study is a simplified neural mass model that is tailored to simulate large-scale regional activities and their interactions, rather than local neuronal activities within a region. We found that the model parameters effectively reproduced descriptive statistic...

**[20]** (src:d830a9d5) The brain manifests coordinated changes of activity across multiple cortical regions, even in the absence of external tasks5,6. Dynamic patterns of functional brain connectivity at rest appear to reflect task-based phenotypes, including processing speed and fluid intelligence7,8. Dynamic jumps betwe...

**[21]** (src:4d15b35c) temporal nature of resting-state networks of interacting brain areas, characterizing its properties in a large cohort of subjects and re-lating its cross-subject variability to behavior and heritability. Results Dynamic Switching Between Brain Networks Is Not Random.We used resting-state fMRI data f...

**[22]** (src:4d15b35c) N EU RO SC IE N CE SE E CO M M HMM states represent unique brain networks of distinct activity and functional connectivity (where functional connectivity is defined as Pearson correlation over time between brain areas) that repeat at different points in time (19, 20). Other approaches (typically bas...

**[23]** (src:b0437311) The searchlight results (Fig. 3) confirm that the categorical and semantic information wasmainly represented in high-level visual, auditory, and multisensory regions. Because these multisensory areas in the superior temporal cortex are established regions to integrate audiovisual input54, our result...

**[24]** (src:b0437311) Previousfindings show that cross-modal interactions occur at different processing stages and can be observed as early as primary sensory Fig. 4 | Comparisons between fMRI voxel searchlight RDMs and two-branch deep neural network (DNN) pre-trained on audiovisual video stimuli. a Schematic illustratio...

**[25]** (src:b0437311) To assess the similarity between the DNN model and the brain, we selected a pre-trained two-branch model113 trained on audiovideo dataset AudioSet114 with a contrastive learning framework115,116 to match the video and audio representations for the same stimulus and repel the representa-tions for dif...

**[26]** (src:7b279216) To better characterize the dynamic changes in DMN correlation patterns that are locked to the processing of external stimuli, we introduce a novel method termed inter-subject functional correlation (ISFC), in which inter-region correlations are calculated between different brains exposed to the same...

**[27]** (src:7b279216) BOLD signal decomposition and the rationale behind ISFC. We model the measured BOLD signal in each voxel as a sum of three components (Fig. 1a): stimulus-induced signal (S), intrinsic neural signal (I) and non-neuronal (for example, physiological) noise signal (N)21–25. The stimulus-induced signal (...

**[28]** (src:7b279216) In a task setting, the pattern of correlations within each individual, as computed by the FC method, will be influenced by each of the three components (Fig. 1b). In contrast, inter-subject correlation (ISC)26 captures the stimulus-induced correlation across subjects within a given region by correla...

**[29]** (src:7b279216) motion34,35. We empirically demonstrate the presence of these noise sources in FC analyses, and their absence in ISFC analyses, both during rest and the intact story, in Supplementary Fig. 1. Inter-subject alignment of the DMN. We next compared the patterns of FC and ISFC in the DMN across four dist...

**[30]** (src:7b279216) Across-subject classification of stimulus type. Next, we trained a classifier to quantify the improvement in discriminating between the four experimental conditions by using ISFC over FC. Clas-sification was performed separately using ISFC and using FC (see Supplementary Note 2). Classification accu...

**[31]** (src:7b279216) The ISFC patterns were specific for different moments in time and also highly reproducible across two independent groups of subjects. Interestingly, the reproducibility of ISFC patterns was observed both when the mean ISFC across all nodes was high and when it was low: that is, reproducibility was h...

**[32]** (src:a24af881) nature human behaviour Article https://doi.org/10.1038/s41562-022-01516-2 Evidence of a predictive coding hierarchy in the human brain listening to speech Charlotte Caucheteux    1,2 , Alexandre Gramfort1,2 & Jean-Rémi King    1,3 Considerable progress has recently been made in natural language proc...

**[33]** (src:a24af881) Results Deep language models map onto brain activity First, we quantified the similarity between deep language models and the brain, when these two systems are inputted with the same stories. For this, we used the Narratives dataset39 and analysed the fMRI of 304 individuals listening to short stori...

**[34]** (src:a24af881) In line with previous studies5,7,40,41, the activations of GPT-2 accu-rately map onto a distributed and bilateral set of brain areas. Brain scores peaked in the auditory cortex and in the anterior temporal and superior temporal areas (Fig. 2a, Supplementary Fig. 1, Supplementary Note 1 and Supplemen...

**[35]** (src:b0437311) Supplementary Fig. 1). We next applied searchlight analysis to identify the brain voxels that showed a significant correlation with model layer RDMs (cluster-corrected 1000 one-side sign permutation test, cluster-definition threshold p < 0.001, cluster threshold p < 0.01; Fig. 4c). The DNN model sho...

**[36]** (src:b0437311) Currently, DNNmodels serve as the best models of the human visual or auditory system140–144. However, their similarity with human brain responses in multisensory perception is less explored145. Generally, the match between DNN models and the brain depends on multiple factors, such as the training da...

**[37]** (src:a24af881) Predictive coding theory25–27 offers a potential explanation to these shortcomings; while deep language models are mostly tuned to predict the very next word, this framework suggests that the human brain makes predictions over multiple timescales and levels of repre-sentations across the cortical hi...

**[38]** (src:a24af881) of the next token. Consequently, the nature of the predicted representa-tions and their temporal scope are largely unknown. In this study, we address these issues by analysing the brain signals of 304 individuals listening to short stories while their brain activity is recorded with fMRI39. After co...

**[39]** (src:a24af881) Overall, these results reveal multiple levels of predictions in the brain in which the superior temporal cortex predominantly pre-dicts short-term, shallow and syntactic representations whereas the inferior-frontal and parietal areas predominantly predict long-term, contextual, high-level and semant...

**[40]** (src:b0437311) https://doi.org/10.1038/s42003-024-07434-5 Neural processing of naturalistic audiovisual events in space and time Check for updates Yu Hu 1,2 & Yalda Mohsenzadeh 1,2,3 Our brain seamlessly integrates distinct sensory information to form a coherent percept. However, when real-world audiovisual events...

**[41]** (src:a24af881) Fine-tuning GPT-2 with a long-range and high-level objective Does fine-tuning GPT-2 to predict long-term, high-level and more contextualized representations increase its similarity with the brain? To test this question, we fine-tuned GPT-2 using a mixture of language modelling loss and high-level an...

**[42]** (src:a24af881) ing words). The high-level objective predicts layer k of word at distance d from the current word and it is given by: ℒk,d high−level = CPC[hhigh−level ∘ f(xt),Nk(xt+d)] where: Nk is a separate and fixed network. Here, we use the pretrained version of GPT-2 provided by Huggingface, taken at layer k....

**[43]** (src:4d15b35c) Edited by Marcus E. Raichle, Washington University in St. Louis, St. Louis, MO, and approved September 28, 2017 (received for review April 3, 2017) The brain recruits neuronal populations in a temporally coordinated manner in task and at rest. However, the extent to which large-scale networks exhibi...

**[44]** (src:4d15b35c) network dynamics, we used a method designed to discover net-works that repeat over time (referred to as brain states). Impor-tantly, we define networks as probability distributions representing graphs, with not only distinct patterns of activation but, crucially, also distinct patterns of functional...

**[45]** (src:7b279216) The ISFC approach uncovered two novel functional characteristics of DMN correlation patterns. First, DMN correlation patterns were less reliable when the story was scrambled at the paragraph level, and even less so when the story was scrambled at the word level. This suggests that DMN correlations w...

**[46]** (src:557496fe) DISCUSSION Complex naturalistic behaviors evoke complex, high-dimensional activity across the cortex that are challenging to analyze and interpret (Hasson et al., 2004; Mathiak and Weber, 2006; Spiers and Maguire, 2007; Mathiak et al., 2011; Nishimoto et al., 2011; Huth et al., 2012, 2016; Çukur et ...

**[47]** (src:557496fe) In sum, our results suggest that while overall cortical activity is high-dimensional, the representation of particular task variables is reflected in a low-dimensional subspace of brain activity. Analyzing the cortical activity vector of the brain complements analyses on single voxel activities by r...

**[48]** (src:d830a9d5) Movie viewing allows the study of transitory brain states linked to an immersive sensory stimulation3,38. This experimental paradigm provides a unique opportunity to capture complex brain dynamics that may not otherwise be detectable through the lens of traditional task designs18. Due to the complex...


**Sources used:** 16 documents
- f12ffd8a-fc8f-40cc-bb99-20a8148fda8a
- 175566f1-e749-44a0-b560-748f51698dd9
- 3fa91849-c249-4c08-9d85-9648a1cda227
- 0334945f-57d7-427f-9ff6-12c33826de6a
- 67a91294-ea55-4ee2-b94f-1676af02528a
- 43b9cbf0-9356-4700-9922-64658c6fff03
- bffb7be6-4fe1-474a-a013-e95e211e712e
- 86696ce1-e360-43d5-a4b8-1740800ce1a0
- 901d683f-e842-4bf4-9441-93b858d20e07
- 4d15b35c-f629-413a-a7ac-aa7b8e81c5cf
