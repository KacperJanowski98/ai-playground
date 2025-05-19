# OpenAI Integration with MCP

This section demonstrates how to integrate the Model Context Protocol (MCP) with OpenAI's API to create a system where OpenAI can access and use tools provided by your MCP server.

## Connection Methods

This example uses the **stdio transport** for communication between the client and server, which means:

- The client and server run in the same process
- The client directly launches the server as a subprocess
- No separate server process is needed

### Data Flow Explanation

1. **User Query**: The user sends a query to the system (e.g., "What is our company's vacation policy?")
2. **OpenAI API**: OpenAI receives the query and available tools from the MCP server
3. **Tool Selection**: OpenAI decides which tools to use based on the query
4. **MCP Client**: The client receives OpenAI's tool call request and forwards it to the MCP server
5. **MCP Server**: The server executes the requested tool (e.g., retrieving knowledge base data)
6. **Response Flow**: The tool result flows back through the MCP client to OpenAI
7. **Final Response**: OpenAI generates a final response incorporating the tool data

## How OpenAI Executes Tools

OpenAI's function calling mechanism works with MCP tools through these steps:

1. **Tool Registration**: The MCP client converts MCP tools to OpenAI's function format
2. **Tool Choice**: OpenAI decides which tools to use based on the user query
3. **Tool Execution**: The MCP client executes the selected tools and returns results
4. **Context Integration**: OpenAI incorporates the tool results into its response

## The Role of MCP

MCP serves as a standardized bridge between AI models and your backend systems:

- **Standardization**: MCP provides a consistent interface for AI models to interact with tools
- **Abstraction**: MCP abstracts away the complexity of your backend systems
- **Security**: MCP allows you to control exactly what tools and data are exposed to AI models
- **Flexibility**: You can change your backend implementation without changing the AI integration

## Implementation Details

### Server (`server.py`)

The MCP server exposes a `get_knowledge_base` tool that retrieves Q&A pairs from a JSON file.

### Client (`client.py`)

The client:

1. Connects to the MCP server
2. Converts MCP tools to OpenAI's function format
3. Handles the communication between OpenAI and the MCP server
4. Processes tool results and generates final responses

### Knowledge Base (`data/kb.json`)

Contains Q&A pairs about company policies that can be queried through the MCP server.
