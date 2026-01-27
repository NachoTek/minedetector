"""Pytest configuration and fixtures for Minedetector tests."""

import os

import pytest

# Skip tests that require a display (like MainWindow tests) when running in headless CI
skipif_no_display = pytest.mark.skipif(
    not os.environ.get("DISPLAY") and os.name != "nt",
    reason="Test requires a display (skipped in headless CI)",
)
