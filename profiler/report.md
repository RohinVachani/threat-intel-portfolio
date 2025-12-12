## **Executive Summary**
This project implements an automated **domain-profiling pipeline** designed to collect **OSINT signals** and convert them into structured, comparable intelligence. The system performs **WHOIS extraction**, **SSL certificate inspection**, **HTTP/HTML analysis**, **favicon hashing**, **robots.txt assessment**, and **Certificate Transparency (CT) subdomain enumeration**. These signals are then transformed into a feature vector used by an **Isolation Forest** model for anomaly scoring.

The focus is on demonstrating **end-to-end capability**: building **data-collection modules**, engineering **threat-relevant features**, handling failure cases, and integrating a lightweight **ML component**. The intent is not to produce a flawless enterprise tool but to show practical reasoning, design choices, and the ability to work with **real-world, inconsistent OSINT data** where responses vary by registry, region, and infrastructure.

A set of **legitimate domains** and **known scam domains** were profiled. Instead of relying solely on the model’s anomaly score, each signal was interpreted manually to understand what it reveals about domain behaviour and how reliable that signal is under different conditions. Several modules encountered expected issues such as **WHOIS redactions**, non-resolving domains, or **SSL mismatches** — these are documented because they reflect realistic constraints rather than errors in approach.

This report outlines the **pipeline’s architecture**, the **rationale** behind each selected signal, an **analysis** of the profiled domains, observed **limitations**, and how the system can be **extended or integrated** into broader threat-intelligence workflows.

# **2. Technical Architecture and Workflow**
The pipeline is structured as a modular **OSINT collector** paired with a lightweight **machine-learning stage**. Each component is isolated in its own script to keep the system transparent, debuggable, and easy to reason about. The workflow moves in a clear sequence: **gather → normalize → engineer features → optionally save → train → score**.

## **2.1 High-Level Flow**

**Input:**  
The user provides a domain along with an optional `--save` flag.

**Passive Reconnaissance:**  
Independent modules collect information from **WHOIS**, **SSL/TLS certificates**, **HTTP metadata**, **favicon files**, **robots.txt**, and **Certificate Transparency logs**.

**Normalization & Feature Engineering:**  
Raw output is standardized, missing-value handling is applied, and domain-level features are derived (entropy, digit ratios, metadata presence, etc.).

**Dataset Growth (optional):**  
When `--save` is used, the engineered feature vector is appended to a **CSV dataset**, and the anomaly model is retrained on the cumulative data.

**Anomaly Scoring:**  
An **Isolation Forest** model estimates how “unusual” the domain is relative to everything seen so far.

**Output:**  
The profiler prints all collected intelligence signals and the ML-derived anomaly score.

This structure allows the pipeline to function as both a **manual analysis helper** (without `--save`) and as a **self-expanding learning system** (with `--save`).

---

## **2.2 Module Breakdown**
Each module is single-responsibility by design:

**WHOIS Lookup** (`whois_lookup.py`)  
Queries domain registration data, extracts creation and expiry dates, registrar information, and checks for WHOIS privacy masking.

**SSL Certificate Fetching** (`ssl_fetch.py`)  
Retrieves the live TLS certificate from port 443 and parses issuer, validity period, and subject. Misconfigurations, mismatches, or default certificates are strong infrastructure indicators.

**HTTP & HTML Metadata** (`html_http_fetch.py`)  
Performs an HTTPS GET request and extracts:  
• server banners  
• X-Powered-By stack information  
• final URL after redirects  
• basic HTML metadata  
These elements help identify hosting quality, framework age, and potential misconfigurations.

**Favicon Hashing** (`favicon_hash.py`)  
Fetches the favicon, computes a MurmurHash value, and returns it.

**Robots.txt Analysis** (`robots_fetch.py`)  
Checks if robots.txt is present and captures a snippet.

**Certificate Transparency Enumeration** (`crtsh_subdomains.py`)  
Queries crt.sh for subdomains linked to the target domain.

---

## **2.3 Feature Engineering Layer**
The `feature_eng.py` script converts raw OSINT into ML-friendly numerical features. Examples include:  
• **domain age in days**  
• **SSL validity period**  
• **stack risk classification**  
• **entropy and digit ratios**  
• **sensitive subdomain indicators**  
• **favicon presence**  
• **metadata completeness**  

This abstraction is the bridge between recon data and machine learning.

---

## **2.4 Machine Learning Layer**
The ML component uses:  
• a **CSV dataset** of accumulated feature vectors  
• an **Isolation Forest** model for anomaly detection  
• a **transformed anomaly score** mapped to an intuitive 0–1+ scale  

