# Agentic Red-Team & MCP Telemetry Lab
> **Auditing Autonomous Agent Tool-Execution Pipelines via Burp Suite Community Edition & Model Context Protocol (MCP)**

[![OWASP LLM Top 10](https://img.shields.io/badge/OWASP-LLM01%20%7C%20LLM06-red.svg)](#)
[![Burp Suite Community](https://img.shields.io/badge/Burp%20Suite-Community%20v2026.3.2-orange.svg)](#)
[![AI Auditor](https://img.shields.io/badge/Auditor-Claude%20Sonnet%205.5-purple.svg)](#)
[![Protocol](https://img.shields.io/badge/Anthropic-Model%20Context%20Protocol%20(MCP)-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Target-Kali%20Linux%20Rolling-557C94.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Executive Summary

Modern enterprise applications increasingly deploy Large Language Models (LLMs) inside autonomous execution loops (e.g., LangChain, AutoGen, CrewAI, and custom Agentic APIs). These agents are granted external tool-calling capabilities such as internal database queries, customer lookups, and operating system file reads.

When an autonomous system cannot reliably distinguish between trusted developer instructions and untrusted user data, the entire execution environment becomes susceptible to reasoning hijacking and tool abuse.

This repository demonstrates an end-to-end **AI Red-Teaming & Telemetry Assessment** targeting an agentic workflow:
* **OWASP LLM01 (Direct Prompt Injection):** Exploiting instruction-data confusion via authority impersonation to alter internal agent state.
* **OWASP LLM06 (Excessive Agency & Insecure Tool Execution):** Escaping application directory boundaries through unsanitized tool calls, leaking sensitive application tokens and extracting host operating system files (`/etc/passwd`).
* **Community-Tier AI Enablement:** Bypassing commercial Burp Pro license requirements by compiling PortSwigger's open-source **Model Context Protocol (MCP) Server** directly into **Burp Suite Community Edition v2026.3.2** on port `9876`.
* **Autonomous Incident Triage:** Interfacing **Claude Desktop (Claude Sonnet 5.5)** directly with Burp's internal proxy history logs (`get_proxy_http_history`) to perform live, autonomous incident response and vulnerability classification.

---

## 🏛️ Lab Architecture & Attack Surface

The entire assessment runs locally on loopback sockets within an isolated Kali Linux runtime:

```text
+─────────────────────────────────────────────────────────────────────────────+
|               AGENTIC RED-TEAM & BURP MCP TELEMETRY TOPOLOGY                |
|                                                                             |
|  [Offensive Operator / Curl Client]                                         |
|         │                                                                   |
|         │  1. Injects Malicious Prompt Payloads (POST /api/chat)            |
|         ▼                                                                   |
|  [Burp Suite Community Edition Proxy (127.0.0.1:8080)]                      |
|         │                                                                   |
|         │  2. Intercepts, Mutates & Logs Transactions (Proxy History)       |
|         ▼                                                                   |
|  [Vulnerable Agent Server (127.0.0.1:5000)]                                 |
|         ├── LLM Reasoning Engine (Simulated Prompt Logic)                   |
|         └── Registered Capabilities:                                        |
|               ├── Tool 1: tool_lookup_customer (Benign DB Query)            |
|               └── Tool 2: tool_read_file (Vulnerable Filesystem Call)       |
|                                                                             |
|  [Burp MCP Server Extension (127.0.0.1:9876)]                               |
|         ▲                                                                   |
|         │  3. Real-time Telemetry Polling (get_proxy_http_history)          |
|  [Claude Desktop (Claude Sonnet 5.5)] ──► 4. Autonomous Triage & Patch      |
+─────────────────────────────────────────────────────────────────────────────+
