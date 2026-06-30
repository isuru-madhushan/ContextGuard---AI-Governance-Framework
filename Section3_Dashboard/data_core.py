import streamlit as st
import pandas as pd
import json
import os
import re
import urllib.parse
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# 🧠 WRSE ENGINE CORE & MASTER 15-SHEET CSV MULTI-ASSET INDEXER
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_KEYWORDS = {
    "production server":  (0.90, "Infrastructure Core Assets"),
    "domain controller":  (0.95, "Infrastructure Core Assets"),
    "database string":    (0.90, "Infrastructure Core Assets"),
    "active directory":   (0.90, "Infrastructure Core Assets"),
    "source code":        (0.85, "Corporate Intellectual Property"),
    "api key":            (0.90, "Corporate Intellectual Property"),
    "proprietary logic":  (0.85, "Corporate Intellectual Property"),
    "hl7 protocol":       (0.85, "Medical Records (PHI)"),
    "patient records":    (0.95, "Medical Records (PHI)"),
    "prescription data":  (0.90, "Medical Records (PHI)"),
}

ASSET_TIERS = [
    "Medical Records (PHI)",
    "Infrastructure Core Assets",
    "Corporate Intellectual Property",
    "Financial Data",
    "HR / Employee Records",
    "Research & Development",
    "Legal & Compliance",
    "Customer PII",
]

W_S, W_D, W_U = 0.50, 0.25, 0.25

# ── FILE PATHS ────────────────────────────────────────────────────────────────
LOG_FILE           = "/home/izu/ShadowAI_Framework/Section1_DataIngestion/wrse_comprehensive_audit.log"
DATA_SHEETS_DIR    = "/home/izu/ShadowAI_Framework/data Sheets"
CUSTOM_ASSETS_FILE = "/home/izu/ShadowAI_Framework/Section3_Dashboard/custom_assets.json"

UNIQUE_ID_COLS = {
    "PATIENT ID", "INSURANCE ID", "POLICY NUMBER", "MEDICARE ID", "INSURANCE CLAIM", "BILLING STATEMENT",
    "SAML TOKEN HASH", "API KEY HASH", "API SECRET REF", "JWT SECRET ID", "DB CONNECTION STRING", 
    "IP ADDRESS", "GIT REPOSITORY", "CONTRACT ID", "HL7 MESSAGE HEADER", "SUBNET", "PRICING SHEET REF", 
    "DOCUMENT TAG", "AD FOREST", "KERBEROS REALM"
}


# ── CUSTOM ASSET MANAGER ──────────────────────────────────────────────────────
def load_custom_assets():
    if os.path.exists(CUSTOM_ASSETS_FILE):
        try:
            with open(CUSTOM_ASSETS_FILE, "r") as f:
                return json.load(f).get("assets", [])
        except Exception:
            return []
    return []


def save_custom_assets(assets_list):
    with open(CUSTOM_ASSETS_FILE, "w") as f:
        json.dump({"assets": assets_list}, f, indent=2)


def get_keywords_db():
    db = dict(DEFAULT_KEYWORDS)
    for a in load_custom_assets():
        db[a["keyword"].lower()] = (float(a["weight"]), a["tier"])
    return db


# ── WRSE CORE FUNCTIONS ───────────────────────────────────────────────────────
def forensic_normalize(text):
    if "%5B" in text or "%22" in text:
        text = urllib.parse.unquote(text)
    strings = re.findall(r'"([a-zA-Z0-9\s\.\,\!\?\:\-\_\/\@\#\$\%\^\&\*\(\)\+]{6,})"', text)
    if strings:
        valid = [s for s in strings if s not in ["en-US","N/A"] and not s.startswith(("c_","r_"))]
        text = max(valid, key=len) if valid else strings[0]
    text = text.replace('\\"','').replace('"','').replace('[','').replace(']','').strip()
    clean = re.sub(r'[^\w\s\.]', ' ', text.lower())
    return clean, text


def calculate_wrse(prompt_text, dest_trust_w, user_auth_w, asset_matches=None):
    clean_text, normalized_str = forensic_normalize(prompt_text)
    detected_keywords = []
    detected_tiers = set()
    KEYWORDS_DB = get_keywords_db()

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


def get_severity(score):
    if score > 80:    return "CRITICAL", "🔴"
    elif score >= 55: return "MEDIUM",   "🟡"
    else:             return "LOW",      "🟢"


