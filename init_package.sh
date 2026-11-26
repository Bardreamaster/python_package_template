#!/usr/bin/env bash
#
# Initialize a new package from this template.
# The script works with GNU tools (Linux) and with BSD tools and bash 3.2 (macOS).

# Exit on error
set -euo pipefail

TEMPLATE_NAME="python-package-template"
TEMPLATE_MODULE="python_package_template"
TEMPLATE_REPO_URL="https://github.com/Bardreamaster/python_package_template"
TEMPLATE_DOCS_URL="https://bardreamaster.github.io/python_package_template/"
TEMPLATE_DESCRIPTION="Add your description here"

# Function to display usage instructions
display_usage() {
    echo "Usage: $0 --name PACKAGE_NAME --author AUTHOR_NAME --email AUTHOR_EMAIL [OPTIONS]"
    echo
    echo "Configure a Python package with custom name, author, and email."
    echo "Run the script in the root directory of the repository."
    echo
    echo "Required arguments:"
    echo "  --name    Package name (use-hyphens-for-multi-word-names)"
    echo "  --author  Author's name"
    echo "  --email   Author's email"
    echo
    echo "Options:"
    echo "  --description  One-line description of the package"
    echo "  --repo         GitHub repository as OWNER/NAME or as a URL"
    echo "                 (default: the 'origin' remote of this clone)"
    echo "  --docs-url     Address of the documentation site"
    echo "                 (default: https://OWNER.github.io/NAME/)"
    echo
    exit 1
}

# Escape a string for use as a literal pattern in a sed "s|...|...|" command.
escape_pattern() {
    printf '%s' "$1" | sed -e 's/[][\\.*^$|]/\\&/g'
}

# Escape a string for use as the replacement in a sed "s|...|...|" command.
escape_replacement() {
    printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'
}

# Escape a string for use inside a double-quoted TOML or Python string.
escape_quoted() {
    printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
}

# Usage: sed_in_place EXPRESSION FILE...
# "sed -i" needs different arguments in GNU sed and BSD sed. "sed -i.bak" works in both.
sed_in_place() {
    local expression="$1"
    shift
    local file
    for file in "$@"; do
        sed -i.bak -e "$expression" "$file"
        rm -f "$file.bak"
    done
}

# Usage: replace_everywhere OLD NEW
# Replace a literal string in all text files of the repository.
replace_everywhere() {
    local pattern replacement file
    pattern=$(escape_pattern "$1")
    replacement=$(escape_replacement "$2")
    grep -rIlF \
        --exclude-dir=.git --exclude-dir=.venv --exclude-dir=build --exclude-dir=dist \
        --exclude=init_package.sh --exclude=uv.lock \
        -e "$1" . | while IFS= read -r file; do
        sed_in_place "s|$pattern|$replacement|g" "$file"
    done
}

# Usage: normalize_repo REPO
# Print the https URL of a GitHub repository. Print nothing if REPO is not usable.
normalize_repo() {
    local repo="${1%/}"
    repo="${repo%.git}"
    case "$repo" in
        git@github.com:*) repo="https://github.com/${repo#git@github.com:}" ;;
        ssh://git@github.com/*) repo="https://github.com/${repo#ssh://git@github.com/}" ;;
        http://* | https://*) ;;
        */*) repo="https://github.com/$repo" ;;
        *) repo="" ;;
    esac
    printf '%s' "$repo"
}

PACKAGE_NAME=""
AUTHOR_NAME=""
AUTHOR_EMAIL=""
DESCRIPTION=""
REPO=""
DOCS_URL=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    if [[ "$key" != "--help" && "$key" != "-h" && $# -lt 2 ]]; then
        echo "Error: $key needs a value"
        display_usage
    fi
    case $key in
        --name)
            PACKAGE_NAME="$2"
            shift 2
            ;;
        --author)
            AUTHOR_NAME="$2"
            shift 2
            ;;
        --email)
            AUTHOR_EMAIL="$2"
            shift 2
            ;;
        --description)
            DESCRIPTION="$2"
            shift 2
            ;;
        --repo)
            REPO="$2"
            shift 2
            ;;
        --docs-url)
            DOCS_URL="$2"
            shift 2
            ;;
        --help | -h)
            display_usage
            ;;
        *)
            echo "Unknown option: $1"
            display_usage
            ;;
    esac
done

# Check if required arguments are provided
if [ -z "$PACKAGE_NAME" ] || [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ]; then
    echo "Error: missing required arguments"
    display_usage
fi

if ! printf '%s' "$PACKAGE_NAME" | grep -Eq '^[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?$'; then
    echo "Error: '$PACKAGE_NAME' is not a valid package name"
    exit 1
fi

if [ ! -f pyproject.toml ] || [ ! -d "src/$TEMPLATE_MODULE" ]; then
    echo "Error: run this script once, in the root directory of the template"
    exit 1
fi

# Convert the package name to a Python module name: lower case, underscores.
PACKAGE_NAME_UNDERSCORE=$(printf '%s' "$PACKAGE_NAME" | tr 'A-Z.-' 'a-z__')

# Get current year
CURRENT_YEAR=$(date +%Y)

# Find the repository URL. Do not use the URL of the template itself.
if [ -z "$REPO" ]; then
    REPO=$(git remote get-url origin 2>/dev/null || true)
fi
REPO_URL=$(normalize_repo "$REPO")
if [ "$(printf '%s' "$REPO_URL" | tr 'A-Z' 'a-z')" = "$(printf '%s' "$TEMPLATE_REPO_URL" | tr 'A-Z' 'a-z')" ]; then
    REPO_URL=""
fi
REPO_IS_PLACEHOLDER=false
if [ -z "$REPO_URL" ]; then
    REPO_URL="https://github.com/OWNER/$PACKAGE_NAME"
    REPO_IS_PLACEHOLDER=true
fi
if [ -z "$DOCS_URL" ]; then
    case "$REPO_URL" in
        https://github.com/OWNER/*)
            DOCS_URL="https://OWNER.github.io/$PACKAGE_NAME/"
            ;;
        https://github.com/*/*)
            repo_path="${REPO_URL#https://github.com/}"
            repo_owner=$(printf '%s' "${repo_path%%/*}" | tr 'A-Z' 'a-z')
            DOCS_URL="https://$repo_owner.github.io/${repo_path#*/}/"
            ;;
        *)
            DOCS_URL="https://OWNER.github.io/$PACKAGE_NAME/"
            REPO_IS_PLACEHOLDER=true
            ;;
    esac
