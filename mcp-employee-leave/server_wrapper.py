#!/usr/bin/env python3
"""
Wrapper script for MCP Employee Leave Server
This script provides better error handling and logging for Claude Desktop integration
"""

import sys
import os
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set up logging to file for debugging
log_file = Path(__file__).parent / "mcp_server.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting MCP Employee Leave Server wrapper...")
        
        # Import and run the actual server
        from server import main as server_main
        import asyncio
        
        logger.info("Running server main function...")
        asyncio.run(server_main())
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Make sure all dependencies are installed in the virtual environment")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()