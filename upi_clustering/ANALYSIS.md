# CLUSTER 0 — data-backed

Cluster 0 is the most normal-looking group of UPI IDs. The prefixes look human, not synthetic — usually 8–11 characters, a mix of names and semi-random numbers. Digit ratios in the sample fall around 0.3–0.9, and entropy is roughly 2.4–3.2.

Sample entries: guri09804@okhdfcbank, gasiram32@ybl, q72669644@ybl, MYN6889921@axisbank, Ashok94169@dbs

PSPs are ordinary and spread out (YBL, Axis, DBS, AUBank, OKICICI).

**Interpretation:** these look like personal accounts or lightly used mule IDs. Likely stolen victims or throwaway accounts used for small opportunistic transfers. They don’t show signs of long-term or structured fraud activity.

**Operational notes:** common in resale/job-scam flows or one-off transfers. Lower priority for infrastructure analysis but worth tracking if they repeat across multiple complaints.

**Confidence:** Medium — behaviour is broad but consistent.

---

# CLUSTER 1 — data-backed

Cluster 1 represents deliberate fraud infrastructure. Prefixes are clearly constructed: long (many fall between 13–22 characters), very low digit ratio (often zero), and high entropy (around 3.1–3.9).

Sample entries: tpsl.government@icici, flipkart.payu@axisbank, ccbillpayment@icici, paytm-onlinelegalindia@ptybl, manmohanmeena667815@okicici, alammondalz7585@okaxis

Two groups appear:

1. **Impersonation handles** — mimic merchants, payment brands, or government names (for example tpsl.government@icici, ixigo.payu@axisbank).  
2. **Overbuilt mule handles** — long name-like prefixes with many digits added (for example manmohanmeena667815).

Many entries come from ICICI, Axis, OKSBI or PSPs flagged as unusual or inconsistent, which matches long-running scam setups.

**Interpretation:** these are intentionally created accounts used for impersonation scams, refund scams, verification scams, and scalable cash-out operations.

**Operational notes:** good candidates for link analysis and PSP escalation. If transaction data becomes available, this cluster should show repeated inflow/outflow patterns.

**Confidence:** High — patterns match well.

---

# CLUSTER 2 — data-backed

Cluster 2 is the mobile-number cluster. All prefixes are 10-digit numbers.

Sample entries: 8926087010@okbizaxis, 8695736195@axl, 9838622663@ybl, 8826183869@paytm, 9923558052@idbi

Digit ratio is basically 1.0, prefix_length is exactly 10, and entropy is around 2.2–2.7.

PSPs include AXL, OKBIZAXIS, YBL, Paytm — all common in OLX and marketplace-style mule flows.

**Interpretation:** these are fast-use disposable accounts tied to mobile numbers: burner SIMs, rented SIMs, or victims’ numbers being reused. They fit short-cycle cash-out behaviour.

**Operational notes:** easier to trace via SIM/KYC but also easy for scammers to obtain through SIM farms. Useful to block or flag when repeated across cases.

**Confidence:** High for mule behaviour, low for attribution without telecom/KYC data.

---

# CLUSTER 3 — data-backed

Cluster 3 contains masked or partially hidden prefixes. Many examples show platform-side redaction.

Sample entries: bi******ya@hdfcbank, 779698***55@kotak, 75687***18@axl, ******9119@ybl, 902788***0dipika@pnb

Masking is usually done by forums, complaint sites, or social media — not by the scammer. Even so, some signals remain: digit ratios tend to be high, visible prefix lengths usually fall around 10–16, and entropy varies depending on how much is hidden.

PSPs include Kotak, OKSBI, PNB, YBL — a mixed set.

**Interpretation:** incomplete data. These could be victims, lightly used mules, legitimate users, or hidden scam numbers. Not enough visibility to draw confident behavioural conclusions.

**Operational notes:** use these as low-confidence leads. They become useful only when supported by metadata such as repeated mentions, state, amount, or source.

**Confidence:** Low–Medium due to limited data.

---

# CLUSTER 4 — data-backed

Cluster 4 is the broken or malformed data group. Many entries have invalid PSPs, missing prefixes, or obvious formatting errors.

Sample entries: fathll@airtel (invalid PSP), @airtel (missing prefix), @centralbank, mi.bills@ic (invalid suffix), plus occasional valid outliers like komers@ybl

Prefix lengths are often zero or very small, digit ratio is zero, and entropy is low or zero depending on the error.

**Interpretation:** this is not a behavioural cluster. It contains scraping errors, OCR mistakes, user typos, and badly copied UPI IDs.

**Operational notes:** quarantine these rows for manual review. They are not worth analysing until verified.

**Confidence:** High for identifying this as a data-quality cluster.

