from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string"
)
def read_document(
    doc_id:str = Field(description="The id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in documents content with another string"
)
def edit_document(
    doc_id:str = Field(description="Id of the document to be edited"),
    old_str:str = Field(description="The text to replace. Must match exactly including the whitespaces"),
    new_str:str = Field(description="The new text to insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
    # mcp python SDK takes care of the return type and converts it to a string when returning

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def doc_fetch(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the content of the document in Markdown format"
)
def format_document(
    doc_id: str=Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    <document_id>

    Add in headers, bullet points, tables, etc as necessary.
    Use the 'edit_document' tool to edit the document.
    """

    return [base.UserMessage(prompt)]

@mcp.prompt(
    name="summarize",
    description="Summarizes the content of the given document"
)
def summarize_document(
    doc_id: str=Field(description="Id of the document to summarize")
) ->  list[base.Message]:
    prompt = f"""
    Summarize the provided document, focusing on the key points, arguments, and conclusions. The summary should be concise and accurate.
    The id of the document you need to summarize is:
    <document_id>
    {doc_id}
    <document_id>
    """

    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
