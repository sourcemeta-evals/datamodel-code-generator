from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from freezegun import freeze_time

from datamodel_code_generator import (
    DataModelType,
    InputFileType,
    generate,
    snooper_to_methods,
)
from datamodel_code_generator.__main__ import Config, Exit, main
from datamodel_code_generator.format import PythonVersion

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

DATA_PATH: Path = Path(__file__).parent.parent / "data"
PYTHON_DATA_PATH: Path = DATA_PATH / "python"
EXPECTED_MAIN_PATH = DATA_PATH / "expected" / "main"

TIMESTAMP = "1985-10-26T01:21:00-07:00"


@pytest.fixture(autouse=True)
def reset_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    namespace_ = Namespace(no_color=False)
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace_)
    monkeypatch.setattr("datamodel_code_generator.arguments.namespace", namespace_)


def test_debug(mocker: MockerFixture) -> None:
    with pytest.raises(expected_exception=SystemExit):
        main(["--debug", "--help"])

    mocker.patch("datamodel_code_generator.pysnooper", None)
    with pytest.raises(expected_exception=SystemExit):
        main(["--debug", "--help"])


@freeze_time("2019-07-26")
def test_snooper_to_methods_without_pysnooper(mocker: MockerFixture) -> None:
    mocker.patch("datamodel_code_generator.pysnooper", None)
    mock = mocker.Mock()
    assert snooper_to_methods()(mock) == mock


@pytest.mark.parametrize(argnames="no_color", argvalues=[False, True])
def test_show_help(no_color: bool, capsys: pytest.CaptureFixture[str]) -> None:
    args = ["--no-color"] if no_color else []
    args += ["--help"]

    with pytest.raises(expected_exception=SystemExit) as context:
        main(args)
    assert context.value.code == Exit.OK

    output = capsys.readouterr().out
    assert ("\x1b" not in output) == no_color


def test_show_help_when_no_input(mocker: MockerFixture) -> None:
    print_help_mock = mocker.patch("datamodel_code_generator.__main__.arg_parser.print_help")
    isatty_mock = mocker.patch("sys.stdin.isatty", return_value=True)
    return_code: Exit = main([])
    assert return_code == Exit.ERROR
    assert isatty_mock.called
    assert print_help_mock.called


def test_no_args_has_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    No argument should have a default value set because it would override pyproject.toml values.

    Default values are set in __main__.Config class.
    """
    namespace = Namespace()
    monkeypatch.setattr("datamodel_code_generator.__main__.namespace", namespace)
    main([])
    for field in Config.get_fields():
        assert getattr(namespace, field, None) is None


@freeze_time("2019-07-26")
def test_space_and_special_characters_dict(tmp_path: Path) -> None:
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(PYTHON_DATA_PATH / "space_and_special_characters_dict.py"),
        "--output",
        str(output_file),
        "--input-file-type",
        "dict",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_MAIN_PATH / "space_and_special_characters_dict.py").read_text()
    )


@freeze_time("2024-12-14")
def test_direct_input_dict(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        {"foo": 1, "bar": {"baz": 2}},
        input_file_type=InputFileType.Dict,
        output=output_file,
        output_model_type=DataModelType.PydanticV2BaseModel,
        snake_case_field=True,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "direct_input_dict.py").read_text()


@freeze_time(TIMESTAMP)
def test_frozen_dataclasses(tmp_path: Path) -> None:
    """Test --frozen-dataclasses flag functionality."""
    output_file = tmp_path / "output.py"
    generate(
        DATA_PATH / "jsonschema" / "simple_frozen_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        frozen_dataclasses=True,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "frozen_dataclasses.py").read_text()


@freeze_time(TIMESTAMP)
def test_frozen_dataclasses_with_keyword_only(tmp_path: Path) -> None:
    """Test --frozen-dataclasses with --keyword-only flag combination."""

    output_file = tmp_path / "output.py"
    generate(
        DATA_PATH / "jsonschema" / "simple_frozen_test.json",
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.DataclassesDataclass,
        frozen_dataclasses=True,
        keyword_only=True,
        target_python_version=PythonVersion.PY_310,
    )
    assert output_file.read_text() == (EXPECTED_MAIN_PATH / "frozen_dataclasses_keyword_only.py").read_text()


@freeze_time(TIMESTAMP)
def test_frozen_dataclasses_command_line(tmp_path: Path) -> None:
    """Test --frozen-dataclasses flag via command line."""
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(DATA_PATH / "jsonschema" / "simple_frozen_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--output-model-type",
        "dataclasses.dataclass",
        "--frozen-dataclasses",
    ])
    assert return_code == Exit.OK
    assert output_file.read_text(encoding="utf-8") == (EXPECTED_MAIN_PATH / "frozen_dataclasses.py").read_text()


@freeze_time(TIMESTAMP)
def test_frozen_dataclasses_with_keyword_only_command_line(tmp_path: Path) -> None:
    """Test --frozen-dataclasses with --keyword-only flag via command line."""
    output_file: Path = tmp_path / "output.py"
    return_code: Exit = main([
        "--input",
        str(DATA_PATH / "jsonschema" / "simple_frozen_test.json"),
        "--output",
        str(output_file),
        "--input-file-type",
        "jsonschema",
        "--output-model-type",
        "dataclasses.dataclass",
        "--frozen-dataclasses",
        "--keyword-only",
        "--target-python-version",
        "3.10",
    ])
    assert return_code == Exit.OK
    assert (
        output_file.read_text(encoding="utf-8")
        == (EXPECTED_MAIN_PATH / "frozen_dataclasses_keyword_only.py").read_text()
    )


@freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    ("output_model_type", "target_python_version", "expected_snippets", "unexpected_snippets"),
    [
        (
            DataModelType.PydanticBaseModel,
            PythonVersion.PY_39,
            [
                "from typing_extensions import TypeAlias",
                "SimpleString: TypeAlias = str",
                "UnionType: TypeAlias = Union[str, int]",
            ],
            ["class SimpleString(RootModel", "TypeAliasType(", "type SimpleString ="],
        ),
        (
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_311,
            [
                "from typing_extensions import TypeAliasType",
                'SimpleString = TypeAliasType("SimpleString", str)',
            ],
            ["class SimpleString(RootModel", "type SimpleString ="],
        ),
        (
            DataModelType.PydanticV2BaseModel,
            PythonVersion.PY_312,
            ["type SimpleString = str", "type UnionType = str | int"],
            ["TypeAliasType(", "class SimpleString(RootModel"],
        ),
        (
            DataModelType.DataclassesDataclass,
            PythonVersion.PY_312,
            ["type SimpleString = str"],
            ["TypeAliasType(", "class SimpleString("],
        ),
    ],
)
def test_use_type_alias_root_models_version_matrix(
    tmp_path: Path,
    output_model_type: DataModelType,
    target_python_version: PythonVersion,
    expected_snippets: list[str],
    unexpected_snippets: list[str],
) -> None:
    output_file = tmp_path / "output.py"
    schema = {
        "definitions": {
            "SimpleString": {"type": "string"},
            "UnionType": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        }
    }

    generate(
        json.dumps(schema),
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=output_model_type,
        target_python_version=target_python_version,
        use_type_alias=True,
        use_union_operator=target_python_version.has_union_operator,
    )

    content = output_file.read_text()
    for expected_snippet in expected_snippets:
        assert expected_snippet in content
    for unexpected_snippet in unexpected_snippets:
        assert unexpected_snippet not in content


@freeze_time(TIMESTAMP)
def test_use_type_alias_preserves_annotated_root_field(tmp_path: Path) -> None:
    output_file = tmp_path / "output.py"
    generate(
        json.dumps(
            {
                "definitions": {
                    "ConstrainedString": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 5,
                    }
                }
            }
        ),
        input_file_type=InputFileType.JsonSchema,
        output=output_file,
        output_model_type=DataModelType.PydanticBaseModel,
        target_python_version=PythonVersion.PY_39,
        field_constraints=True,
        use_annotated=True,
        use_type_alias=True,
    )

    content = output_file.read_text()
    assert "from typing import Annotated" in content
    assert "from pydantic import Field" in content
    assert "ConstrainedString: TypeAlias = Annotated[str, Field(" in content
    assert "min_length=1" in content
    assert "max_length=5" in content


def test_filename_with_newline_injection(tmp_path: Path) -> None:
    """Test that filenames with newlines cannot inject code into generated files"""

    schema_content = """{"type": "object", "properties": {"name": {"type": "string"}}}"""

    malicious_filename = """schema.json
