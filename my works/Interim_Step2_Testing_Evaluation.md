# 7. Testing / Evaluation Plan (Draft)

This section outlines the comprehensive testing strategy and empirical validation plan for the **ContextGuard** Shadow AI Governance Framework. It provides a detailed account of the live host machine AI exfiltration experiments, mathematical calibration tests, and security boundary validations performed on the working prototype.

---

## 7.1 Proposed Testing Strategy

The testing strategy for ContextGuard follows a rigorous, multi-tiered verification model designed to evaluate both the underlying data engineering pipeline and the frontend administrative governance controls.

```
+-----------------------------------------------------------------------+
|                   TIER 4: UI & SECURITY VALIDATION                    |
|      (WAF Sanitization, Brute-Force Lockout, Session Persistence)     |
+-----------------------------------------------------------------------+
                                    ^
+-----------------------------------------------------------------------+
|                 TIER 3: WRSE MATHEMATICAL CALIBRATION                 |
|             (Linear Weighted Sum Verification, Threshold Alerts)      |
+-----------------------------------------------------------------------+
                                    ^
+-----------------------------------------------------------------------+
|                 TIER 2: NLP & MASTER ASSET INDEXING                   |
|          (15 CSV Matching, Substring Token Collision Defense)         |
+-----------------------------------------------------------------------+
                                    ^
+-----------------------------------------------------------------------+
|                TIER 1: LIVE HOST MACHINE INTERCEPTION                 |
|              (mitmproxy Active Interception, WAF Logging)             |
+-----------------------------------------------------------------------+
```

### Verification Tiers:
1. **Tier 1 - Live Host Machine Interception:** Verifying the Man-in-the-Middle (`mitmproxy`) logger's ability to intercept outbound TLS-encrypted POST requests to prominent AI domains (`chatgpt.com`, `gemini.google.com`) directly from the host machine.
2. **Tier 2 - NLP & Master Asset Indexing:** Validating `data_core.py`'s ability to parse prompt payloads, clean escape characters, and accurately match high-specificity tokens against the 15 Master CSV data sheets without triggering false positive collisions.
3. **Tier 3 - WRSE Mathematical Calibration:** Verifying that the Weighted Risk Scoring Engine correctly integrates Data Sensitivity ($W_s$), Destination Trust ($W_d$), and User Authority ($W_u$) to generate normalized scores (0–100) and trigger appropriate severity badges (`CRITICAL`, `MEDIUM`, `LOW`).
4. **Tier 4 - UI & Security Validation:** Executing boundary tests on `auth.py` and `app.py` to prove the operational resilience of WAF input sanitization, 5-attempt brute-force lockout mechanisms, file-backed session persistence, and SQLite table status tracking.

---

## 7.2 Planned Experiments or Performance Measures (Active Host Machine AI Experiments)

To establish empirical proof of ContextGuard's threat detection capabilities, we conducted live exfiltration experiments on the host machine. These tests simulated real-world insider threats where employees copy sensitive data strings from the Master CSV asset sheets and paste them into public generative AI platforms.

---

### Experiment 1: Active Host Machine Exfiltration (Tier 1 PHI Asset Leak)
- **Objective:** Verify that pasting a highly sensitive Medical Record ID (`HL7-517169`) from `T1_Medical_Records.csv` into `chatgpt.com` on the host machine is successfully intercepted by `live_mitm_logger.py`, accurately scored by the WRSE engine, and displayed on the dashboard.
- **Experimental Execution:** 
  1. An engineering workstation session (`idx_e = 0`) opens `chatgpt.com` in a local host browser.
  2. The user copies an exact HL7 healthcare protocol header (`HL7-517169`) from the Master Asset Registry and pastes it into the ChatGPT prompt: *"Refactor this HL7 header for our cloud migration: HL7-517169"*.
  3. The prompt is submitted via an HTTPS POST request.
- **Empirical Observations & Results:**
  - **Interception:** `live_mitm_logger.py` intercepts the `HTTPFlow`, identifies the destination domain (`chatgpt.com`), parses the underlying JSON messages array, extracts the exact text, and commits the entry to `wrse_comprehensive_audit.log`.
  - **Matching & Scoring:** `data_core.py` ingests the log, normalizes the text, and matches `HL7-517169` against the in-memory CSV dictionary. It establishes a baseline Asset Weight $W_i = 0.95$ (Tier 1 - Medical Records/PHI).
  - **Mathematical Execution:** Applying $W_S = 0.50, W_D = 0.25, W_U = 0.25$, the engine evaluates the public destination penalty ($D = 0.95$) and user authority weight ($U = 0.90$).
  
$$RS = (0.50 \times 0.95) + (0.25 \times 0.95) + (0.25 \times 0.90) = 0.9375 \rightarrow 93.75\%$$

  - **Actionable Alerting:** Because the score exceeds the critical threshold ($Score > 80$), the dashboard instantly attaches a **`CRITICAL`** severity label and a red visual alert icon (`🔴`).

