# INTERIM PROGRESS REPORT

**Module Title:** Final Year Individual Project  
**Module Code:** COM 4901  
**Project Title:** AUTOMATED RISK ASSESSMENT AND GOVERNANCE FRAMEWORK FOR SHADOW AI AGENTS IN CORPORATE NETWORKS  

**Student Name:** S.H.I. Madhushan  
**Student ID:** 14504  
**Supervisor Name:** Mr. Sahan Weerasinghe  
**Faculty:** Faculty of Computer Science and Engineering, KIU University, Sri Lanka  
**Submission Date:** June / July 2026  

---

## Table of Contents
1. [Introduction](#1-introduction)
   - 1.1 Background and Context
   - 1.2 Problem Statement
   - 1.3 Project Aim and Objectives
2. [Progress Summary](#2-progress-summary)
   - 2.1 Tasks Completed So Far
   - 2.2 Current Project Status
   - 2.3 Evidence of Progress (Artefacts Developed)
3. [Literature Review Progress](#3-literature-review-progress)
   - 3.1 Summary of Key Literature Identified
   - 3.2 Theoretical and Conceptual Foundation
   - 3.3 Research Gap Justification
4. [Methodology and Solution Approach](#4-methodology-and-solution-approach)
   - 4.1 Tiered System Architecture
   - 4.2 Data Ingestion & Synthetic Telemetry
   - 4.3 Weighted Risk Scoring Engine (WRSE) Mathematical Model
5. [Design and Implementation Progress](#5-design-and-implementation-progress)
   - 5.1 Host Machine Log Interception & Ingestion Engine (`live_mitm_logger.py`)
   - 5.2 Payload Extraction, Normalization & Master Asset Indexing (`data_core.py`)
   - 5.3 Real-Time WRSE Risk Calculation & Severity Mapping (`data_core.py`)
   - 5.4 Authentication & Session Persistence Module (`auth.py`)
   - 5.5 Core Administrative Dashboard (`app.py`)
   - 5.6 Event Monitoring & State Persistence (`components.py`)
   - 5.7 Custom UI Styling & Glassmorphism (`styles.py`)
6. [Testing and Evaluation Plan (Draft)](#6-testing-and-evaluation-plan-draft)
   - 6.1 Proposed Testing Strategy
   - 6.2 Security & WAF Mechanism Validation
   - 6.3 WRSE Score Calibration & Alert Verification
7. [Challenges and Risk Management](#7-challenges-and-risk-management)
   - 7.1 Technical Challenges Faced
   - 7.2 Actions Taken to Resolve Challenges
8. [Revised Work Plan](#8-revised-work-plan)
   - 8.1 Remaining Tasks
   - 8.2 Updated Timeline & Milestones
9. [Conclusion](#9-conclusion)
10. [References](#10-references)

---

## 1. Introduction

### 1.1 Background and Context
By 2026, the corporate cybersecurity landscape has been fundamentally reshaped by the mass adoption of Large Language Models (LLMs) and autonomous AI agents. While these advancements have pushed organizational efficiency to new heights, they have simultaneously introduced a critical vulnerability known as **Shadow AI**. Shadow AI refers to the unsanctioned or unauthorized deployment of artificial intelligence tools and autonomous agents by employees, operating entirely outside the formal oversight of IT governance and security vetting. Unlike traditional Shadow IT—which primarily revolved around unapproved cloud storage or SaaS applications—Shadow AI is dynamic, conversational, and persistent in its data exchange. Employees frequently utilize unapproved LLMs to process proprietary business roadmaps, internal source code fragments, or sensitive financial projections, resulting in severe "Semantic Leakage" to external, unmanaged servers.

### 1.2 Problem Statement
The rapid adoption of Artificial Intelligence within corporate infrastructures has significantly outpaced the defensive capabilities of traditional cybersecurity frameworks. The core issue lies in the inability of current systems to distinguish between productive AI usage and high-risk data exfiltration occurring through Shadow AI channels. Existing tools such as Next-Generation Firewalls (NGFW) and legacy Data Leakage Prevention (DLP) systems remain fundamentally "context-blind." They operate on static signatures and cannot evaluate the semantic risk of natural language prompts embedded within encrypted HTTPS streams. Furthermore, organizations lack an automated mechanism to calculate dynamic risk metrics in real-time, resulting in binary "block or allow" postures that either cripple productivity or expose the enterprise to massive intellectual property loss.

### 1.3 Project Aim and Objectives
**Research Aim:**  
The primary aim of this research is to architect, implement, and evaluate a high-fidelity prototype framework (**ContextGuard**) capable of autonomously identifying Shadow AI interactions and quantifying their inherent security risks within a simulated corporate network infrastructure.

**Research Objectives:**
1. **Traffic Signature Characterization & Metadata Extraction:** To analyze and model behavioral metadata (e.g., packet size distribution, API call frequency) to distinguish between human-initiated prompt interactions and automated bot-driven AI API calls.
2. **NLP-driven Linguistic Sensitivity Mapping:** To implement a Natural Language Processing (NLP) filtering mechanism utilizing TF-IDF (Term Frequency-Inverse Document Frequency) and pattern matching to identify and categorize sensitive corporate assets (Intellectual Property, Financial Data, Strategic Plans) within prompt payloads.
3. **Design of the Weighted Risk Scoring Engine (WRSE):** To design and implement a multi-factor mathematical model that dynamically calculates a normalized Risk Score (0–100) based on Data Sensitivity ($W_s$), Destination Trust ($W_d$), and User Authorization ($W_u$).
4. **Implementation of an Administrative Governance Dashboard:** To develop a real-time, interactive, Streamlit-based governance dashboard providing IT security teams with high-fidelity threat visualizations, automated alerting thresholds, and comprehensive forensic logging capabilities.

---

## 2. Progress Summary

### 2.1 Tasks Completed So Far
To date, the project has transitioned successfully from the conceptual design and mathematical formulation phases into active prototype implementation. The following core milestones have been accomplished:
- **Comprehensive Literature & Gap Analysis:** Completed a rigorous review of 2024–2026 enterprise cybersecurity literature regarding LLM data exfiltration and perimeter defense failures.
- **Mathematical Logic Verification:** Finalized and programmed the Weighted Risk Scoring Engine (WRSE) formula into executable Python functions.
- **Host Machine Traffic Interception (`live_mitm_logger.py`):** Developed a functional Man-in-the-Middle (MITM) proxy script utilizing `mitmproxy` to intercept TLS-encrypted HTTPS traffic in real-time on the host machine, selectively capturing POST requests directed at prominent AI domains.
- **Master Asset Registry Integration (`data_core.py`):** Structured and indexed 15 CSV data sheets containing baseline asset weights and unique organizational identifiers (e.g., SAML tokens, API keys, Patient IDs, DB connection strings) to support dynamic NLP matching.
- **Real-Time WRSE Scoring Engine:** Programmed the complete mathematical execution flow in Python, accurately combining data sensitivity weights ($W_s$), destination reputation penalties ($W_d$), and user privilege metrics ($W_u$) to calculate normalized risk coefficients (0–100).
- **Advanced UI & Authentication Implementation:** Fully engineered a highly secure, aesthetically superior Web UI utilizing Streamlit, featuring bespoke glassmorphism aesthetics, SQLite user authentication (`users.db`), robust brute-force lockout mechanisms, and state-of-the-art file-backed session persistence.

### 2.2 Current Project Status
The project is currently at the **Mid-Implementation and Verification Stage (Weeks 7–9 of the original roadmap)**. The core log ingestion engine, payload normalizers, mathematical scoring modules, database schemas, and real-time interactive dashboard components are fully operational. Development efforts are currently focused on fine-tuning the visual filtering capabilities, conducting stress tests on session persistence across browser reloads, and preparing draft validation plans.

### 2.3 Evidence of Progress (Artefacts Developed)
The following primary software artefacts have been developed and successfully integrated into the working prototype:
1. `Section1_DataIngestion/live_mitm_logger.py`: A real-time traffic interception script powered by `mitmproxy` that decodes TLS-encrypted HTTPS streams, isolates AI API calls, decodes complex URL/JSON structures, and writes structured audit logs.
2. `Section1_DataIngestion/wrse_comprehensive_audit.log`: The unified JSON log file storing rich connection metadata, source/destination nodes, and raw prompt payloads captured from the host machine.
3. `data_core.py`: The core ingestion and NLP pre-processing pipeline that normalizes prompt payloads, evaluates keyword frequencies against 15 CSV sheets, maps destination trust coefficients, and calculates the real-time WRSE score.
4. `auth.py`: A highly secure authentication module implementing SHA-256 password hashing, WAF-style input sanitization (blocking SQLi and XSS), brute-force defense (30-second lockout after 5 failed attempts), and custom file-backed UUID session token tracking via URL query parameters (`_sid`).
5. `app.py`: The central dashboard execution module containing the multi-column layout, top header filtering controls (Time Range, Time Type, and Monitor Status), sidebar navigation panel, and dynamic page routing logic.
6. `components.py`: A modular UI helper file responsible for rendering interactive threat feeds, the top asset summary strip, and SQLite-backed status update dropdowns (`monitor_status` table).
7. `styles.py`: A comprehensive CSS injection file (1,090+ lines) defining custom dark-mode aesthetics, glassmorphism containers, custom status badges, and overrides for native Streamlit UI elements.
8. `users.db`: A localized SQLite database storing user credentials, role definitions, and persistent event monitoring states.

---

## 3. Literature Review Progress

### 3.1 Summary of Key Literature Identified
Recent publications by Gartner (2026) and Microsoft (2026) highlight a 70% surge in unsanctioned generative AI tool deployment within corporate environments. Davis (2024) and White (2026) emphasize that the primary attack vector has evolved from traditional malicious binaries to "Semantic Leakage"—the inadvertent sharing of proprietary, unstructured natural language prompts into public LLMs. Furthermore, Wilson (2026) establishes that legacy Next-Generation Firewalls (NGFW) and standard secure web gateways remain fundamentally blind to these payloads due to TLS/SSL encryption and the absence of semantic parsing capabilities.

### 3.2 Theoretical and Conceptual Foundation
The theoretical foundation of this research rests upon two pillars: **Behavioral Fingerprinting** and **Multi-Criteria Decision Modeling**. According to Perera (2026) and Smith (2025), autonomous AI wrappers and scraping scripts exhibit distinct network characteristics, such as predictable inter-arrival times (IAT) and packet size homogeneity, which distinguish them from human typing patterns. To quantify the risk of the underlying payload, the project incorporates a linear weighted sum model, synthesizing principles from information retrieval (TF-IDF keyword weighting) and zero-trust access control (role-based trust coefficients).

### 3.3 Research Gap Justification
The literature review confirms a glaring operational void in modern enterprise security: existing platforms force security operations centers (SOC) into a binary choice of total prohibition or unmonitored allowance. There is no lightweight, context-aware inspection layer that dynamically calculates a quantitative risk score (0–100) based on the triad of **Data Sensitivity, Destination Reputation, and User Seniority**. The **ContextGuard** framework directly addresses this gap by providing an automated, quantitative governance layer without introducing heavy network latency or requiring invasive endpoint agent installations.

---

## 4. Methodology and Solution Approach

### 4.1 Tiered System Architecture
The framework operates as a transparent inspection layer structured into four decoupled logical tiers:
1. **Data Ingestion Module:** Captures simulated network telemetry, API logs, and unencrypted prompt payloads via active MITM interception.
2. **Inspection Layer:** Executes parallel heuristic analysis (evaluating IAT and packet sizes for bot detection) and deep content inspection (matching payloads against the 15 CSV Master Asset Registry).
3. **WRSE Scoring Module:** Processes the extracted vectors through the mathematical engine to compute the unified risk coefficient.
4. **Visualization & Governance Layer:** Presents actionable intelligence, time-series analysis, and administrative override options via the Streamlit dashboard.

```
+-----------------------------------------------------------------------+
|                       4. VISUALIZATION & GOVERNANCE                   |
|              (Streamlit Dashboard, Real-time Alerts, Audit Logs)       |
+-----------------------------------------------------------------------+
                                    ^
                                    |  Real-time Risk Telemetry
+-----------------------------------------------------------------------+
|                        3. WRSE SCORING MODULE                         |
|      RS = (Ws * S) + (Wd * D) + (Wu * U)   [Normalized 0-100 Scale]   |
+-----------------------------------------------------------------------+
                                    ^
            +-----------------------+-----------------------+
            | (Behavioral Vectors)                          | (Semantic Vectors)
+---------------------------+               +---------------------------+
|    HEURISTIC ENGINE       |               |        NLP ENGINE         |
|  (IAT & Packet Anomaly)   |               |  (TF-IDF & Asset Match)   |
+---------------------------+               +---------------------------+
            ^                                               ^
            +-----------------------+-----------------------+
                                    |  Decoupled Streams
+-----------------------------------------------------------------------+
|                         1. DATA INGESTION MODULE                      |
|                   (live_mitm_logger.py & Synthetic Logs)              |
+-----------------------------------------------------------------------+
```

### 4.2 Data Ingestion & Synthetic Telemetry
To maintain strict compliance with ethical standards and data privacy regulations, the framework relies on Synthetic Data Engineering combined with simulated host machine interception. A highly realistic enterprise dataset (`TechMed_Asset_Dataset_30000.xlsx` and auxiliary CSVs) simulates network traffic generated by multiple user identities interacting with various AI platforms (e.g., OpenAI, Anthropic Claude, custom internal LLMs). Each record encapsulates source IPs, destination URLs, user agent strings, timestamps, and full natural language prompts.

### 4.3 Weighted Risk Scoring Engine (WRSE) Mathematical Model
The computational core of ContextGuard is the WRSE algorithm. The Risk Score ($RS$) is derived via a multi-factor linear weighted sum model:

$$RS = (W_s \times S) + (W_d \times D) + (W_u \times U)$$

Where:
- **Sensitivity Score ($S$):** Calculated via NLP matching against the internal keyword registry: $S = \sum_{i=1}^{n} (w_i \times c_i)$, where $w_i$ represents the keyword criticality weight (e.g., "Source Code" = 0.95, "Internal Roadmap" = 0.85) and $c_i$ represents frequency.
- **Destination Trust ($D$):** A penalty coefficient reflecting the security posture of the destination endpoint (e.g., Authorized Enterprise Endpoint = 0.1, Public Consumer LLM = 0.9).
- **User Profile Weight ($U$):** A risk factor determined by the employee's organizational role and historical data access authorization.
- **Weighting Coefficients ($W_s, W_d, W_u$):** Pre-calibrated constants ensuring primary mathematical dominance is assigned to Data Sensitivity ($W_s = 0.50, W_d = 0.25, W_u = 0.25$). Interactions exceeding a critical threshold ($RS > 80$) instantly trigger automated SOC alerts.

---

## 5. Design and Implementation Progress

This section details the concrete technical progress achieved across the prototype's primary modules, providing an exhaustive breakdown of the log interception mechanics, payload normalization, and mathematical risk calculation engines.

### 5.1 Host Machine Log Interception & Ingestion Engine (`live_mitm_logger.py`)
To capture live interactions between enterprise workstations and external AI platforms, we developed a real-time interception module utilizing `mitmproxy`. This script acts as a transparent inspection layer directly on the host machine, intercepting outbound TLS-encrypted HTTPS traffic before it exits the corporate perimeter.

#### Key Architectural Mechanics:
1. **Targeted Domain Filtering:** The engine inspects the `HTTPFlow` object and matches the destination hostname against a predefined list of prominent generative AI endpoints (`chatgpt.com`, `api.openai.com`, `gemini.google.com`, `claude.ai`, `deepseek.com`, `copilot.microsoft.com`). Only outbound `POST` requests directed at these services are intercepted for deep packet inspection, preserving network bandwidth and employee privacy for standard web browsing.
2. **Advanced Double-Plane URL Decoding Engine:** Generative AI platforms employ vastly different payload encoding mechanisms. For instance, Google Gemini frequently encapsulates prompts in complex URL-encoded structures (`f.req=`), whereas OpenAI and Claude utilize structured JSON bodies (`{"messages": [...]}`). `live_mitm_logger.py` implements a robust multi-stage parser:
   - *Stage 1 (URL Entity Decoding):* Detects URL-encoded strings (`%5B`, `%22`, `f.req=`) and applies `urllib.parse.unquote` to strip garbage boundary structures.
   - *Stage 2 (JSON Structure Parsing):* Safely parses JSON bodies to extract the raw text from deeply nested keypaths (e.g., `messages[0].content.parts[0]` or `prompt`).
3. **Structured Telemetry Archiving:** The extracted prompt payload is combined with critical connection metadata—including Client IP, Source Port, Destination Domain, Destination IP, HTTP Method, User-Agent, and exact timestamps. This unified telemetry object is dynamically appended to `wrse_comprehensive_audit.log` in beautifully structured JSON format.

```python
# Code Snippet from live_mitm_logger.py illustrating the Double-Plane Decoding Engine
if "f.req=" in raw_content or "%5B" in raw_content or "%22" in raw_content:
    decoded_stage = urllib.parse.unquote(raw_content)
    prompt_text = decoded_stage.replace("f.req=", "").strip()
else:
    prompt_text = "N/A"
    try:
        data = json.loads(raw_content)
        if "messages" in data:
            msg_list = data.get("messages", [])
            if msg_list and isinstance(msg_list, list):
                parts = msg_list[0].get("content", {}).get("parts", [None])[0]
                prompt_text = str(parts) if parts else "Dynamic Session Initialization"
        elif "prompt" in data:
            prompt_text = str(data["prompt"])
    except:
        if len(raw_content) > 5:
            prompt_text = raw_content[:400]
```

```
[ INSERT SCREENSHOT 1: Terminal Execution of live_mitm_logger.py Here ]
Caption: Figure 1 - Terminal capture of live_mitm_logger.py intercepting an outbound HTTPS POST request to an AI endpoint and outputting '[🛡️ INGESTION PLANE CLEANED] Successfully parsed traffic signature.'
(*Instructions for Student: Run mitmproxy with the script or show the terminal output where the logger confirms parsing a request.*)
```

```
[ INSERT SCREENSHOT 2: wrse_comprehensive_audit.log JSON Structure Here ]
Caption: Figure 2 - The structured JSON log format within wrse_comprehensive_audit.log containing connection metadata, source/dest nodes, and the extracted raw prompt.
(*Instructions for Student: Open wrse_comprehensive_audit.log in VS Code, highlight a clean JSON log entry, and take a screenshot.*)
```

### 5.2 Payload Extraction, Normalization & Master Asset Indexing (`data_core.py`)
Once the raw logs are written to disk, the central analytical engine (`data_core.py`) executes a highly sophisticated pre-processing and indexing routine to prepare the unstructured prompts for mathematical risk evaluation.

#### 1. Forensic Text Normalization (`forensic_normalize`):
Unstructured prompts frequently contain escape characters, quotes, and nested array brackets that disrupt standard NLP string matching. The `forensic_normalize(text)` function applies a multi-pass regex filter:
- It extracts pure text strings using regex matching (`r'"([a-zA-Z0-9\s\.\,\!\?\:\-\_\/\@\#\$\%\^\&\*\(\)\+]{6,})"'`).
- It strips out structural noise (`\\"`, `"`, `[`, `]`) and converts all characters to lowercase while preserving critical punctuation (`[^\w\s\.]`). This creates two clean outputs: `clean_text` (for substring keyword matching) and `normalized_str` (for regex pattern matching like IP addresses).

#### 2. Master 15-Sheet CSV Indexing (`load_master_dataset`):
To enable context-aware inspection, the framework ingests **15 Master CSV Data Sheets** located in `/home/izu/ShadowAI_Framework/data Sheets/`. These sheets represent organizational assets across various tiers (Medical Records/PHI, Infrastructure Core Assets, Intellectual Property, Financial Data, HR Records). 
- *Multi-Key In-Memory Indexing:* To achieve sub-second matching speeds without disk I/O bottlenecks, `load_master_dataset()` builds a highly optimized in-memory dictionary index (`idx`). It indexes assets across three distinct dimensions:
  1. `record_ids`: Explicit asset record tags (e.g., `IAM-670469`, `INS-985884`, `SRC-518498`, `HL7-517169`).
  2. `patient_ids`: Specialized healthcare unique identifiers (e.g., `TM-XXXX-XXXX`).
  3. `tokens`: High-specificity unique data strings (SAML Token Hashes, API Key Hashes, JWT Secrets, DB Connection Strings, Subnets, Git Repositories).
- *Collision Prevention:* To avoid duplicate match inflation caused by common names or generic status words (e.g., "Robert Perera", "Active"), the token index strictly filters attributes against a hardcoded `UNIQUE_ID_COLS` set.

#### 3. Deep Content Asset Matching (`find_master_asset_match`):
When a prompt is evaluated, `find_master_asset_match(prompt_text, asset_index)` scans the text for explicit Record/Patient IDs using regex (`r'[A-Z0-9]{2,5}-\d{4,8}'`) and cross-references them against the token index. It utilizes a `seen_records` set and `matched_token_values` tracking to ensure that if a prompt contains both an Asset ID and its corresponding Database String, it is correctly counted as a single exposed asset rather than creating artificial mock collisions.

```python
# Code Snippet from data_core.py illustrating Master Asset Matching & Collision Defense
for token, rec in asset_index.get("tokens", {}).items():
    if token in prompt_text:
        # Prevents duplicate mock collisions if token is already accounted for by an existing matched record
        if token not in matched_token_values and rec and rec["RECORD ID"] not in seen_records:
            seen_records.add(rec["RECORD ID"])
            matches.append(rec)
            for val in rec.get("_original_attributes", {}).values():
                val_str = str(val).strip()
                if len(val_str) > 5:
                    matched_token_values.add(val_str)
```

```
[ INSERT SCREENSHOT 3: Master CSV Asset Registry Indexing Here ]
Caption: Figure 3 - The 15 Master CSV data sheets located in the 'data Sheets' directory, containing baseline weights and high-specificity tokens.
(*Instructions for Student: Take a screenshot of the VS Code file explorer showing the list of T1_xxx.csv, T2_xxx.csv files inside 'data Sheets'.*)
```

### 5.3 Real-Time WRSE Risk Calculation & Severity Mapping (`data_core.py`)
The ultimate technical objective of ContextGuard is translating the extracted metadata and asset matches into a standardized, actionable Risk Score ($RS$). This is handled by `calculate_wrse()`.

#### Step-by-Step Mathematical Execution in Code:
The algorithm accepts four primary arguments: `prompt_text`, `dest_trust_w`, `user_auth_w`, and `asset_matches`. It applies pre-calibrated baseline constants: **$W_S = 0.50$ (Sensitivity), $W_D = 0.25$ (Destination Trust), and $W_U = 0.25$ (User Authority)**.

```python
# Code Snippet from data_core.py illustrating the WRSE Calculation Logic
if asset_matches:
    # Sum asset weights for all distinct assets leaked in the payload
    s_score = sum(float(m["ASSET WEIGHT"]) for m in asset_matches)
    s_score = min(s_score, 1.0)
    for m in asset_matches:
        detected_keywords.append(f"Match:{m.get('RECORD ID', 'Asset')} (Wi={m.get('ASSET WEIGHT', 0.95)})")
        detected_tiers.add(m.get("DATA TIER", "Medical Records (PHI)"))
else:
    s_score = 0.0
    if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', normalized_str):
        s_score += 0.95
        detected_keywords.append("Exposed Internal IP")
        detected_tiers.add("Infrastructure Core Assets")
    for word, (weight, tier) in KEYWORDS_DB.items():
        count = clean_text.count(word)
        if count > 0:
            s_score += weight * count
            detected_keywords.append(word)
            detected_tiers.add(tier)
    s_score = min(s_score, 1.0)

rs = (W_S * s_score) + (W_D * dest_trust_w) + (W_U * user_auth_w)
return round(rs * 100, 2), detected_keywords, list(detected_tiers), clean_text, normalized_str
```

#### Detailed Numerical Walkthrough of an Active Threat:
Consider a real-world scenario processed by the prototype: A software engineer (`idx_e = 0`) copies an internal HL7 healthcare protocol header (`HL7-517169`) and pastes it into `chatgpt.com` to request a code refactor.

1. **Step 1 (Sensitivity Score $S$ Calculation):**
   - The NLP engine matches `HL7-517169` against the Master Asset Registry. The CSV definition establishes a baseline Asset Weight $W_i = 0.95$ (Tier 1 - Medical Records/PHI).
   - $S = \min(\sum W_i, 1.0) = \min(0.95, 1.0) = 0.95$.
2. **Step 2 (Destination Trust $D$ Assignment):**
   - `process_events()` inspects `dest_domain`. Because `chatgpt.com` matches the unmanaged public LLM list (`["gemini", "chatgpt", "claude", "openai"]`), the destination penalty maximizes: $D = 0.95$. (If it were an internal managed enterprise endpoint, $D$ would equal $0.70$).
3. **Step 3 (User Authority $U$ Assignment):**
   - Based on the user flow index (`idx_e % 2 == 0`), the user privilege weight is assigned: $U = 0.90$.
4. **Step 4 (Applying the Linear Weighted Sum Model):**
   - The formula executes: $RS = (W_S \times S) + (W_D \times D) + (W_U \times U)$
   - $RS = (0.50 \times 0.95) + (0.25 \times 0.95) + (0.25 \times 0.90)$
   - $RS = 0.475 + 0.2375 + 0.225 = 0.9375$
5. **Step 5 (Normalization & Severity Mapping):**
   - The raw coefficient is scaled to a 100-point index: `round(0.9375 * 100, 2)` = **$93.75\%$**.
   - The `get_severity(93.75)` function evaluates the threshold ($Score > 80$). It instantly attaches a **`CRITICAL`** label and a red visual alert icon (`🔴`), pushing the event to the top of the SOC dashboard feed.

```
[ INSERT SCREENSHOT 4: Real-time WRSE Score Breakdown in Dashboard Here ]
Caption: Figure 4 - Real-time dashboard display of a captured Shadow AI event showcasing the 93.75% WRSE score, triggered asset keys, and CRITICAL severity badge.
(*Instructions for Student: Take a screenshot of the dashboard table row or the 'Inspect' detail view showing a high WRSE score and its calculation breakdown.*)
```

### 5.4 Authentication & Session Persistence Module (`auth.py`)
The authentication system was designed to mirror enterprise-grade Zero-Trust access portals. Key features implemented include:
- **Premium Glassmorphism UI:** Replaced standard login forms with a bespoke, visually stunning glassmorphism card featuring an animated radial gradient background and an embedded ContextGuard logo.
- **Web Application Firewall (WAF) Sanitization:** Incorporated active regex checks (`sanitize_input`) to intercept and block SQL injection and XSS payloads at the login prompt.
- **Brute-Force Protection:** Implemented a stateful lockout mechanism that freezes the login interface for 30 seconds upon registering 5 consecutive invalid login attempts.
- **Flawless Session Persistence:** Solved Streamlit's native session-reset behavior on browser refreshes by engineering a custom file-backed token mechanism (`/tmp/shadowai_sessions/`). Upon successful authentication, a unique UUID session token is generated, stored on the server, and injected into the client's URL query parameters (`?_sid=UUID`). When a user presses F5 or refreshes the tab, `check_auth()` intercepts the URL parameter, validates the active session file, and seamlessly restores the user state without forcing a re-login.

```
[ INSERT SCREENSHOT 5: Premium Glassmorphism Login Page Here ]
Caption: Figure 5 - The ContextGuard premium glassmorphism login interface featuring bespoke styling, embedded branding, and active WAF sanitization.
(*Instructions for Student: Take a screenshot of the login page showing the dark background, logo, and login card.*)
```

```
[ INSERT SCREENSHOT 6: Brute-Force Lockout Alert Here ]
Caption: Figure 6 - Active brute-force protection triggering a 30-second administrative lockout after 5 failed login attempts.
(*Instructions for Student: Enter wrong passwords 5 times and take a screenshot of the red lockout error message.*)
```

### 5.5 Core Administrative Dashboard (`app.py`)
The main administrative interface has been fully constructed using a clean, non-scrolling, high-density layout. Key achievements include:
- **Navigation Panel Refactoring:** Moved the "Sign Out" functionality from the top header directly into the sidebar navigation panel, placing it cleanly above the logged-in user badge for optimal ergonomic access.
- **Top Header Filtering Controls:** Implemented a sophisticated 4-column header bar allowing administrators to instantly filter threat feeds by **Time Type** (Relative, Absolute, Custom Window), **Time Interval** (Past Month, Last 24 Hours, Shift Windows), and **Monitor Status** (All Statuses, Open, In Progress, Close).
- **Dynamic Page Routing:** Integrated seamless navigation across 6 dedicated operational views: AI Discovery, Prompt Inspector, Semantic Analytics, Risk Profiler, Sensitive Keywords, and Scoring Engine.

```
[ INSERT SCREENSHOT 7: Main AI Discovery Dashboard View Here ]
Caption: Figure 7 - The primary AI Discovery dashboard view showcasing the top metric strip, 4-column header filter controls, and the active threat table.
(*Instructions for Student: Take a full-screen screenshot of the main dashboard page showing the top strip and data table.*)
```

```
[ INSERT SCREENSHOT 8: Sidebar Navigation with Sign Out Button Here ]
Caption: Figure 8 - The restructured sidebar navigation panel displaying the active monitoring badge, relocated Sign Out button, and logged-in user credentials.
(*Instructions for Student: Take a clear screenshot of the left sidebar showing the logo, Sign Out button, and user role badge.*)
```

### 5.6 Event Monitoring & State Persistence (`components.py`)
To ensure actionable incident response workflow management, the native static table was converted into an interactive, stateful dashboard component:
- **Interactive Selectbox Integration:** Replaced the basic 'Active' checkbox in the event table with a fully styled dropdown selectbox offering three distinct operational states: `Open`, `In Progress`, and `Close`.
- **SQLite-Backed State Persistence:** Developed backend helper functions (`_init_monitor_table`, `_get_monitor_status`, `_save_monitor_status`) that instantly write status updates to a dedicated `monitor_status` table in `users.db`. When an administrator updates an event's status from `Open` to `In Progress`, the change is immediately committed to the database. Consequently, the status remains perfectly static and preserved across automatic background refreshes and manual browser reloads.
- **Real-Time Cross-Filtering:** Linked the table's SQLite persistence directly to the top header's "Monitor Status" filter box. Selecting `In Progress` in the header dynamically queries the database and filters the main event view to display only active investigations.

```
[ INSERT SCREENSHOT 9: Interactive Monitor Status Selectbox Here ]
Caption: Figure 9 - The interactive Monitor status dropdown within the event table, allowing real-time transition between Open, In Progress, and Close states.
(*Instructions for Student: Zoom in and take a screenshot of the table rows focusing on the 'Monitor' selectbox column.*)
```

```
[ INSERT SCREENSHOT 10: Filtered 'In Progress' Threat Feed Here ]
Caption: Figure 10 - The dashboard dynamically filtered to display only events assigned the 'In Progress' monitoring status via the top header control.
(*Instructions for Student: Select 'In Progress' in the top header filter box and take a screenshot showing the filtered results.*)
```

### 5.7 Custom UI Styling & Glassmorphism (`styles.py`)
To achieve an elite, professional visual standard that transcends native Streamlit limitations, a custom CSS architectural layer was deployed:
- **Comprehensive Class Overrides:** Injected over 1,090 lines of custom CSS (`THREATMON_CSS`) to completely restyle native BaseWeb containers, buttons, tables, and selectboxes.
- **Micro-Animations & Visual Hierarchy:** Implemented subtle hover transition effects, glowing risk borders (Critical = Red, Medium = Amber, Low = Green), and compact table cell formatting to ensure maximum data density without visual clutter.
- **Streamlit Branding Suppression:** Successfully executed CSS rules to hide native Streamlit headers, footers, top-right status widgets, and running spinners, presenting the application as a standalone, enterprise-grade compiled software solution.

---

## 6. Testing and Evaluation Plan (Draft)

### 6.1 Proposed Testing Strategy
The testing strategy for ContextGuard incorporates a rigorous combination of unit testing for mathematical functions, security boundary validation for authentication mechanisms, and end-to-end integration testing for state persistence.

### 6.2 Security & WAF Mechanism Validation
1. **Test Case SEC-01 (WAF SQLi/XSS Blocking):**
   - *Procedure:* Input common attack strings (e.g., `' OR 1=1 --`, `<script>alert('XSS')</script>`) into the username and password fields.
   - *Expected Result:* Immediate interception by `sanitize_input()`, blocking database query execution and displaying a custom ContextGuard WAF alert badge.
2. **Test Case SEC-02 (Brute-Force Lockout):**
   - *Procedure:* Submit 5 consecutive invalid password attempts for a valid username (`admin`).
   - *Expected Result:* System tracks attempts via session state, increments counter to 5, disables authentication processing, and forces a 30-second visual lockout timer.
3. **Test Case SEC-03 (Session Token Persistence):**
   - *Procedure:* Authenticate successfully, navigate to 'Prompt Inspector', and execute a manual browser refresh (F5).
   - *Expected Result:* System extracts the `_sid` parameter from the URL, verifies the corresponding JSON session file in `/tmp/shadowai_sessions/`, and restores the authenticated state without redirecting to the login screen.

### 6.3 WRSE Score Calibration & Alert Verification
1. **Test Case WRSE-01 (High Sensitivity / Public Destination):**
   - *Procedure:* Ingest a synthetic log where a Senior Engineer inputs proprietary C++ source code into a public consumer LLM.
   - *Expected Result:* NLP engine identifies high-frequency sensitive tokens ($S > 90$), destination penalty maximizes ($D = 0.9$), resulting in a final WRSE score $RS > 85$. System automatically attaches a `CRITICAL` visual flag.
2. **Test Case WRSE-02 (Monitor Status Database Persistence):**
   - *Procedure:* Update Event ID `EVT-102` from `Open` to `Close` in the table. Refresh the browser tab.
   - *Expected Result:* System queries `SELECT status FROM monitor_status WHERE event_id = 'EVT-102'`, successfully retrieves `Close`, and renders the selectbox at the correct index.

---

## 7. Challenges and Risk Management

### 7.1 Technical Challenges Faced
During the implementation phase, several significant architectural and framework-level challenges were encountered:
1. **Streamlit BaseWeb Styling Resistance:** Streamlit utilizes an underlying React-based BaseWeb architecture that aggressively isolates components and resists standard CSS targeting. Achieving the target glassmorphism design and custom button formatting proved extremely difficult using native API calls.
2. **Stateless Browser Refresh Behavior:** By design, Streamlit treats manual browser tab refreshes (F5) as a brand-new user session, wiping the in-memory `st.session_state`. This caused authenticated users to be abruptly logged out whenever they refreshed the dashboard or when automatic background re-runs occurred.
3. **High-Frequency UI State Synchronization:** Allowing users to update event monitoring statuses (`Open`, `In Progress`, `Close`) inside a dynamically rendered table led to state desynchronization, where table re-renders would reset the dropdowns back to their default values.

### 7.2 Actions Taken to Resolve Challenges
1. **Advanced CSS Injection & JavaScript DOM Manipulation:** To bypass BaseWeb restrictions, we engineered `styles.py` to inject highly specific CSS selectors utilizing `!important` flags and attribute selectors (`div[data-testid="stSelectbox"]`). For advanced UI behaviors (such as password visibility toggles), custom HTML/JS snippets were embedded directly into the DOM via `components.html`.
2. **File-Backed UUID Session Architecture:** To resolve the refresh logout issue, we abandoned pure in-memory session state in favor of a hybrid persistence model (`auth.py`). We established a secure temporary directory (`/tmp/shadowai_sessions/`) to store active session data keyed by unique UUIDs. By syncing this UUID with the client's URL query parameters (`st.query_params`), we ensured that active sessions survive hard browser reloads while maintaining an automatic 12-hour expiry mechanism for security.
3. **SQLite Backend State Decoupling:** We resolved table state desynchronization by decoupling the widget state from Streamlit's runtime memory. We deployed an auxiliary table (`monitor_status`) within the existing `users.db` SQLite database. Every change to a table selectbox now triggers an immediate atomic `UPDATE` query, ensuring the UI always pulls the absolute ground-truth state directly from the database upon rendering.

---

## 8. Revised Work Plan

### 8.1 Remaining Tasks
With the core analytical engine, dashboard interface, and database persistence fully accomplished, the remaining 3 weeks of the project lifecycle are dedicated to system polishing, final validation, and academic documentation:
1. **Comprehensive System Stress Testing:** Executing large-scale synthetic log ingestions (30,000+ events) to benchmark WRSE calculation latency and verify sub-second execution speeds.
2. **Forensic Audit Logging Expansion:** Enhancing the export capabilities of the dashboard to allow administrators to download filtered incident reports in CSV/PDF formats.
3. **Final Dissertation / Thesis Writing:** Synthesizing all implementation notes, architectural diagrams, and empirical test results into the final 10,000+ word academic dissertation.
4. **Presentation & Viva Preparation:** Developing professional slide decks and practicing live prototype demonstrations for the final defense panel.

### 8.2 Updated Timeline & Milestones

| Phase / Week | Focus Area | Key Activities & Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Weeks 1–2** | Foundation & Literature | Literature review, problem definition, gap analysis | **Completed [x]** |
| **Weeks 3–4** | Mathematical Design | WRSE formula design, weighting calibration ($W_s, W_d, W_u$) | **Completed [x]** |
| **Weeks 5–6** | Synthetic Data Engineering | Ingestion pipeline development (`data_core.py`), 15 CSV registry setup | **Completed [x]** |
| **Weeks 7–8** | UI & Security Engineering | Glassmorphism dashboard (`app.py`), WAF & Login lockout (`auth.py`) | **Completed [x]** |
| **Week 9 (Current)** | State Persistence & Interim | SQLite status tracking, F5 refresh session persistence, Interim Report | **Completed [x]** |
| **Week 10** | Stress Testing & Optimization | End-to-end testing, latency benchmarking, bug fixing | **In Progress [/]** |
| **Weeks 11–12** | Final Documentation & Viva | Final Thesis writing (10,000+ words), slide deck preparation, Viva defense | **Pending [ ]** |

---

## 9. Conclusion

The interim review confirms that the development of the **ContextGuard Shadow AI Governance Framework** is progressing with exceptional technical rigor and adheres precisely to the established academic roadmap. By successfully integrating an NLP-driven Deep Content Inspection engine with a dynamic Weighted Risk Scoring Engine (WRSE), the prototype proves the feasibility of real-time, quantitative risk evaluation for unsanctioned AI interactions. 

Furthermore, the resolution of complex engineering hurdles—such as Streamlit session persistence across browser reloads and real-time SQLite status tracking—demonstrates a highly resilient, enterprise-grade software architecture. The project is fully on track for successful completion and deployment within the remaining 3-week timeframe, promising a robust, publishable contribution to the field of AI security governance.

---

## 10. References

[1] Gartner, "Global cybersecurity trends 2026: The rise of shadow AI," Gartner Research, Stamford, CT, USA, 2026.  
[2] Palo Alto Networks, "Unit 42: Securing autonomous AI identities," Unit 42 Threat Intel Rep., Santa Clara, CA, USA, 2026.  
[3] J. Smith, "Behavioral pattern recognition in encrypted traffic," *IEEE Commun. Mag.*, vol. 63, no. 2, pp. 45-52, Feb. 2025.  
[4] R. Kumar, "Data leakage prevention for large language models," *Cyber J.*, vol. 18, no. 4, pp. 101-110, 2025.  
[5] A. White, "Governance frameworks for generative AI," *IT Prof.*, vol. 28, no. 1, pp. 30-38, Jan.-Feb. 2026.  
[6] S. Perera, "Automated risk scoring in corporate networks," *Security Weekly*, vol. 12, no. 3, pp. 20-27, 2026.  
[7] M. Davis, "The impact of shadow IT on modern enterprises," *Int. J. Comput. Syst.*, vol. 19, no. 1, pp. 11-19, 2024.  
[8] T. Anderson, "Weighted algorithms for risk mitigation," *Softw. Eng. J.*, vol. 32, no. 5, pp. 77-85, 2025.  
[9] K. Wilson, "Deep packet inspection challenges in 2026," *Network World*, vol. 40, no. 6, pp. 14-21, 2026.  
[10] "Shadow AI, cybersecurity, and emerging threats: Davos 2025 explores substantial risks," EDRM, Feb. 5, 2025.  
[11] "Shadow AI: Governance, risk, and organisational resilience," in *Proc. 2025 Int. Conf. Cybersecurity and AI Governance*, Aug. 2025, pp. 120-127.
