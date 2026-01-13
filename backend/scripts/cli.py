"""
ToolChain CLI - Command line interface for the AI tool discovery platform.

This module provides CLI utilities for:
- Seeding the vector database
- Running health checks
- Testing API endpoints
- Managing tool data

Usage:
    python -m scripts.cli seed     # Seed the database
    python -m scripts.cli health   # Check API health
    python -m scripts.cli stats    # Show tool statistics
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def seed_database():
    """Seed the vector database with tool data."""
    from database.vectorstore import get_or_create_vectorstore, index_tools
    from data.seed_tools import get_seed_tools
    
    print("🌱 Seeding vector database...")
    tools = get_seed_tools()
    vectorstore = get_or_create_vectorstore()
    index_tools(vectorstore, tools)
    print(f"✅ Indexed {len(tools)} tools")


def check_health():
    """Check API health status."""
    import httpx
    
    api_url = "http://localhost:8000"
    print(f"🔍 Checking health at {api_url}...")
    
    try:
        response = httpx.get(f"{api_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   LLM Available: {data.get('llm_available', 'unknown')}")
        else:
            print(f"❌ API returned status {response.status_code}")
    except httpx.ConnectError:
        print("❌ Could not connect to API. Is it running?")
    except Exception as e:
        print(f"❌ Health check failed: {e}")


def show_stats():
    """Show tool database statistics."""
    from database.vectorstore import get_or_create_vectorstore
    
    print("📊 Tool Database Statistics")
    print("-" * 40)
    
    try:
        vectorstore = get_or_create_vectorstore()
        collection = vectorstore._collection
        count = collection.count()
        print(f"   Total tools indexed: {count}")
    except Exception as e:
        print(f"   Error getting stats: {e}")


def test_query(query: str):
    """Test a query against the agent workflow."""
    from agents.workflow import run_query
    
    print(f"🔍 Testing query: {query}")
    print("-" * 40)
    
    result = asyncio.run(run_query(query))
    print(result.get("final_response", "No response"))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ToolChain CLI - AI Tool Discovery Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m scripts.cli seed      Seed the vector database
    python -m scripts.cli health    Check API health
    python -m scripts.cli stats     Show tool statistics
    python -m scripts.cli query "best vector databases"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Seed command
    subparsers.add_parser("seed", help="Seed the vector database")
    
    # Health command
    subparsers.add_parser("health", help="Check API health")
    
    # Stats command
    subparsers.add_parser("stats", help="Show tool statistics")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Test a query")
    query_parser.add_argument("text", help="Query text")
    
    args = parser.parse_args()
    
    if args.command == "seed":
        seed_database()
    elif args.command == "health":
        check_health()
    elif args.command == "stats":
        show_stats()
    elif args.command == "query":
        test_query(args.text)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
