import streamlit as st
import pandas as pd
from datetime import datetime
from data_core import (
    DEFAULT_KEYWORDS, ASSET_TIERS, load_custom_assets, save_custom_assets,
    score_bar_html
)
from components import (
    render_threatmon_top_strip, render_horizontal_stacked_bar,
    render_donut_chart, render_custom_table
)

# ══════════════════════════════════════════════════════════════════════════════
# 🗂️ THREATMON-STYLE PAGE VIEWS (EXACT MATCH & NEWEST FIRST)
# ══════════════════════════════════════════════════════════════════════════════

def render_dashboard_page(df_all, phi_mc, custom_assets_count):
    """
    The exact ThreatMon 'Digital Assets' view from the user's screenshot.
    """
    # 1. ThreatMon Top Strip
    render_threatmon_top_strip(df_all, phi_mc, custom_assets_count)

    if df_all.empty:
        st.markdown('<div class="info-box">🛰️ No events found in the selected time range.</div>', unsafe_allow_html=True)
        return

    # 2. Middle 3 Charts Row (Exactly like ThreatMon screenshot)
    ch1, ch2, ch3 = st.columns([1.2, 1.2, 1.1])
    with ch1:
        render_horizontal_stacked_bar(df_all)
    with ch2:
        st.markdown("""<div class="tm-card">
<div class="tm-card-title">📈 Event Frequency Timeline</div>""", unsafe_allow_html=True)
        t_df = df_all["Timestamp"].value_counts().reset_index()
        t_df.columns = ["Timestamp", "Events"]
        t_df = t_df.sort_values("Timestamp")
        st.area_chart(t_df, x="Timestamp", y="Events", color="#06B6D4", height=210)
        st.markdown("</div>", unsafe_allow_html=True)
    with ch3:
        render_donut_chart(df_all)

    # 3. Filter Container (Replaced static HTML with fully functional Streamlit expander)
    with st.expander("🔍 Advanced Live Table Filter & Quick Search", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            flt_ass = st.text_input("Asset Keyword / Match", placeholder="Search asset name...", key="flt_ass")
            flt_cat = st.text_input("Category Tier", placeholder="Asset category...", key="flt_cat")
        with f2:
            flt_ip  = st.text_input("Source IP", placeholder="Client IP address...", key="flt_ip")
            flt_dest = st.text_input("AI Platform", placeholder="Destination domain...", key="flt_dest")
        with f3:
            flt_sev = st.selectbox("Severity Level", ["All", "CRITICAL", "MEDIUM", "LOW"], key="flt_sev")
            flt_id  = st.selectbox("Session Type", ["All", "Human Session", "Automated Bot"], key="flt_id")

    # Filter the dataframe dynamically
    df_table = df_all.copy()
    if flt_ass: df_table = df_table[df_table["PHI Matched"].str.contains(flt_ass, case=False, na=False) | df_table["Triggered Keys"].str.contains(flt_ass, case=False, na=False)]
    if flt_cat: df_table = df_table[df_table["Data Tier"].str.contains(flt_cat, case=False, na=False)]
    if flt_ip:  df_table = df_table[df_table["Source IP"].str.contains(flt_ip, case=False, na=False)]
    if flt_dest: df_table = df_table[df_table["Destination"].str.contains(flt_dest, case=False, na=False)]
    if flt_sev != "All": df_table = df_table[df_table["Severity"] == flt_sev]
    if flt_id != "All":  df_table = df_table[df_table["Identity"] == flt_id]

    # 4. ThreatMon Custom Table (Newest first guaranteed, fully interactive)
    render_custom_table(df_table)


def render_alert_feed_page(df_all):
    """
    Live Alert Feed with full payload viewer and 3-column deep dive expanders.
    """
    if df_all.empty:
        st.markdown('<div class="info-box">No events available in selected time range.</div>', unsafe_allow_html=True)
        return

    # Filter Bar
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1: sev_f  = st.selectbox("Severity", ["ALL","CRITICAL","MEDIUM","LOW"], key="af_sev")
    with fc2: phi_f  = st.selectbox("Asset Match", ["All Events","Asset Matched Only","No Match"], key="af_phi")
    with fc3: dest_f = st.selectbox("Destination", ["ALL"] + sorted(df_all["Destination"].unique().tolist()), key="af_dest")
    with fc4: id_f   = st.selectbox("Identity", ["ALL","Human Session","Automated Bot"], key="af_id")

    fdf = df_all.copy()
    if sev_f != "ALL":     fdf = fdf[fdf["Severity"] == sev_f]
    if phi_f == "Asset Matched Only": fdf = fdf[fdf["PHI Matched"] != "—"]
    elif phi_f == "No Match": fdf = fdf[fdf["PHI Matched"] == "—"]
    if dest_f != "ALL":    fdf = fdf[fdf["Destination"] == dest_f]
    if id_f != "ALL":      fdf = fdf[fdf["Identity"] == id_f]

    # ── GUARANTEE NEWEST ALERTS FIRST ──
    fdf = fdf.sort_values("Timestamp", ascending=False).reset_index(drop=True)
    
    # ── CHECK FOR AUTO-NAVIGATION FROM DASHBOARD TABLE ──
    sel_id = st.session_state.get("selected_alert_id")
    if sel_id and sel_id in fdf["Event ID"].values:
        st.success(f"🎯 **Auto-Navigated to Selected Alert:** `{sel_id}` from Digital Assets Dashboard Table! (Brought to top)")
        selected_row = fdf[fdf["Event ID"] == sel_id]
        other_rows = fdf[fdf["Event ID"] != sel_id]
        fdf = pd.concat([selected_row, other_rows]).reset_index(drop=True)

    st.markdown(f'<div class="sec-title">📋 Showing {len(fdf)} Filtered Events (Newest First)</div>', unsafe_allow_html=True)

    for idx_row, ev in fdf.iterrows():
        sev   = ev["Severity"]
        score = ev["WRSE Score"]
        phi_records = ev["_phi_records"]
        has_phi = bool(phi_records)
        
        is_selected = (ev["Event ID"] == sel_id)
        card_cls = "c-PHI" if (sev == "CRITICAL" and has_phi) else f"c-{sev}"
        if is_selected:
            card_cls += " selected-alert-card"

        score_col = "#FF2D5B" if sev == "CRITICAL" else ("#F59E0B" if sev == "MEDIUM" else "#10B981")
        phi_pill = f'<span class="phi-tag">🗄️ MASTER ASSET REGISTRY MATCH ({len(phi_records)} ASSETS)</span>' if has_phi else ""

        phi_html = ""
        if has_phi:
            for phi in phi_records:
                orig_attrs = phi.get("_original_attributes", {})
                attr_chunks = [f"{k}: <strong style='color:#38BDF8;'>{v}</strong>" for k, v in orig_attrs.items() if k not in ["SHEET_NAME", "SECTION", "SENSITIVITY LEVEL", "ASSET WEIGHT"]]
                lines = []
                for i in range(0, len(attr_chunks), 3):
                    lines.append(" &nbsp;|&nbsp; ".join(attr_chunks[i:i+3]))
                attrs_display = "<br>".join(lines)

                phi_html += (
                    f'<div class="phi-record-inline" style="margin-top:6px;">'
                    f'&#9877;&#65039; <strong>MASTER ASSET REGISTRY MATCH ({phi.get("SHEET_NAME","T1")})</strong><br>'
                    f'{attrs_display}<br>'
                    f'Tier: <strong>{phi.get("DATA TIER", "Tier 1 - PHI")}</strong> &nbsp;|&nbsp; '
                    f'Asset Weight (Wi): <strong style="color:#F59E0B;">{phi.get("ASSET WEIGHT", 0.95)}</strong> &nbsp;|&nbsp; '
                    f'Sensitivity: <strong style="color:#FF8099;">{phi.get("SENSITIVITY LEVEL", "CRITICAL")}</strong>'
                    f'</div>'
                )

        st.markdown(
            f'<div class="alert-card {card_cls}" style="{"border:2px solid #38BDF8;box-shadow:0 0 15px rgba(56,189,248,0.4);" if is_selected else ""}">'
            f'<div class="alert-header">'
            f'<span class="sev-{sev}">{sev}</span> {phi_pill}'
            f'<span class="alert-score" style="color:{score_col};margin-left:auto;">WRSE: {score}%</span>'
            f'<span class="alert-ts">{ev["Timestamp"]}</span></div>'
            f'<div class="alert-flow">{ev["Identity Icon"]} {ev["Source IP"]}:{ev["Source Port"]} '
            f'<span style="color:#647E9C;">→</span> {ev["Destination"]}'
            f'<span style="color:#647E9C;font-size:11px;"> [{ev["HTTP Method"]}]</span></div>'
            f'<div class="alert-body">Prompt: <em style="color:#38BDF8;">{ev["Extracted Prompt"][:150]}</em><br>'
            f'Keys: {ev["Triggered Keys"][:100]} | Tier: {ev["Data Tier"]} | Asset Weight: {ev["Asset Weight"]}</div>'
            f'{score_bar_html(score)}'
            f'{phi_html}'
            f'</div>',
            unsafe_allow_html=True
        )

        with st.expander(f"🔍 Inspect Full Detail — {ev['Timestamp']} | WRSE {score}%", expanded=is_selected):
            d1, d2, d3 = st.columns(3)
            with d1:
                st.markdown('<div class="sec-title">🖥️ Source Host</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="host-card">'
                    f'<div class="host-label">Client IP</div><div class="host-val danger">{ev["Source IP"]}</div>'
                    f'<div class="host-label">Source Port</div><div class="host-val">{ev["Source Port"]}</div>'
                    f'<div class="host-label">HTTP Method</div><div class="host-val">{ev["HTTP Method"]}</div>'
                    f'<div class="host-label">Session Type</div><div class="host-val">{ev["Identity Icon"]} {ev["Identity"]}</div>'
                    f'<div class="host-label">User Agent</div><div style="font-size:10px;font-family:monospace;color:#647E9C;word-break:break-all;">{ev["User Agent"][:120]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.markdown('<div class="sec-title" style="margin-top:12px;">🎯 Destination (AI Service)</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="host-card">'
                    f'<div class="host-label">AI Platform</div><div class="host-val ok">{ev["Destination"]}</div>'
                    f'<div class="host-label">Destination IP</div><div class="host-val">{ev["Dest IP"]}</div>'
                    f'<div class="host-label">Full URL</div><div style="font-size:10px;font-family:monospace;color:#647E9C;word-break:break-all;">{ev["Full URL"][:180]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with d2:
                st.markdown('<div class="sec-title">📦 Captured Payload (Full)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="payload-box">{ev["Raw Prompt"]}</div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-title" style="margin-top:12px;">📋 Raw Log Entry (JSON)</div>', unsafe_allow_html=True)
                st.json(ev["_raw_entry"])

            with d3:
                st.markdown('<div class="sec-title">📐 WRSE Calculation Breakdown</div>', unsafe_allow_html=True)
                score_col2 = "#FF2D5B" if sev == "CRITICAL" else ("#F59E0B" if sev == "MEDIUM" else "#10B981")
                aw_val = ev["Asset Weight"] if ev["Asset Weight"] != "—" else "keyword-based"
                st.markdown(
                    f'<div class="host-card">'
                    f'<div class="host-label">FINAL RISK SCORE</div>'
                    f'<div style="font-size:36px;font-weight:900;font-family:monospace;color:{score_col2};">{score}%</div>'
                    f'<div class="host-label" style="margin-top:8px;">Severity Classification</div>'
                    f'<span class="sev-{sev}" style="font-size:13px;">{sev}</span><br><br>'
                    f'<div style="font-size:14px;font-weight:700;color:#E2EBF8;font-family:monospace;margin-bottom:4px;">RS = (0.50×S) + (0.25×D) + (0.25×U)</div>'
                    f'<div style="font-size:11px;color:#647E9C;font-family:monospace;line-height:1.8;">'
                    f'S (Sensitivity) = {aw_val}<br>'
                    f'D (Dest Trust)  = 0.95 [AI platform]<br>'
                    f'U (User Weight) = {"0.90" if idx_row % 2 == 0 else "0.65"}<br>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
                st.markdown('<div class="sec-title" style="margin-top:10px;">🔑 Triggered Indicators</div>', unsafe_allow_html=True)
                for kw in ev["Triggered Keys"].split(", "):
                    if kw and kw != "None":
                        st.markdown(f'`{kw}`', unsafe_allow_html=False)

    st.markdown("<br>", unsafe_allow_html=True)
    exp_cols = ["Timestamp","Source IP","Source Port","Destination","Dest IP","Full URL","HTTP Method",
                "Identity","Extracted Prompt","Triggered Keys","Data Tier","Asset Weight",
                "WRSE Score","Severity","Sensitivity Level","PHI Matched","PHI Patient ID","PHI Record ID"]
    csv = fdf[exp_cols].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Alert Feed CSV", csv, "contextguard_alerts.csv", "text/csv")


def render_forensic_page(df_all):
    """
    Forensic Viewer with Advanced Multi-Filter Search and Host Intelligence.
    """
    if df_all.empty:
        st.markdown('<div class="info-box">No events available in selected time range.</div>', unsafe_allow_html=True)
        return

    st.markdown('<div class="sec-title">🔎 Advanced Multi-Filter Search (Real-Time Interactive)</div>', unsafe_allow_html=True)
    
    # Use a container instead of st.form for real-time flexible filtering!
    with st.container():
        r1c1, r1c2, r1c3, r1c4 = st.columns(4)
        with r1c1: ip_search    = st.text_input("Source IP", "", placeholder="e.g. 192.168.x.x", key="fs_ip")
        with r1c2: kw_search    = st.text_input("Keyword / Payload", "", placeholder="e.g. patient, api key...", key="fs_kw")
        with r1c3: dest_search  = st.text_input("Destination", "", placeholder="e.g. chatgpt.com, claude.ai", key="fs_dest")
        with r1c4: phi_search   = st.text_input("Entity Name / PHI", "", placeholder="e.g. John Davis, DB server...", key="fs_phi")

        r2c1, r2c2, r2c3, r2c4 = st.columns(4)
        with r2c1: sev_ms = st.multiselect("Severity", ["CRITICAL","MEDIUM","LOW"], default=["CRITICAL","MEDIUM","LOW"], key="fs_sev")
        with r2c2: score_min, score_max = st.slider("WRSE Score Range", 0, 100, (0, 100), key="fs_score")
        with r2c3: id_ms = st.multiselect("Identity", ["Human Session","Automated Bot"], default=["Human Session","Automated Bot"], key="fs_id")
        with r2c4: phi_only = st.checkbox("Asset Matched Only", value=False, key="fs_phionly")

        st.markdown("<div style='margin-bottom:5px;'></div>", unsafe_allow_html=True)

    # Apply search robustly with .strip() and expanded field coverage
    sdf = df_all.copy()
    if ip_search.strip():
        sdf = sdf[sdf["Source IP"].astype(str).str.contains(ip_search.strip(), case=False, na=False)]
    if kw_search.strip():
        kw_clean = kw_search.strip()
        sdf = sdf[
            sdf["Extracted Prompt"].astype(str).str.contains(kw_clean, case=False, na=False) | 
            sdf["Triggered Keys"].astype(str).str.contains(kw_clean, case=False, na=False)
        ]
    if dest_search.strip():
        sdf = sdf[sdf["Destination"].astype(str).str.contains(dest_search.strip(), case=False, na=False)]
    if phi_search.strip():
        phi_clean = phi_search.strip()
        sdf = sdf[
            sdf["PHI Matched"].astype(str).str.contains(phi_clean, case=False, na=False) | 
            sdf["PHI Patient ID"].astype(str).str.contains(phi_clean, case=False, na=False) | 
            sdf["PHI Record ID"].astype(str).str.contains(phi_clean, case=False, na=False) |
            sdf["Extracted Prompt"].astype(str).str.contains(phi_clean, case=False, na=False)
        ]
    if sev_ms:
        sdf = sdf[sdf["Severity"].isin(sev_ms)]
    else:
        sdf = sdf.iloc[0:0] # if no severity selected, show none
        
    sdf = sdf[(sdf["WRSE Score"] >= score_min) & (sdf["WRSE Score"] <= score_max)]
    
    if id_ms:
        sdf = sdf[sdf["Identity"].isin(id_ms)]
    else:
        sdf = sdf.iloc[0:0]
        
    if phi_only:
        sdf = sdf[sdf["PHI Matched"] != "—"]

    # ── GUARANTEE NEWEST EVENTS FIRST ──
    sdf = sdf.sort_values("Timestamp", ascending=False).reset_index(drop=True)

    st.markdown(f'<div class="sec-title" style="margin-top:20px;">📋 Search Results — {len(sdf)} events matching criteria (Newest First)</div>', unsafe_allow_html=True)
    disp_cols = ["Timestamp","Source IP","Source Port","Destination","HTTP Method",
                 "Identity","WRSE Score","Severity","Sensitivity Level","Data Tier",
                 "Asset Weight","PHI Matched","PHI Patient ID","PHI Record ID","Extracted Prompt"]
    
    # ── MATCH COUNT SUMMARY BANNER ──
    if not sdf.empty:
        c_crit = len(sdf[sdf["Severity"] == "CRITICAL"])
        c_med  = len(sdf[sdf["Severity"] == "MEDIUM"])
        c_low  = len(sdf[sdf["Severity"] == "LOW"])
        c_phi  = len(sdf[sdf["PHI Matched"] != "—"])
        st.markdown(f"""<div style='background: linear-gradient(90deg, #111E3E 0%, #0D1938 100%); border: 1px solid #1D3364; border-radius: 8px; padding: 12px 18px; margin-top: 10px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;'>
<div>
<span style='font-size:15px; font-weight:800; color:#06B6D4;'>🎯 FILTER MATCH SUMMARY:</span>
<span style='font-size:16px; font-weight:900; color:#FFFFFF; margin-left:8px; background:#0284C7; padding:2px 10px; border-radius:12px;'>{len(sdf)} Events</span>
</div>
<div style='display: flex; gap: 16px; font-size: 13px; font-family: monospace; font-weight: 700;'>
<span style='color:#FF2D5B;'>🔴 CRITICAL: {c_crit}</span>
<span style='color:#F59E0B;'>🟡 MEDIUM: {c_med}</span>
<span style='color:#10B981;'>🟢 LOW: {c_low}</span>
<span style='color:#C4B5FD;'>⚕️ ASSET LEAKS: {c_phi}</span>
</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box" style="margin-top:15px; margin-bottom: 20px;">⚠️ No events match your filter criteria.</div>', unsafe_allow_html=True)

    # ── FULL-WIDTH TOPIC WITH FULL-WIDTH DIVIDING LINE (EXACTLY LIKE SEARCH RESULTS HEADING) ──
    st.markdown("""<div style='font-size: 16px; font-weight: 700; color: #06B6D4; margin-bottom: 4px; margin-top: 15px;'>👁️ Table Presentation Mode</div>
<hr style='border: 1px solid #1D3364; margin-top: 0px; margin-bottom: 16px;'>""", unsafe_allow_html=True)

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2.2, 2.0, 1.2])
    with ctrl_col1:
        view_mode = st.radio(
            "Table Presentation Mode",
            ["📊 Interactive Dataframe", "📄 Full Expanded Table"],
            horizontal=True,
            label_visibility="collapsed",
            key="table_view_mode"
        )
    with ctrl_col2:
        show_count_match = st.checkbox("📊 Enable Dynamic Match Count Analytics", value=True, key="show_count_match")
    with ctrl_col3:
        st.write("") # Blank buffer column to keep widgets perfectly snug on the left without middle gap

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ── CUSTOM COLUMN SELECTOR (NEATLY COLLAPSED TO PREVENT UI CLUTTER) ──
    with st.expander("⚙️ Customize Table Columns & Export Fields", expanded=False):
        selected_cols = st.multiselect(
            "Select visible columns for the table and CSV export:", 
            disp_cols, 
            default=disp_cols, 
            key="custom_table_cols"
        )
        if not selected_cols:
            selected_cols = disp_cols # Fallback if user clears all

    # ── DYNAMIC COUNT MATCH / VALUE BREAKDOWN FOR SELECTED FIELDS ──
    if not sdf.empty and show_count_match:
        with st.expander("📊 Dynamic Match Count Analytics Panel", expanded=True):
            avail_cat_cols = [c for c in disp_cols if c in ["Source IP", "Destination", "Identity", "Severity", "Sensitivity Level", "Data Tier", "PHI Matched", "HTTP Method"]]
            count_match_cols = st.multiselect(
                "📌 Target Analytics Fields (Select fields to generate live match counts):", 
                avail_cat_cols, 
                default=["Destination", "Severity", "Source IP"], 
                key="custom_count_match_cols"
            )
            st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
            
            if count_match_cols:
                # Group into columns of 3 or 4 for beautiful presentation
                grid_cols = st.columns(min(len(count_match_cols), 4))
                for idx, c in enumerate(count_match_cols):
                    col_target = grid_cols[idx % len(grid_cols)]
                    with col_target:
                        vc = sdf[c].value_counts().reset_index()
                        vc.columns = [c, "Match Count"]
                        st.markdown(f"**📌 {c} Counts**")
                        st.dataframe(vc, use_container_width=True, height=140, hide_index=True)
            else:
                st.markdown("<div style='color:#F59E0B; font-size: 13px;'>ℹ️ Please select at least one field above to view its dynamic match count breakdown.</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

    if not sdf.empty:
        if view_mode == "📊 Interactive Dataframe":
            col_config = {
                "Timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
                "Source IP": st.column_config.TextColumn("Source IP", width="medium"),
                "Source Port": st.column_config.NumberColumn("Port", width="small"),
                "Destination": st.column_config.TextColumn("Destination", width="medium"),
                "HTTP Method": st.column_config.TextColumn("Method", width="small"),
                "Identity": st.column_config.TextColumn("Identity", width="medium"),
                "WRSE Score": st.column_config.NumberColumn("WRSE Score", width="small"),
                "Severity": st.column_config.TextColumn("Severity", width="small"),
                "Sensitivity Level": st.column_config.TextColumn("Sensitivity", width="small"),
                "Data Tier": st.column_config.TextColumn("Data Tier", width="small"),
                "Asset Weight": st.column_config.NumberColumn("Weight", width="small"),
                "PHI Matched": st.column_config.TextColumn("PHI Matched / Asset", width="medium"),
                "PHI Patient ID": st.column_config.TextColumn("Patient ID", width="small"),
                "PHI Record ID": st.column_config.TextColumn("Record ID", width="small"),
                "Extracted Prompt": st.column_config.TextColumn("Extracted Prompt (Payload)", width="large"),
            }
            st.dataframe(sdf[selected_cols], use_container_width=True, height=400, column_config=col_config)
        else:
            st.table(sdf[selected_cols])


    if not sdf.empty:
        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        with st.expander("🔍 Deep-Dive Event Inspector (View Full Extracted Prompt & Metadata)", expanded=True):
            inspect_opts = [f"Event #{i} — {row['Timestamp']} | {row['Source IP']} ➔ {row['Destination']} ({row['Severity']} - WRSE: {row['WRSE Score']})" for i, row in sdf.iterrows()]
            selected_evt = st.selectbox("Select Event to Inspect", range(len(sdf)), format_func=lambda x: inspect_opts[x], key="forensic_select")
            
            row_data = sdf.iloc[selected_evt]
            
            st.markdown(f"""<div style='background: linear-gradient(135deg, #0D1938, #070D1F); border: 1px solid #1D3364; border-radius: 10px; padding: 18px 22px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); margin-top: 10px;'>
<div style='display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1D3364; padding-bottom: 12px; margin-bottom: 14px;'>
<div>
<span style='font-size:16px; font-weight:800; color:#E2EBF8;'>{row_data['Source IP']} ➔ {row_data['Destination']}</span>
<span style='font-size:12px; color:#647E9C; font-family:monospace; margin-left: 10px;'>{row_data['Timestamp']}</span>
</div>
<div>
<span style='font-size:13px; font-weight:800; color:{"#FF2D5B" if row_data["Severity"]=="CRITICAL" else "#F59E0B" if row_data["Severity"]=="MEDIUM" else "#10B981"}; background:{"rgba(255,45,91,0.15)" if row_data["Severity"]=="CRITICAL" else "rgba(245,158,11,0.15)" if row_data["Severity"]=="MEDIUM" else "rgba(16,185,129,0.15)"}; padding: 4px 12px; border-radius: 12px; border: 1px solid {"#FF2D5B" if row_data["Severity"]=="CRITICAL" else "#F59E0B" if row_data["Severity"]=="MEDIUM" else "#10B981"};'>{row_data['Severity']} (WRSE: {row_data['WRSE Score']})</span>
</div>
</div>
<div style='font-size:12px; font-weight:700; color:#06B6D4; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;'>📝 FULL EXTRACTED PROMPT / PAYLOAD</div>
<div style='background: rgba(0,0,0,0.3); border: 1px solid #162C54; border-radius: 8px; padding: 14px 18px; font-size:14px; font-family:monospace; color:#38BDF8; line-height:1.6; white-space: pre-wrap; word-break: break-word; margin-bottom: 16px;'>{row_data['Extracted Prompt']}</div>
<div style='display: flex; flex-wrap: wrap; gap: 12px;'>
<div style='flex: 1; min-width: 200px; background: rgba(255,255,255,0.02); border: 1px solid #1D3364; border-radius: 8px; padding: 10px 14px;'>
<div style='font-size:11px; color:#647E9C; font-family:monospace;'>IDENTITY</div>
<div style='font-size:13px; font-weight:700; color:#E2EBF8; margin-top:2px;'>{row_data['Identity']}</div>
</div>
<div style='flex: 1; min-width: 200px; background: rgba(255,255,255,0.02); border: 1px solid #1D3364; border-radius: 8px; padding: 10px 14px;'>
<div style='font-size:11px; color:#647E9C; font-family:monospace;'>PHI MATCHED / ASSET</div>
<div style='font-size:13px; font-weight:700; color:#C4B5FD; margin-top:2px;'>{row_data['PHI Matched']}</div>
</div>
<div style='flex: 1; min-width: 200px; background: rgba(255,255,255,0.02); border: 1px solid #1D3364; border-radius: 8px; padding: 10px 14px;'>
<div style='font-size:11px; color:#647E9C; font-family:monospace;'>DATA TIER & WEIGHT</div>
<div style='font-size:13px; font-weight:700; color:#6EE7B7; margin-top:2px;'>{row_data['Data Tier']} (Wi: {row_data['Asset Weight']})</div>
</div>
<div style='flex: 1; min-width: 200px; background: rgba(255,255,255,0.02); border: 1px solid #1D3364; border-radius: 8px; padding: 10px 14px;'>
<div style='font-size:11px; color:#647E9C; font-family:monospace;'>SENSITIVITY LEVEL</div>
<div style='font-size:13px; font-weight:700; color:#FF8099; margin-top:2px;'>{row_data['Sensitivity Level']}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr style="border:none;height:1px;background:#1D3364;margin:24px 0;">', unsafe_allow_html=True)

    # Host Analysis
    st.markdown('<div class="sec-title">🖥️ Host Intelligence Summary</div>', unsafe_allow_html=True)
    ha1, ha2 = st.columns(2)
    with ha1:
        st.markdown("**Source IPs & Activity**")
        ip_df = sdf.groupby("Source IP").agg(
            Events=("WRSE Score","count"),
            Avg_WRSE=("WRSE Score","mean"),
            Max_WRSE=("WRSE Score","max"),
            Asset_Matches=("PHI Matched", lambda x: (x != "—").sum())
        ).round(1).sort_values("Max_WRSE", ascending=False)
        st.dataframe(ip_df, use_container_width=True)
    with ha2:
        st.markdown("**AI Destination Summary**")
        dest_df2 = sdf.groupby("Destination").agg(
            Events=("WRSE Score","count"),
            Avg_WRSE=("WRSE Score","mean"),
            Max_WRSE=("WRSE Score","max"),
            Asset_Leaked=("PHI Matched", lambda x: (x != "—").sum())
        ).round(1).sort_values("Events", ascending=False)
        st.dataframe(dest_df2, use_container_width=True)

    csv_s = sdf[selected_cols].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Selected Columns CSV", csv_s, "forensic_custom_results.csv", "text/csv")


def render_asset_manager_page(custom_assets):
    """
    IT Admin Asset Manager for dynamic keyword weight configurations.
    """
    am1, am2 = st.columns([2, 1])
    with am1:
        st.markdown('<div class="sec-title">📋 Current Asset Registry</div>', unsafe_allow_html=True)
        st.markdown("**🔒 System Default Assets** *(read-only)*", unsafe_allow_html=False)
        default_rows = [{"Keyword": kw, "Weight (Wi)": w, "Asset Tier": tier, "Added By": "System"} for kw, (w, tier) in DEFAULT_KEYWORDS.items()]
        st.dataframe(pd.DataFrame(default_rows), use_container_width=True, height=220)

        st.markdown("**🛠️ Custom Assets** *(editable)*")
        if custom_assets:
            custom_df = pd.DataFrame(custom_assets)[["keyword","weight","tier","added_by","added_on"]]
            custom_df.columns = ["Keyword","Weight (Wi)","Asset Tier","Added By","Date Added"]
            st.dataframe(custom_df, use_container_width=True, height=220)
        else:
            st.markdown('<div class="info-box">No custom assets yet. Add one below.</div>', unsafe_allow_html=True)

    with am2:
        st.markdown('<div class="sec-title">➕ Add New Asset</div>', unsafe_allow_html=True)
        with st.form("add_asset_form"):
            new_kw   = st.text_input("Keyword / Phrase", placeholder="e.g. surgery report")
            new_w    = st.slider("Asset Weight (Wi)", min_value=0.1, max_value=1.0, value=0.85, step=0.05)
            new_tier = st.selectbox("Asset Tier", ASSET_TIERS)
            new_desc = st.text_input("Description", placeholder="Short description...")
            new_by   = st.text_input("Added By", placeholder="IT Admin / Your name")
            add_btn  = st.form_submit_button("➕ Add Asset", use_container_width=True)

            if add_btn and new_kw.strip():
                new_asset = {
                    "keyword":    new_kw.strip().lower(),
                    "weight":     float(new_w),
                    "tier":       new_tier,
                    "description":new_desc,
                    "added_by":   new_by if new_by else "IT Admin",
                    "added_on":   datetime.now().strftime("%Y-%m-%d"),
                }
                existing_kws = [a["keyword"] for a in custom_assets]
                if new_asset["keyword"] in existing_kws:
                    st.error(f"⚠️ Keyword '{new_asset['keyword']}' already exists!")
                else:
                    custom_assets.append(new_asset)
                    save_custom_assets(custom_assets)
                    st.success(f"✅ Added: '{new_asset['keyword']}' (Wi={new_w})")
                    st.cache_data.clear()
                    st.rerun()
            elif add_btn:
                st.warning("⚠️ Keyword cannot be empty.")

    st.markdown('<hr style="border:none;height:1px;background:#1D3364;margin:24px 0;">', unsafe_allow_html=True)

    if custom_assets:
        st.markdown('<div class="sec-title">🗑️ Remove Custom Asset</div>', unsafe_allow_html=True)
        del1, del2 = st.columns([3, 1])
        with del1:
            kw_to_delete = st.selectbox("Select keyword to remove", [a["keyword"] for a in custom_assets], key="del_kw")
        with del2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete Selected", key="del_btn"):
                custom_assets = [a for a in custom_assets if a["keyword"] != kw_to_delete]
                save_custom_assets(custom_assets)
                st.success(f"✅ Removed: '{kw_to_delete}'")
                st.cache_data.clear()
                st.rerun()


def render_phi_registry_page(all_sheets):
    """
    Master Asset Registry showing ALL 15 CSV sheets from the data Sheets directory.
    """
    if not all_sheets:
        st.error("❌ Data Sheets directory not found or empty.")
        return

    st.markdown('<div class="sec-title">📂 Select Data Sheet (CSV)</div>', unsafe_allow_html=True)
    sheet_names = list(all_sheets.keys())
    
    selected_sheet = st.selectbox("Active Data Sheet", sheet_names, key="sel_sheet")
    df_sheet = all_sheets[selected_sheet]

    st.markdown(f'<div style="font-family:monospace;font-size:13px;color:#38BDF8;margin-bottom:16px;">Active Sheet: <strong>{selected_sheet}.csv</strong> · Showing {len(df_sheet):,} records · ASSET WEIGHT = <strong style="color:#F59E0B;">{df_sheet["ASSET WEIGHT"].iloc[0] if "ASSET WEIGHT" in df_sheet.columns and not df_sheet.empty else 0.95}</strong></div>', unsafe_allow_html=True)
    
    # Filter within sheet
    st.markdown('**🔍 Filter Current Sheet**')
    sh_col1, sh_col2 = st.columns(2)
    with sh_col1:
        search_txt = st.text_input("Search any column text...", key="sh_search")
    with sh_col2:
        if "SENSITIVITY LEVEL" in df_sheet.columns:
            sen_flt = st.selectbox("Sensitivity Level", ["All"] + sorted(df_sheet["SENSITIVITY LEVEL"].dropna().unique().tolist()), key="sh_sen")
        else:
            sen_flt = "All"

    f_df = df_sheet.copy()
    if search_txt:
        mask = f_df.astype(str).apply(lambda x: x.str.contains(search_txt, case=False)).any(axis=1)
        f_df = f_df[mask]
    if sen_flt != "All":
        f_df = f_df[f_df["SENSITIVITY LEVEL"] == sen_flt]

    st.dataframe(f_df, use_container_width=True, height=450)

    csv_phi = f_df.to_csv(index=False).encode("utf-8")
    st.download_button(f"📥 Export {selected_sheet} CSV", csv_phi, f"{selected_sheet}_registry.csv", "text/csv")


def render_wrse_ref_page(custom_assets):
    """
    WRSE Reference explaining the mathematics and exact matching priorities.
    """
    wr1, wr2 = st.columns(2)
    with wr1:
        st.markdown('<div class="sec-title">📌 Equation 1 — Sensitivity Score</div>', unsafe_allow_html=True)
        st.markdown("""<div class="host-card">
<div style="font-size:18px;font-weight:800;color:#E2EBF8;font-family:monospace;margin-bottom:10px;">S = &Sigma; (W&iota; &times; C&iota;)</div>
<div style="font-size:12px;color:#647E9C;font-family:monospace;line-height:1.8;">
<strong>Master Asset Match Mode (Primary & Multi-Asset):</strong><br>
&nbsp;&nbsp;S = &Sigma; CSV ASSET WEIGHTS (0.95/0.90/0.85) — sums weights for ALL distinct assets leaked in a single payload (capped at 1.0)<br><br>
<strong>Fallback Mode (No match):</strong><br>
&nbsp;&nbsp;W&iota; = keyword weight (0.0–1.0)<br>
&nbsp;&nbsp;C&iota; = keyword occurrence count<br>
&nbsp;&nbsp;+ IP sniffer (+0.95 if IPv4 found)
</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-title" style="margin-top:20px;">📌 Equation 2 — Final Risk Score</div>', unsafe_allow_html=True)
        st.markdown("""<div class="host-card">
<div style="font-size:18px;font-weight:800;color:#E2EBF8;font-family:monospace;margin-bottom:10px;">RS = (0.50&times;S) + (0.25&times;D) + (0.25&times;U)</div>
<div style="font-size:12px;color:#647E9C;font-family:monospace;line-height:1.8;">
S = Sensitivity Score (from CSV or Eq.1)<br>
D = Destination Trust (0.95 if AI platform)<br>
U = User Profile Weight (0.90 / 0.65)<br>
<strong style="color:#FF2D5B;">CRITICAL if RS &gt; 80 &nbsp;|&nbsp; MEDIUM 55–80 &nbsp;|&nbsp; LOW &lt; 55</strong>
</div>
</div>""", unsafe_allow_html=True)

    with wr2:
        st.markdown('<div class="sec-title">🔍 Master 15-Sheet CSV Multi-Asset Matcher</div>', unsafe_allow_html=True)
        st.markdown("""<div class="host-card">
<div style="font-size:12px;color:#647E9C;font-family:monospace;line-height:1.8;">
<strong style="color:#E2EBF8;">Multi-Asset Support:</strong> Detects and extracts multiple distinct assets leaked within the same prompt/payload.<br>
<strong style="color:#E2EBF8;">Priority 1:</strong> RECORD ID (e.g. IAM-670469, INS-985884, VND-723528)<br>
<strong style="color:#E2EBF8;">Priority 2:</strong> PATIENT ID (e.g. TM-XXXX-XXXX)<br>
<strong style="color:#E2EBF8;">Priority 3:</strong> Substrings & Hashes → SAML Token, API Key, Git Repo, Subnet, Unique Identifiers<br>
<br>When matched: S = &Sigma; CSV ASSET WEIGHTS<br>
Display: Aggregated CSV SENSITIVITY LEVEL & Tags<br>
Covers all 15 individual CSV sheets across Tiers 1, 2, and 3
</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-title" style="margin-top:20px;">🗂️ All Asset Keywords</div>', unsafe_allow_html=True)
        all_kw_df = pd.DataFrame(
            [{"Keyword": k, "Wi": v[0], "Tier": v[1], "Source": "System"} for k, v in DEFAULT_KEYWORDS.items()] +
            [{"Keyword": a["keyword"], "Wi": a["weight"], "Tier": a["tier"], "Source": "Custom"} for a in custom_assets]
        ).sort_values("Wi", ascending=False)
        st.dataframe(all_kw_df, use_container_width=True, height=240)