# INJECTED CODE:
import os
os.system('echo INJECTED')
# END INJECTION"""

    output_path = tmp_path / "output.py"

    generate(
        input_=schema_content,
        input_filename=malicious_filename,
        input_file_type=InputFileType.JsonSchema,
        output=output_path,
    )

    generated_content = output_path.read_text()

    assert "#   filename:  schema.json # INJECTED CODE: import os" in generated_content, (
        "Filename not properly sanitized"
    )

    assert not any(
        line.strip().startswith("import os") and not line.strip().startswith("#")
        for line in generated_content.split("\n")
    )
    assert not any("os.system" in line and not line.strip().startswith("#") for line in generated_content.split("\n"))

    compile(generated_content, str(output_path), "exec")


def test_filename_with_various_control_characters(tmp_path: Path) -> None:
    """Test that various control characters in filenames are properly sanitized"""

    schema_content = """{"type": "object", "properties": {"test": {"type": "string"}}}"""

    test_cases = [
        ("newline", "schema.json\nimport os; os.system('echo INJECTED')"),
        ("carriage_return", "schema.json\rimport os; os.system('echo INJECTED')"),
        ("crlf", "schema.json\r\nimport os; os.system('echo INJECTED')"),
        ("tab_newline", "schema.json\t\nimport os; os.system('echo TAB')"),
        ("form_feed", "schema.json\f\nimport os; os.system('echo FF')"),
        ("vertical_tab", "schema.json\v\nimport os; os.system('echo VT')"),
        ("unicode_line_separator", "schema.json\u2028import os; os.system('echo U2028')"),
        ("unicode_paragraph_separator", "schema.json\u2029import os; os.system('echo U2029')"),
        ("multiple_newlines", "schema.json\n\n\nimport os; os.system('echo MULTI')"),
        ("mixed_characters", "schema.json\n\r\t\nimport os; os.system('echo MIXED')"),
    ]

    for test_name, malicious_filename in test_cases:
        output_path = tmp_path / "output.py"

        generate(
            input_=schema_content,
            input_filename=malicious_filename,
            input_file_type=InputFileType.JsonSchema,
            output=output_path,
        )

        generated_content = output_path.read_text()

        assert not any(
            line.strip().startswith("import ") and not line.strip().startswith("#")
            for line in generated_content.split("\n")
        ), f"Injection found for {test_name}"

        assert not any(
            "os.system" in line and not line.strip().startswith("#") for line in generated_content.split("\n")
        ), f"System call found for {test_name}"

        compile(generated_content, str(output_path), "exec")