```
[ INSERT SCREENSHOT 1: Terminal Active Capture of Host Machine AI POST Request ]
Caption: Figure 7.1 - Terminal capture of live_mitm_logger.py intercepting the live ChatGPT HTTPS POST request on the host machine and outputting '[🛡️ INGESTION PLANE CLEANED]'.
(*Instructions for Student: Run mitmproxy with live_mitm_logger.py, send a prompt to ChatGPT on your host machine, and take a screenshot of the terminal capture.*)
```

```
[ INSERT SCREENSHOT 2: Dashboard UI Showing Captured HL7-517169 Event ]
Caption: Figure 7.2 - Real-time dashboard display of the captured HL7-517169 event showcasing the 93.75% WRSE score, triggered asset keys, and CRITICAL severity badge.
(*Instructions for Student: Take a screenshot of the dashboard table row or the 'Inspect' detail view showing the captured HL7-517169 event and its 93.75% score.*)
```

---

### Experiment 2: High-Specificity Token Exfiltration (Tier 2 Infrastructure Asset Leak)
- **Objective:** Verify that pasting a Database Connection String or API Key Hash from `T2_Infrastructure_Assets.csv` into Google Gemini (`gemini.google.com`) is correctly decoded by the Advanced Double-Plane URL Engine and matched via substring token indexing.
- **Experimental Execution:**
  1. A user session opens `gemini.google.com` on the host machine.
  2. The user pastes an active Database Connection String (`mongodb+srv://admin:prodSecret99@cluster0.corp.internal`) from `T2_Database_Credentials.csv` into the Gemini prompt.
  3. The prompt is submitted via an HTTPS POST request.
- **Empirical Observations & Results:**
  - **URL Entity Decoding:** Google Gemini encapsulates prompt payloads in complex URL-encoded structures (`f.req=`). `live_mitm_logger.py` detects `f.req=`, executes `urllib.parse.unquote`, strips the garbage boundary structures, and successfully isolates the raw connection string.
  - **Token Substring Matching:** `data_core.py` bypasses standard regex ID lookups and scans the prompt against the `idx["tokens"]` dictionary. It successfully isolates the DB string, matches the exact CSV record, and prevents mock collisions using `matched_token_values` tracking.
  - **Mathematical Execution:** The engine identifies a Tier 2 Infrastructure Asset ($W_i = 0.90$), public destination penalty ($D = 0.95$), and user weight ($U = 0.65$).
  
$$RS = (0.50 \times 0.90) + (0.25 \times 0.95) + (0.25 \times 0.65) = 0.45 + 0.2375 + 0.1625 = 0.85 \rightarrow 85.00\%$$

  - **Actionable Alerting:** The dashboard instantly flags the event as **`CRITICAL`** (`🔴`) and lists `DB CONNECTION STRING` under Triggered Keys.

```
[ INSERT SCREENSHOT 3: wrse_comprehensive_audit.log Showing Decoded Gemini Payload ]
Caption: Figure 7.3 - JSON log entry within wrse_comprehensive_audit.log showing the successfully decoded Google Gemini f.req payload containing the database connection string.
(*Instructions for Student: Open wrse_comprehensive_audit.log in VS Code, highlight the decoded Gemini log entry, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 4: Dashboard UI Showing Captured Database Connection String Event ]
Caption: Figure 7.4 - Real-time dashboard display of the captured Database Connection String event showcasing the 85.00% WRSE score and Infrastructure Core Assets tier.
(*Instructions for Student: Take a screenshot of the dashboard showing the captured Database Connection String event and its 85.00% score.*)
```

---

### Experiment 3: Heuristic Bot vs. Human Traffic Signature Test
- **Objective:** Verify that short automated polling strings (`trace=`, `PCck7e`, `aPya6c`) are correctly tagged as `🤖 Automated Bot` while natural language prompts are tagged as `🧑‍💻 Human Session`.
- **Experimental Execution:** Synthetic ingestion of raw background telemetry logs containing automated trace headers mixed with genuine employee AI queries.
- **Empirical Observations & Results:**
  - `process_events()` evaluates packet characteristics (`len < 25`, `trace=`).
  - The dashboard successfully categorizes automated background pings with a robot icon (`🤖 Automated Bot`) and genuine employee prompts with a human icon (`🧑‍💻 Human Session`), allowing SOC teams to filter out automated noise.

```
[ INSERT SCREENSHOT 5: Dashboard UI Highlighting Bot vs Human Identity Classification ]
Caption: Figure 7.5 - The AI Discovery dashboard view highlighting the clear visual separation between Automated Bot (🤖) and Human Session (🧑‍💻) traffic identities.
(*Instructions for Student: Take a screenshot of the dashboard table focusing on the 'Identity' column showing both Bot and Human icons.*)
```

---

## 7.3 Evaluation Metrics & Security Validation Plan

To prove the operational resilience of ContextGuard's administrative interface, we executed rigorous security boundary validation tests on the working prototype.

---

