# Configuration

Configure mdconvert using environment variables or `.env` file.

## Environment Variables

All settings use the `MDCONVERT_` prefix.

| Variable | Description | Default |
|----------|-------------|---------|
| `MDCONVERT_ANTIGRAVITY_PROXY` | Antigravity proxy URL | `http://127.0.0.1:8045` |
| `MDCONVERT_LLAMA_CLOUD_API_KEY` | LlamaCloud API key | None |
| `MDCONVERT_GEMINI_API_KEY` | Gemini API key | None |
| `MDCONVERT_MAX_OUTPUT_TOKENS` | Max tokens for LLM output | 65536 |
| `MDCONVERT_TIMEOUT_SECONDS` | Request timeout | 600 |
| `MDCONVERT_TEMPERATURE` | LLM temperature | 0.1 |
| `MDCONVERT_MIN_CONTENT_LENGTH` | Min output length | 100 |
| `MDCONVERT_HIGH_QUALITY_THRESHOLD` | Quality score threshold | 95 |

## .env File

Create a `.env` file in your project root:

```bash
# API Keys
MDCONVERT_LLAMA_CLOUD_API_KEY=llx-your-key-here
MDCONVERT_ANTIGRAVITY_PROXY=http://127.0.0.1:8045

# Conversion Settings
MDCONVERT_MAX_OUTPUT_TOKENS=65536
MDCONVERT_TIMEOUT_SECONDS=600
MDCONVERT_TEMPERATURE=0.1

# Quality Settings
MDCONVERT_MIN_CONTENT_LENGTH=100
MDCONVERT_HIGH_QUALITY_THRESHOLD=95
```

## View Current Config

```bash
mdconvert config
```

## Model Priority

The converter tries models in this order:

1. `gemini-3-flash`
2. `gemini-2.5-flash`
3. `gemini-2.5-pro`
4. `gemini-2.0-flash-exp`

If one fails, it automatically falls back to the next.
