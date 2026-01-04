"""
Pandoc-based converter for DOCX, HTML, and other formats.

Uses Pandoc as a subprocess for reliable conversion.
"""

import subprocess
import time
from pathlib import Path

from mdconverter.core.base import BaseConverter, ConversionResult, ConversionStatus


class PandocConverter(BaseConverter):
    """Document converter using Pandoc."""

    SUPPORTED_EXTENSIONS = {".docx", ".doc", ".html", ".htm", ".rtf", ".odt", ".epub"}

    def __init__(self, output_dir: Path | None = None) -> None:
        """Initialize Pandoc converter."""
        super().__init__(output_dir)
        self._pandoc_available: bool | None = None

    def supports(self, file_extension: str) -> bool:
        """Check if extension is supported."""
        return file_extension.lower() in self.SUPPORTED_EXTENSIONS

    def is_pandoc_available(self) -> bool:
        """Check if Pandoc is installed."""
        if self._pandoc_available is None:
            try:
                result = subprocess.run(
                    ["pandoc", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self._pandoc_available = result.returncode == 0
            except (subprocess.SubprocessError, FileNotFoundError):
                self._pandoc_available = False
        return self._pandoc_available

    def convert(self, source_path: Path) -> ConversionResult:
        """Convert document using Pandoc."""
        start_time = time.time()

        if not source_path.exists():
            return ConversionResult(
                source_path=source_path,
                status=ConversionStatus.FAILED,
                error_message=f"File not found: {source_path}",
            )

        if not self.supports(source_path.suffix):
            return ConversionResult(
                source_path=source_path,
                status=ConversionStatus.SKIPPED,
                error_message=f"Unsupported extension: {source_path.suffix}",
            )

        if not self.is_pandoc_available():
            return ConversionResult(
                source_path=source_path,
                status=ConversionStatus.FAILED,
                error_message="Pandoc is not installed",
            )

        try:
            output_path = self.get_output_path(source_path)

            # Run Pandoc conversion
            result = subprocess.run(
                [
                    "pandoc",
                    str(source_path),
                    "-o",
                    str(output_path),
                    "-t",
                    "gfm",
                    "--wrap=none",
                    "--extract-media",
                    str(output_path.parent / "media"),
                ],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode != 0:
                return ConversionResult(
                    source_path=source_path,
                    status=ConversionStatus.FAILED,
                    tool_used="pandoc",
                    duration_seconds=time.time() - start_time,
                    error_message=result.stderr or "Pandoc conversion failed",
                )

            # Read and optionally add frontmatter
            content = output_path.read_text(encoding="utf-8")
            final_content = self.add_frontmatter(content, source_path, "pandoc")
            output_path.write_text(final_content, encoding="utf-8")

            return ConversionResult(
                source_path=source_path,
                output_path=output_path,
                status=ConversionStatus.SUCCESS,
                tool_used="pandoc",
                content=final_content,
                quality_score=self._calculate_quality(final_content),
                duration_seconds=time.time() - start_time,
            )

        except subprocess.TimeoutExpired:
            return ConversionResult(
                source_path=source_path,
                status=ConversionStatus.FAILED,
                tool_used="pandoc",
                duration_seconds=time.time() - start_time,
                error_message="Pandoc conversion timed out",
            )
        except Exception as e:
            return ConversionResult(
                source_path=source_path,
                status=ConversionStatus.FAILED,
                tool_used="pandoc",
                duration_seconds=time.time() - start_time,
                error_message=str(e),
            )

    def _calculate_quality(self, content: str) -> int:
        """Calculate quality score (0-100)."""
        score = 60  # Pandoc is reliable

        # Length check
        if len(content) > 500:
            score += 10
        if len(content) > 2000:
            score += 10

        # Structure check
        if "##" in content:
            score += 10
        if "|" in content:
            score += 10

        return min(score, 100)
