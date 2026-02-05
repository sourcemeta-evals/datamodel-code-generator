from __future__ import annotations

import pytest

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.model.type_alias import (
    TypeAliasModel,
    create_type_alias_model_class,
)
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType


class TestTypeAliasModel:
    def test_create_type_alias_model_class_py312_pydantic_v2(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_312, use_pydantic_v2=True)
        assert cls._class_target_python_version == PythonVersion.PY_312
        assert cls._class_use_pydantic_v2 is True

    def test_create_type_alias_model_class_py310_pydantic_v2(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_310, use_pydantic_v2=True)
        assert cls._class_target_python_version == PythonVersion.PY_310
        assert cls._class_use_pydantic_v2 is True

    def test_create_type_alias_model_class_py39_pydantic_v1(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_39, use_pydantic_v2=False)
        assert cls._class_target_python_version == PythonVersion.PY_39
        assert cls._class_use_pydantic_v2 is False

    def test_type_alias_style_py312(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_312, use_pydantic_v2=True)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic_v2 import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        assert instance.type_alias_style == "type_statement"

    def test_type_alias_style_py310_pydantic_v2(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_310, use_pydantic_v2=True)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic_v2 import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        assert instance.type_alias_style == "type_alias_type"

    def test_type_alias_style_py39_pydantic_v1(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_39, use_pydantic_v2=False)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        assert instance.type_alias_style == "type_alias_annotation"

    def test_render_type_statement(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_312, use_pydantic_v2=True)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic_v2 import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        assert instance.render() == "type Total = int"

    def test_render_type_alias_type(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_310, use_pydantic_v2=True)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic_v2 import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        assert instance.render() == 'Total = TypeAliasType("Total", int)'

    def test_render_type_alias_annotation(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_39, use_pydantic_v2=False)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        assert instance.render() == "Total: TypeAlias = int"

    def test_imports_type_statement(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_312, use_pydantic_v2=True)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic_v2 import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        imports = instance.imports
        import_strs = [f"{i.from_}.{i.import_}" for i in imports]
        assert "typing_extensions.TypeAliasType" not in import_strs
        assert "typing.TypeAlias" not in import_strs

    def test_imports_type_alias_type(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_310, use_pydantic_v2=True)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic_v2 import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        imports = instance.imports
        import_strs = [f"{i.from_}.{i.import_}" for i in imports]
        assert "typing_extensions.TypeAliasType" in import_strs

    def test_imports_type_alias_annotation_py39(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_39, use_pydantic_v2=False)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        imports = instance.imports
        import_strs = [f"{i.from_}.{i.import_}" for i in imports]
        assert "typing_extensions.TypeAlias" in import_strs

    def test_imports_type_alias_annotation_py310(self) -> None:
        cls = create_type_alias_model_class(PythonVersion.PY_310, use_pydantic_v2=False)
        ref = Reference(path="test", name="Total")
        dt = DataType(type="int")
        from datamodel_code_generator.model.pydantic import DataModelField

        field = DataModelField(data_type=dt, required=True)
        instance = cls(reference=ref, fields=[field])
        imports = instance.imports
        import_strs = [f"{i.from_}.{i.import_}" for i in imports]
        assert "typing.TypeAlias" in import_strs

    def test_is_py_312_or_later(self) -> None:
        for version in [PythonVersion.PY_312, PythonVersion.PY_313, PythonVersion.PY_314]:
            cls = create_type_alias_model_class(version, use_pydantic_v2=True)
            ref = Reference(path="test", name="Total")
            dt = DataType(type="int")
            from datamodel_code_generator.model.pydantic_v2 import DataModelField

            field = DataModelField(data_type=dt, required=True)
            instance = cls(reference=ref, fields=[field])
            assert instance._is_py_312_or_later is True

        for version in [PythonVersion.PY_39, PythonVersion.PY_310, PythonVersion.PY_311]:
            cls = create_type_alias_model_class(version, use_pydantic_v2=True)
            ref = Reference(path="test", name="Total")
            dt = DataType(type="int")
            from datamodel_code_generator.model.pydantic_v2 import DataModelField

            field = DataModelField(data_type=dt, required=True)
            instance = cls(reference=ref, fields=[field])
            assert instance._is_py_312_or_later is False
