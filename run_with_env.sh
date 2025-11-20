#!/bin/bash
# Load .env and run command
set -a
source .env
set +a
exec "$@"
