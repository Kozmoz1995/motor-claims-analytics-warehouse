"""Motor collision warehouse ingestion and quality package."""

from .quality import QualityResult, validate_crash

__all__ = ["QualityResult", "validate_crash"]
