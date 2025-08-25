import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Any, Dict, List

import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import google.generativeai as genai

# Apply nest_asyncio to allow nested event loops (needed for Jupyter/IPython)
nest_asyncio.apply()

# Load environment variables
load_dotenv("../.env")

# Configure Gemini client - FIXED: Use actual environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Global variables to store session state
session = None
exit_stack = AsyncExitStack()
gemini_client = genai.GenerativeModel("gemini-1.5-flash")  # FIXED: Use correct model name
stdio = None
write = None


async def connect_to_server(server_script_path: str = "server.py"):
    """Connect to an MCP server.

    Args:
        server_script_path: Path to the server script.
    """
    global session, stdio, write, exit_stack

    # Server configuration
    server_params = StdioServerParameters(
        command="python",
        args=[server_script_path],
    )

    # Connect to the server
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))

    # Initialize the connection
    await session.initialize()

    # List available tools
    tools_result = await session.list_tools()
    print("\nConnected to server with tools:")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description}")


async def get_mcp_tools() -> List[Any]:
    """Get available tools from the MCP server in Gemini format.

    Returns:
        A list of tools in Gemini format.
    """
    global session

    tools_result = await session.list_tools()
    # FIXED: Convert to Gemini function calling format
    gemini_tools = []
    for tool in tools_result.tools:
        gemini_tools.append(
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                prop_name: genai.protos.Schema(
                                    type=getattr(genai.protos.Type, prop_schema.get("type", "STRING").upper()),
                                    description=prop_schema.get("description", "")
                                )
                                for prop_name, prop_schema in tool.inputSchema.get("properties", {}).items()
                            },
                            required=tool.inputSchema.get("required", [])
                        )
                    )
                ]
            )
        )
    return gemini_tools


async def process_query(query: str) -> str:
    """Process a query using Gemini and available MCP tools.

    Args:
        query: The user query.

    Returns:
        The response from Gemini.
    """
    global session, gemini_client

    try:
        # Get available tools
        tools = await get_mcp_tools()

        # FIXED: Use Gemini's native API
        chat = gemini_client.start_chat()
        
        # Send initial message with tools
        response = await asyncio.to_thread(
            chat.send_message,
            query,
            tools=tools if tools else None
        )

        # Check if the model wants to use function calls
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    # Execute the function call
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)

                    # Call the MCP tool
                    result = await session.call_tool(
                        function_name,
                        arguments=function_args,
                    )

                    # Send the function result back to Gemini
                    function_response = genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": result.content[0].text}
                        )
                    )

                    # Get final response with function result
                    final_response = await asyncio.to_thread(
                        chat.send_message,
                        function_response
                    )
                    
                    return final_response.text

        # No function calls, return direct response
        return response.text

    except Exception as e:
        return f"Error processing query: {str(e)}"


async def cleanup():
    """Clean up resources."""
    global exit_stack
    await exit_stack.aclose()


async def main():
    """Main entry point for the client."""
    try:
        await connect_to_server("server.py")

        # Example: Ask about company vacation policy
        query = "What is our company's vacation policy?"
        print(f"\nQuery: {query}")

        response = await process_query(query)
        print(f"\nResponse: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())