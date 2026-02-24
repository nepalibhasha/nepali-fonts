#!/usr/bin/env bash
# Download Tier 1 font releases from GitHub.
# Idempotent — safe to re-run. Overwrites existing files.
#
# Pinned versions:
#   Noto Sans Devanagari  NotoSansDevanagari-v2.006
#   Noto Serif Devanagari NotoSerifDevanagari-v2.006
#   Mukta                 2.539
#   Hind                  v2.000

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONTS_DIR="$(cd "$SCRIPT_DIR/../fonts/sources" && pwd)"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

download_and_extract() {
    local repo="$1" tag="$2" asset="$3" dest="$4"
    shift 4
    local extract_globs=("$@")

    mkdir -p "$dest"
    local zip_path="$TMP_DIR/$asset"

    if [[ ! -f "$zip_path" ]]; then
        echo "Downloading $repo @ $tag ..."
        local url="https://github.com/$repo/releases/download/$tag/$asset"
        curl -fsSL "$url" -o "$zip_path"
    fi

    # Extract to a staging dir, then copy font files into dest
    local staging="$TMP_DIR/staging"
    rm -rf "$staging"
    mkdir -p "$staging"

    for glob in "${extract_globs[@]}"; do
        unzip -o "$zip_path" "$glob" -d "$staging" 2>/dev/null || true
    done

    # Flatten: copy all TTF/OTF files into dest regardless of subdirectory
    find "$staging" -type f \( -name "*.ttf" -o -name "*.otf" \) -exec cp {} "$dest/" \;

    local count
    count=$(find "$dest" -type f \( -name "*.ttf" -o -name "*.otf" \) | wc -l | tr -d ' ')
    echo "  -> $count font files in $dest"

    rm -rf "$staging"
}

# --- Noto Sans Devanagari ---
download_and_extract \
    "notofonts/devanagari" \
    "NotoSansDevanagari-v2.006" \
    "NotoSansDevanagari-v2.006.zip" \
    "$FONTS_DIR/noto-sans-devanagari" \
    "NotoSansDevanagari/googlefonts/ttf/*" \
    "NotoSansDevanagari/full/variable-ttf/*"

# --- Noto Serif Devanagari ---
download_and_extract \
    "notofonts/devanagari" \
    "NotoSerifDevanagari-v2.006" \
    "NotoSerifDevanagari-v2.006.zip" \
    "$FONTS_DIR/noto-serif-devanagari" \
    "NotoSerifDevanagari/googlefonts/ttf/*" \
    "NotoSerifDevanagari/full/variable-ttf/*"

# --- Mukta (Devanagari only from multi-script zip) ---
download_and_extract \
    "EkType/Mukta" \
    "2.539" \
    "Mukta.Font.Family.2.539.zip" \
    "$FONTS_DIR/mukta" \
    "Mukta-Devanagari/*"

# --- Hind (flat zip, OTF only) ---
download_and_extract \
    "itfoundry/hind" \
    "v2.000" \
    "Hind-2_000.zip" \
    "$FONTS_DIR/hind" \
    "*.otf"

echo ""
echo "Done. All Tier 1 fonts downloaded to fonts/sources/."