### Security Validation 1: Web Application Firewall (WAF) SQLi & XSS Defense
- **Objective:** Validate `auth.py`'s ability to intercept and sanitize malicious input strings at the login portal, preventing database injection and cross-site scripting.
- **Test Procedure:** Input known attack payloads (`' OR 1=1 --`, `<script>alert('XSS')</script>`) into the username and password fields and attempt authentication.
- **Empirical Results:** The `sanitize_input(val)` regex engine intercepts the strings, strips out illegal characters (`';--<script>`), halts database execution, and displays a custom ContextGuard WAF alert badge on the login screen.

```
[ INSERT SCREENSHOT 6: Code Segment from auth.py (Lines 35 to 52) ]
Caption: Figure 7.6 - Code implementation of the sanitize_input WAF function in auth.py (Lines 35–52), utilizing regex patterns to block SQLi and XSS payloads.
(*Instructions for Student: Open Section3_Dashboard/auth.py in VS Code, scroll to lines 35–52 showing sanitize_input, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 7: Login UI Displaying ContextGuard WAF Alert Badge ]
Caption: Figure 7.7 - The ContextGuard login interface successfully intercepting an SQL injection attempt and displaying a custom WAF security alert badge.
(*Instructions for Student: Enter an SQLi string like ' OR 1=1 -- in the login box and take a screenshot of the resulting WAF security warning.*)
```

---

### Security Validation 2: Brute-Force Lockout Engine
- **Objective:** Verify that `auth.py` actively defends against automated credential stuffing by locking the login interface after 5 consecutive failed authentication attempts.
- **Test Procedure:** Submit 5 consecutive invalid passwords for a valid username (`admin`).
- **Empirical Results:** `st.session_state['login_attempts']` tracks the failures, increments the counter to 5, disables the authentication button, and forces a stateful 30-second visual lockout timer (`time.sleep` / UI freeze).

```
[ INSERT SCREENSHOT 8: Login UI Displaying 30-Second Security Lockout ]
Caption: Figure 7.8 - Active brute-force protection triggering a 30-second administrative lockout after 5 failed login attempts.
(*Instructions for Student: Enter wrong passwords 5 times and take a screenshot of the red lockout error message.*)
```

---

### Security Validation 3: Session Token Persistence across Browser Refreshes
- **Objective:** Prove that the custom file-backed UUID session token architecture successfully preserves active user sessions across manual browser reloads (F5), solving Streamlit's native session-reset limitation.
- **Test Procedure:** Authenticate successfully into the dashboard, navigate to the 'Prompt Inspector' view, and press F5 to execute a hard browser reload.
- **Empirical Results:** Upon reload, `check_auth()` extracts the unique `_sid` query parameter from `st.query_params`, locates the corresponding JSON session file in `/tmp/shadowai_sessions/`, validates the timestamp, and seamlessly restores `st.session_state['authenticated'] = True` without kicking the user back to the login screen.

```
[ INSERT SCREENSHOT 9: Code Segment from auth.py (Lines 110 to 145) ]
Caption: Figure 7.9 - Code implementation of the validate_session function in auth.py (Lines 110–145), verifying server-side JSON session files via URL query parameters.
(*Instructions for Student: Open Section3_Dashboard/auth.py in VS Code, scroll to lines 110–145 showing validate_session, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 10: Browser URL Showing ?_sid=UUID Parameter ]
Caption: Figure 7.10 - The active browser address bar displaying the ?_sid=UUID query parameter utilized to maintain session persistence across page refreshes.
(*Instructions for Student: Take a screenshot of your browser's top address bar showing the full URL with the ?_sid=... parameter.*)
```

---

### Security Validation 4: SQLite Monitor Status Persistence
- **Objective:** Verify that updating an event's monitoring status (`Open`, `In Progress`, `Close`) inside the dashboard commits the change to `users.db` and preserves the state across hard browser reloads.
- **Test Procedure:** Select `In Progress` from the interactive dropdown for Event ID `EVT-102`. Perform a hard browser reload (F5). Select `In Progress` in the top header filter box.
- **Empirical Results:** `_save_monitor_status()` executes an atomic `UPDATE` query on the `monitor_status` table in `users.db`. Upon reload, `_get_monitor_status()` queries the database, retrieves `In Progress`, and successfully renders the table with the preserved state and active filtering intact.

```
[ INSERT SCREENSHOT 11: Code Segment from components.py (Lines 15 to 45) ]
Caption: Figure 7.11 - Code implementation of the _save_monitor_status and _get_monitor_status helper functions in components.py (Lines 15–45), managing SQLite state persistence.
(*Instructions for Student: Open Section3_Dashboard/components.py in VS Code, scroll to lines 15–45 showing the SQLite helper functions, and take a screenshot.*)
```

```
[ INSERT SCREENSHOT 12: Filtered 'In Progress' Threat Feed Preserved after Hard Reload ]
Caption: Figure 7.12 - The dashboard view successfully preserving the 'In Progress' monitoring status and active header filtering after a hard browser reload (F5).
(*Instructions for Student: Set an event to 'In Progress', select 'In Progress' in the top filter box, press F5 to reload, and take a screenshot showing the preserved state.*)
```
