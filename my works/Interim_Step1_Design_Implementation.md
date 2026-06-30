# 6. Design and Implementation Progress

This section outlines the concrete technical progress achieved during the mid-implementation stage of the **ContextGuard** Shadow AI Governance Framework. It details the underlying system architecture, the active modules and functions developed, and the visual proof of the working prototype.

---

## 6.1 Architecture / Design Diagrams

The system operates as a transparent inspection layer structured into four decoupled logical tiers. This layered design facilitates asynchronous feature extraction, ensuring that network latency is minimized during real-time risk evaluation.

```
+-----------------------------------------------------------------------+
|                 4. VISUALIZATION & GOVERNANCE LAYER                   |
|       (Streamlit Dashboard, Real-time Alerts, SQLite Persistence)     |
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
|             (live_mitm_logger.py & Synthetic Host Telemetry)          |
+-----------------------------------------------------------------------+
```

```
[ INSERT SCREENSHOT 1: Official Architecture Diagram ]
Caption: Figure 6.1 - The 4-Tier System Architecture of the ContextGuard Shadow AI Governance Framework.
(*Instructions for Student: Insert your official architectural diagram image here, illustrating the data flow from Ingestion to the Streamlit Dashboard.*)
```

### Architectural Tier Breakdown:
1. **Data Ingestion Module:** Captures live workstation telemetry, API logs, and unencrypted prompt payloads via active Man-in-the-Middle (MITM) interception.
2. **Inspection Layer:** Executes parallel heuristic analysis (evaluating Inter-Arrival Time and packet size variance for bot detection) and deep content inspection (matching prompt payloads against the Master Asset Registry).
3. **WRSE Scoring Module:** Processes the extracted vectors through the mathematical engine to compute the unified risk coefficient.
4. **Visualization & Governance Layer:** Presents actionable intelligence, time-series filtering, and administrative override options via the Streamlit dashboard.

---

## 6.2 Implementation Progress (Modules Completed, Functions Developed, Prototypes)

To date, the project has successfully transitioned from conceptual formulation into a fully operational software prototype. The following core modules and functions have been developed and integrated.

---

### Module 1: Host Machine Traffic Interception (`live_mitm_logger.py`)
To capture live interactions between enterprise workstations and external AI platforms, we developed a real-time interception module utilizing `mitmproxy`. This script acts as a transparent inspection layer directly on the host machine, intercepting outbound TLS-encrypted HTTPS traffic before it exits the corporate perimeter.

#### Developed Functions & Mechanics:
- **`request(flow)` - Targeted Domain Filtering:** Inspects the `HTTPFlow` object and matches the destination hostname against a predefined list of prominent generative AI endpoints (`chatgpt.com`, `api.openai.com`, `gemini.google.com`, `claude.ai`, `deepseek.com`, `copilot.microsoft.com`). Only outbound `POST` requests directed at these services are intercepted for deep packet inspection, preserving network bandwidth and employee privacy for standard web browsing.
- **Advanced Double-Plane URL Decoding Engine:** Generative AI platforms employ vastly different payload encoding mechanisms. For instance, Google Gemini frequently encapsulates prompts in complex URL-encoded structures (`f.req=`), whereas OpenAI and Claude utilize structured JSON bodies (`{"messages": [...]}`). `live_mitm_logger.py` implements a robust multi-stage parser:
  - *Stage 1 (URL Entity Decoding):* Detects URL-encoded strings (`%5B`, `%22`, `f.req=`) and applies `urllib.parse.unquote` to strip garbage boundary structures.
  - *Stage 2 (JSON Structure Parsing):* Safely parses JSON bodies to extract the raw text from deeply nested keypaths (e.g., `messages[0].content.parts[0]` or `prompt`).
- **Structured Telemetry Archiving:** The extracted prompt payload is combined with critical connection metadata—including Client IP, Source Port, Destination Domain, Destination IP, HTTP Method, User-Agent, and exact timestamps. This unified telemetry object is dynamically appended to `wrse_comprehensive_audit.log` in structured JSON format.

```
[ INSERT SCREENSHOT 2: Code Segment from live_mitm_logger.py (Lines 14 to 48) ]
Caption: Figure 6.2 - Code implementation of the request interception and Advanced Double-Plane URL Decoding Engine in live_mitm_logger.py (Lines 14–48).
(*Instructions for Student: Open Section1_DataIngestion/live_mitm_logger.py in VS Code, scroll to lines 14–48 showing the request function and decoding logic, and take a clear screenshot.*)
```

```
[ INSERT SCREENSHOT 3: JSON Log Structure from wrse_comprehensive_audit.log ]
Caption: Figure 6.3 - The structured JSON log format within wrse_comprehensive_audit.log containing connection metadata, source/dest nodes, and the extracted raw prompt.
(*Instructions for Student: Open Section1_DataIngestion/wrse_comprehensive_audit.log in VS Code, highlight a clean JSON log entry, and take a screenshot.*)
```

---

### Module 2: Payload Extraction, Normalization & Master Asset Indexing (`data_core.py`)
Once the raw logs are written to disk, the central analytical engine (`data_core.py`) executes a highly sophisticated pre-processing and indexing routine to prepare the unstructured prompts for mathematical risk evaluation.

