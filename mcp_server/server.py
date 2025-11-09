#!/usr/bin/env python3
"""
MCP Server for Civil Maps Document Repository
Indexes and provides search capabilities for:
- 220 Case court filings (65 PDFs)
- Luminar SEC filings (115+ documents)
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
import pypdf

# Initialize MCP server
server = Server("civil-maps-docs")

# Base paths
BASE_DIR = Path(__file__).parent.parent
CASE_220_DIR = BASE_DIR / "220 Case"
LUMINAR_SEC_DIR = BASE_DIR / "Luminar_SEC_Filings"
TIMELINE_JSON = BASE_DIR / "js" / "timeline.json"

# Load timeline data
def load_timeline_data():
    """Load the pre-extracted timeline data."""
    if TIMELINE_JSON.exists():
        with open(TIMELINE_JSON) as f:
            return json.load(f)
    return []

# Document index cache
DOCUMENT_INDEX = []

def build_document_index():
    """Build searchable index of all documents."""
    global DOCUMENT_INDEX
    DOCUMENT_INDEX = []

    # Index 220 Case files
    if CASE_220_DIR.exists():
        for root, dirs, files in os.walk(CASE_220_DIR):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(BASE_DIR)

                    DOCUMENT_INDEX.append({
                        "path": str(rel_path),
                        "filename": file,
                        "folder": Path(root).name,
                        "category": "220_case",
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })

    # Index Luminar SEC files
    if LUMINAR_SEC_DIR.exists():
        metadata_file = LUMINAR_SEC_DIR / "filings_metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)

            for filing in metadata.get("filings", []):
                filename = f"{filing['filingDate']}_{filing['form']}_{filing['primaryDocument']}"
                file_path = LUMINAR_SEC_DIR / filename

                if file_path.exists():
                    DOCUMENT_INDEX.append({
                        "path": str(file_path.relative_to(BASE_DIR)),
                        "filename": filename,
                        "filing_date": filing["filingDate"],
                        "form_type": filing["form"],
                        "accession_number": filing["accessionNumber"],
                        "category": "luminar_sec",
                        "size": file_path.stat().st_size if file_path.exists() else 0
                    })

    # Load timeline data for 220 cases
    timeline_data = load_timeline_data()
    for entry in timeline_data:
        # Find matching doc in index and add timestamp
        for doc in DOCUMENT_INDEX:
            if doc["path"] == entry["path"] and "timestamp" not in doc:
                doc["timestamp"] = entry.get("timestamp", "Unknown")

    return DOCUMENT_INDEX


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available document search and retrieval tools."""
    return [
        types.Tool(
            name="list_documents",
            description="List all documents in the repository with optional filtering by category, date range, or folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["220_case", "luminar_sec", "all"],
                        "description": "Filter by document category",
                        "default": "all"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Filter documents from this date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Filter documents up to this date (YYYY-MM-DD)"
                    },
                    "folder": {
                        "type": "string",
                        "description": "Filter by folder name (e.g., 'VERIFIED COMPLAINT', 'DEFENDANT MOTION TO DISMISS')"
                    }
                }
            }
        ),
        types.Tool(
            name="search_documents",
            description="Search documents by filename, form type, or folder name",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches filename, folder, and form type)"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["220_case", "luminar_sec", "all"],
                        "description": "Limit search to specific category",
                        "default": "all"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_document_info",
            description="Get detailed information about a specific document",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the document"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="get_case_timeline",
            description="Get the chronological timeline of 220 case filings with timestamps",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="get_sec_filings_summary",
            description="Get summary statistics of Luminar SEC filings",
            inputSchema={
                "type": "object",
                "properties": {
                    "form_type": {
                        "type": "string",
                        "description": "Filter by form type (e.g., '10-K', '10-Q', '8-K')"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""

    if not arguments:
        arguments = {}

    # Build index if not already built
    if not DOCUMENT_INDEX:
        build_document_index()

    if name == "list_documents":
        category = arguments.get("category", "all")
        start_date = arguments.get("start_date")
        end_date = arguments.get("end_date")
        folder = arguments.get("folder")

        filtered = DOCUMENT_INDEX.copy()

        # Filter by category
        if category != "all":
            filtered = [d for d in filtered if d.get("category") == category]

        # Filter by folder
        if folder:
            filtered = [d for d in filtered if folder.lower() in d.get("folder", "").lower()]

        # Filter by date (for SEC filings)
        if start_date or end_date:
            date_filtered = []
            for doc in filtered:
                if doc.get("category") == "luminar_sec":
                    filing_date = doc.get("filing_date")
                    if filing_date:
                        if start_date and filing_date < start_date:
                            continue
                        if end_date and filing_date > end_date:
                            continue
                        date_filtered.append(doc)
                elif doc.get("category") == "220_case":
                    # Use timestamp if available
                    timestamp = doc.get("timestamp", "")
                    if timestamp and timestamp != "Not found":
                        # Extract date from timestamp
                        date_filtered.append(doc)
            filtered = date_filtered

        result = {
            "total_count": len(filtered),
            "documents": filtered[:100]  # Limit to 100 for readability
        }

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "search_documents":
        query = arguments.get("query", "").lower()
        category = arguments.get("category", "all")

        results = []
        for doc in DOCUMENT_INDEX:
            if category != "all" and doc.get("category") != category:
                continue

            searchable = f"{doc.get('filename', '')} {doc.get('folder', '')} {doc.get('form_type', '')}".lower()
            if query in searchable:
                results.append(doc)

        result = {
            "query": arguments.get("query"),
            "count": len(results),
            "results": results[:50]  # Limit to 50 results
        }

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_document_info":
        path = arguments.get("path", "")
        doc = next((d for d in DOCUMENT_INDEX if d.get("path") == path), None)

        if not doc:
            return [types.TextContent(type="text", text=json.dumps({"error": "Document not found"}))]

        # Add full path
        full_path = BASE_DIR / path
        doc_info = doc.copy()
        doc_info["full_path"] = str(full_path)
        doc_info["exists"] = full_path.exists()

        return [types.TextContent(type="text", text=json.dumps(doc_info, indent=2))]

    elif name == "get_case_timeline":
        timeline_data = load_timeline_data()

        # Group by timestamp
        timeline_by_date = {}
        for entry in timeline_data:
            timestamp = entry.get("timestamp", "Unknown")
            if timestamp not in timeline_by_date:
                timeline_by_date[timestamp] = []
            timeline_by_date[timestamp].append(entry)

        result = {
            "total_filings": len(timeline_data),
            "timeline": timeline_by_date
        }

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_sec_filings_summary":
        form_type = arguments.get("form_type")

        sec_docs = [d for d in DOCUMENT_INDEX if d.get("category") == "luminar_sec"]

        if form_type:
            sec_docs = [d for d in sec_docs if d.get("form_type") == form_type]

        # Count by form type
        form_counts = {}
        for doc in sec_docs:
            ft = doc.get("form_type", "Unknown")
            form_counts[ft] = form_counts.get(ft, 0) + 1

        # Get date range
        dates = [d.get("filing_date") for d in sec_docs if d.get("filing_date")]

        result = {
            "total_filings": len(sec_docs),
            "form_type_counts": dict(sorted(form_counts.items(), key=lambda x: x[1], reverse=True)),
            "date_range": {
                "earliest": min(dates) if dates else None,
                "latest": max(dates) if dates else None
            }
        }

        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available document resources."""
    # Build index if needed
    if not DOCUMENT_INDEX:
        build_document_index()

    resources = []

    # Expose each document as a resource
    for doc in DOCUMENT_INDEX[:100]:  # Limit to 100 resources
        uri = f"document://{doc['path']}"
        name = doc['filename']
        description = f"{doc.get('category', 'document')} - {doc.get('folder', doc.get('form_type', 'filing'))}"

        resources.append(
            types.Resource(
                uri=uri,
                name=name,
                description=description,
                mimeType="application/pdf" if doc['path'].endswith('.pdf') else "text/html"
            )
        )

    return resources


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a document resource."""
    # Extract path from URI
    if uri.startswith("document://"):
        path = uri[len("document://"):]
        full_path = BASE_DIR / path

        if full_path.exists():
            # For PDFs, extract text
            if path.endswith('.pdf'):
                try:
                    reader = pypdf.PdfReader(full_path)
                    text = ""
                    for page_num in range(min(5, len(reader.pages))):  # First 5 pages
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += reader.pages[page_num].extract_text()
                    return text
                except Exception as e:
                    return f"Error reading PDF: {e}"
            else:
                # For HTML/text files
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()[:50000]  # Limit to 50KB
        else:
            return f"Document not found: {path}"

    return "Invalid resource URI"


async def main():
    """Run the MCP server."""
    # Build initial index
    build_document_index()
    print(f"Indexed {len(DOCUMENT_INDEX)} documents", flush=True)
    print(f"- 220 Case documents: {len([d for d in DOCUMENT_INDEX if d.get('category') == '220_case'])}", flush=True)
    print(f"- Luminar SEC filings: {len([d for d in DOCUMENT_INDEX if d.get('category') == 'luminar_sec'])}", flush=True)

    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="civil-maps-docs",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
