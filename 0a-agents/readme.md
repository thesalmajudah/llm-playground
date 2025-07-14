# 🧠 BONUS – AI Agents

![Agents Overview](agents.png)

## 🚀 Agents, Function Calling & Tool Integration

This module was all about turning LLMs into intelligent *agents* — systems that can reason, plan, and interact with tools.

I built an **LLM-powered chatbot** that:

- Takes user questions
- Searches or generates answers
- Writes new entries back into a database using **tool calls** 💾

---

## 💡 Key Learnings

### 🧠 Agents
- LLMs become more than responders — they can plan and decide which tools to invoke.

### 🔧 Function Calling
- Structured JSON schema enables the LLM to understand external functions.
- Used **Groq** to power fast LLM function invocation.

### 🔗 Tool Use
- Tools were defined as Python functions with metadata.
- LLM decides which tool to use, what arguments to pass, and integrates the result.

### 🔁 MCP (Model Context Protocol)
- Used `FastMCP` to simulate a lightweight server that LLMs can call over stdio using JSON-RPC.
- Built a custom `MCPClient` and `MCPTools` wrapper to plug external tools into the chat interface.

---

## 🛠 Agent Workflow

```mermaid
flowchart TD
    User -->|question| Chatbot
    Chatbot -->|tool call| Tool[get_weather / add_entry]
    Tool -->|result| Chatbot
    Chatbot -->|final response| User