def score_bar_html(score):
    color = "#FF2D5B" if score > 80 else ("#F59E0B" if score >= 55 else "#10B981")
    return f'<div class="score-bar-wrap"><div class="score-bar" style="width:{min(score,100)}%;background:{color};"></div></div>'


# ── MASTER 15-SHEET CSV ASSET DATASET LOADING & MATCHING ──────────────────────
@st.cache_data(show_spinner=False)
def load_master_dataset():
    if not os.path.exists(DATA_SHEETS_DIR):
        return {}, {}
    
    all_sheets = {}
    idx = {
        "record_ids": {},
        "patient_ids": {},
        "tokens": {},
    }

    # Load all CSV files in the data Sheets directory
    for fname in sorted(os.listdir(DATA_SHEETS_DIR)):
        if not fname.endswith(".csv"):
            continue
        sheet_name = fname.replace(".csv", "")
        fpath = os.path.join(DATA_SHEETS_DIR, fname)
        try:
            df = pd.read_csv(fpath)
            all_sheets[sheet_name] = df
            
            for _, row in df.iterrows():
                # Extract original dynamic attributes matching the exact tier sheet columns
                original_attrs = {str(k): str(v) for k, v in row.items() if pd.notna(v) and str(v).strip() != ""}
                
                # Determine fallback display values for dashboard columns
                entity_name = ""
                for name_col in ["PATIENT NAME", "USERNAME", "SERVER NAME", "DB TYPE", "MODULE NAME", "PROJECT NAME", "NODE NAME", "TOPOLOGY ID", "PERIMETER ID", "VENDOR NAME", "ALGORITHM NAME", "PROTOCOL ID"]:
                    if name_col in original_attrs:
                        entity_name = original_attrs[name_col]
                        break
                if not entity_name:
                    entity_name = row.get("RECORD ID", "Asset Match")

                sec_id = ""
                for sec_col in ["PATIENT ID", "IP ADDRESS", "GIT REPOSITORY", "AD FOREST", "DB CONNECTION STRING", "SUBNET", "API KEY HASH", "CONTRACT ID", "HL7 MESSAGE HEADER"]:
                    if sec_col in original_attrs:
                        sec_id = original_attrs[sec_col]
                        break

                date_val = ""
                for dt_col in ["DATE OF BIRTH", "LAST LOGIN", "LAST BACKUP", "LAST COMMIT DATE", "CLAIM DATE", "EXECUTION DATE", "EXPIRATION DATE"]:
                    if dt_col in original_attrs:
                        date_val = str(original_attrs[dt_col])
                        break

                details_val = ""
                for d_col in ["BLOOD TYPE", "IAM ROLE", "OS VERSION", "PROGRAMMING LANGUAGE", "DB ENGINE", "DEVICE TYPE", "PROTOCOL TYPE", "STATUS", "ACCOUNT STATUS"]:
                    if d_col in original_attrs:
                        details_val = str(original_attrs[d_col])
                        break

                loc_val = ""
                for l_col in ["NATIONALITY", "DEPARTMENT", "LOCATION", "CLOUD PROVIDER", "REGION", "FACILITY", "INSURANCE PROVIDER"]:
                    if l_col in original_attrs:
                        loc_val = str(original_attrs[l_col])
                        break

                tier_val = row.get("DATA TIER", f"Tier {'1' if sheet_name.startswith('T1') else ('2' if sheet_name.startswith('T2') else '3')} - {sheet_name[3:]}")
                weight_val = float(row.get("ASSET WEIGHT", 0.95 if sheet_name.startswith("T1") else (0.90 if sheet_name.startswith("T2") else 0.85)))
                sens_val = row.get("SENSITIVITY LEVEL", "CRITICAL" if sheet_name.startswith("T1") else "HIGH")

                record = {
                    "SHEET_NAME":          sheet_name,
                    "RECORD ID":           row.get("RECORD ID", ""),
                    "PATIENT NAME":        entity_name,
                    "PATIENT ID":          sec_id,
                    "SSN":                 row.get("SSN", ""),
                    "DATE OF BIRTH":       date_val,
                    "BLOOD TYPE":          details_val,
                    "NATIONALITY":         loc_val,
                    "DATA TIER":           tier_val,
                    "SECTION":             row.get("SECTION", sheet_name),
                    "ASSET WEIGHT":        weight_val,
                    "SENSITIVITY LEVEL":   sens_val,
                    "_original_attributes": original_attrs,
                }

                # Index Record ID (e.g. IAM-670469, INS-985884, SRC-518498, HL7-517169, etc.)
                rec_id = str(row.get("RECORD ID", "")).strip().upper()
                if rec_id: idx["record_ids"][rec_id] = record

                # Index Patient ID (e.g. TM-XXXX-XXXX)
                pid = str(row.get("PATIENT ID", "")).strip().upper()
                if pid: idx["patient_ids"][pid] = record

                # Index ONLY highly specific unique identifiers (Hashes, Contract IDs, Tokens, DB Strings, API Keys, IPs)
                # This prevents common names or status words like "Robert Perera" or "Under Review" from causing duplicate matches!
                for col_name, val in original_attrs.items():
                    val_str = str(val).strip()
                    if len(val_str) > 5 and col_name in UNIQUE_ID_COLS:
                        if val_str not in idx["tokens"]:
                            idx["tokens"][val_str] = record

        except Exception:
            continue

    return all_sheets, idx


