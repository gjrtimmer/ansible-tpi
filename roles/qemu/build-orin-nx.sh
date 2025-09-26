#!/usr/bin/env bash
set -euo pipefail

QEMU_VERSION="v10.0.2"

echo "🛠 Building QEMU ${QEMU_VERSION} for all static user-mode targets on ARM64..."

# Install dependencies
sudo apt-get update
sudo apt-get install -y \
  git build-essential ninja-build \
  libglib2.0-dev zlib1g-dev \
  libpixman-1-dev \
  xz-utils python3-tomli

# Prepare source directory
rm -rf qemu
mkdir qemu
curl -LO https://download.qemu.org/qemu-10.0.2.tar.xz
tar -xf qemu-10.0.2.tar.xz -C qemu --strip-components=1
cd qemu

 # Configure and build
./configure --static --disable-docs
make -j"$(nproc)"

# Copy binaries
OUTPUT_DIR="../qemu-static-bin"
mkdir -p "${OUTPUT_DIR}"
find build -type f -name 'qemu-*-static' -exec cp {} "${OUTPUT_DIR}" \;

echo "✅ QEMU ${QEMU_VERSION} build complete. Binaries in ${OUTPUT_DIR}:"
ls -lh "${OUTPUT_DIR}/qemu-"*-static
