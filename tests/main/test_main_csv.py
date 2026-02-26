"""Tests for CSV input file code generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.conftest import create_assert_file_content
from tests.main.conftest import (
    CSV_DATA_PATH,
    EXPECTED_CSV_PATH,
    run_main_and_assert,
)

if TYPE_CHECKING:
    from pathlib import Path

assert_file_content = create_assert_file_content(EXPECTED_CSV_PATH)