The model is not intended to label domains as malicious or safe. Instead, it highlights how **abnormal the domain’s infrastructure** appears relative to previously seen data.

---

## **2.5 Limitations by Design**
Some OSINT signals intentionally remain out of scope (**DNS records**, **MX behavior**, **hosting ASN**, **screenshot analysis**, **content hashing**, etc.). These were excluded to emphasize **engineered depth over exhaustive breadth**.

# **3. Why These Signals Matter**
The profiler does not try to collect everything possible. Instead, it focuses on signals that consistently reflect how a domain is **built, maintained, and operated**. These indicators tend to expose patterns seen across legitimate businesses, small personal sites, and scam infrastructure. Each signal was included because it contributes directly to understanding **intent**, **maturity**, or **operational discipline**.

## **3.1 WHOIS Registration Signals**
Domain age, registrar choice, and WHOIS privacy often reveal the “story” of a domain:
• Older domains with stable renewal history tend to belong to established entities.  
• Very young domains frequently appear in scam campaigns, throwaway phishing operations, and short-lived fraud schemes.  
• Registrar patterns matter because certain low-cost, low-friction registrars are repeatedly used in fraudulent registrations.  
• WHOIS privacy is not inherently suspicious, but widespread abuse by scam operators makes it a useful supporting indicator.  

These values are not judged in isolation — **context** is what makes them meaningful.

## **3.2 SSL/TLS Certificate Signals**
A valid certificate doesn’t imply legitimacy, but how the certificate is **obtained and configured** matters:
• Issuer categories (enterprise CA vs free CA vs unknown) reflect operational maturity.  
• Short validity cycles (Let’s Encrypt 90-day certs) are common across both legit and malicious sites — the key is how the certificate fits with other signals.  
• Certificate mismatches, handshake failures, or self-signed certs are strong red flags for impersonation attempts or abandoned infrastructure.  
• SSL configuration exposes whether the domain is maintained carefully or assembled hastily.

## **3.3 HTTP & HTML Behavior**
Infrastructure leaks through HTTP responses:
• Server banners show hosting stack quality and patch hygiene.  
• Redirect chains may reveal domain parking, impersonation, or cloaking behavior.  
• Metadata completeness reflects whether the domain is part of a genuine business or a minimal template site.  

Small inconsistencies here often correlate with **scam infrastructure**.

## **3.4 Favicon Hash as an Infrastructure Fingerprint**
Favicon hashing is effective for:
• correlating domains sharing infrastructure  
• identifying reused website kits  
• spotting clusters of scam sites using identical assets  

Even favicon **presence or absence** becomes a lightweight maturity indicator.

## **3.5 Certificate Transparency Subdomains**
Subdomain footprint acts as a proxy for:
• organizational scale  
• domain lifecycle  
• shadow or forgotten services  
• impersonation patterns  
• wildcard certificate spreading  

Legitimate companies naturally accumulate many subdomains. Scam sites usually don’t.

## **3.6 Robots.txt Behavior**
Robots.txt supports broader intuition:
• Legitimate sites almost always have one.  
• Scam sites often skip it or leave boilerplate defaults.  
• Some fraudulent sites block all indexing.  

The value comes from how this aligns with the **overall profile**.

## **3.7 String-Level Domain Features**
Entropy, digit ratio, and domain length expose common scam-domain patterns:
• high entropy → algorithmically mixed characters  
• random digits → impersonation variants  
• disposable naming  
• typo-squatting characteristics  

These features raise suspicion when they **align with other signals**.

## **3.8 Why Not Add More Signals?**
Signals were intentionally limited:
• **Clarity over noise** — to avoid a bloated, unfocused pipeline.  
• **Interpretability** — each chosen signal is explainable and relevant.  
• **Portfolio focus** — demonstrates deliberate engineering, not exhaustive coverage.  

More signals can always be added, but this set already forms a **coherent intelligence framework**.

# **Domain Case Studies & Signal-Based Assessment**

Before diving into individual domains, it is important to clarify how these assessments were produced.  
All domain evaluations in this section rely exclusively on the raw signals collected by the profiler (**WHOIS**, **SSL certificate properties**, **HTTP/HTML headers**, **metadata**, **favicon hash**, **robots.txt behaviour**, and **Certificate Transparency logs**).  
The machine-learning anomaly score was **not** used to classify or influence the judgments.  
Every conclusion in this section is based on **manual threat analysis** and independent reasoning, not on the model’s output.  
This separation is intentional.  
The ML component is experimental; the analytical purpose of the project is to demonstrate how **consistent, interpretable signals** can be combined to evaluate domain legitimacy.  
The following case studies examine each domain individually, highlighting how specific indicators support the classification outcome.

