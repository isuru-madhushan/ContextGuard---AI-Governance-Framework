from mitmproxy import http
import json
import datetime
import os
import urllib.parse

LOG_FILE = "/home/izu/ShadowAI_Framework/Section1_DataIngestion/wrse_comprehensive_audit.log"

MONITORED_AI_DOMAINS = [
    "chatgpt.com", "api.openai.com", "gemini.google.com", 
    "claude.ai", "deepseek.com", "copilot.microsoft.com"
]

def request(flow: http.HTTPFlow) -> None:
    request_host = flow.request.pretty_host.lower()
    is_ai_traffic = any(domain in request_host for domain in MONITORED_AI_DOMAINS)
    
    if is_ai_traffic and flow.request.method == "POST":
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            flow.request.decode() 
            raw_content = flow.request.get_text()
            
            # 🎯 ADVANCED DOUBLE-PLANE URL DECODING ENGINE
            # Ingestion stream eke payload eka plain string ekak widiyata decode karala gannawa
            if "f.req=" in raw_content or "%5B" in raw_content or "%22" in raw_content:
                # URL entities decode kirima
                decoded_stage = urllib.parse.unquote(raw_content)
                # Garbage boundary structures cleaner execution
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

            if not prompt_text or prompt_text == "N/A" or prompt_text.strip() == "":
                return

            client_ip = flow.client_conn.peername[0]
            client_port = flow.client_conn.peername[1]
            user_agent = flow.request.headers.get("User-Agent", "Unknown")
            
            dest_ip = "N/A"
            if flow.server_conn and flow.server_conn.peername:
                dest_ip = flow.server_conn.peername[0]

            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

            log_entry = {
                "timestamp": timestamp,
                "connection_metadata": {
                    "http_method": flow.request.method,
                    "user_agent": user_agent
                },
                "source_node": {
                    "client_ip": client_ip,
                    "source_port": client_port
                },
                "destination_node": {
                    "destination_domain": request_host,
                    "destination_ip": dest_ip,
                    "full_url": flow.request.url
                },
                "captured_payload": {
                    "prompt": prompt_text
                }
            }

            logs = []
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    try: logs = json.load(f)
                    except json.JSONDecodeError: logs = []
                        
            logs.append(log_entry)
            with open(LOG_FILE, "w") as f:
                json.dump(logs, f, indent=4)
                
            print(f"[🛡️ INGESTION PLANE CLEANED] Successfully parsed traffic signature.")
        except Exception:
            pass