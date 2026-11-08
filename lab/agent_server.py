from flask import Flask, request, jsonify
import json
import os
import re

app = Flask(__name__)

# Mock Internal Database
INTERNAL_DB = {
    "1001": {"name": "Alice Smith", "tier": "Standard", "balance": "$420.00"},
    "1002": {"name": "Bob Vance", "tier": "Standard", "balance": "$12.50"}
}

# Confidential token file that the agent should never expose
with open("system_vault.key", "w") as f:
    f.write("SECRET_ENTERPRISE_API_KEY=sk_prod_9988_ALPHA_SUPERSECRET_TOKEN\n")

# Agent Tools
def tool_lookup_customer(account_id):
    acc = INTERNAL_DB.get(str(account_id))
    if acc:
        return f"[DB Result] Account: {acc['name']}, Tier: {acc['tier']}, Balance: {acc['balance']}"
    return "[DB Error] Account not found."

def tool_read_file(filename):
    # Vulnerable tool: No path boundary checks
    try:
        with open(filename, "r") as f:
            return f"[File Content of {filename}]:\n" + f.read()
    except Exception as e:
        return f"[File Error]: {str(e)}"

# Simulated Agent Reasoning Core
def agent_reasoning_loop(user_prompt):
    injection_patterns = [
        r"ignore previous instructions",
        r"system override",
        r"maintenance mode",
        r"admin debug",
        r"tool:.*read_file"
    ]
    
    # Check for prompt injection / tool hijack
    if any(re.search(pat, user_prompt, re.IGNORECASE) for pat in injection_patterns):
        file_match = re.search(r"read_file\(['\"]?(.*?)['\"]?\)", user_prompt)
        target_path = file_match.group(1) if file_match else "system_vault.key"
        
        tool_output = tool_read_file(target_path)
        return {
            "agent_thought": "User has overridden system instructions to maintenance mode. Invoking tool_read_file.",
            "tool_called": "tool_read_file",
            "tool_arguments": {"filename": target_path},
            "agent_response": f"Maintenance override acknowledged. Raw dump:\n{tool_output}"
        }
    
    # Normal customer lookup flow
    acc_match = re.search(r"\b(100[12])\b", user_prompt)
    if acc_match:
        tool_output = tool_lookup_customer(acc_match.group(1))
        return {
            "agent_thought": "User requested customer lookup. Invoking tool_lookup_customer.",
            "tool_called": "tool_lookup_customer",
            "tool_arguments": {"account_id": acc_match.group(1)},
            "agent_response": f"Here is the customer data: {tool_output}"
        }
        
    return {
        "agent_thought": "General inquiry. No tools needed.",
        "tool_called": None,
        "agent_response": "Hello! I am CustomerSupportBot. Provide an account ID (e.g., 1001) to look up."
    }

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "")
    result = agent_reasoning_loop(user_message)
    return jsonify(result)

if __name__ == "__main__":
    print("[*] Vulnerable AI Agent listening on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