---

## **4.1 hdfcsec.com (legitimate financial institution)**

**Observed signals:**  
• Domain age: established (2000).  
• SSL: Google Trust Services, consistent with Cloudflare-backed infra.  
• HTTP: clean 200 response, controlled redirect to `www` subdomain.  
• Metadata: limited, but typical for financial sites.  
• Robots.txt: restrictive but valid.  
• Favicon: stable hash.

**Interpretation:**  
Everything aligns with a **mature banking infrastructure**. No threat indicators.

---

## **4.2 fabindia.com (legitimate e-commerce brand)**

**Observed signals:**  
• Long domain age (1998).  
• SSL: Let’s Encrypt wildcard for `*.fabindia.com`.  
• HTTP: modern Nitrogen / Express stack.  
• Metadata: strong and complete.  
• Robots.txt: large, structured.  
• Subdomains: extensive (blog, API, mobile, etc.).

**Interpretation:**  
Exactly what a **large retail brand** exhibits. No impersonation traits.

---

## **4.3 mod.gov.in (Indian Ministry of Defence)**

**Observed signals:**  
• WHOIS: NIC registry (expected).  
• SSL: EV certificate (GlobalSign).  
• HTTP: stable 200, no redirect.  
• Metadata: dense.  
• Robots.txt: missing.  
• Favicon: 404.  
• CT logs: many structured subdomains.

**Interpretation:**  
Despite missing assets, EV certificate + government subdomain ecosystem strongly confirm legitimacy.

---

## **4.4 neal.fun (legitimate personal/creative site)**

**Observed signals:**  
• WHOIS partially redacted (normal for individuals).  
• SSL: Google Trust Services.  
• HTTP: Cloudflare edge.  
• Metadata: present.  
• Favicon: 404 (design choice).  
• CT logs: many project subdomains.  
• Robots.txt: present with simple sitemap.

**Interpretation:**  
Typical **developer/creator domain**. No threat indicators.

---

## **4.5 qwantz.com (long-running webcomic)**

**Observed signals:**  
• Domain age: 2002.  
• SSL: Let’s Encrypt.  
• HTTP: Apache, loads correctly.  
• Metadata: complete.  
• Favicon: stable.  
• Robots.txt: selective crawler blocks.  
• CT logs: minimal (root + www).

**Interpretation:**  
Consistent with a **long-standing static content site**. No anomalies.

---

## **4.6 perfumelab.in (abandoned or unstable infrastructure)**

**Observed signals:**  
• WHOIS: real creation data (GoDaddy).  
• SSL: valid Let’s Encrypt.  
• HTTP: all HTTPS connections time out.  
• Metadata: unreachable.  
• Favicon: unreachable.  
• Robots.txt: unreachable.  
• CT logs: meaningful subdomains (catalog, order, version).

**Interpretation:**  
Likely **abandoned infrastructure**:  
valid SSL + historical subdomains but **total unreachability**.  
Moderately risky because abandoned domains are often reused for fraud.

---

## **4.7 youprint.in (high-risk abandoned domain)**

**Observed signals:**  
• WHOIS: domain appears “available for registration”.  
• SSL: handshake fails.  
• HTTP: DNS resolution fails.  
• Favicon: unreachable.  
• Robots.txt: unreachable.  
• CT logs: unusually large set, including wildcard entries.

**Interpretation:**  
Classic **abandoned domain footprint** with a history of wildcard certs.  
High-risk due to common exploitation in scam cycles.

---

## **4.8 hdfcsec.xyz (clear scam / impersonation domain)**

**Observed signals:**  
• WHOIS: no useful data.  
• SSL: certificate fetch fails.  
• HTTP: resolution failure.  
• Favicon: unreachable.  
• Robots.txt: unreachable.  
• CT logs: entries for `*.hdfcsec.xyz` and mobile patterns.

**Interpretation:**  
Not a misconfiguration — a **brand impersonation** domain for “hdfcsec.com”.  
Broken infra + minimal CT traces = common scam pattern.

---

## **4.9 fabindia.club (impersonation domain)**

**Observed signals:**  
• WHOIS: no ownership data.  
• SSL: timeout.  
• HTTP: unreachable.  
• Subdomains: only root + www.  
• Robots.txt / favicon: unreachable.

**Interpretation:**  
Matches a **brand-squatting impersonation domain**: alternate TLD + no real infrastructure.

---

## **4.10 mod.gov.in.aboutcase.nl (malicious impersonation)**

**Observed signals:**  
• WHOIS: recent creation, low-trust registrar (“Edomains LLC”).  
• SSL: presents certificate for `airtel.com` (mismatch).  
• HTTP: fails due to hostname mismatch.  
• Favicon + robots.txt: unreachable.  
• CT logs: only minimal entries.

