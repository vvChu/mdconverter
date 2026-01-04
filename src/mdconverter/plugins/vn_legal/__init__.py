"""Vietnamese Legal Document plugins."""

from mdconverter.plugins.vn_legal.detector import is_legal_document
from mdconverter.plugins.vn_legal.linter import VNLegalLinter
from mdconverter.plugins.vn_legal.processor import VNLegalProcessor

__all__ = ["is_legal_document", "VNLegalLinter", "VNLegalProcessor"]
