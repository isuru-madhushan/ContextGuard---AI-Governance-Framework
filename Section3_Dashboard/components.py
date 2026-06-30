import streamlit as st
import pandas as pd
import sqlite3
import os
from data_core import score_bar_html

# ── MONITOR STATUS PERSISTENCE (SQLite) ──────────────────────────────────────
_MON_DB = "/home/izu/ShadowAI_Framework/Section3_Dashboard/users.db"
_MON_OPTIONS = ["Open", "In Progress", "Close"]

def _init_monitor_table():
    """Create monitor_status table if it doesn't exist yet."""
    conn = sqlite3.connect(_MON_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitor_status (
            event_id TEXT PRIMARY KEY,
            status   TEXT DEFAULT 'Open'
        )
    """)
    conn.commit()
    conn.close()

def _get_monitor_status(event_id):
    """Return saved status for event_id, default 'Open'."""
    try:
        conn = sqlite3.connect(_MON_DB)
        row = conn.execute(
            "SELECT status FROM monitor_status WHERE event_id = ?", (event_id,)
        ).fetchone()
        conn.close()
        return row[0] if row else "Open"
    except Exception:
        return "Open"

def _save_monitor_status(event_id, status):
    """Upsert the status for an event."""
    try:
        conn = sqlite3.connect(_MON_DB)
        conn.execute("""
            INSERT INTO monitor_status (event_id, status)
            VALUES (?, ?)
            ON CONFLICT(event_id) DO UPDATE SET status = excluded.status
        """, (event_id, status))
        conn.commit()
        conn.close()
    except Exception:
        pass

_init_monitor_table()

# ══════════════════════════════════════════════════════════════════════════════
# 🧩 THREATMON REUSABLE UI COMPONENTS (ZERO INDENTATION HTML TO PREVENT CODE BLOCKS)
# ══════════════════════════════════════════════════════════════════════════════

def render_threatmon_top_strip(df_all, phi_mc, custom_assets_count):
    """
    Renders the exact horizontal icon circle strip seen in ThreatMon:
    11 circular icons with metrics underneath.
    """
    total_ev = len(df_all) if not df_all.empty else 0
    dests = df_all["Destination"].nunique() if not df_all.empty else 0
    ips = df_all["Source IP"].nunique() if not df_all.empty else 0
    crit_n = len(df_all[df_all["Severity"] == "CRITICAL"]) if not df_all.empty else 0
    med_n = len(df_all[df_all["Severity"] == "MEDIUM"]) if not df_all.empty else 0
    low_n = len(df_all[df_all["Severity"] == "LOW"]) if not df_all.empty else 0
    tiers_n = df_all["Data Tier"].nunique() if not df_all.empty else 1
    bots_n = len(df_all[df_all["Identity"] == "Automated Bot"]) if not df_all.empty else 0
    humans_n = len(df_all[df_all["Identity"] == "Human Session"]) if not df_all.empty else 0

    strip_html = f"""<div class="tm-asset-strip">
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-blue">🌐</div>
<div class="tm-asset-num">{total_ev}</div>
<div class="tm-asset-lbl">Total Events</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-orange">📇</div>
<div class="tm-asset-num">{dests}</div>
<div class="tm-asset-lbl">AI Destinations</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-purple">🗄️</div>
<div class="tm-asset-num">{phi_mc}</div>
<div class="tm-asset-lbl">Asset Matches</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-red">🚨</div>
<div class="tm-asset-num">{crit_n}</div>
<div class="tm-asset-lbl">Critical Risk</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-cyan">📡</div>
<div class="tm-asset-num">{ips}</div>
<div class="tm-asset-lbl">Client IPs</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-orange">⚠️</div>
<div class="tm-asset-num">{med_n}</div>
<div class="tm-asset-lbl">Medium Risk</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-green">✅</div>
<div class="tm-asset-num">{low_n}</div>
<div class="tm-asset-lbl">Low Risk</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-purple">⚙️</div>
<div class="tm-asset-num">{custom_assets_count + 10}</div>
<div class="tm-asset-lbl">Asset Keywords</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-blue">🛡️</div>
<div class="tm-asset-num">{tiers_n}</div>
<div class="tm-asset-lbl">Active Tiers</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-cyan">🤖</div>
<div class="tm-asset-num">{bots_n}</div>
<div class="tm-asset-lbl">Auto Bots</div>
</div>
<div class="tm-asset-item">
<div class="tm-icon-circle tm-icon-green">🧑‍💻</div>
<div class="tm-asset-num">{humans_n}</div>
<div class="tm-asset-lbl">Human Sessions</div>
</div>
</div>"""
    st.markdown(strip_html, unsafe_allow_html=True)


def render_horizontal_stacked_bar(df_all):
    """
    Renders the beautiful horizontal stacked bar chart matching 'Main Domains Type'.
    """
    if df_all.empty:
        return
    
    total = len(df_all)
    crit_n = len(df_all[df_all["Severity"] == "CRITICAL"])
    med_n  = len(df_all[df_all["Severity"] == "MEDIUM"])
    low_n  = len(df_all[df_all["Severity"] == "LOW"])
    
    crit_pct = max(15, int((crit_n / total) * 100)) if total > 0 else 33
    med_pct  = max(15, int((med_n / total) * 100)) if total > 0 else 33
    low_pct  = max(15, 100 - crit_pct - med_pct) if total > 0 else 34

    html = f"""<div class="tm-card">
<div class="tm-card-title">🛡️ Event Severity Breakdown</div>
<div class="stacked-bar-legend">
<div class="legend-item"><div class="legend-box" style="background:#FF2D5B;"></div>CRITICAL ({crit_n})</div>
<div class="legend-item"><div class="legend-box" style="background:#F59E0B;"></div>MEDIUM ({med_n})</div>
<div class="legend-item"><div class="legend-box" style="background:#10B981;"></div>LOW ({low_n})</div>
</div>
<div class="stacked-bar-container">
<div class="stacked-segment" style="width:{crit_pct}%; background:#FF2D5B;">{crit_n if crit_n>0 else ''}</div>
<div class="stacked-segment" style="width:{med_pct}%; background:#F59E0B;">{med_n if med_n>0 else ''}</div>
<div class="stacked-segment" style="width:{low_pct}%; background:#10B981;">{low_n if low_n>0 else ''}</div>
</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_donut_chart(df_all):
    """
    Renders the beautiful donut chart matching 'Active/Passive DNS'.
    """
    if df_all.empty:
        return

    phi_matches = len(df_all[df_all["PHI Matched"] != "—"])
    no_phi = len(df_all) - phi_matches

    html = f"""<div class="tm-card">
<div class="tm-card-title">🗄️ Master Registry Leakage Proportions</div>
<div class="donut-container">
<div class="donut-ring">
<div class="donut-hole">{phi_matches}</div>
</div>
<div class="donut-legend">
<div class="legend-item"><div class="legend-box" style="background:#A78BFA;"></div>Asset Confirmed ({phi_matches})</div>
<div class="legend-item"><div class="legend-box" style="background:#FB7185;"></div>General / Setup ({no_phi})</div>
</div>
</div>
</div>"""
    st.markdown(html, unsafe_allow_html=True)


def nav_to_alert(event_id):
    st.session_state.inspect_button_clicked = True
    st.session_state.selected_alert_id = event_id
    st.session_state.nav_radio = "💬 Prompt Inspector"
    st.query_params["page"] = "Prompt Inspector"


def render_custom_table(df):
    """
    Renders the sleek ThreatMon live interactive table using Streamlit columns
    with fully functional Monitor switches and Action inspect auto-navigation buttons.
    """
    if df.empty:
        st.markdown("<div class='info-box'>No data available for table.</div>", unsafe_allow_html=True)
        return

    st.markdown('<div class="sec-title" style="margin-top:16px;">🛡️ Live Digital Assets Attack Surface Table</div>', unsafe_allow_html=True)
    
    # Table Header
    cols = st.columns([1.5, 2.0, 1.8, 1.2, 1.2, 1.0, 1.0, 1.0, 1.2])
    headers = ["AI Platform", "Status / Match", "Category Tier", "Source IP", "Session Type", "WRSE Score", "Last Update", "Monitor", "Actions"]
    for c, h in zip(cols, headers):
        c.markdown(f"**{h}**")
    st.markdown("<hr style='border:none;height:1px;background:#1D3364;margin:8px 0;'>", unsafe_allow_html=True)

    for idx, row in df.head(50).iterrows():
        cols = st.columns([1.5, 2.0, 1.8, 1.2, 1.2, 1.0, 1.0, 1.0, 1.2])
        
        # AI Platform
        cols[0].markdown(f"`{row.get('Destination', 'Unknown')}`")
        
        # Status / Match
        sev = row.get("Severity", "LOW")
        phi_match_val = row.get("PHI Matched", "—")
        if phi_match_val != "—":
            tier_str = str(row.get("Data Tier", ""))
            icon = "🗂️" if ("+" in phi_match_val or "," in tier_str) else ("🖥️" if ("Infrastructure" in tier_str or "Tier 2" in tier_str) else ("💡" if ("IP" in tier_str or "Tier 3" in tier_str) else "⚕️"))
            pill = f'<span class="pill-custom">{icon} {phi_match_val}</span>'
        elif sev == "CRITICAL":
            pill = '<span class="pill-passive">Critical Risk</span>'
        elif sev == "MEDIUM":
            pill = '<span class="pill-custom">Medium Risk</span>'
        else:
            pill = '<span class="pill-active">Low Risk</span>'
        cols[1].markdown(pill, unsafe_allow_html=True)
        
        # Category Tier
        cols[2].markdown(f"<span style='font-size:12px;color:#E2EBF8;'>{row.get('Data Tier', 'Tier 1 - PHI')}</span>", unsafe_allow_html=True)
        
        # Source IP
        cols[3].markdown(f"`{row.get('Source IP', '192.168.89.134')}`")
        
        # Session Type
        cols[4].markdown(f"<span style='font-size:12px;color:#8C9BAE;'>{row.get('Identity', 'Human Session')}</span>", unsafe_allow_html=True)
        
        # WRSE Score
        cols[5].markdown(f"<span style='font-family:monospace;font-weight:700;color:#F59E0B;'>{row.get('WRSE Score', 0)}%</span>", unsafe_allow_html=True)
        
        # Last Update
        ts = row.get("Timestamp", "N/A")
        ts_short = ts.split(" ")[1] if " " in ts else ts
        cols[6].markdown(f"<span style='font-family:monospace;font-size:11px;color:#647E9C;'>{ts_short}</span>", unsafe_allow_html=True)
        
        # Monitor Status Selectbox — persisted in SQLite
        evt_id = row.get("Event ID", f"evt_{idx}")
        saved_status  = _get_monitor_status(evt_id)
        saved_index   = _MON_OPTIONS.index(saved_status) if saved_status in _MON_OPTIONS else 0

        def _on_monitor_change(eid=evt_id):
            _save_monitor_status(eid, st.session_state[f"mon_{eid}"])

        cols[7].selectbox(
            "Monitor",
            options=_MON_OPTIONS,
            index=saved_index,
            key=f"mon_{evt_id}",
            label_visibility="collapsed",
            on_change=_on_monitor_change,
        )
        
        # Actions Button (Auto Navigation to Alerts & Payloads!)
        cols[8].button("🔍 Inspect", key=f"act_{evt_id}", on_click=nav_to_alert, args=(evt_id,))
        
        st.markdown("<hr style='border:none;height:1px;background:#101D3A;margin:4px 0;'>", unsafe_allow_html=True)
