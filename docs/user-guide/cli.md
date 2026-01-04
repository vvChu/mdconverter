# CLI Commands

Complete reference for all mdconvert commands.

## convert

Convert documents to Markdown.

```bash
mdconvert convert INPUT [OPTIONS]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `INPUT` | Input file or directory to convert |

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output directory | Same as input |
| `-r, --recursive` | Recursively process directories | False |
| `-t, --tool` | Conversion tool: auto, gemini, pandoc, llamaparse | auto |
| `--dry-run` | Show what would be converted | False |

### Examples

```bash
# Convert single file
mdconvert convert document.pdf

# Convert directory recursively
mdconvert convert ./docs/ -r -o ./output/

# Use specific tool
mdconvert convert scan.pdf --tool llamaparse

# Dry run
mdconvert convert ./docs/ --dry-run
```

---

## validate

Validate Markdown files for quality and structure.

```bash
mdconvert validate TARGET [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --fix` | Automatically fix issues | False |

### Examples

```bash
# Validate a file
mdconvert validate document.md

# Validate and fix a directory
mdconvert validate ./output/ --fix
```

---

## lint

Lint Markdown files using VN Legal rules.

```bash
mdconvert lint [TARGET] [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --fix` | Automatically fix lint issues | False |
| `--vn-only` | Only run Vietnamese legal checks | False |

### VN Legal Rules

| Rule | Description |
|------|-------------|
| VN001 | Merged list items (a, b, c on same line) |
| VN002 | Suspicious numbering reset |
| VN003 | Missing blank line before Điều headers |
| VN004 | Incorrect Điểm format |

---

## config

Show current configuration.

```bash
mdconvert config
```

### Output

Displays a table with all current settings including proxy URL, models, tokens, and thresholds.
