"""Entropy-Governance — S∝A vs S∝V duality, entropic pricing, CREP and Tesseract time-slices."""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "GenesisAeon Team"

from .core import crep, duality_factor, entropy_price
from .entropy_table_bridge import EntropyTableBridge
from .tesseract import TesseractSlice

__all__ = [
    "__version__",
    "entropy_price",
    "crep",
    "duality_factor",
    "EntropyTableBridge",
    "TesseractSlice",
]
