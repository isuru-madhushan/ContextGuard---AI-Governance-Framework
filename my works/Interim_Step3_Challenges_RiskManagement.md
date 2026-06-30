# 8. Challenges and Risk Management

This section provides a transparent evaluation of the technical hurdles, time constraints, resource limitations, and data parsing complexities encountered during the development of the **ContextGuard** Shadow AI Governance Framework. It details the precise software engineering actions taken to overcome these obstacles and outlines a comprehensive risk mitigation plan for the remaining phases of the project.

---

## 8.1 Issues Faced & Actions Taken to Resolve Challenges

Developing an enterprise-grade Zero-Trust inspection portal on top of a rapid prototyping framework like Streamlit introduced significant architectural challenges. The following subsections detail the primary obstacles encountered and the technical solutions implemented.

---

### Challenge 1: Streamlit Session State Volatility on Browser Refreshes
- **Issue Faced (Technical & Architectural):** Streamlit operates on a stateless execution model where the entire Python script re-runs from top to bottom upon every user interaction or page reload (F5). During initial prototype testing, this behavior caused active administrative sessions to completely reset whenever the browser was refreshed, instantly logging users out and returning them to the login screen.
- **Action Taken to Resolve:** We engineered a custom server-side session persistence architecture within `auth.py`. Upon successful authentication, the system generates a cryptographically secure UUID session token, stores the session metadata in a temporary server-side directory (`/tmp/shadowai_sessions/`), and dynamically injects the token into the client's browser URL query parameters (`?_sid=UUID`). When an administrator refreshes the tab, `check_auth()` intercepts the URL parameter, executes `validate_session()`, verifies the local session file, and seamlessly restores `st.session_state['authenticated'] = True` without disrupting the user experience.

```
[ INSERT SCREENSHOT 1: Code Segment from auth.py (Lines 115 to 135) ]
Caption: Figure 8.1 - Code implementation of the validate_session function in auth.py (Lines 115–135), managing file-backed session verification via URL query parameters.
(*Instructions for Student: Open Section3_Dashboard/auth.py in VS Code, scroll to lines 115–135 showing validate_session, and take a screenshot.*)
```

---

### Challenge 2: UI State Loss in BaseWeb Table Component & Monitor Status Persistence
- **Issue Faced (Technical & UI Limitations):** To enable SOC administrators to track threat investigations, we integrated an interactive selectbox (`Open`, `In Progress`, `Close`) directly into the event monitoring table. However, because Streamlit dataframes are inherently stateless, any time an administrator updated an event's status, the table would reset to its default state upon the next background telemetry refresh or manual browser reload.
- **Action Taken to Resolve:** We decoupled the table UI state from the frontend dataframe by engineering an SQLite-backed state persistence layer in `components.py`. We initialized a dedicated `monitor_status` table inside `users.db`. Whenever an administrator toggles a selectbox, the helper function `_save_monitor_status()` instantly commits the new status (`EventID`, `Status`) to the database. During table rendering, `_get_monitor_status()` queries the database and dynamically updates `df_all`, ensuring that investigation statuses remain perfectly static and preserved across all reloads.

```
[ INSERT SCREENSHOT 2: Code Segment from components.py (Lines 18 to 44) ]
Caption: Figure 8.2 - Code implementation of the SQLite state persistence functions (_save_monitor_status and _get_monitor_status) in components.py (Lines 18–44).
(*Instructions for Student: Open Section3_Dashboard/components.py in VS Code, scroll to lines 18–44 showing the SQLite helper functions, and take a screenshot.*)
```

---

### Challenge 3: Advanced Custom UI Styling & Glassmorphism over Streamlit BaseWeb
- **Issue Faced (UI Aesthetics & Framework Limitations):** Native Streamlit applications exhibit a basic, standardized visual appearance that fails to convey the premium, dark-themed, glassmorphism aesthetics expected of a modern enterprise Security Operations Center (SOC) dashboard. Streamlit does not natively support deep DOM manipulation or customized CSS styling for individual BaseWeb containers.
- **Action Taken to Resolve:** We bypassed Streamlit's native styling engine by creating a comprehensive custom styling module (`styles.py`). We injected over 1,090 lines of highly specific CSS (`THREATMON_CSS`) utilizing `st.markdown(..., unsafe_allow_html=True)`. This custom stylesheet restyles BaseWeb containers with semi-transparent dark backgrounds (`background: rgba(23, 27, 38, 0.75)`), applies backdrop blur filters (`backdrop-filter: blur(16px)`), adds glowing neon borders for critical risks, implements subtle micro-animations on hover, and suppresses native Streamlit branding elements (headers, footers, and execution spinners).

