# OSINT & Threat Intelligence Portfolio

This repository contains four independent analytical units.  
Two are **casefiles** built through passive OSINT and behavioural reconstruction.  
Two are **technical pipelines** focused on automation, signal engineering, and unsupervised modelling.

Across all projects, the objective remains the same:  
**derive operational understanding from incomplete, inconsistent, and openly available signals.**

---

# 1. Casefile — Passive Investigation of a Long-Running Scam Lure

A passive OSINT examination of a website repeatedly referenced in public complaints.  
The focus is not attribution but **structure**: what the visible footprint suggests about the operational model behind it.

Key observations include:

- simple, inexpensive, long-lived infrastructure  
- highly variable extraction behaviour across complaints  
- rotating payment channels, inconsistent personas, and improvised documentation  
- a stable lure paired with **distributed extraction operators**, not a centralized team  

The casefile outlines the workflow, recurring shapes, and intelligence gaps that define the limits of passive assessment.

---

# 2. Casefile — Scam Ecosystem Structure & Behaviour

A reasoning-driven analysis of fraud ecosystems: how they recruit, scale, adapt, and eventually collapse.  
This document treats scams as systems shaped by incentives and repetition, rather than isolated incidents.

Coverage includes:

- recruitment pathways and psychological framing  
- group hierarchies and compartmentalization  
- emotional leverage and compliance engineering  
- mule networks and cashout architecture  
- procedural evolution and natural selection  
- OPSEC decay and actionable weak points  

This casefile approaches scams the way intelligence teams map hostile networks: through **behaviour, incentives, and structure**, not individual events.

---

# 3. Technical Project — Domain Profiling Pipeline  
*Passive Recon | Feature Engineering | Automated ML Scoring*

A modular pipeline that performs **automated passive reconnaissance** and converts heterogeneous OSINT signals into a coherent feature set for anomaly scoring.

### Collection Modules
- WHOIS extraction  
- SSL/TLS certificate inspection  
- HTTP/HTML metadata analysis  
- favicon hashing (MurmurHash)  
- robots.txt retrieval  
- Certificate Transparency enumeration  

### Feature Engineering
Signals are normalized into structured indicators:

- domain age and lifecycle signals  
- certificate validity windows  
- entropy and digit ratios  
- metadata completeness  
- infrastructure and stack hints  
- presence/absence of expected assets  

### ML Component
An **Isolation Forest** generates an anomaly score based on accumulated profiles.  
The intent is not classification; the score highlights whether a domain’s infrastructure posture diverges from typical patterns.

The pipeline reflects an intelligence-style approach: wide passive coverage, interpretable features, and conservative conclusions.

---

# 4. Technical Project — UPI Fraud-Pattern Clustering  
*Behavioural Feature Engineering | Unsupervised ML | OSINT-Derived Data*

A workflow that turns irregular, user-submitted UPI handles into structured behavioural features and groups them using unsupervised learning.

### Data
Collected manually from open OSINT sources: complaint platforms, Reddit, X, YouTube, LinkedIn.  
Noise and inconsistency are part of the dataset by design.

### Processing
Scripts handle:

- prefix/PSP parsing  
- anomaly tagging (invalid PSPs, malformed strings, masking)  
- controlled normalization  
- manual correction where automation risks destroying signal  

### Feature Engineering
Each handle is mapped into:

- prefix length  
- digit ratio  
- Shannon entropy  
- mobile-number pattern detection  
- masking indicator  
- PSP category  

These features allow clustering based purely on observable behaviour.

### Clustering Output
KMeans (k=5) produces five stable behavioural groups:

- **Cluster 0** — human-like handles; personal or lightly misused mules  
- **Cluster 1** — impersonation-style or constructed mule infrastructure  
- **Cluster 2** — mobile-number mule pattern (burner SIM flows)  
- **Cluster 3** — masked or partially visible entries  
- **Cluster 4** — malformed/noisy data, often scraping or transcription artefacts  

The pipeline demonstrates how minimal strings, when engineered properly, reveal operational signatures.

---

# Repository Structure

    osint-casefile/
    scam-ecosystem-study/
    profiler/
    upi-clustering/

---

# Notes

Each project is scoped deliberately.  
The casefiles prioritize **behavioural and structural inference**.  
The technical projects emphasize **automation, signal engineering, and unsupervised modelling**.  
Together, they form a cohesive picture of how to extract intelligence from limited, noisy, public data.