#### Developed Functions & Mechanics:
- **`forensic_normalize(text)`:** Unstructured prompts frequently contain escape characters, quotes, and nested array brackets that disrupt standard NLP string matching. This function applies a multi-pass regex filter to extract pure text strings (`r'"([a-zA-Z0-9\s\.\,\!\?\:\-\_\/\@\#\$\%\^\&\*\(\)\+]{6,})"'`), strip out structural noise (`\\"`, `"`, `[`, `]`), and convert all characters to lowercase while preserving critical punctuation (`[^\w\s\.]`).
- **`load_master_dataset()` - Master 15-Sheet CSV Indexing:** To enable context-aware inspection, the framework ingests **15 Master CSV Data Sheets** located in `data Sheets/`. These sheets represent organizational assets across various tiers (Medical Records/PHI, Infrastructure Core Assets, Intellectual Property, Financial Data, HR Records). To achieve sub-second matching speeds without disk I/O bottlenecks, this function builds a highly optimized in-memory dictionary index (`idx`), categorizing assets by `record_ids` (`IAM-670469`, `HL7-517169`), `patient_ids` (`TM-XXXX-XXXX`), and high-specificity `tokens` (SAML Token Hashes, API Key Hashes, DB Connection Strings).
- **`find_master_asset_match(prompt_text, asset_index)`:** Scans the text for explicit Record/Patient IDs using regex (`r'[A-Z0-9]{2,5}-\d{4,8}'`) and cross-references them against the token index. It utilizes a `seen_records` set and `matched_token_values` tracking to ensure that if a prompt contains both an Asset ID and its corresponding Database String, it is correctly counted as a single exposed asset rather than creating artificial mock collisions.

```
[ INSERT SCREENSHOT 4: Code Segment from data_core.py (Lines 232 to 272) ]
Caption: Figure 6.4 - Implementation of the find_master_asset_match function in data_core.py (Lines 232–272), showcasing token matching and collision defense logic.
(*Instructions for Student: Open Section3_Dashboard/data_core.py in VS Code, scroll to lines 232–272 showing the find_master_asset_match function, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 5: Master CSV Asset Registry Indexing in File Explorer ]
Caption: Figure 6.5 - The 15 Master CSV data sheets located in the 'data Sheets' directory, containing baseline weights and high-specificity tokens.
(*Instructions for Student: Take a screenshot of the VS Code file explorer showing the list of T1_xxx.csv, T2_xxx.csv files inside the 'data Sheets' folder.*)
```

---

### Module 3: Real-Time WRSE Risk Calculation & Severity Mapping (`data_core.py`)
The ultimate technical objective of ContextGuard is translating the extracted metadata and asset matches into a standardized, actionable Risk Score ($RS$). This is handled by `calculate_wrse()`.

#### Developed Functions & Mechanics:
- **`calculate_wrse(prompt_text, dest_trust_w, user_auth_w, asset_matches)`:** Accepts the extracted prompt, destination penalty, user privilege weight, and matched asset records. It applies pre-calibrated baseline constants: **$W_S = 0.50$ (Sensitivity), $W_D = 0.25$ (Destination Trust), and $W_U = 0.25$ (User Authority)**.

$$RS = (W_s \times S) + (W_d \times D) + (W_u \times U)$$

- **`get_severity(score)`:** Evaluates the normalized 0–100 score against strict administrative thresholds: $Score > 80 \rightarrow \text{CRITICAL } (🔴)$, $Score \ge 55 \rightarrow \text{MEDIUM } (🟡)$, and $Score < 55 \rightarrow \text{LOW } (🟢)$.

#### Detailed Numerical Walkthrough of an Active Threat:
Consider a real-world scenario processed by the prototype: A software engineer (`idx_e = 0`) copies an internal HL7 healthcare protocol header (`HL7-517169`) and pastes it into `chatgpt.com` to request a code refactor.

1. **Step 1 (Sensitivity Score $S$ Calculation):**
   - The NLP engine matches `HL7-517169` against the Master Asset Registry. The CSV definition establishes a baseline Asset Weight $W_i = 0.95$ (Tier 1 - Medical Records/PHI).
   - $S = \min(\sum W_i, 1.0) = \min(0.95, 1.0) = 0.95$.