def find_master_asset_match(prompt_text, asset_index):
    """
    Check prompt against ALL 15 CSV sheets and return ALL matches found in the payload.
    Ensures multiple assets leaked in a single prompt are fully identified without duplicates!
    """
    matches = []
    seen_records = set()
    matched_token_values = set()

    # 1. Record ID & Patient ID (Any prefix 2-5 alphanumeric chars followed by a dash and 4-8 digits)
    rec_matches = re.findall(r'[A-Z0-9]{2,5}-\d{4,8}', prompt_text, re.IGNORECASE)
    for rm in rec_matches:
        rm_upper = rm.upper()
        rec = None
        if rm_upper in asset_index.get("record_ids", {}):
            rec = asset_index["record_ids"][rm_upper]
        elif rm_upper in asset_index.get("patient_ids", {}):
            rec = asset_index["patient_ids"][rm_upper]
        
        if rec and rec["RECORD ID"] not in seen_records:
            seen_records.add(rec["RECORD ID"])
            matches.append(rec)
            # Store all attribute values of this matched record to prevent duplicate mock collisions in Step 2!
            for val in rec.get("_original_attributes", {}).values():
                val_str = str(val).strip()
                if len(val_str) > 5:
                    matched_token_values.add(val_str)

    # 2. Token / Substring matching (Only specific Hashes, API Keys, IPs, Git Repos, Contract IDs, etc.)
    for token, rec in asset_index.get("tokens", {}).items():
        if token in prompt_text:
            # Check if this token is already accounted for by an existing matched record
            if token not in matched_token_values and rec and rec["RECORD ID"] not in seen_records:
                seen_records.add(rec["RECORD ID"])
                matches.append(rec)
                for val in rec.get("_original_attributes", {}).values():
                    val_str = str(val).strip()
                    if len(val_str) > 5:
                        matched_token_values.add(val_str)

    return matches


# ── LOG INGESTION & PROCESSING ────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def load_logs():
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


