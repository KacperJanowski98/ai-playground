# Long-Term Memory for AI Agents with mem0

## Quick Start
1. Create a venv with Python 3.11+
2. Install requirements
3. Run code examples
4. Run `docker compose up -d` before running the example in the `oss` folder

## What is mem0?

Mem0 is a memory architecture that enables AI agents to maintain coherent, contextually rich conversations over extended periods. Unlike traditional approaches that struggle with fixed context windows, Mem0 intelligently extracts, consolidates, and retrieves only the most salient information from conversations.

Learn more at: https://mem0.ai/research

### Key Features

- **Two-Phase Memory Pipeline**: Extraction phase captures key facts from conversations, while the Update phase intelligently manages the knowledge base
- **Selective Memory Formation**: Stores only critical information rather than entire conversation chunks
- **Intelligent Operations**: Automatically determines whether to add, update, or delete memories
- **Efficient Retrieval**: Uses vector embeddings to quickly find relevant memories
- **Graph-Enhanced Option**: Mem0ᵍ variant represents memories as a directed labeled graph for complex relational reasoning

## Core Components

### Prompts

You can view the core prompts that power Mem0's memory system here: [prompts.py](https://github.com/mem0ai/mem0/blob/main/mem0/configs/prompts.py)

1. **MEMORY_ANSWER_PROMPT**: Guides the system to answer questions based on retrieved memories, ensuring responses are accurate, concise, and always helpful even when relevant memories aren't found.

2. **FACT_RETRIEVAL_PROMPT**: The extraction phase prompt that extracts structured facts from conversations. It identifies personal preferences, details, plans, activities, health information, and professional details from conversations, organizing them into a JSON list format.

3. **DEFAULT_UPDATE_MEMORY_PROMPT**: Handles the update phase, showing how the system manages memory through four operations:
   - ADD: Creates new memory entries with new IDs
   - UPDATE: Modifies existing memories while preserving IDs
   - DELETE: Removes contradicted memories
   - NONE: Makes no changes when information is already present

4. **PROCEDURAL_MEMORY_SYSTEM_PROMPT**: Creates comprehensive summaries of agent-human interactions with structured metadata.

The `get_update_memory_messages()` function combines retrieved memories with new facts, applying the update logic to maintain a coherent, non-redundant memory store.

## How It Works

### 1. Adding Memories

When you call `memory.add()`, here's what happens:

```python
# Basic usage
memory.add(messages, user_id="user123")
```

The process follows these steps:

1. **Message Parsing**
   - Messages are parsed into a format suitable for processing
   - System messages are filtered out
   - Source: `mem0/memory/main.py`

2. **Fact Extraction**
   - The system uses an LLM to extract key facts from the conversation
   - Facts are structured into a JSON format
   - Source: `mem0/memory/main.py`

3. **Memory Management**
   - New facts are compared with existing memories
   - The system decides whether to:
     - ADD new memories
     - UPDATE existing memories
     - DELETE contradicted memories
     - Do nothing (NONE)
   - Source: `mem0/memory/main.py`

4. **Storage**
   - Memories are stored in a vector database for semantic search
   - Optional graph storage for relational information
   - History tracking for all changes

### 2. Retrieving Memories

Memories can be retrieved in three ways:

```python
# Get by ID
memory.get(memory_id)

# Search semantically
memory.search(query="What do you know about me?", user_id="user123")

# Get all memories
memory.get_all(user_id="user123")
```