2. **Step 2 (Destination Trust $D$ Assignment):**
   - `process_events()` inspects `dest_domain`. Because `chatgpt.com` matches the unmanaged public LLM list (`["gemini", "chatgpt", "claude", "openai"]`), the destination penalty maximizes: $D = 0.95$.
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
[ INSERT SCREENSHOT 6: Code Segment from data_core.py (Lines 88 to 117) ]
Caption: Figure 6.6 - Implementation of the calculate_wrse function in data_core.py (Lines 88–117), showing the linear weighted sum model execution.
(*Instructions for Student: Open Section3_Dashboard/data_core.py in VS Code, scroll to lines 88–117 showing calculate_wrse, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 7: Real-time WRSE Score Breakdown in Dashboard UI ]
Caption: Figure 6.7 - Real-time dashboard display of a captured Shadow AI event showcasing the 93.75% WRSE score, triggered asset keys, and CRITICAL severity badge.
(*Instructions for Student: Take a screenshot of the dashboard table row or the 'Inspect' detail view showing a high WRSE score and its calculation breakdown.*)
```

---

### Module 4: Secure Authentication & Session Persistence (`auth.py`)
The authentication system was designed to mirror enterprise-grade Zero-Trust access portals.

#### Developed Functions & Mechanics:
- **`sanitize_input(val)` - Web Application Firewall (WAF) Sanitization:** Incorporated active regex checks to intercept and block SQL injection (`' OR 1=1 --`) and XSS (`<script>`) payloads at the login prompt.
- **Brute-Force Lockout Defense:** Implemented a stateful lockout mechanism that freezes the login interface for 30 seconds upon registering 5 consecutive invalid login attempts (`st.session_state['login_attempts'] >= 5`).
- **`create_session`, `validate_session`, `check_auth` - File-Backed Session Persistence:** Solved Streamlit's native session-reset behavior on browser refreshes by engineering a custom file-backed token mechanism (`/tmp/shadowai_sessions/`). Upon successful authentication, a unique UUID session token is generated, stored on the server, and injected into the client's URL query parameters (`?_sid=UUID`). When a user presses F5 or refreshes the tab, `check_auth()` intercepts the URL parameter, validates the active session file, and seamlessly restores the user state without forcing a re-login.

```
[ INSERT SCREENSHOT 8: Code Segment from auth.py (Lines 466 to 485) ]
Caption: Figure 6.8 - Code implementation of persistent session token creation and URL query parameter storage upon successful authentication in auth.py (Lines 466–485).
(*Instructions for Student: Open Section3_Dashboard/auth.py in VS Code, scroll to lines 466–485 showing the 'if success:' block and create_session call, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 9: Premium Glassmorphism Login Page UI ]
Caption: Figure 6.9 - The ContextGuard premium glassmorphism login interface featuring bespoke styling, embedded branding, and active WAF sanitization.
(*Instructions for Student: Take a screenshot of the login page showing the dark background, logo, and login card.*)
```

```
[ INSERT SCREENSHOT 10: Brute-Force Lockout Alert UI ]
Caption: Figure 6.10 - Active brute-force protection triggering a 30-second administrative lockout after 5 failed login attempts.
(*Instructions for Student: Enter wrong passwords 5 times and take a screenshot of the red lockout error message.*)
```

---

### Module 5: Stateful UI & Event Monitoring (`app.py`, `components.py`, `styles.py`)
The main administrative interface has been fully constructed using a clean, non-scrolling, high-density layout.

#### Developed Functions & Mechanics:
- **`app.py` - Top Header Filtering Controls:** Implemented a sophisticated 4-column header bar allowing administrators to instantly filter threat feeds by **Time Type**, **Time Interval**, and **Monitor Status** (`All Statuses`, `Open`, `In Progress`, `Close`).
- **`components.py` - SQLite-Backed State Persistence:** Developed backend helper functions (`_init_monitor_table`, `_get_monitor_status`, `_save_monitor_status`) that instantly write status updates from the table's interactive selectbox to a dedicated `monitor_status` table in `users.db`. When an administrator updates an event's status from `Open` to `In Progress`, the change is immediately committed to the database. Consequently, the status remains perfectly static and preserved across automatic background refreshes and manual browser reloads.
- **`styles.py` - Custom UI Styling & Glassmorphism:** Injected over 1,090 lines of custom CSS (`THREATMON_CSS`) to completely restyle native BaseWeb containers, implement micro-animations, add glowing risk borders, and suppress native Streamlit branding (headers, footers, running spinners).

```
[ INSERT SCREENSHOT 11: Code Segment from components.py (Lines 204 to 215) ]
Caption: Figure 6.11 - Code implementation of the interactive Monitor status selectbox inside the event table rendering logic in components.py (Lines 204–215).
(*Instructions for Student: Open Section3_Dashboard/components.py in VS Code, scroll to lines 204–215 showing the selectbox configuration, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 12: Main AI Discovery Dashboard UI with Top Header Filters ]
Caption: Figure 6.12 - The primary AI Discovery dashboard view showcasing the top metric strip, 4-column header filter controls, and the active threat table.
(*Instructions for Student: Take a full-screen screenshot of the main dashboard page showing the top strip, filter boxes, and data table.*)
```

```
[ INSERT SCREENSHOT 13: Sidebar Navigation UI with Relocated Sign Out Button ]
Caption: Figure 6.13 - The restructured sidebar navigation panel displaying the active monitoring badge, relocated Sign Out button, and logged-in user credentials.
(*Instructions for Student: Take a clear screenshot of the left sidebar showing the logo, Sign Out button, and user role badge.*)
```

```
[ INSERT SCREENSHOT 14: Filtered 'In Progress' Threat Feed UI ]
Caption: Figure 6.14 - The dashboard dynamically filtered to display only events assigned the 'In Progress' monitoring status via the top header control.
(*Instructions for Student: Select 'In Progress' in the top header filter box and take a screenshot showing the filtered results.*)
```
