"""General integration tests for main code generation functionality."""

from __future__ import annotations

from typing import TYPE_CHECKING

from datamodel_code_generator import snooper_to_methods
from tests.conftest import create_assert_file_content
from tests.main.conftest import (
    DATA_PATH,
    EXPECTED_MAIN_PATH,
)

if TYPE_CHECKING:
    from pathlib import Path

assert_file_content = create_assert_file_content(EXPECTED_MAIN_PATH)
