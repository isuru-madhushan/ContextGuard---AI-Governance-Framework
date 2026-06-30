# 🛡️ ContextGuard: Shadow AI Governance Framework

**ContextGuard** is an automated risk assessment and governance framework designed to detect, analyze and mitigate insider threats arising from the unauthorized use of Large Language Models (LLMs) in corporate environments (Shadow AI).

By establishing a non-intrusive, context-aware inspection plane, the framework intercepts outbound AI API traffic, decodes complex payload structures and evaluates data sensitivity using Natural Language Processing (NLP). It calculates a dynamic **Weighted Risk Scoring Engine (WRSE)** score and routes real-time alerts to a Zero-Trust Security Operations dashboard.

---

## ✨ Key Features
- **Live Network Interception (`mitmproxy`):** Actively intercepts TLS-encrypted POST requests sent to AI domains (`chatgpt.com`, `gemini.google.com`, `claude.ai`).
- **Advanced Double-Plane URL Decoder:** Automatically parses nested OpenAI JSON arrays and unquotes deeply nested Google Gemini string objects (`f.req=`).
- **In-Memory NLP Asset Indexing:** Cross-references prompt text against 15 Master CSV Corporate Asset sheets (Medical Records, Infrastructure Credentials, IP) in sub-second latency.
- **Weighted Risk Scoring Engine (WRSE):** Computes a unified risk coefficient (0-100) based on Data Sensitivity ($W_S$), Destination Trust ($W_D$), and User Authority ($W_U$).
- **Zero-Trust Administrative Dashboard:** A premium glassmorphism Streamlit UI featuring WAF SQLi/XSS sanitization, brute-force lockout, SQLite state persistence, and file-backed session management.

---

## 🏗️ System Architecture
The framework operates on a decoupled 4-tier pipeline:
1. **Tier 1 - Data Ingestion:** `live_mitm_logger.py` captures and logs network metadata and raw prompts into `wrse_comprehensive_audit.log`.
2. **Tier 2 - NLP Inspection Layer:** `data_core.py` executes `forensic_normalize()` and indexes prompts against the Corporate Asset Vault to identify data leaks.
3. **Tier 3 - WRSE Scoring Module:** Calculates the mathematical risk score and assigns severity classifications (`CRITICAL`, `MEDIUM`, `LOW`).
4. **Tier 4 - Governance Visualization:** `app.py` serves the real-time dashboard for administrators.

---

## 🛠️ Installation Requirements
Ensure you have **Python 3.10+** installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/isuru-madhushan/ContextGuard-AI-Governance-Framework.git
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

*(Note: The framework requires NLTK for tokenization. If prompted during execution, download the 'punkt' package via Python).*

---

## 🚀 How to Run the Framework

To execute the complete prototype, you must run the interception logger and the administrative dashboard simultaneously in two separate terminal windows.

### Terminal 1: Start the Interception Plane
This service listens for outbound AI traffic and writes captured prompts to the central log file.
```bash
cd /ShadowAI_Framework/Section1_DataIngestion
```

```bash
mitmdump -p 8080 --set listen_host=0.0.0.0 -s live_mitm_logger.py
```

### Terminal 2: Start the Zero-Trust Dashboard
Navigate to the dashboard directory and launch the Streamlit server.

```bash
cd /ShadowAI_Framework/Section3_Dashboard
```

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

**Accessing the Portal:**
Once initialized, open your browser and navigate to `http://localhost:8501`.
- **Default Username:** `admin`
- **Default Password:** `adminpass`

---

## 🧪 Testing the Framework
To test the interception capabilities on the host machine:
1. Ensure both the `mitmproxy` logger and the Dashboard are running.
2. Open a browser and navigate to `chatgpt.com`.
3. Paste a highly sensitive asset from the CSV files (e.g., Medical Record: `HL7-517169`) into the ChatGPT prompt and hit send.
4. The terminal will log `[🛡️ INGESTION PLANE CLEANED]`.
5. Check the ContextGuard dashboard to see the real-time alert trigger with a `CRITICAL` severity badge and its mathematical breakdown.

---

**Developed by:** S.H.I. Madhushan (14504)  
**Institution:** KIU University, Sri Lanka (COM4901 Final Year Project)
