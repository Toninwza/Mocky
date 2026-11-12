#!/usr/bin/env bash
# Build an AWS Emulator binary that contains only the EC2-related services Mocky targets.
# Usage: tools/emulator-subset/build.sh <path-to-aws-emulator-checkout>
# Needs ~25 GB free disk and a Rust toolchain. Takes ~10-15 min on 4 cores.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$1" && pwd)"
seeds=$(tail -n +2 "$here/services.txt")
python3 "$here/trim.py" "$repo" $seeds
(cd "$repo" && cargo build -p aws-emulator-router)
echo "Binary: $repo/target/debug/aws-emulator (run: aws-emulator -t off -a off)"
