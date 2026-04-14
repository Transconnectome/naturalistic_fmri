#!/usr/bin/env python3
"""
Extended PubMed search for naturalistic fMRI papers 2021-2026 MISSED by initial 8 queries.
Targets underrepresented topics: music, VR, hyperscanning, encoding models, clinical populations,
cross-species, concurrent EEG/MEG-fMRI, predictive coding, event segmentation, etc.
"""
import requests
import time
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import Counter

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path("/home/juke/naturalistic_fmri_pdfs")
EXISTING_PMIDS_FILE = OUT_DIR / "existing_pmids.txt"
OUT_FILE = OUT_DIR / "papers_missed_pubmed.json"

# ============================================================================
# JOURNAL FILTER — Expanded to include mid-tier naturalistic-relevant journals
# ============================================================================
TOP_JOURNALS = [
    # Already in original corpus
    "Nature neuroscience",
    "Neuron",
    "Nature communications",
    "NeuroImage",
    "Cerebral cortex",
    "eLife",
    "Proceedings of the National Academy of Sciences",
    "The Journal of neuroscience",
    "Journal of neuroscience",
    "Current biology",
    "Human brain mapping",
    "Cortex",
    "Imaging neuroscience",
    "Trends in cognitive sciences",
    "Nature human behaviour",
    "Science advances",
    "Communications biology",
    "PLoS biology",
    "Brain",
    "Cell reports",
    "Cognitive neurodynamics",
    "Network neuroscience",
    "Brain sciences",
    "NeuroImage. Clinical",
    "Brain imaging and behavior",
    "Brain connectivity",
    "European journal of neuroscience",
    "Brain and cognition",
    "Brain structure & function",
    # Expanded — mid-tier naturalistic-relevant journals
    "Neuropsychologia",
    "Frontiers in human neuroscience",
    "Frontiers in neuroscience",
    "Frontiers in neurology",
    "Frontiers in psychology",
    "Frontiers in psychiatry",
    "Frontiers in systems neuroscience",
    "Brain research",
    "Trends in neurosciences",
    "Nature methods",
    "Nature reviews neuroscience",
    "Nature reviews neurology",
    "Annual review of neuroscience",
    "Annual review of psychology",
    "Biological psychiatry",
    "Molecular psychiatry",
    "Translational psychiatry",
    "JAMA psychiatry",
    "Nature mental health",
    "Science",
    "Nature",
    "PLoS computational biology",
    "PLoS one",
    "Social cognitive and affective neuroscience",
    "Developmental cognitive neuroscience",
    "Cognitive neuroscience",
    "Cognition",
    "Psychological science",
    "Neuropsychology review",
    "Cognitive, affective & behavioral neuroscience",
    "Journal of cognitive neuroscience",
    "Scientific reports",
    "iScience",
    "Patterns",
    "Neuron behavior research methods",
    "Behavior research methods",
    "Neuroinformatics",
    "GigaScience",
    "Scientific data",
    "Journal of neural engineering",
    "Brain topography",
    "NeuroImage: Reports",
    "Neuroscience",
    "Developmental science",
    "Child development",
    "Aging",
    "Neurobiology of aging",
    "Autism research",
    "Schizophrenia research",
    "Journal of psychiatric research",
    "Depression and anxiety",
    "Biological psychology",
    "Psychophysiology",
    "Emotion",
]

