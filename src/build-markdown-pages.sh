#!/bin/bash
# Build script to generate HTML pages from markdown-page.template.html
# 
# This script uses envsubst to substitute environment variables in the template
# and generate static HTML files. This approach is cleaner than runtime JavaScript
# loading and produces static HTML files that work without JavaScript.
#
# Usage: ./src/build-markdown-pages.sh (from project root)
#        or cd src && ./build-markdown-pages.sh
#
# To add a new page, add a build_page call at the bottom with:
#   - output_file: HTML filename to generate
#   - markdown_file: Path to the markdown file
#   - page_description: Meta description for the page
#   - include_anchor_js: "true" or "false" (for anchor links)
#   - include_code_styles: "true" or "false" (for Prism code highlighting)
#   - zero_md_attributes: Additional attributes for zero-md (e.g., " no-shadow")

set -e

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the project root (parent of src)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TEMPLATE="$PROJECT_ROOT/markdown-page.template.html"

# Function to build a page
build_page() {
    local output_file=$1
    local markdown_file=$2
    local page_description=$3
    local include_anchor_js=${4:-false}
    local include_code_styles=${5:-false}
    local zero_md_attributes=${6:-""}
    
    # Build ZERO_MD_CONFIG (only for FAQ which needs Prism)
    local zero_md_config=""
    if [ "$include_code_styles" = "true" ]; then
        read -r -d '' zero_md_config << 'ZERO_MD_CONFIG_EOF' || true
  <script>
    // Make use of global config object to change default options
    window.ZeroMdConfig = {
      prismUrl: [
        // Default Prism URLs
        ["https://cdn.jsdelivr.net/gh/PrismJS/prism@1/prism.min.js", "data-manual"],
        "https://cdn.jsdelivr.net/gh/PrismJS/prism@1/plugins/autoloader/prism-autoloader.min.js",
        // Also load Prism's toolbar and copy-to-clipboard plugins
        "https://cdn.jsdelivr.net/gh/PrismJS/prism@1/plugins/toolbar/prism-toolbar.min.js",
        "https://cdn.jsdelivr.net/gh/PrismJS/prism@1/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js"
      ],
      cssUrls: [
        // Default stylesheets
        "https://cdn.jsdelivr.net/gh/sindresorhus/github-markdown-css@4/github-markdown.min.css",
        "https://cdn.jsdelivr.net/gh/PrismJS/prism@1/themes/prism.min.css",
        // Include CSS for toolbar plugin
        "https://cdn.jsdelivr.net/gh/PrismJS/prism@1/plugins/toolbar/prism-toolbar.min.css"
      ]
    }
  </script>
ZERO_MD_CONFIG_EOF
    fi
    
    # Build ANCHOR_JS_SCRIPT
    local anchor_js_script=""
    if [ "$include_anchor_js" = "true" ]; then
        read -r -d '' anchor_js_script << 'ANCHOR_JS_EOF' || true
  <script type="module">
    import 'https://cdn.jsdelivr.net/npm/anchor-js/anchor.min.js'
    document.addEventListener('zero-md-rendered', function (event) {
      if (typeof anchors !== 'undefined') {
        anchors.add()
      }
    })
  </script>
ANCHOR_JS_EOF
    fi
    
    # Build CODE_BLOCK_STYLES
    local code_block_styles=""
    if [ "$include_code_styles" = "true" ]; then
        read -r -d '' code_block_styles << 'CODE_STYLES_EOF' || true

    /* markdown code block */
    pre[class*="language-"],
    code[class*="language-"] {
      overflow: auto;
      background-color: whitesmoke;
    }
CODE_STYLES_EOF
    fi
    
    # Build ANCHOR_JS_STYLES
    local anchor_js_styles=""
    if [ "$include_anchor_js" = "true" ]; then
        read -r -d '' anchor_js_styles << 'ANCHOR_STYLES_EOF' || true

            .anchorjs-link {
              text-decoration: none;
            }
ANCHOR_STYLES_EOF
    fi
    
    # Export variables for envsubst
    export MARKDOWN_FILE="$markdown_file"
    export PAGE_DESCRIPTION="$page_description"
    export ZERO_MD_CONFIG="$zero_md_config"
    export ANCHOR_JS_SCRIPT="$anchor_js_script"
    export CODE_BLOCK_STYLES="$code_block_styles"
    export ANCHOR_JS_STYLES="$anchor_js_styles"
    export ZERO_MD_ATTRIBUTES="$zero_md_attributes"
    
    # Generate the file in project root
    envsubst < "$TEMPLATE" > "$PROJECT_ROOT/$output_file"
    echo "Generated: $PROJECT_ROOT/$output_file"
}

# Build FAQ page
FAQ_DESC="Have questions about the Orca Call Catalogue Library at SFU's HALLO project? Check out our FAQ page for answers on accessing resources and materials for effective learning, teaching, and more."
build_page "faq.html" \
    "FAQ.md" \
    "$FAQ_DESC" \
    "true" \
    "true" \
    " no-shadow"

# Build License page
LICENSE_DESC="Learn about the licensing agreements and terms of use for the resources available at the Call Catalogue Library, part of SFU's HALLO project. Understand your rights and responsibilities."
build_page "license.html" \
    "LICENSE.md" \
    "$LICENSE_DESC" \
    "false" \
    "false" \
    ""

echo "All pages built successfully!"

