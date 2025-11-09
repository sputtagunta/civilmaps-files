# Civil Maps Document MCP Server

Model Context Protocol (MCP) server that indexes and provides search capabilities for Civil Maps case documents.

## What it Indexes

- **220 Case Documents** (65 PDFs): Court filings from Delaware Court of Chancery §220 books and records action
- **Luminar SEC Filings** (115+ documents): SEC filings from Luminar Technologies (LAZR) from July 2022 to present

## Installation

```bash
cd mcp_server
pip install -r requirements.txt
```

## Usage with Claude Desktop

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "civil-maps-docs": {
      "command": "python3",
      "args": ["/absolute/path/to/civilmaps-files/mcp_server/server.py"]
    }
  }
}
```

## Available Tools

### 1. list_documents
List all documents with optional filtering:
- **category**: Filter by "220_case", "luminar_sec", or "all"
- **start_date**: Filter from date (YYYY-MM-DD)
- **end_date**: Filter to date (YYYY-MM-DD)
- **folder**: Filter by folder name

### 2. search_documents
Search documents by filename, form type, or folder:
- **query**: Search text
- **category**: Limit to specific category

### 3. get_document_info
Get detailed information about a specific document:
- **path**: Relative path to document

### 4. get_case_timeline
Get chronological timeline of 220 case filings with timestamps

### 5. get_sec_filings_summary
Get statistics about Luminar SEC filings:
- **form_type**: Optional filter by form type (10-K, 10-Q, 8-K, etc.)

## Available Resources

Each document is exposed as a resource with URI format: `document://path/to/file.pdf`

Resources can be read directly, with:
- PDFs: First 5 pages extracted as text
- HTML/Text: First 50KB of content

## Example Queries

**List all 220 case documents:**
```
Use the list_documents tool with category="220_case"
```

**Search for 10-K filings:**
```
Use the search_documents tool with query="10-K" and category="luminar_sec"
```

**Get timeline of court filings:**
```
Use the get_case_timeline tool
```

**Get SEC filing statistics:**
```
Use the get_sec_filings_summary tool
```

## Technical Details

- Written in Python using the MCP SDK
- Indexes documents on startup
- Provides fast search and filtering
- Integrates timeline data from timeline.json
- Supports both PDF and HTML document types

## Development

To test the server locally:

```bash
python3 server.py
```

The server runs via stdio and communicates using the Model Context Protocol.
