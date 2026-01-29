# MCP Server Repository

This repository contains a collection of implementations, examples, and demos for the **Model Context Protocol (MCP)**. It explores various aspects of MCP including different transports (Stdio, HTTP/SSE), capabilities (Sampling, Logging, Progress), and integrations.

## Repository Structure

- **[cli_project/](./cli_project/)**: A command-line chat application interacting with AI models via Anthropic API. Features document retrieval and command-based prompts.
- **[roots/](./roots/)**: An enhanced version of the CLI chat that adds **file system access** and **video conversion** capabilities using FFmpeg.
- **[notifications/](./notifications/)**: Demonstrates MCP's **logging** and **progress** tracking features via Stdio transport.
- **[sampling/](./sampling/)**: Demonstrates **MCP Sampling**, where the server requests the client/host application to perform LLM inference (e.g., summarizing text).
- **[transport-http/](./transport-http/)**: An example of using **HTTP** as the transport layer for MCP, complete with a simple web-based client (`index.html`) served by the application.
- **[practice/](./practice/)**: Contains various learning exercises and basic implementations:
  - **Docker/**: Containerization examples for MCP clients and servers.
  - **basic client and server/**: Fundamental examples of Client/Server pairs using SSE and Stdio transports.
  - **LLM integration/**: Experiments with integrating LLMs and knowledge bases (`kb.json`).

## Getting Started

### Prerequisites

Most projects in this repository require:
- **Python 3.10+**
- **[uv](https://github.com/astral-sh/uv)** (Recommended for dependency management) or `pip`
- An **[Anthropic API Key](https://console.anthropic.com/)** (for chat and sampling demos)

### General Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd MCP_Server
    ```

2.  **Set up Virtual Environment:**
    ```powershell
    # Windows
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    
    # Unix/MacOS
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    Each sub-project is generally a standalone Python package managed by `uv` or `pip`. 
    
    To set up a specific project (e.g., `cli_project`):
    ```bash
    cd cli_project
    uv sync
    # OR
    pip install -e .
    ```

### Running the Projects

Refer to the `README.md` within each sub-directory for specific instructions on how to run that project.

**Example (Using the MCP Inspector):**
You can debug and test any of the servers using the official [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```powershell
npx @modelcontextprotocol/inspector python <path_to_server_script.py>
```
*Note: This requires Node.js and npm to be installed.*

## Environment Configuration

Many projects in this repository rely on environment variables (specifically `ANTHROPIC_API_KEY`).
Look for `.env.example` files in the sub-directories to create your own local `.env` configuration.

## Notes

- The **[roots/](./roots/)** project requires **FFmpeg** to be installed on your system path for video conversion features to work.
- The `notes.txt` file in the root directory contains quick reference commands mainly for the `cli_project` or general debugging.
