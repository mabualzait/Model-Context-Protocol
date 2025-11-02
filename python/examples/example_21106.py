# 📖 Chapter: Appendices
# 📖 Section: E.3 Performance Tuning Guide

# Use async for concurrent operations
import asyncio

async def call_tools_concurrently(tools):
    tasks = [
        client.call_tool_async(tool["name"], {})
        for tool in tools
    ]
    return await asyncio.gather(*tasks)