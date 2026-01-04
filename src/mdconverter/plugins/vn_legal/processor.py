"""
Vietnamese Legal Document Processor.

Post-processing rules specifically for Vietnamese legal documents.
"""

import re
from typing import Dict, List


class VNLegalProcessor:
    """Post-processor for Vietnamese legal documents."""

    def __init__(self) -> None:
        """Initialize processor with rule counters."""
        self.fixes: Dict[str, int] = {}

    def process(self, content: str) -> str:
        """
        Apply all Vietnamese legal document processing rules.

        Args:
            content: Raw Markdown content.

        Returns:
            Processed Markdown content.
        """
        self.fixes = {}

        # Apply rules in order
        content = self._remove_bullet_from_intro(content)
        content = self._fix_definition_lists(content)
        content = self._fix_bold_header_spacing(content)
        content = self._normalize_list_markers(content)
        content = self._ensure_trailing_newline(content)

        return content

    def _remove_bullet_from_intro(self, content: str) -> str:
        """Remove bullets from introductory phrases (Đối với..., Trường hợp...)."""
        patterns = [
            (r"^- (Đối với[^:]+:)", r"\1"),
            (r"^- (Trường hợp[^:]+:)", r"\1"),
            (r"^- (Riêng với[^:]+:)", r"\1"),
        ]

        for pattern, replacement in patterns:
            matches = len(re.findall(pattern, content, re.MULTILINE))
            if matches > 0:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                self.fixes["bullet_intro"] = self.fixes.get("bullet_intro", 0) + matches

        return content

    def _fix_definition_lists(self, content: str) -> str:
        """Convert inline definitions to proper list format."""
        # Pattern: KEY: value on same line without bullet
        pattern = r"^([A-ZĐÀÁẢÃẠ][A-ZĐÀÁẢÃẠA-Z0-9\s]{2,20}):\s*([^\n]+)$"

        def replace_def(match: re.Match[str]) -> str:
            key = match.group(1).strip()
            value = match.group(2).strip()
            return f"- **{key}:** {value}"

        matches = len(re.findall(pattern, content, re.MULTILINE))
        if matches > 0:
            content = re.sub(pattern, replace_def, content, flags=re.MULTILINE)
            self.fixes["definition_lists"] = matches

        return content

    def _fix_bold_header_spacing(self, content: str) -> str:
        """Ensure blank line after bold headers (**N. Header**)."""
        pattern = r"(\*\*\d+\..*\*\*)(\n)([^\n])"

        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, r"\1\n\n\3", content)
            self.fixes["bold_header_spacing"] = matches

        return content

    def _normalize_list_markers(self, content: str) -> str:
        """Normalize list markers to use - consistently."""
        # Convert + or * to -
        pattern = r"^(\s*)[\+\*](?=\s)"
        matches = len(re.findall(pattern, content, re.MULTILINE))
        if matches > 0:
            content = re.sub(pattern, r"\1-", content, flags=re.MULTILINE)
            self.fixes["list_markers"] = matches

        return content

    def _ensure_trailing_newline(self, content: str) -> str:
        """Ensure file ends with exactly one newline."""
        if not content.endswith("\n") or content.endswith("\n\n"):
            content = content.rstrip() + "\n"
            self.fixes["trailing_newline"] = 1

        return content

    def get_fix_summary(self) -> Dict[str, int]:
        """Get summary of fixes applied."""
        return self.fixes.copy()
