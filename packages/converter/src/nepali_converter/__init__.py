"""Legacy Nepali font to Unicode converter."""

from nepali_converter.converter import convert
from nepali_converter.detector import detect_font


def rescue_pdf(*args, **kwargs):
    """Lazy proxy for PDF rescue to avoid importing PyMuPDF on package import."""
    from nepali_converter.pdf import rescue_pdf as _rescue_pdf

    return _rescue_pdf(*args, **kwargs)

__all__ = ["convert", "detect_font", "rescue_pdf"]
