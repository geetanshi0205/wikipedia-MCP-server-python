# Wikipedia MCP Server

A Model Context Protocol (MCP) server that provides Wikipedia search and article retrieval capabilities. This server allows Claude to search Wikipedia, get article summaries, retrieve full articles, explore sections, and find related topics.

## Features

- **Search Wikipedia**: Search for articles matching a query
- **Get Article Summary**: Retrieve concise summaries of Wikipedia articles
- **Get Full Article**: Fetch complete article content with sections
- **Get Article Sections**: List all sections in an article
- **Get Article Links**: Retrieve links contained within an article
- **Get Related Topics**: Find topics related to an article based on categories

## Installation

1. **Clone or download this repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup with Claude Desktop

### Method 1: Using Python directly

1. **Add to Claude Desktop configuration**:
   
   On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   
   On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add this configuration**:
   ```json
   {
     "mcpServers": {
       "wikipedia": {
         "command": "python",
         "args": ["/path/to/your/wikipedia-mcp/server.py"],
         "env": {}
       }
     }
   }
   ```

### Method 2: Using UV (Recommended)

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Add to Claude Desktop configuration**:
   ```json
   {
     "mcpServers": {
       "wikipedia": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/your/wikipedia-mcp",
           "run",
           "server.py"
         ],
         "env": {}
       }
     }
   }
   ```

### Method 3: Using virtual environment

1. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Add to Claude Desktop configuration**:
   ```json
   {
     "mcpServers": {
       "wikipedia": {
         "command": "/path/to/your/wikipedia-mcp/venv/bin/python",
         "args": ["/path/to/your/wikipedia-mcp/server.py"],
         "env": {}
       }
     }
   }
   ```

## Configuration Steps

1. **Find your Claude Desktop config file location**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Create or edit the config file** with one of the methods above

3. **Replace `/path/to/your/wikipedia-mcp`** with the actual path to this directory

4. **Restart Claude Desktop** completely (quit and reopen)

5. **Verify connection**: Look for a 🔌 icon next to the input box in Claude Desktop

## Available Tools

Once configured, Claude will have access to these Wikipedia tools:

### `search_wikipedia(query: str, limit: int = 10)`
Search Wikipedia for articles matching a query.
- `query`: Search terms
- `limit`: Maximum number of results (1-20)

### `get_wikipedia_summary(title: str)`
Get a concise summary of a Wikipedia article.
- `title`: Article title

### `get_wikipedia_article(title: str)`
Get the full content of a Wikipedia article including sections.
- `title`: Article title

### `get_wikipedia_sections(title: str)`
Get the sections of a Wikipedia article.
- `title`: Article title

### `get_wikipedia_links(title: str, limit: int = 20)`
Get links contained within a Wikipedia article.
- `title`: Article title
- `limit`: Maximum number of links (1-50)

### `get_related_topics(title: str, limit: int = 10)`
Get topics related to an article based on categories.
- `title`: Article title
- `limit`: Maximum number of related topics

## Example Usage

After setup, you can ask Claude:

- "Search Wikipedia for information about quantum computing"
- "Get a summary of the article about Marie Curie"
- "What are the main sections in the Python programming language article?"
- "Find articles related to machine learning"
- "Get links from the artificial intelligence Wikipedia page"

## Troubleshooting

### Server not connecting
1. Check that the path in your config file is correct
2. Ensure Python can find all dependencies: `pip install -r requirements.txt`
3. Test the server directly: `python server.py`
4. Restart Claude Desktop completely

### Permission errors
- Make sure the Python executable and script files are readable
- On macOS/Linux, you may need: `chmod +x server.py`

### Import errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Consider using a virtual environment to avoid conflicts

## Development

To modify or extend the server:

1. **Edit `server.py`** to add new tools or modify existing ones
2. **Use the `@mcp.tool()` decorator** for new functions
3. **Follow the existing pattern** for Wikipedia API calls
4. **Test changes** by restarting Claude Desktop

## API Rate Limiting

This server respects Wikipedia's API guidelines:
- Uses proper User-Agent headers
- Implements reasonable timeouts
- Limits result counts to prevent overwhelming requests

## License

This project is open source. Please respect Wikipedia's terms of service and API guidelines when using this server.