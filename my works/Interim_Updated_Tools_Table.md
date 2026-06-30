# 5.3 Tools, Techniques, Technologies Selected and Justification

The operational transition from a theoretical framework into an enterprise-grade Zero-Trust prototype required an expanded technical stack. In addition to the foundational data science libraries, several specialized network interception, database persistence, and cryptographic modules were integrated into the production environment.

---

### Expanded Technical Stack & Library Justification

| Category | Tool / Library | Technical Purpose & Justification |
| :--- | :--- | :--- |
| **Core Engine** | **Python 3.10+** | Primary programming language chosen for its extensive asynchronous networking capabilities, robust standard libraries, and seamless integration with ML/NLP frameworks. |
| **Network Interception** | **mitmproxy (`mitmproxy.http`)** | Core proxy kernel utilized in `live_mitm_logger.py` to establish a Man-in-the-Middle inspection plane on the host machine. It transparently intercepts and exposes outbound TLS-encrypted HTTPS POST flows directed at unmanaged AI endpoints (`chatgpt.com`, `gemini.google.com`). |
| **Payload Decoding** | **`urllib.parse` & `json`** | Foundational modules powering the Advanced Double-Plane URL Decoding Engine. `urllib.parse.unquote` strips percent-encoded entities (`%5B`, `%22`, `f.req=`) from Google Gemini prompts, while `json.loads` extracts deeply nested prompt arrays from OpenAI payloads. |
| **Data Processing & Indexing** | **Pandas & NumPy** | Utilized in `data_core.py` for high-performance in-memory dataset manipulation, statistical aggregation of network metadata, and rapid loading of the 15 Master CSV asset sheets. |
| **NLP & Deep Inspection** | **NLTK & `re` (Regex Engine)** | Serves as the central intelligence engine for the content inspection layer. The `re` module executes multi-pass regex normalization (`forensic_normalize`), while NLTK handles tokenization and TF-IDF weighting for the Sensitivity Score ($S$). |
| **Database Persistence** | **SQLite3 (`sqlite3`)** | Lightweight, serverless relational database engine utilized in `components.py` and `auth.py` (`users.db`). It provides atomic state persistence for the `monitor_status` table, ensuring investigation states (`Open`, `In Progress`, `Close`) remain locked across hard browser reloads. |
| **Zero-Trust Security** | **`uuid` & Server Storage (`/tmp`)** | Powers the bespoke session persistence architecture in `auth.py`. `uuid.uuid4()` generates cryptographically secure session identification tokens (`_sid`) stored in `/tmp/shadowai_sessions/`, preserving administrative sessions across page refreshes (F5). |
| **Dashboarding & UI** | **Streamlit** | Rapid frontend deployment framework providing the administrative Security Operations Center (SOC) interface, real-time threat feed rendering, and visual telemetry charts. |
| **Custom Aesthetics** | **HTML5 & Custom CSS Injection** | Over 1,090 lines of bespoke CSS (`THREATMON_CSS` in `styles.py`) injected via `st.markdown(unsafe_allow_html=True)`. It overrides native BaseWeb containers to implement premium glassmorphism panels, dark backdrops, glowing risk borders, and micro-animations. |
| **IDE & Version Control** | **VS Code & Git** | Integrated development environment and versioning infrastructure utilized for modular scripting, debugging, and maintaining an immutable audit trail of source code changes. |
