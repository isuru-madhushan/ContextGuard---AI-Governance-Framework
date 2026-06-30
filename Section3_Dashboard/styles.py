# ══════════════════════════════════════════════════════════════════════════════
# 🎨 THREATMON-STYLE ADVANCED CSS DESIGNS (FIXED COLLAPSE BUG & SIDEBAR MENU)
# ══════════════════════════════════════════════════════════════════════════════

THREATMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    /* Exact ThreatMon screenshot palette */
    --bg-base:      #050B1A; 
    --bg-panel:     #0A142B;
    --bg-card:      #111E3E;
    --bg-card-hover:#16274E;
    --border:       #1D3364;
    --border-glow:  rgba(24, 119, 242, 0.3);
    
    /* ThreatMon Icon Palette */
    --tm-blue:      #1877F2;
    --tm-orange:    #FF8A00;
    --tm-purple:    #8B5CF6;
    --tm-red:       #FF2D5B;
    --tm-cyan:      #06B6D4;
    --tm-green:     #10B981;
    --tm-navy:      #1E3E62;
    
    --text-main:    #E2EBF8;
    --text-muted:   #647E9C;
    --text-sub:     #8C9BAE;
    
    --grad-main:    linear-gradient(135deg, #1877F2, #00D4AA);
}

/* ── BASE RESET ── */
html, body, .stApp { 
    background: var(--bg-base) !important; 
    color: var(--text-main) !important; 
    font-family: 'Inter', sans-serif !important; 
}
#MainMenu, footer, .stDeployButton { visibility: hidden; display: none; }

/* ── FIXED STREAMLIT SIDEBAR COLLAPSE / REOPEN BUG ── */
header { 
    background: transparent !important; 
    box-shadow: none !important;
}
[data-testid="collapsedControl"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #1877F2 !important; 
    background: #0A142B !important; 
    border: 1px solid #1D3364 !important; 
    border-radius: 8px !important; 
    padding: 6px 10px !important; 
    margin-top: 12px !important;
    margin-left: 12px !important;
    z-index: 999999 !important; 
    box-shadow: 0 4px 14px rgba(0,0,0,0.4) !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
[data-testid="collapsedControl"]:hover {
    background: #111E3E !important;
    border-color: #1877F2 !important;
    box-shadow: 0 4px 16px rgba(24,119,242,0.4) !important;
}

/* ── THREATMON EXACT SIDEBAR MENU ── */
[data-testid="stSidebar"] {
    background: #040916 !important;
    border-right: 1px solid var(--border) !important;
}
.sb-brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}
.sb-logo-icon {
    font-size: 28px;
    color: var(--tm-blue);
    filter: drop-shadow(0 0 10px rgba(24,119,242,0.6));
}
.sb-brand-text {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #FFFFFF;
}
.sb-menu-title {
    font-size: 11px;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-muted);
    letter-spacing: 1px;
    padding: 4px 14px;
    margin-top: 12px;
    margin-bottom: 8px;
}