@st.cache_data(ttl=30, show_spinner=False)
def process_events():
    raw_logs = load_logs()
    all_sheets, asset_idx = load_master_dataset()
    if not raw_logs:
        return pd.DataFrame(), 0, all_sheets

    events = []
    asset_match_count = 0

    for idx_e, entry in enumerate(raw_logs):
        timestamp   = entry.get("timestamp", "N/A")
        source      = entry.get("source_node", {})
        client_ip   = source.get("client_ip", "192.168.89.134")
        client_port = str(source.get("source_port", "?"))
        dest        = entry.get("destination_node", {})
        dest_domain = dest.get("destination_domain", "unknown")
        dest_ip     = dest.get("destination_ip", "?")
        dest_url    = dest.get("full_url", "?")
        http_method = entry.get("connection_metadata", {}).get("http_method", "POST")
        user_agent  = entry.get("connection_metadata", {}).get("user_agent", "Unknown")
        raw_prompt  = entry.get("captured_payload", {}).get("prompt", "N/A")

        if raw_prompt in ("Dynamic Content", "N/A") or "conversation_mode" in str(raw_prompt):
            continue

        dest_weight = 0.95 if any(d in dest_domain for d in ["gemini","chatgpt","claude","openai"]) else 0.70
        user_weight = 0.90 if idx_e % 2 == 0 else 0.65

        is_bot = (len(str(raw_prompt)) < 25 or "f.req=" in str(raw_prompt) or
                  str(raw_prompt).startswith("trace=") or "PCck7e" in str(raw_prompt) or
                  "aPya6c" in str(raw_prompt))
        identity = "Automated Bot" if is_bot else "Human Session"
        identity_icon = "🤖" if is_bot else "🧑‍💻"

        # Find ALL asset matches in the prompt
        asset_matches = find_master_asset_match(str(raw_prompt), asset_idx)

        score, keywords, tiers, clean_prompt, norm_str = calculate_wrse(
            str(raw_prompt), dest_weight, user_weight,
            asset_matches=asset_matches
        )

        if len(clean_prompt.strip()) <= 3 and score < 30 and not asset_matches:
            continue

        sev_label, sev_icon = get_severity(score)
        if asset_matches: asset_match_count += len(asset_matches)

        primary_match = asset_matches[0] if asset_matches else None

        if asset_matches:
            if len(asset_matches) > 1:
                phi_matched_label = f"{primary_match['PATIENT NAME']} (+{len(asset_matches)-1} Assets)"
                phi_record_id = ", ".join(m["RECORD ID"] for m in asset_matches if m.get("RECORD ID"))
                data_tier = ", ".join(sorted(set(m["DATA TIER"] for m in asset_matches)))
                asset_section = ", ".join(sorted(set(m["SECTION"] for m in asset_matches)))
                asset_weight = max(m["ASSET WEIGHT"] for m in asset_matches)
                sens_levels = [m.get("SENSITIVITY LEVEL", "HIGH") for m in asset_matches]
                asset_sensitivity = "CRITICAL" if "CRITICAL" in sens_levels else "HIGH"
            else:
                phi_matched_label = primary_match["PATIENT NAME"]
                phi_record_id = primary_match["RECORD ID"]
                data_tier = primary_match["DATA TIER"]
                asset_section = primary_match["SECTION"]
                asset_weight = primary_match["ASSET WEIGHT"]
                asset_sensitivity = primary_match["SENSITIVITY LEVEL"]
        else:
            phi_matched_label = "—"
            phi_record_id = "—"
            data_tier = tiers[0] if tiers else "—"
            asset_section = "—"
            asset_weight = "—"
            asset_sensitivity = "CRITICAL" if score > 80 else ("MODERATE" if score >= 55 else "LOW")

        event_id = f"EVT-{idx_e}-{timestamp.replace(' ', '-').replace(':', '')}"

        events.append({
            # Core
            "Event ID":          event_id,
            "Timestamp":         timestamp,
            "Source IP":         client_ip,
            "Source Port":       client_port,
            "Source (full)":     f"{client_ip}:{client_port}",
            "Destination":       dest_domain,
            "Dest IP":           dest_ip,
            "Full URL":          dest_url,
            "HTTP Method":       http_method,
            "User Agent":        user_agent,
            "Identity":          identity,
            "Identity Icon":     identity_icon,
            # Payload
            "Raw Prompt":        str(raw_prompt),
            "Extracted Prompt":  clean_prompt[:200] if clean_prompt else norm_str[:150],
            # WRSE
            "Triggered Keys":    ", ".join(keywords[:3]) if keywords else "None",
            "Data Tier":         data_tier,
            "Asset Section":     asset_section,
            "Asset Weight":      asset_weight,
            "WRSE Score":        score,
            "Severity":          sev_label,
            "Sev Icon":          sev_icon,
            # Master Asset Match info
            "PHI Matched":       phi_matched_label,
            "PHI Patient ID":    primary_match["PATIENT ID"] if primary_match else "—",
            "PHI Record ID":     phi_record_id,
            "PHI Blood Type":    primary_match["BLOOD TYPE"] if primary_match else "—",
            "PHI Nationality":   primary_match["NATIONALITY"] if primary_match else "—",
            "PHI DOB":           primary_match["DATE OF BIRTH"] if primary_match else "—",
            "Sensitivity Level": asset_sensitivity,
            "_phi_records":      asset_matches, # FULL LIST OF MATCHES
            "_raw_entry":        entry,
        })

    df = pd.DataFrame(events)
    # ── GUARANTEE NEWEST ALERTS FIRST (AT THE TOP) ──
    if not df.empty:
        df = df.sort_values("Timestamp", ascending=False).reset_index(drop=True)

    return df, asset_match_count, all_sheets