# ============================================================================
# EXTENDED QUERIES — Target gaps in the original corpus
# ============================================================================
QUERIES = [
    # ========== Music listening + fMRI (very underrepresented, n=6 in corpus)
    ("music_listening", '("music listening"[Title/Abstract] OR "musical listening"[Title/Abstract] OR "music perception"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "functional MRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("music_naturalistic", '("music"[Title/Abstract] AND ("naturalistic"[Title/Abstract] OR "continuous"[Title/Abstract])) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("music_brain", '("naturalistic music"[Title/Abstract]) AND ("brain"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Virtual Reality + fMRI (very underrepresented, n=2-3 in corpus)
    ("vr_fmri", '("virtual reality"[Title/Abstract] OR "VR"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("immersive_fmri", '("immersive"[Title/Abstract] OR "virtual environment"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain imaging"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Hyperscanning / dyadic (very underrepresented, n=4 in corpus)
    ("hyperscanning_fmri", '("hyperscanning"[Title/Abstract] OR "dyadic"[Title/Abstract] OR "two-person"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("social_interaction_fmri", '("real-time interaction"[Title/Abstract] OR "live interaction"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("brain_to_brain", '("brain-to-brain"[Title/Abstract] OR "brain synchronization"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Game playing / video game + fMRI (underrepresented)
    ("video_game_fmri", '("video game"[Title/Abstract] OR "gaming"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("game_playing_fmri", '("game playing"[Title/Abstract] OR "game-playing"[Title/Abstract] OR "interactive game"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Shared Response Model / Hyperalignment / Encoding models
    ("srm_fmri", '("shared response model"[Title/Abstract] OR "SRM"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("hyperalignment_fmri", '("hyperalignment"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("encoding_model_fmri", '("encoding model"[Title/Abstract] OR "voxel-wise encoding"[Title/Abstract] OR "voxelwise encoding"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("brain_decoding_naturalistic", '("brain decoding"[Title/Abstract] OR "neural decoding"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "story"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Theory of Mind / Mentalizing / Social cognition with naturalistic (underrepresented)
    ("theory_of_mind_fmri", '("theory of mind"[Title/Abstract] OR "mentalizing"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "narrative"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("empathy_fmri_naturalistic", '("empathy"[Title/Abstract] OR "empathic"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "film"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("social_cognition_movie", '("social cognition"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "film"[Title/Abstract] OR "video"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Emotion regulation + naturalistic (underrepresented)
    ("emotion_regulation_movie", '("emotion regulation"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "film"[Title/Abstract] OR "video"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("affective_naturalistic", '("affective"[Title/Abstract] OR "affect"[Title/Abstract]) AND "naturalistic"[Title/Abstract] AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Event segmentation / Event boundaries
    ("event_segmentation", '("event segmentation"[Title/Abstract] OR "event boundary"[Title/Abstract] OR "event boundaries"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("event_boundary", '("event boundary"[Title/Abstract]) AND ("brain"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Memory / Encoding during naturalistic (underrepresented)
    ("naturalistic_memory", '("naturalistic"[Title/Abstract] OR "movie"[Title/Abstract]) AND ("episodic memory"[Title/Abstract] OR "memory encoding"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("naturalistic_recall", '("naturalistic recall"[Title/Abstract] OR "free recall"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Populations: Infants / Children naturalistic (very underrepresented, n=5 infants)
    ("infant_fmri_movie", '("infant"[Title/Abstract] OR "infants"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "video"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("developmental_naturalistic", '("developmental"[Title/Abstract] OR "pediatric"[Title/Abstract] OR "children"[Title/Abstract]) AND ("movie watching"[Title/Abstract] OR "naturalistic viewing"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("adolescent_naturalistic", '("adolescent"[Title/Abstract] OR "adolescence"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "film"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Populations: Clinical (underrepresented)
    ("depression_naturalistic", '("depression"[Title/Abstract] OR "major depressive"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "film"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("anxiety_naturalistic", '("anxiety"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("autism_naturalistic", '("autism"[Title/Abstract] OR "ASD"[Title/Abstract] OR "autistic"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "film"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("schizophrenia_naturalistic", '("schizophrenia"[Title/Abstract] OR "psychosis"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("adhd_naturalistic", '("ADHD"[Title/Abstract] OR "attention deficit"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Methods: Concurrent EEG-fMRI / MEG-fMRI (underrepresented, n=2-5)
    ("eeg_fmri_naturalistic", '("EEG-fMRI"[Title/Abstract] OR "concurrent EEG"[Title/Abstract] OR "simultaneous EEG-fMRI"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "movie"[Title/Abstract] OR "narrative"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("meg_naturalistic", '("MEG"[Title/Abstract] OR "magnetoencephalography"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("fnirs_naturalistic", '("fNIRS"[Title/Abstract] OR "near-infrared"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== 7T / ultra-high field naturalistic
    ("7T_naturalistic", '("7T"[Title/Abstract] OR "7 Tesla"[Title/Abstract] OR "ultra-high field"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Theory-driven: Predictive coding, active inference, free energy
    ("predictive_coding_naturalistic", '("predictive coding"[Title/Abstract] OR "predictive processing"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("active_inference_naturalistic", '("active inference"[Title/Abstract] OR "free energy"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "movie"[Title/Abstract] OR "narrative"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Specific famous stimuli (Sherlock, Partly Cloudy, Forrest Gump, Inscapes)
    ("sherlock_fmri", '("Sherlock"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("partly_cloudy", '("Partly Cloudy"[Title/Abstract] OR "Pixar"[Title/Abstract]) AND ("brain"[Title/Abstract] OR "fMRI"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("forrest_gump", '("Forrest Gump"[Title/Abstract] OR "studyforrest"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("inscapes", '("Inscapes"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Cross-species naturalistic (underrepresented)
    ("macaque_movie", '("macaque"[Title/Abstract] OR "rhesus"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "video"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("marmoset_naturalistic", '("marmoset"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "video"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("nonhuman_primate_naturalistic", '("non-human primate"[Title/Abstract] OR "nonhuman primate"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Large language models / Neural networks + fMRI
    ("llm_brain_fmri", '("large language model"[Title/Abstract] OR "LLM"[Title/Abstract] OR "GPT"[Title/Abstract] OR "BERT"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("deep_learning_fmri_naturalistic", '("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("cnn_brain_vision", '("convolutional neural network"[Title/Abstract] OR "CNN"[Title/Abstract]) AND ("video"[Title/Abstract] OR "movie"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Semantic / Language processing during naturalistic
    ("semantic_naturalistic", '("semantic"[Title/Abstract] OR "semantic map"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "story"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("linguistic_naturalistic", '("linguistic"[Title/Abstract] OR "language processing"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "story"[Title/Abstract] OR "podcast"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Real-world / Everyday / Ecological validity
    ("real_world_fmri", '("real-world"[Title/Abstract] OR "real world"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain imaging"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("ecological_fmri", '("ecological validity"[Title/Abstract] OR "ecological"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "movie"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("everyday_fmri", '("everyday"[Title/Abstract] OR "daily life"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "ambulatory"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Dynamic connectivity / brain state naturalistic
    ("dynamic_fc_movie", '("dynamic functional connectivity"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("brain_state_movie", '("brain state"[Title/Abstract] OR "brain states"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Hippocampus + naturalistic (memory circuits)
    ("hippocampus_naturalistic", '("hippocampus"[Title/Abstract] OR "hippocampal"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "movie"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Default mode network naturalistic
    ("dmn_naturalistic", '("default mode network"[Title/Abstract] OR "default mode"[Title/Abstract] OR "DMN"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Inter-subject functional correlation (ISFC), synchronization
    ("isfc_fmri", '("ISFC"[Title/Abstract] OR "inter-subject functional correlation"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("neural_sync_naturalistic", '("neural synchronization"[Title/Abstract] OR "neural synchrony"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Attention + naturalistic (specifically attention-focused)
    ("attention_movie", '("selective attention"[Title/Abstract] OR "sustained attention"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
    ("mind_wandering_fmri", '("mind wandering"[Title/Abstract] OR "mind-wandering"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Individual differences in naturalistic
    ("individual_differences_naturalistic", '("individual differences"[Title/Abstract] OR "individual variability"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Functional parcellation from movie
    ("parcellation_movie", '("parcellation"[Title/Abstract] OR "parcellate"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Reinforcement learning in naturalistic
    ("rl_naturalistic", '("reinforcement learning"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Cinema / visual features + neural
    ("cinematography_fmri", '("cinematography"[Title/Abstract] OR "film cuts"[Title/Abstract] OR "cinematic"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract] OR "neural"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Prediction / Expectation in naturalistic
    ("prediction_naturalistic", '("neural prediction"[Title/Abstract] OR "brain prediction"[Title/Abstract] OR "expectation"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Alzheimer / neurodegeneration + movie watching
    ("alzheimer_naturalistic", '("Alzheimer"[Title/Abstract] OR "dementia"[Title/Abstract] OR "MCI"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Stroke / lesion + naturalistic
    ("stroke_naturalistic", '("stroke"[Title/Abstract] OR "lesion"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Traumatic brain injury
    ("tbi_naturalistic", '("traumatic brain injury"[Title/Abstract] OR "TBI"[Title/Abstract] OR "concussion"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "fMRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== PTSD + naturalistic
    ("ptsd_naturalistic", '("PTSD"[Title/Abstract] OR "post-traumatic"[Title/Abstract] OR "trauma"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "film"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Consciousness / anesthesia + naturalistic
    ("consciousness_naturalistic", '("consciousness"[Title/Abstract] OR "anesthesia"[Title/Abstract] OR "vegetative state"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Sleep + naturalistic
    ("sleep_naturalistic", '("sleep"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "narrative"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Biomarker / prediction from movie
    ("biomarker_movie", '("biomarker"[Title/Abstract] OR "prediction"[Title/Abstract]) AND ("movie watching"[Title/Abstract] OR "naturalistic paradigm"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Individual / subject-specific fingerprinting naturalistic
    ("fingerprinting_naturalistic", '("fingerprint"[Title/Abstract] OR "fingerprinting"[Title/Abstract] OR "identification"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Review / Meta-analysis on naturalistic fMRI
    ("naturalistic_review", '("naturalistic"[Title/Abstract] OR "movie watching"[Title/Abstract]) AND ("review"[Title/Abstract] OR "meta-analysis"[Title/Abstract] OR "perspective"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Open datasets / Public databases naturalistic
    ("open_dataset_naturalistic", '("open dataset"[Title/Abstract] OR "public dataset"[Title/Abstract] OR "HBN"[Title/Abstract] OR "Healthy Brain Network"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Emotional film / affect-inducing movie
    ("emotional_film_fmri", '("emotional film"[Title/Abstract] OR "affective film"[Title/Abstract] OR "emotional video"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Dementia, aging, cognitive decline
    ("aging_movie", '("older adult"[Title/Abstract] OR "aging brain"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "narrative"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Multimodal / Audiovisual integration
    ("audiovisual_fmri", '("audiovisual"[Title/Abstract] OR "multimodal"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Pain + movie / naturalistic
    ("pain_naturalistic", '("pain"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "film"[Title/Abstract] OR "naturalistic"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Immersive / 360 video
    ("360_video_fmri", '("360 video"[Title/Abstract] OR "360-degree"[Title/Abstract] OR "360 degree"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Face perception in naturalistic
    ("face_naturalistic", '("face perception"[Title/Abstract] OR "face processing"[Title/Abstract]) AND ("movie"[Title/Abstract] OR "naturalistic"[Title/Abstract] OR "film"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Auditory cortex naturalistic
    ("auditory_naturalistic", '("auditory cortex"[Title/Abstract] OR "auditory processing"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "speech"[Title/Abstract] OR "podcast"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),

    # ========== Visual cortex + naturalistic video
    ("visual_cortex_movie", '("visual cortex"[Title/Abstract] OR "V1"[Title/Abstract]) AND ("naturalistic"[Title/Abstract] OR "movie"[Title/Abstract] OR "video"[Title/Abstract]) AND "fMRI"[Title/Abstract] AND ("2021"[PDAT] : "2026"[PDAT])'),
]

# ============================================================================

def load_existing_pmids():
    """Load PMIDs from existing_pmids.txt."""
    with open(EXISTING_PMIDS_FILE) as f:
        return set(line.strip() for line in f if line.strip())

def esearch(query, retmax=300):
    url = f"{BASE}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "sort": "relevance",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("esearchresult", {}).get("idlist", [])

def efetch(pmids):
    if not pmids:
        return b""
    url = f"{BASE}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.content

def parse_record(art):
    info = {
        "pmid": None, "title": None, "journal": None, "year": None,
        "authors": [], "doi": None, "pmc_id": None, "abstract": None,
    }
    pmid_el = art.find(".//PMID")
    if pmid_el is not None:
        info["pmid"] = pmid_el.text
    title_el = art.find(".//ArticleTitle")
    if title_el is not None:
        info["title"] = "".join(title_el.itertext()).strip()
    journal_el = art.find(".//Journal/Title")
    if journal_el is not None:
        info["journal"] = journal_el.text
    year_el = art.find(".//PubDate/Year")
    if year_el is None:
        year_el = art.find(".//PubDate/MedlineDate")
    if year_el is not None and year_el.text:
        m = re.search(r"\d{4}", year_el.text)
        if m:
            info["year"] = m.group(0)
    for au in art.findall(".//Author")[:3]:
        last = au.find("LastName")
        first = au.find("Initials")
        if last is not None:
            name = last.text
            if first is not None and first.text:
                name = f"{first.text} {name}"
            info["authors"].append(name)
    for id_el in art.findall(".//ArticleId"):
        idtype = id_el.get("IdType")
        if idtype == "doi":
            info["doi"] = id_el.text
        elif idtype == "pmc":
            info["pmc_id"] = id_el.text
    abstract_parts = []
    for a in art.findall(".//AbstractText"):
        label = a.get("Label")
        text = "".join(a.itertext()).strip()
        if label:
            abstract_parts.append(f"{label}: {text}")
        else:
            abstract_parts.append(text)
    if abstract_parts:
        info["abstract"] = " ".join(abstract_parts)
    return info

def journal_matches(journal_name):
    if not journal_name:
        return False
    j = journal_name.lower()
    for t in TOP_JOURNALS:
        if t.lower() in j or j in t.lower():
            return True
    return False

def is_relevant(info):
    """Relevance filter: must clearly involve a naturalistic paradigm + fMRI.

    Strict version: requires (a) explicit fMRI / BOLD / MRI mention AND
    (b) clear naturalistic paradigm indicator (not just 'real-world' as adjective).
    """
    if not info.get("title"):
        return False
    # Year filter
    y = info.get("year")
    if not y or not y.isdigit():
        return False
    yi = int(y)
    if yi < 2021 or yi > 2026:
        return False

    text = ((info.get("title") or "") + " " + (info.get("abstract") or "")).lower()

    # STRONG naturalistic paradigm indicators (at least one required — these imply
    # an actual continuous / movie / narrative / music / VR / game paradigm)
    strong_nat = [
        "naturalistic", "movie", "movie-watching", "movie watching", "movie-viewing",
        "narrative", "storytelling", "story listening", "story-listening",
        "story comprehension", "spoken narrative", "spoken story", "stories",
        "audiobook", "podcast",
        "inter-subject correlation", "intersubject correlation",
        "inter-subject synchroniz", "intersubject synchroniz",
        "inter-subject functional", "intersubject functional",
        "isc analysis", "isfc",
        "film viewing", "film-viewing", "film clip", "film stimuli",
        "movie clip", "movie stimuli", "movie paradigm", "movie-driven",
        "cinematic", "cinematography",
        "naturalistic stimul", "naturalistic paradigm", "naturalistic viewing",
        "naturalistic listening", "naturalistic movie", "naturalistic film",
        "naturalistic music", "naturalistic task", "naturalistic setting",
        "naturalistic speech", "naturalistic narrative", "naturalistic sound",
        "audiovisual movie", "audiovisual stimul", "video clip", "video stimuli",
        "continuous speech", "continuous stimul", "continuous narrative",
        "continuous listening", "continuous viewing",
        "virtual reality", "vr paradigm", "vr environment", "immersive virtual",
        "immersive video", "360-degree video", "360 degree video",
        "hyperscanning", "dyadic", "two-person", "brain-to-brain",
        "music listening", "naturalistic music",
        "video game", "gaming", "gameplay", "interactive game",
        "sherlock", "partly cloudy", "forrest gump", "studyforrest",
        "inscapes", "despicable me", "pixar", "the present",
        "healthy brain network", "cam-can", "cam can",
        "speech comprehension", "speech perception",
        "event segmentation", "event boundary", "event boundaries",
        "encoding model", "voxel-wise encoding", "voxelwise encoding",
        "hyperalignment", "shared response model",
        "episode 1", "episode of",
    ]
    has_strong_nat = any(k in text for k in strong_nat)
    if not has_strong_nat:
        return False

    # STRICT fMRI-specific keywords (requires actual MRI/fMRI/BOLD signal)
    fmri_keywords = [
        "fmri", "f-mri", "f mri",
        "functional mri", "functional magnetic resonance",
        "bold signal", "bold response", "bold activity", "bold activation",
        "bold-fmri", "bold fmri", "bold imaging",
        "blood-oxygen-level", "blood oxygen level",
        "3t mri", "7t mri", "3 tesla", "7 tesla", "ultra-high field",
        "mri scan", "mri paradigm", "mr imaging", "mri data",
        "mri experiment", "mri study", "hcp ", "human connectome",
        "healthy brain network", "midnight scan", "studyforrest",
        "narratives dataset", "multimodal mri", "cam-can", "cam can",
        "ukb ", "uk biobank", "abcd ",
    ]
    has_fmri = any(k in text for k in fmri_keywords)
    if not has_fmri:
        return False

    return True

def build_pdf_url(info):
    if info.get("pmc_id"):
        pmc = info["pmc_id"].replace("PMC", "")
        return f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc}/pdf/"
    return None

def main():
    existing_pmids = load_existing_pmids()
    print(f"Loaded {len(existing_pmids)} existing PMIDs to skip")

    # Check for cached raw results
    cache_file = OUT_DIR / "raw_metadata_cache.json"
    if cache_file.exists():
        print(f"\nLoading cached raw metadata from {cache_file}")
        with open(cache_file) as f:
            cache = json.load(f)
        pmid_to_record = {p["pmid"]: p for p in cache["records"] if p.get("pmid")}
        new_pmids_by_query = {k: set(v) for k, v in cache["query_pmids"].items()}
        query_counts = cache["query_counts"]
    else:
        # Phase 1: Collect all new PMIDs via esearch (dedup against existing early)
        print(f"\n{'='*60}")
        print(f"Phase 1: Running {len(QUERIES)} queries")
        print(f"{'='*60}")
        new_pmids_by_query = {}  # tag -> set of pmids
        new_pmids_all = set()
        query_counts = []

        for tag, query in QUERIES:
            try:
                pmids = esearch(query, retmax=300)
                pmid_set = set(pmids) - existing_pmids
                new_pmids_by_query[tag] = pmid_set
                new_pmids_all.update(pmid_set)
                query_counts.append((tag, len(pmids), len(pmid_set)))
                print(f"  [{tag}] {len(pmids):3d} total / {len(pmid_set):3d} new")
            except Exception as e:
                print(f"  [{tag}] ERROR: {e}")
                new_pmids_by_query[tag] = set()
                query_counts.append((tag, 0, 0))
            time.sleep(0.4)

        print(f"\nTotal unique NEW PMIDs (post-dedup): {len(new_pmids_all)}")

        # Phase 2: efetch metadata in batches of 100
        print(f"\n{'='*60}")
        print(f"Phase 2: Fetching metadata for {len(new_pmids_all)} new PMIDs")
        print(f"{'='*60}")
        pmid_list = list(new_pmids_all)
        BATCH = 100
        pmid_to_record = {}
        for i in range(0, len(pmid_list), BATCH):
            batch = pmid_list[i:i+BATCH]
            print(f"  batch {i//BATCH + 1}/{(len(pmid_list)+BATCH-1)//BATCH} ({len(batch)} records)...")
            try:
                xml = efetch(batch)
                root = ET.fromstring(xml)
                for art in root.findall(".//PubmedArticle"):
                    info = parse_record(art)
                    if info.get("pmid"):
                        pmid_to_record[info["pmid"]] = info
            except Exception as e:
                print(f"    ERROR: {e}")
            time.sleep(0.4)

        print(f"Parsed {len(pmid_to_record)} records")

        # Save raw cache
        with open(cache_file, "w") as f:
            json.dump({
                "records": list(pmid_to_record.values()),
                "query_pmids": {k: list(v) for k, v in new_pmids_by_query.items()},
                "query_counts": query_counts,
            }, f)
        print(f"Cached raw metadata to {cache_file}")

    # Phase 3: Apply relevance filter + journal filter
    print(f"\n{'='*60}")
    print(f"Phase 3: Filtering")
    print(f"{'='*60}")

    # Build reverse lookup: pmid -> first matching query tag
    pmid_to_tag = {}
    for tag, pmids in new_pmids_by_query.items():
        for p in pmids:
            if p not in pmid_to_tag:
                pmid_to_tag[p] = tag

    rel_count = 0
    jrn_count = 0
    final = []
    for pmid, rec in pmid_to_record.items():
        if not is_relevant(rec):
            continue
        rel_count += 1
        if not journal_matches(rec.get("journal")):
            continue
        jrn_count += 1
        rec["matched_query"] = pmid_to_tag.get(pmid, "unknown")
        rec["has_pmc"] = bool(rec.get("pmc_id"))
        rec["pdf_url"] = build_pdf_url(rec)
        final.append(rec)

    print(f"  Passed relevance filter:    {rel_count}/{len(pmid_to_record)}")
    print(f"  Passed journal filter also: {jrn_count}/{len(pmid_to_record)}")

    # Sort: PMC-available first, then by year desc
    final.sort(key=lambda r: (not r.get("has_pmc", False), -int(r.get("year") or 0)))

    # Save
    with open(OUT_FILE, "w") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved {len(final)} new papers to {OUT_FILE}")

    # Stats
    pmc_count = sum(1 for r in final if r.get("has_pmc"))
    print(f"  PMC-available (direct PDF): {pmc_count}")
    print(f"  Not in PMC: {len(final) - pmc_count}")

    years = Counter(r.get("year") for r in final)
    print(f"\nYears: {dict(sorted(years.items()))}")

    journals = Counter(r.get("journal", "Unknown") for r in final)
    print(f"\nTop 20 journals:")
    for j, c in journals.most_common(20):
        print(f"  {c:3d}  {j}")

    tags = Counter(r.get("matched_query") for r in final)
    print(f"\nTop matched queries:")
    for t, c in tags.most_common(25):
        print(f"  {c:3d}  {t}")

    # Save query-level stats
    with open(OUT_DIR / "missed_query_stats.json", "w") as f:
        json.dump({
            "query_raw_counts": {tag: total for tag, total, _ in query_counts},
            "query_new_counts": {tag: new_n for tag, _, new_n in query_counts},
            "total_unique_new_pmids": len(new_pmids_all),
            "final_filtered_papers": len(final),
        }, f, indent=2)

if __name__ == "__main__":
    main()