fi
DOCS_URL="${DOCS_URL%/}/"

echo "Initializing Python package:"
echo "Package Name: $PACKAGE_NAME"
echo "Python Module Name: $PACKAGE_NAME_UNDERSCORE"
echo "Author: $AUTHOR_NAME"
echo "Email: $AUTHOR_EMAIL"
echo "Repository: $REPO_URL"
echo "Documentation: $DOCS_URL"

AUTHOR_QUOTED=$(escape_replacement "$(escape_quoted "$AUTHOR_NAME")")
EMAIL_QUOTED=$(escape_replacement "$(escape_quoted "$AUTHOR_EMAIL")")

# Update the URLs first. They contain the template name.
echo "Updating project URLs..."
replace_everywhere "$TEMPLATE_DOCS_URL" "$DOCS_URL"
replace_everywhere "$TEMPLATE_REPO_URL" "$REPO_URL"

# Update pyproject.toml
echo "Updating pyproject.toml..."
sed_in_place "s|{ name = \"[^\"]*\", email = \"[^\"]*\" }|{ name = \"$AUTHOR_QUOTED\", email = \"$EMAIL_QUOTED\" }|" pyproject.toml
if [ -n "$DESCRIPTION" ]; then
    DESCRIPTION_QUOTED=$(escape_replacement "$(escape_quoted "$DESCRIPTION")")
    sed_in_place "s|^description = \".*\"$|description = \"$DESCRIPTION_QUOTED\"|" pyproject.toml
else
    DESCRIPTION="$TEMPLATE_DESCRIPTION"
fi

# Update the copyright line of the license
echo "Updating LICENSE..."
sed_in_place "s|^Copyright (c) .*$|Copyright (c) $CURRENT_YEAR $(escape_replacement "$AUTHOR_NAME")|" LICENSE

# Update documentation info
echo "Updating documentation..."
sed_in_place "s|^copyright = \".*\"$|copyright = \"$CURRENT_YEAR, $AUTHOR_QUOTED\"|" docs/conf.py
sed_in_place "s|^author = \".*\"$|author = \"$AUTHOR_QUOTED\"|" docs/conf.py

# Update the package name in all files
echo "Renaming the package..."
replace_everywhere "$TEMPLATE_MODULE" "$PACKAGE_NAME_UNDERSCORE"
replace_everywhere "$TEMPLATE_NAME" "$PACKAGE_NAME"

# Update the source directory name
echo "Renaming source directory..."
mv "src/$TEMPLATE_MODULE" "src/$PACKAGE_NAME_UNDERSCORE"
echo "Source directory renamed from 'src/$TEMPLATE_MODULE' to 'src/$PACKAGE_NAME_UNDERSCORE'"

# Update README.md and README.zh-CN.md
echo "Updating README.md and README.zh-CN.md..."
cat > README.md << README_EOF
# $PACKAGE_NAME

[简体中文](README.zh-CN.md)

$DESCRIPTION

## Installation

\`\`\`bash
python3 -m pip install $PACKAGE_NAME
\`\`\`

## Usage

\`\`\`python
import $PACKAGE_NAME_UNDERSCORE

# Add a short usage example here
\`\`\`

## Documentation

Read the documentation at <$DOCS_URL>.
AI agents: start with [AGENTS.md](AGENTS.md).

## License

[MIT](LICENSE)
README_EOF

cat > README.zh-CN.md << README_EOF
# $PACKAGE_NAME

[English](README.md)

$DESCRIPTION

## 安装

\`\`\`bash
python3 -m pip install $PACKAGE_NAME
\`\`\`

## 用法

\`\`\`python
import $PACKAGE_NAME_UNDERSCORE

# 在这里补一个简短的例子
\`\`\`

## 文档

完整文档见 <${DOCS_URL}zh/>。
AI agent 请先读 [AGENTS.md](AGENTS.md)。

## 许可证

[MIT](LICENSE)
README_EOF

echo "Package successfully initialized!"
echo "Next steps:"
echo "1. Delete init_package.sh"
echo "2. Run 'uv sync' and 'uv run pytest'"
echo "3. Add your code to src/$PACKAGE_NAME_UNDERSCORE"
echo "4. Replace the placeholders in docs/en/ and docs/zh/, and the Chinese description in README.zh-CN.md"
echo "5. Build your package with: uv build"
echo "6. Build documentation with: uv run python docs/build_docs.py"
if [ "$DESCRIPTION" = "$TEMPLATE_DESCRIPTION" ]; then
    echo "7. Set 'description' in pyproject.toml and in both README files"
fi
if [ "$REPO_IS_PLACEHOLDER" = true ]; then
    echo
    echo "Warning: the repository is unknown. Replace OWNER in pyproject.toml, docs/conf.py and the README files."
fi
