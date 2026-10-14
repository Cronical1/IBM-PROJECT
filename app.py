"""
app.py – CyberSentinel AI Web Application Entrypoint
Flask REST API & Autonomous SecOps Center Server.
"""

import os
from flask import Flask, render_template, request, jsonify
from config import Config
from agents.orchestrator import SecOpsOrchestrator

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Lead SecOps Orchestrator
orchestrator = SecOpsOrchestrator()

SAMPLE_LOGS_DIR = os.path.join(os.path.dirname(__file__), "sample_logs")


@app.route("/", methods=["GET"])
def index():
    """
    Renders the CyberSentinel SOC Command & Operations Center Dashboard.
    """
    return render_template("index.html")


@app.route("/api/sample/<scenario_name>", methods=["GET"])
def get_sample_log(scenario_name: str):
    """
    Returns the content of a pre-configured enterprise attack scenario log.
    """
    allowed_scenarios = {
        "ssh_bruteforce": "ssh_bruteforce.log",
        "sqli_exfiltration": "sqli_exfiltration.log",
        "c2_beaconing": "c2_beaconing.log",
        "privilege_escalation": "privilege_escalation.log",
        "normal_traffic": "normal_traffic.log",
    }

    if scenario_name not in allowed_scenarios:
        return jsonify({"error": "Scenario not found"}), 404

    file_path = os.path.join(SAMPLE_LOGS_DIR, allowed_scenarios[scenario_name])
    if not os.path.exists(file_path):
        return jsonify({"error": "Sample file missing on disk"}), 404

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({"scenario": scenario_name, "logs": content})


@app.route("/api/analyze", methods=["POST"])
def analyze_logs():
    """
    Main endpoint for autonomous multi-agent log triage and threat analysis.
    Accepts raw log string or file upload.
    """
    raw_logs = ""

    # Check for file upload
    if "file" in request.files and request.files["file"].filename != "":
        uploaded_file = request.files["file"]
        raw_logs = uploaded_file.read().decode("utf-8", errors="ignore")
    elif request.is_json:
        data = request.get_json()
        raw_logs = data.get("logs", "")
    else:
        raw_logs = request.form.get("logs", "")

    if not raw_logs or not raw_logs.strip():
        return jsonify({"error": "No log data received. Please paste log text or select a scenario."}), 400

    try:
        # Run full end-to-end multi-agent pipeline
        results = orchestrator.run_pipeline(raw_logs)
        return jsonify({"status": "success", "data": results})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    System status and active capabilities diagnostic.
    """
    has_gemini = bool(Config.GEMINI_API_KEY)
    return jsonify({
        "status": "ONLINE",
        "system": "CyberSentinel AI SecOps Core",
        "gemini_api_configured": has_gemini,
        "gemini_model": Config.GEMINI_MODEL,
        "scikit_learn_mode": orchestrator.ml_agent.detector.has_sklearn
    })


if __name__ == "__main__":
    print("=" * 65)
    print("  [CYBERSENTINEL AI] Autonomous SecOps Orchestrator Online")
    print("=" * 65)
    print(f"  * Status: Online & Monitoring")
    print(f"  * AI Model: {Config.GEMINI_MODEL} (Key Configured: {bool(Config.GEMINI_API_KEY)})")
    print(f"  * Web UI: http://127.0.0.1:{Config.PORT}")
    print("=" * 65)
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