```
[ INSERT SCREENSHOT 3: Code Segment from styles.py (Lines 15 to 65) ]
Caption: Figure 8.3 - Code snippet of the custom THREATMON_CSS definitions in styles.py (Lines 15–65), injecting custom glassmorphism properties and overriding BaseWeb containers.
(*Instructions for Student: Open Section3_Dashboard/styles.py in VS Code, scroll to lines 15–65 showing the CSS definitions, and take a screenshot.*)
```

---

### Challenge 4: Data Limitations & NLP Parsing (Google Gemini f.req URL Encoding vs OpenAI JSON)
- **Issue Faced (Data Limitations & Interception Complexity):** Extracting pure prompt text from intercepted HTTPS POST requests proved highly complex because external generative AI platforms utilize fundamentally divergent payload architectures. While OpenAI (`api.openai.com`) and Claude (`claude.ai`) transmit clean, structured JSON arrays (`{"messages": [{"content": "..."}]}`), Google Gemini (`gemini.google.com`) encapsulates prompts within complex, deeply nested URL-encoded string structures (`f.req=%5B%22...%22%5D`). Standard string matching failed completely on Gemini payloads due to severe structural noise.
- **Action Taken to Resolve:** We developed the Advanced Double-Plane URL Decoding Engine within `live_mitm_logger.py`. The engine actively inspects the raw payload structure. If it detects `f.req=` or URL entities (`%5B`, `%22`), it routes the payload through a multi-pass `urllib.parse.unquote` routine, strips out the surrounding boundary garbage, and passes a perfectly clean text string to `data_core.py` for NLP evaluation.

---

### Challenge 5: Time & Computational Resources (Master Asset Registry Collision & Memory Overhead)
- **Issue Faced (Time, Resources & Disk I/O Bottlenecks):** To establish Zero-Trust data governance, ContextGuard must scan every intercepted prompt against **15 Master CSV Asset Sheets** (`data Sheets/`) representing Medical Records, Infrastructure Credentials, Financial Data, and IP. During initial testing, repeatedly opening and parsing 15 CSV files from disk for every incoming network packet created severe disk I/O bottlenecks, raising response times to over 4 seconds and causing false-positive mock collisions.
- **Action Taken to Resolve:** We refactored `data_core.py` to eliminate real-time disk I/O. Using `load_master_dataset()`, the framework ingests and indexes all 15 CSV sheets into a highly optimized in-memory dictionary (`idx`) during system startup. Furthermore, we integrated a `seen_records` set and `matched_token_values` tracking inside `find_master_asset_match()`. This algorithmic optimization ensures sub-second evaluation speeds while preventing duplicate collision counting when a single prompt contains multiple related asset parameters.

---

## 8.2 Risk Mitigation Plan

To ensure the long-term viability and successful final delivery of the ContextGuard framework, we have established a proactive risk management matrix. This plan anticipates potential operational, technical, and external risks during the final implementation phase.

| Risk ID | Identified Risk | Potential Impact | Probability | Proposed Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **RM-01** | **External AI API Schema Changes** | **High** | **High** | External platforms (OpenAI, Gemini, Claude) frequently update their internal POST payload structures. We are implementing an abstract parsing interface in `live_mitm_logger.py` with fallback regex pattern matching to ensure continuous prompt extraction even if JSON keypaths change. |
| **RM-02** | **mitmproxy Certificate Pinning Bypasses** | **High** | **Medium** | Enterprise desktop client apps (e.g., native ChatGPT desktop app) may utilize strict SSL certificate pinning, bypassing standard `mitmproxy` inspection. Mitigation involves deploying custom Enterprise Root CAs via Microsoft Intune / Group Policy Objects (GPO) across workstation trust stores. |
| **RM-03** | **Prompt Injection & Obfuscation Attacks** | **Medium** | **Medium** | Malicious insiders may attempt to bypass the NLP engine by obfuscating sensitive tokens (e.g., base64 encoding or inserting special characters into Medical IDs). We are expanding `forensic_normalize()` to execute automated base64 decoding and advanced string normalization prior to asset matching. |
| **RM-04** | **Scalability & Memory Overhead in Large SOCs** | **Medium** | **Low** | Scaling the in-memory master asset dictionary to accommodate millions of corporate records could increase server RAM usage. Mitigation involves migrating the in-memory dictionary to a dedicated Redis caching layer or an in-memory SQLite database instance for enterprise production deployment. |
| **RM-05** | **Strict Project Timeline & Testing Constraints** | **Low** | **Low** | Unforeseen debugging requirements could impact the final submission schedule. We have established a strict modular milestone schedule, finalizing core ingestion and UI engines early to reserve the final 4 weeks exclusively for empirical testing and documentation compilation. |
