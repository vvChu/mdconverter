# Installation

## Requirements

- Python 3.10 or higher
- Pandoc (for DOCX/HTML conversion)

## Install from PyPI

```bash
pip install mdconvert-cli
```

## Install from Source

```bash
git clone https://github.com/vvChu/mdconverter.git
cd mdconverter
pip install -e ".[dev]"
```

## Verify Installation

```bash
mdconvert --version
# Output: mdconverter version 1.0.0
```

## Optional Dependencies

### LlamaParse (for scanned PDFs)

```bash
pip install mdconvert-cli[llm]
```

Set your API key:

```bash
export MDCONVERT_LLAMA_CLOUD_API_KEY=your_key_here
```

### Pandoc

Install Pandoc for DOCX/HTML conversion:

- **Windows**: `winget install pandoc`
- **macOS**: `brew install pandoc`
- **Linux**: `apt install pandoc`
