"""
Blog Agent main entry point

Allows running as: python -m blog_agent
"""
import sys
from .adapters.cli.commands import main

if __name__ == '__main__':
    # Enable unbuffered output for real-time logs
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
    main()