/* ── CONTEXTGUARD SIDEBAR MENU STYLING (FLAWLESS NO-CIRCLE PREMIUM LOOK) ── */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    padding: 0 12px !important;
    background: transparent !important;
    border: none !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    width: 100% !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    border-radius: 8px !important;
    background: transparent !important;
    border: none !important;
    color: #8C9BAE !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    text-align: left !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    transition: all 0.2s ease-in-out !important;
    cursor: pointer !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    color: #FFFFFF !important;
    background: rgba(6, 182, 212, 0.15) !important;
    border: none !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"],
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, #06B6D4 0%, #0284C7 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.35) !important;
    font-weight: 700 !important;
    border: none !important;
}
/* HIDE STREAMLIT RADIO CIRCLES ENTIRELY & ASSURE FLAWLESS LEFT ALIGNMENT IN SIDEBAR */
section[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"],
section[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stRadioButton"] > div:first-child,
section[data-testid="stSidebar"] div[role="radiogroup"] label span[data-baseweb="radio"] > div:first-child {
    display: none !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label div:not(:has(p)):not(:has(input)) {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label div:has(p) {
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #8C9BAE !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    width: 100% !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] p,
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    background: transparent !important;
    border: none !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stRadioButton"],
section[data-testid="stSidebar"] div[role="radiogroup"] label span[data-baseweb="radio"] {
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 0px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label[data-testid="stWidgetLabel"] {
    display: none !important;
}

/* ── MAIN PAGE HORIZONTAL RADIO BUTTONS (ULTRA-PREMIUM GLASSMORPHISM SEGMENTED CONTROL) ── */
section[data-testid="stMain"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 10px !important;
    background: linear-gradient(135deg, rgba(16, 29, 66, 0.85) 0%, rgba(11, 21, 48, 0.95) 100%) !important;
    backdrop-filter: blur(12px) !important;
    padding: 8px 10px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 15px rgba(6, 182, 212, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    height: 58px !important;
    min-height: 58px !important;
    max-height: 58px !important;
    box-sizing: border-box !important;
}
section[data-testid="stMain"] div[role="radiogroup"]:hover {
    border: 1px solid rgba(6, 182, 212, 0.8) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45), 0 0 25px rgba(6, 182, 212, 0.35) !important;
    transform: translateY(-2px) !important;
}
section[data-testid="stMain"] div[role="radiogroup"] > label {
    padding: 0 20px !important;
    margin: 0 !important;
    border-radius: 8px !important;
    background: transparent !important;
    border: none !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    line-height: 1 !important;
    box-sizing: border-box !important;
}
section[data-testid="stMain"] div[role="radiogroup"] > label:hover {
    color: #FFFFFF !important;
    background: rgba(6, 182, 212, 0.2) !important;
    box-shadow: 0 0 12px rgba(6, 182, 212, 0.2) !important;
}
section[data-testid="stMain"] div[role="radiogroup"] > label[aria-checked="true"],
section[data-testid="stMain"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, #0EA5E9 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
    font-weight: 700 !important;
}
/* HIDE STREAMLIT RADIO CIRCLES IN MAIN PAGE */
section[data-testid="stMain"] div[role="radiogroup"] input[type="radio"],
section[data-testid="stMain"] div[role="radiogroup"] label div[data-testid="stRadioButton"] > div:first-child,
section[data-testid="stMain"] div[role="radiogroup"] label span[data-baseweb="radio"] > div:first-child {
    display: none !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stMain"] div[role="radiogroup"] label div:not(:has(p)):not(:has(input)) {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stMain"] div[role="radiogroup"] label p {
    font-size: 13px !important;
    font-weight: inherit !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}
section[data-testid="stMain"] div[role="radiogroup"] > label[aria-checked="true"] p,
section[data-testid="stMain"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* ── MAIN PAGE CHECKBOX (ULTRA-PREMIUM SYMMETRICAL TOGGLE BUTTON STYLING WITH CUSTOM TICK & GAP) ── */
section[data-testid="stMain"] div[data-testid="stCheckbox"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: linear-gradient(135deg, rgba(16, 29, 66, 0.85) 0%, rgba(11, 21, 48, 0.95) 100%) !important;
    backdrop-filter: blur(12px) !important;
    padding: 8px 12px !important;
    margin: 0 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 15px rgba(6, 182, 212, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-sizing: border-box !important;
    width: max-content !important;
    min-width: max-content !important;
    white-space: nowrap !important;
    height: 58px !important;
    min-height: 58px !important;
    max-height: 58px !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"]:hover {
    border: 1px solid rgba(6, 182, 212, 0.8) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45), 0 0 25px rgba(6, 182, 212, 0.35) !important;
    transform: translateY(-2px) !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"] label {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 12px !important;
    margin: 0 auto !important;
    padding: 0 !important;
    width: max-content !important;
    min-width: max-content !important;
    white-space: nowrap !important;
    cursor: pointer !important;
    box-sizing: border-box !important;
    height: 100% !important;
}
/* CUSTOM CYAN TICK BOX STYLING (PERFECT VERTICAL & HORIZONTAL ALIGNMENT) */
section[data-testid="stMain"] div[data-testid="stCheckbox"] input[type="checkbox"] + span,
section[data-testid="stMain"] div[data-testid="stCheckbox"] input[type="checkbox"] + div,
section[data-testid="stMain"] div[data-testid="stCheckbox"] label > span:first-of-type:not(:has(p)),
section[data-testid="stMain"] div[data-testid="stCheckbox"] label > div:first-of-type:not(:has(p)) {
    background-color: #0A1329 !important;
    border: 2px solid #1D3364 !important;
    border-radius: 6px !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 22px !important;
    height: 22px !important;
    flex: 0 0 22px !important;
    transition: all 0.2s ease-in-out !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"]:hover input[type="checkbox"] + span,
section[data-testid="stMain"] div[data-testid="stCheckbox"]:hover input[type="checkbox"] + div,
section[data-testid="stMain"] div[data-testid="stCheckbox"]:hover label > span:first-of-type:not(:has(p)),
section[data-testid="stMain"] div[data-testid="stCheckbox"]:hover label > div:first-of-type:not(:has(p)) {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.3) !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"] input[type="checkbox"]:checked + span,
section[data-testid="stMain"] div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div,
section[data-testid="stMain"] div[data-testid="stCheckbox"]:has(input[type="checkbox"]:checked) label > span:first-of-type:not(:has(p)),
section[data-testid="stMain"] div[data-testid="stCheckbox"]:has(input[type="checkbox"]:checked) label > div:first-of-type:not(:has(p)) {
    background: linear-gradient(90deg, #06B6D4 0%, #0284C7 100%) !important;
    background-color: #06B6D4 !important;
    border: none !important;
    box-shadow: 0 0 12px rgba(6, 182, 212, 0.4) !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"] input[type="checkbox"] + span svg,
section[data-testid="stMain"] div[data-testid="stCheckbox"] input[type="checkbox"] + div svg,
section[data-testid="stMain"] div[data-testid="stCheckbox"] label > span:first-of-type:not(:has(p)) svg,
section[data-testid="stMain"] div[data-testid="stCheckbox"] label > div:first-of-type:not(:has(p)) svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
    width: 14px !important;
    height: 14px !important;
    margin: 0 !important;
    padding: 0 !important;
}
/* TURN THE TEXT CONTAINER INTO A GORGEOUS TAB BUTTON WITH PERFECT CENTERING */
section[data-testid="stMain"] div[data-testid="stCheckbox"] label > div {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 20px !important;
    margin: 0 !important;
    border-radius: 8px !important;
    background: transparent !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: max-content !important;
    min-width: max-content !important;
    white-space: nowrap !important;
    flex: 0 0 max-content !important;
    text-align: center !important;
    box-sizing: border-box !important;
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    line-height: 1 !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"] label:hover > div {
    color: #FFFFFF !important;
    background: rgba(6, 182, 212, 0.2) !important;
    box-shadow: 0 0 12px rgba(6, 182, 212, 0.2) !important;
}
section[data-testid="stMain"] div[data-testid="stCheckbox"]:has(input[type="checkbox"]:checked) label > div,
section[data-testid="stMain"] div[data-testid="stCheckbox"] label:has(input[type="checkbox"]:checked) > div,
section[data-testid="stMain"] div[data-testid="stCheckbox"] label[aria-checked="true"] > div {
    background: linear-gradient(90deg, #0EA5E9 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
    font-weight: 700 !important;
}

/* ── ELITE CONTROL DECK COLUMNS (PERFECTLY TIGHT GAP & 100% HORIZONTAL ALIGNMENT) ── */
section[data-testid="stMain"] div[data-testid="stColumns"]:has(div[data-testid="stRadio"]),
section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(div[data-testid="stRadio"]),
section[data-testid="stMain"] div[data-testid="columns"]:has(div[data-testid="stRadio"]) {
    display: flex !important;
    gap: 15px !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stMain"] div[data-testid="stColumns"]:has(div[data-testid="stRadio"]) > div[data-testid="stColumn"],
section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(div[data-testid="stRadio"]) > div[data-testid="stColumn"],
section[data-testid="stMain"] div[data-testid="columns"]:has(div[data-testid="stRadio"]) > div[data-testid="column"] {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: fit-content !important;
    display: flex !important;
    align-items: flex-start !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stMain"] div[data-testid="stColumns"]:has(div[data-testid="stRadio"]) div[data-testid="stVerticalBlock"],
section[data-testid="stMain"] div[data-testid="stColumns"]:has(div[data-testid="stRadio"]) div[data-testid="stVerticalBlockBorderWrapper"],
section[data-testid="stMain"] div[data-testid="stColumns"]:has(div[data-testid="stRadio"]) div[data-testid="stRadio"] {
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: flex-start !important;
    gap: 0 !important;
}

.live-badge { 
    display: flex; 
    align-items: center; 
    gap: 8px; 
    background: rgba(16,185,129,.08); 
    border: 1px solid rgba(16,185,129,.25); 
    border-radius: 6px; 
    padding: 8px 14px; 
    margin: 0 20px 16px; 
}
.live-dot { 
    width: 8px; 
    height: 8px; 
    border-radius: 50%; 
    background: var(--tm-green); 
    box-shadow: 0 0 10px var(--tm-green); 
    animation: blink 1.5s ease-in-out infinite; 
}
.live-txt { 
    font-size: 11px; 
    font-family: 'JetBrains Mono', monospace; 
    color: var(--tm-green); 
    font-weight: 700; 
    letter-spacing: 1px; 
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* ── SCREENSHOT TOP TITLE ── */
.tm-main-title {
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 20px;
    padding-left: 4px;
    letter-spacing: 0.5px;
}

/* ── THREATMON TOP ASSETS STRIP ── */
.tm-asset-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 24px;
    gap: 16px;
    overflow-x: auto;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.tm-asset-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-width: 75px;
    cursor: pointer;
    transition: transform 0.2s;
}
.tm-asset-item:hover {
    transform: translateY(-3px);
}
.tm-icon-circle {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 10px;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}
.tm-icon-blue   { background: var(--tm-blue);   box-shadow: 0 0 12px rgba(24,119,242,0.4); }
.tm-icon-orange { background: var(--tm-orange); box-shadow: 0 0 12px rgba(255,138,0,0.4); }
.tm-icon-purple { background: var(--tm-purple); box-shadow: 0 0 12px rgba(139,92,246,0.4); }
.tm-icon-red    { background: var(--tm-red);    box-shadow: 0 0 12px rgba(255,45,91,0.4); }
.tm-icon-green  { background: var(--tm-green);  box-shadow: 0 0 12px rgba(16,185,129,0.4); }
.tm-icon-cyan   { background: var(--tm-cyan);   box-shadow: 0 0 12px rgba(6,182,212,0.4); }
.tm-icon-navy   { background: var(--tm-navy);   box-shadow: 0 0 12px rgba(30,62,98,0.4); }

.tm-asset-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-main);
    line-height: 1.1;
}
.tm-asset-lbl {
    font-size: 11px;
    color: var(--text-sub);
    margin-top: 4px;
    font-weight: 500;
}

/* ── MIDDLE CHARTS CARDS ── */
.tm-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.tm-card-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── CUSTOM HORIZONTAL STACKED BAR (Main Domains Type) ── */
.stacked-bar-legend {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 20px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: var(--text-sub);
}
.legend-box { width: 12px; height: 8px; border-radius: 2px; }

.stacked-bar-container {
    height: 70px;
    width: 100%;
    display: flex;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin-bottom: 10px;
}
.stacked-segment {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 16px;
    transition: opacity 0.2s;
}
.stacked-segment:hover { opacity: 0.9; }

/* ── CUSTOM DONUT CHART (Active/Passive DNS) ── */
.donut-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
}
.donut-ring {
    position: relative;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: conic-gradient(#FB7185 0% 75%, #A78BFA 75% 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.donut-hole {
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: var(--bg-panel);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 800;
    color: white;
}
.donut-legend {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 20px;
}

/* ── FILTER CONTAINER ── */
.tm-filter-container {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.tm-filter-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 16px;
}
.tm-actions-link {
    color: var(--text-sub);
    font-size: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* ── THREATMON DATA TABLE ── */
.tm-table-container {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.tm-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 12px;
}
.tm-table th {
    background: #0A142B;
    color: var(--text-muted);
    font-weight: 600;
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.tm-table td {
    padding: 16px 18px;
    border-bottom: 1px solid var(--border);
    color: var(--text-main);
}
.tm-table tr:hover td {
    background: var(--bg-card-hover);
}
.tm-table td.kw-col {
    color: #38BDF8;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}
.tm-table td.ip-col {
    font-family: 'JetBrains Mono', monospace;
    color: #E2EBF8;
}

/* ── STATUS PILLS & TOGGLES ── */
.pill-passive {
    background: rgba(244, 63, 94, 0.15);
    border: 1px solid rgba(244, 63, 94, 0.4);
    color: #FB7185;
    padding: 4px 12px;
    border-radius: 14px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}
.pill-active {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34D399;
    padding: 4px 12px;
    border-radius: 14px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}
.pill-custom {
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #C4B5FD;
    padding: 4px 12px;
    border-radius: 14px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}
.tm-switch {
    width: 34px;
    height: 18px;
    background: #1877F2;
    border-radius: 10px;
    position: relative;
    display: inline-block;
    cursor: pointer;
}
.tm-switch::after {
    content: '';
    position: absolute;
    right: 2px;
    top: 2px;
    width: 14px;
    height: 14px;
    background: white;
    border-radius: 50%;
}
.tm-action-dots {
    color: var(--text-muted);
    font-size: 16px;
    cursor: pointer;
    padding: 4px;
}
.tm-action-dots:hover { color: white; }

/* ── PAGE HEADERS & METRICS ── */
.pg-header { 
    background: linear-gradient(135deg, #111E3E, #0A142B); 
    border: 1px solid var(--border); 
    border-radius: 12px; 
    padding: 24px 28px; 
    margin-bottom: 24px; 
    position: relative; 
    overflow: hidden; 
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.pg-header::before { 
    content: ''; 
    position: absolute; 
    top: 0; left: 0; right: 0; 
    height: 3px; 
    background: var(--grad-main); 
}
.pg-title { 
    font-size: 22px; 
    font-weight: 900; 
    letter-spacing: -0.5px; 
    color: #FFFFFF; 
}
.pg-sub { 
    font-size: 11px; 
    font-family: 'JetBrains Mono', monospace; 
    color: var(--tm-cyan); 
    letter-spacing: 1.5px; 
    text-transform: uppercase; 
    margin-top: 4px; 
}

/* ── ALERT CARDS & PHI INLINES ── */
.alert-card { 
    background: #0A142B; 
    border: 1px solid var(--border); 
    border-radius: 10px; 
    padding: 16px 20px; 
    margin-bottom: 12px; 
    transition: all 0.2s; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.alert-card:hover { 
    border-color: var(--tm-blue); 
    box-shadow: 0 6px 20px rgba(24,119,242,0.2); 
}
.alert-card.c-CRITICAL { border-left: 4px solid var(--tm-red); background: rgba(255,45,91,.04); }
.alert-card.c-MEDIUM   { border-left: 4px solid var(--tm-orange); background: rgba(255,138,0,.03); }
.alert-card.c-LOW      { border-left: 4px solid var(--tm-green); background: rgba(16,185,129,.03); }
.alert-card.c-PHI      { border-left: 4px solid var(--tm-purple); background: rgba(139,92,246,.06); }

.alert-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
.alert-ts { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted); }
.alert-score { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 800; margin-left: auto; }
.alert-flow { font-size: 14px; font-weight: 600; color: var(--text-main); margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.alert-body { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #8C9BAE; line-height: 1.6; }

.sev-CRITICAL { background: rgba(255,45,91,.15); border: 1px solid rgba(255,45,91,.4); color: #FF8099; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 14px; letter-spacing: 0.8px; }
.sev-MEDIUM   { background: rgba(255,138,0,.15); border: 1px solid rgba(255,138,0,.4); color: #FCD34D; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 14px; letter-spacing: 0.8px; }
.sev-LOW      { background: rgba(16,185,129,.15); border: 1px solid rgba(16,185,129,.4); color: #6EE7B7; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 14px; letter-spacing: 0.8px; }
.phi-tag      { background: rgba(139,92,246,.15); border: 1px solid rgba(139,92,246,.4); color: #C4B5FD; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; padding: 2px 10px; border-radius: 14px; letter-spacing: 0.8px; }

.score-bar-wrap { background: rgba(255,255,255,.05); border-radius: 3px; height: 4px; margin-top: 12px; overflow: hidden; }
.score-bar { height: 100%; border-radius: 3px; }

.phi-record-inline { 
    margin-top: 12px; 
    padding: 12px 16px; 
    background: rgba(139,92,246,.08); 
    border: 1px solid rgba(139,92,246,.25); 
    border-radius: 8px; 
    font-family: 'JetBrains Mono', monospace; 
    font-size: 11px; 
    color: #C4B5FD; 
    line-height: 1.8; 
}

/* ── STREAMLIT WIDGET ASSIMILATION (PERFECT UNIFIED BASEWEB STYLING) ── */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div, 
div[data-baseweb="base-input"] > div {
    background-color: #111E3E !important; 
    border: 1px solid var(--border) !important;
    border-radius: 8px !important; 
    color: var(--text-main) !important;
    font-family: 'JetBrains Mono', monospace !important; 
    font-size: 13px !important;
    min-height: 38px !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 12px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
    margin: 0 !important;
}

div[data-baseweb="select"] > div:hover, 
div[data-baseweb="input"] > div:hover,
div[data-baseweb="base-input"] > div:hover {
    border-color: var(--tm-blue) !important;
    background-color: #16274E !important;
}

div[data-baseweb="select"] > div:focus-within, 
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="base-input"] > div:focus-within {
    border-color: var(--tm-blue) !important;
    box-shadow: 0 0 10px rgba(24,119,242,0.3) !important;
}

/* MASTER FIX: Prevent ALL inner elements/wrappers from creating double borders/boxes while keeping perfect vertical text alignment */
div[data-baseweb="select"] > div div, 
div[data-baseweb="input"] > div div,
div[data-baseweb="base-input"] > div div,
div[data-baseweb="select"] > div input, 
div[data-baseweb="input"] > div input,
div[data-baseweb="base-input"] > div input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text-main) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    line-height: normal !important;
    overflow: visible !important;
}

/* Ensure inputs sit perfectly centered vertically */
div[data-baseweb="select"] > div input, 
div[data-baseweb="input"] > div input,
div[data-baseweb="base-input"] > div input {
    padding: 0 !important;
    margin: 0 !important;
    height: 100% !important;
}

/* Fix dropdown arrow container styling */
div[data-baseweb="select"] > div > div:last-child {
    background: transparent !important;
    border: none !important;
    padding: 0 4px !important;
}

/* Dropdown menu item styling */
ul[role="listbox"] {
    background-color: #0A142B !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
}
ul[role="listbox"] li {
    color: var(--text-main) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    transition: background 0.2s !important;
}
ul[role="listbox"] li:hover, ul[role="listbox"] li[aria-selected="true"] {
    background-color: #1877F2 !important;
    color: #FFFFFF !important;
}

button[kind="primary"], .stDownloadButton>button {
    background: var(--grad-main) !important; 
    border: none !important; 
    border-radius: 8px !important;
    color: white !important; 
    font-weight: 700 !important; 
    padding: 12px 20px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(24,119,242,0.3) !important;
}
button[kind="primary"]:hover, .stDownloadButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(24,119,242,0.5) !important;
}
[data-testid="stExpander"] { 
    background: #0D1B3E !important; 
    border: 1px solid #06B6D4 !important; 
    border-radius: 10px !important; 
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.15) !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    background: linear-gradient(90deg, #11224F 0%, #0C1938 100%) !important;
    color: #06B6D4 !important;
    font-weight: 700 !important;
    border-bottom: 1px solid rgba(6, 182, 212, 0.3) !important;
    padding: 12px 18px !important;
}
[data-testid="stExpander"] summary p {
    color: #06B6D4 !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}
[data-testid="stForm"] { 
    background: #0A142B !important; 
    border: 1px solid var(--border) !important; 
    border-radius: 12px !important; 
    padding: 24px !important; 
}
.sec-title { 
    font-size: 14px; 
    font-weight: 700; 
    color: var(--text-main); 
    display: flex; 
    align-items: center; 
    gap: 8px; 
    margin-bottom: 16px; 
    padding-bottom: 8px; 
    border-bottom: 1px solid var(--border); 
}
.payload-box { 
    background: #050B1A; 
    border: 1px solid rgba(24,119,242,0.2); 
    border-radius: 8px; 
    padding: 16px; 
    font-family: 'JetBrains Mono', monospace; 
    font-size: 11px; 
    color: #38BDF8; 
    line-height: 1.7; 
    max-height: 320px; 
    overflow-y: auto; 
    white-space: pre-wrap; 
    word-break: break-all; 
}
.host-card { 
    background: #111E3E; 
    border: 1px solid var(--border); 
    border-radius: 8px; 
    padding: 16px; 
}
.host-label { 
    font-size: 10px; 
    font-family: 'JetBrains Mono', monospace; 
    color: var(--text-muted); 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    margin-bottom: 4px; 
}
.host-val { 
    font-size: 14px; 
    font-family: 'JetBrains Mono', monospace; 
    color: #93C5FD; 
    font-weight: 700; 
    margin-bottom: 12px; 
    word-break: break-all; 
}
.host-val.danger { color: #FF8099; }
.host-val.ok { color: #34D399; }

/* ── STREAMLIT BUTTON STYLING (SLEEK FUTURISTIC ENTERPRISE GLOW) ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #16274E 0%, #0D1938 100%) !important;
    border: 1px solid #1D3364 !important;
    border-radius: 8px !important;
    color: #06B6D4 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 6px 16px !important;
    min-height: 38px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1D3364 0%, #16274E 100%) !important;
    border-color: #06B6D4 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 16px rgba(6, 182, 212, 0.3) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stButton"] > button:active {
    transform: translateY(1px) !important;
}

/* ── HIDE STREAMLIT RUNNING SPINNER & TOP RIGHT STATUS WIDGET ── */
div[data-testid="stStatusWidget"],
div[data-testid="stTopRightStatus"],
.stApp [data-testid="stTopRightStatus"],
.stApp [data-testid="stStatusWidget"] {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
/* ── MONITOR STATUS SELECTBOX — compact table cell style ── */
div[data-testid="stSelectbox"][aria-label="Monitor"] > div,
div[class*="stSelectbox"] > div[data-baseweb="select"] {
    min-height: 0 !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: rgba(6, 182, 212, 0.08) !important;
    border: 1px solid rgba(6, 182, 212, 0.25) !important;
    border-radius: 8px !important;
    padding: 2px 6px !important;
    min-height: 28px !important;
    font-size: 11.5px !important;
    font-family: monospace !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    cursor: pointer !important;
    transition: border-color 0.2s ease !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
    border-color: rgba(6, 182, 212, 0.6) !important;
}
</style>
"""
