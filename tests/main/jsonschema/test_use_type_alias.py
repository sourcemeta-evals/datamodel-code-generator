from __future__ import annotations

import json
from typing import TYPE_CHECKING

from datamodel_code_generator.__main__ import Exit, main

if TYPE_CHECKING:
    from pathlib import Path

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Root",
    "type": "object",
    "properties": {"name": {"$ref": "#/definitions/SimpleString"}},
    "definitions": {"SimpleString": {"type": "string"}},
}


def test_use_type_alias(tmp_path: Path) -> None:
    input_file = tmp_path / "schema.json"
    input_file.write_text(json.dumps(SCHEMA), encoding="utf-8")
    output_file = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(input_file),
        "--input-file-type",
        "jsonschema",
        "--output",
        str(output_file),
        "--use-type-alias",
    ])
    assert return_code == Exit.OK
    generated = output_file.read_text(encoding="utf-8")
    assert "SimpleString: TypeAlias = str" in generated
    assert "RootModel" not in generated
