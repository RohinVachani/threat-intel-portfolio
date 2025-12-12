# UPI Fraud Intelligence: Behavioural Clustering & Scam Pattern Analysis
*A hands-on CTI + ML investigation. Real UPI handles from public scam complaints*

## Why I did this*
I set out to show that I can take messy OSINT, turn it into meaningful features, and use ML to uncover real behavioural patterns.

### What this demonstrates:
- I’m comfortable working with unstructured, imperfect data.
- I design features that actually matter in a fraud context.
- I use ML to reveal structure and signal, not as a blunt tool.
- I approach problems like an analyst, not just a coder.

This is my proof-of-work.

---

## Project summary 
I manually collected UPI IDs from public sources — consumer-complaint sites, Reddit, X, YouTube comments, and LinkedIn. These were handles people shared while discussing scams. I want to be explicit: I did not verify any allegations or treat these as confirmed scam IDs. The goal was strictly structural and behavioural analysis of the UPI strings themselves.

I engineered a set of string-level and metadata-derived features and applied unsupervised clustering to identify behaviourally coherent groups of handles.

---

## What each script actually does

### src/load_data.py
reads raw CSVs  
normalizes strings  
splits prefix and PSP (prefix@psp)  
lowercases everything  
tags obvious anomalies: missing prefix, masked prefixes, unknown PSPs, malformed entries  

### src/process_features.py
Converts a UPI prefix into features that map to behaviour:  
prefix (raw)  
psp (suffix)  
prefix_length — short vs long tells you intent/automation  
digit_ratio — high → phone-number style; low → alphabetic impersonation  
shannon_entropy — randomness vs dictionary-like text  
has_masking — * present (platform redaction or deliberate)  
looks_like_mobile — matches [6-9]\d{9}.  

### src/cluster_analysis.py
standardize numeric features (mean=0, std=1)  
run KMeans (k=5)  
PCA → 2D for visual check  
persist cluster labels  

### display_final_data.py
merge cluster labels with metadata (source, scam type, amount, state)  
output upi_final.csv for analysts  

---

## Analyzing The Clusters
I wrote a full write-up (cluster_analysis.md) with:  
cluster-by-cluster behavioural roles  
hypotheses about fraud intent  
PSP patterns (which PSPs appear repeatedly in suspicious clusters)  
confidence levels and where the signals are weak  

---

## Practical Skills
Manual OSINT acquisition: extracted dozens of real UPI handles from noisy, unstructured posts across multiple platforms.  
Cleaning under uncertainty: dealt with redactions, OCR artefacts, and truncated IDs using a combination of scripted checks and analyst judgement.  
Behaviour-driven feature engineering: built features that reflect operational behaviour — entropy, digit-ratio, mobile-pattern match, masking indicators, PSP taxonomy, and structural signatures.  
ML for discovery, not labelling: used KMeans to surface infrastructure patterns and behavioural clusters, not to force hard classifications.  
Turning structure into intent: interpreted the clusters in terms of likely workflows and operational habits — the core of CTI analysis.  
End-to-end execution: designed and iterated the entire pipeline, from raw OSINT collection to an analyst-ready, documented CSV.  

---

## Limitations (transparent and realistic):
Small dataset: results are indicative, not production-grade.  
Heavy masking/redaction: some rows have reduced reliability due to partial or obscured identifiers.  
KMeans is structural, not semantic: the model captures pattern similarity, not intent or meaning.  
Incomplete metadata: several entries lack contextual fields, which constrains richer analysis.  
Infrastructure-level inference only: this surfaces structural patterns, not fraud attribution or confirmation.  

---

## Closing note
This work was an exercise in analytical discipline: start with imperfect OSINT, extract reliable signals, and use unsupervised methods to expose underlying structure. The value isn’t in the algorithms, but in the judgement applied throughout the pipeline. Every component — from collection to clustering to interpretation — was built and reasoned through end-to-end.
