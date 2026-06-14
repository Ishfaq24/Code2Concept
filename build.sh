#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/ml-services"
python -m pip install --upgrade pip
pip install -r requirements.txt
#!/bin/bash
cd ml-services
pip install -r requirements.txt
