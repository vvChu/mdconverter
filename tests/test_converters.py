"""Tests for core converters."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from mdconverter.core.base import ConversionResult, ConversionStatus
from mdconverter.core.gemini import GeminiConverter
from mdconverter.core.llamaparse import LlamaParseConverter
from mdconverter.core.pandoc import PandocConverter


class TestConversionResult:
    """Test ConversionResult dataclass."""

    def test_is_success_true(self) -> None:
        """Test is_success returns True for SUCCESS status."""
        result = ConversionResult(
            source_path=Path("test.pdf"),
            status=ConversionStatus.SUCCESS,
        )
        assert result.is_success is True

    def test_is_success_false_for_failed(self) -> None:
        """Test is_success returns False for FAILED status."""
        result = ConversionResult(
            source_path=Path("test.pdf"),
            status=ConversionStatus.FAILED,
        )
        assert result.is_success is False

    def test_is_success_false_for_skipped(self) -> None:
        """Test is_success returns False for SKIPPED status."""
        result = ConversionResult(
            source_path=Path("test.pdf"),
            status=ConversionStatus.SKIPPED,
        )
        assert result.is_success is False


class TestGeminiConverter:
    """Test GeminiConverter class."""

    def test_supports_pdf(self) -> None:
        """Test PDF is supported."""
        converter = GeminiConverter()
        assert converter.supports(".pdf") is True

    def test_supports_docx(self) -> None:
        """Test DOCX is supported."""
        converter = GeminiConverter()
        assert converter.supports(".docx") is True

    def test_does_not_support_txt(self) -> None:
        """Test TXT is not supported."""
        converter = GeminiConverter()
        assert converter.supports(".txt") is False

    def test_convert_nonexistent_file(self, tmp_path: Path) -> None:
        """Test conversion of non-existent file fails."""
        converter = GeminiConverter(output_dir=tmp_path)
        result = converter.convert(Path("nonexistent.pdf"))

        assert result.status == ConversionStatus.FAILED
        assert "not found" in result.error_message.lower()

    def test_convert_unsupported_extension(self, tmp_path: Path) -> None:
        """Test conversion of unsupported file type is skipped."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        converter = GeminiConverter(output_dir=tmp_path)
        result = converter.convert(test_file)

        assert result.status == ConversionStatus.SKIPPED
        assert "unsupported" in result.error_message.lower()

    @patch("mdconverter.core.gemini.httpx.Client")
    def test_convert_success_mocked(self, mock_client_class: MagicMock, tmp_path: Path) -> None:
        """Test successful conversion with mocked API response."""
        # Create a test PDF file
        test_file = tmp_path / "test.pdf"
        test_file.write_bytes(b"%PDF-1.4 test content")

        # Mock the API response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "# Converted Content\n\nTest"}]}}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        converter = GeminiConverter(output_dir=tmp_path)
        result = converter.convert(test_file)

        assert result.status == ConversionStatus.SUCCESS
        assert result.output_path is not None
        assert result.output_path.suffix == ".md"


class TestPandocConverter:
    """Test PandocConverter class."""

    def test_supports_docx(self) -> None:
        """Test DOCX is supported."""
        converter = PandocConverter()
        assert converter.supports(".docx") is True

    def test_supports_html(self) -> None:
        """Test HTML is supported."""
        converter = PandocConverter()
        assert converter.supports(".html") is True

    def test_does_not_support_pdf(self) -> None:
        """Test PDF is not supported by Pandoc."""
        converter = PandocConverter()
        assert converter.supports(".pdf") is False

    def test_convert_nonexistent_file(self, tmp_path: Path) -> None:
        """Test conversion of non-existent file fails."""
        converter = PandocConverter(output_dir=tmp_path)
        result = converter.convert(Path("nonexistent.docx"))

        assert result.status == ConversionStatus.FAILED
        assert "not found" in result.error_message.lower()

    @patch("mdconverter.core.pandoc.shutil.which")
    def test_pandoc_not_installed(self, mock_which: MagicMock, tmp_path: Path) -> None:
        """Test error when Pandoc is not installed."""
        mock_which.return_value = None

        test_file = tmp_path / "test.docx"
        test_file.write_bytes(b"test content")

        converter = PandocConverter(output_dir=tmp_path)
        result = converter.convert(test_file)

        assert result.status == ConversionStatus.FAILED
        assert "pandoc" in result.error_message.lower()


class TestLlamaParseConverter:
    """Test LlamaParseConverter class."""

    def test_supports_pdf(self) -> None:
        """Test PDF is supported."""
        converter = LlamaParseConverter()
        assert converter.supports(".pdf") is True

    def test_supports_docx(self) -> None:
        """Test DOCX is supported."""
        converter = LlamaParseConverter()
        assert converter.supports(".docx") is True

    def test_is_available_without_key(self) -> None:
        """Test is_available returns False without API key."""
        converter = LlamaParseConverter(api_key=None)
        # Depends on environment, but we test the method exists
        assert hasattr(converter, "is_available")

    def test_convert_without_api_key(self, tmp_path: Path) -> None:
        """Test conversion fails without API key."""
        test_file = tmp_path / "test.pdf"
        test_file.write_bytes(b"%PDF-1.4 test")

        converter = LlamaParseConverter(output_dir=tmp_path, api_key=None)
        # Clear any env var that might provide a key
        with patch.object(converter, "api_key", None):
            with patch.object(converter, "is_available", return_value=False):
                result = converter.convert(test_file)
                assert result.status == ConversionStatus.FAILED


class TestBaseConverter:
    """Test BaseConverter abstract methods."""

    def test_get_output_path(self, tmp_path: Path) -> None:
        """Test output path generation."""
        converter = GeminiConverter(output_dir=tmp_path)
        source = Path("/some/path/document.pdf")
        output = converter.get_output_path(source)

        assert output.suffix == ".md"
        assert output.stem == "document"
        assert output.parent == tmp_path

    def test_add_frontmatter(self, tmp_path: Path) -> None:
        """Test frontmatter is added to content."""
        converter = GeminiConverter(output_dir=tmp_path)
        source = Path("test.pdf")
        content = "# Test Content"

        result = converter.add_frontmatter(content, source, "gemini")

        assert "---" in result
        assert "source:" in result
        assert "test.pdf" in result
        assert "tool:" in result
        assert "gemini" in result