**Interpretation:**  
Classic **string-based impersonation tactic** embedding “mod.gov.in” inside a longer hostname.  
Airtel cert mismatch confirms **generic shared hosting**, not government infra. Clear malicious intent.

---

# **Summary of Domain Classes Identified**

     **Domain Type**     |                        **Domains**  
           ---           |                            ---  
**Legitimate, stable**   | hdfcsec.com, fabindia.com, mod.gov.in, neal.fun, qwantz.com  
**Abandoned / unstable** | perfumelab.in, youprint.in  
**Active impersonation** | hdfcsec.xyz, fabindia.club, mod.gov.in.aboutcase.nl  

This mapping shows the tool’s ability to distinguish **genuine infrastructure** from **high-risk or malicious lookalikes**, even when individual signals are incomplete.

# **5. Failure Modes, Limitations & Iterative Debugging**
No profiler is flawless, and this project was not built to pretend otherwise.  
A core part of the work involved discovering **what breaks, why it breaks, and how failures strengthen understanding** rather than undermine the tool.  
This section documents the limitations observed during testing and the reasoning behind the fixes and design choices.

---

## **5.1 WHOIS Variability, Timeouts & Redaction Rules**
WHOIS lookups are **inconsistent by nature**. During testing, several domains returned:  
• Redacted responses due to GDPR/ICANN privacy rules  
• Timeouts from registry rate-limiting  
• Incomplete records (`creation_date = None`, `registrar = None`, etc.)

Instead of treating this as tool error, it was reframed as **realistic signal behaviour**:  
• Scam domains often hide behind privacy shields  
• Some malicious operators choose registrars with restrictive WHOIS endpoints  
• Some scam domains genuinely produce malformed or missing WHOIS records  

The profiler was updated to:  
• Treat missing WHOIS fields as **graceful fallbacks**, not fatal failures  
• Avoid assumptions about registrar, nameservers, or dates  
• Encode missing values directly into feature vectors instead of crashing  

A **major reliability improvement**.

---

## **5.2 SSL Fetching Breakpoints: Hostname Mismatch, Timeout & NXDOMAIN**
Many malicious or newly created domains exhibit:  
• No DNS resolution  
• Misconfigured SSL certificates  
• Certificates issued for unrelated domains (e.g., Airtel for *mod.gov.in.aboutcase.nl*)  
• Expired or nonexistent certificates  

Originally these errors **halted execution**.  
The tool was modified to convert SSL failures into structured intelligence:

# **6. Conclusions & Reflection**
This project set out with a clear objective: build a small, practical **threat-intelligence pipeline** that can pull signals from multiple sources, normalize them, and present an **interpretable risk picture** for arbitrary domains. The goal was not to create a perfect classifier or claim high detection accuracy — it was to demonstrate **technical competence**, **reasoning**, and the ability to design, adapt, and debug **real-world intelligence workflows**.

The profiler now does exactly that. It retrieves **WHOIS**, **SSL**, **HTTP headers**, **HTML metadata**, **favicon hashes**, **robots.txt behaviour**, and **Certificate Transparency (CT)** data, then converts them into a coherent feature set. Every module is **independent**, **failure-tolerant**, and designed to output useful intelligence even when external data is incomplete or inconsistent.

A major part of the learning came from embracing the realities of **threat-intelligence data**. Domains behave differently across regions, CT logs timeout, WHOIS records are redacted, SSL certificates misalign, and scam domains disappear mid-analysis. Instead of enforcing how the web “should” behave, the profiler was adapted to how it **actually behaves**. This required multiple cycles of debugging, restructuring, and exception-handling — and these adjustments are now intentionally built into the design.

The anomaly-detection model sits on top of the pipeline not as a decisive authority, but as a demonstration of how these signals can extend into **automated detection workflows**. The model is intentionally simple; its purpose is to show that the pipeline can support machine learning, not to serve as a production classifier.

The broader takeaway is that **technical threat intelligence is about correlation, context, and infrastructure behaviour**, not single metrics or magical detection heuristics. Effective analysis requires examining inconsistencies, not ignoring them. This project demonstrates that mindset clearly: every signal is chosen with intent, and every failure is handled in a way that increases reliability and interpretability.

This work is not meant to be final — real profilers evolve over hundreds of signals and years of operational refinement. But as a compact, well-structured demonstration of **capability, reasoning, and adaptability**, this project meets its purpose.  
The tool works, the design is defensible, and the analysis reflects a genuine understanding of how infrastructure-level signals reveal intent and risk on the internet.

