# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.6 Deployment and Distribution

from setuptools import setup, find_packages

setup(
    name="my-mcp-server",
    version="1.0.0",
    description="A simple MCP server example",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "mcp>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "my-mcp-server=my_mcp_server.server:main",
        ],
    },
)