from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable, NamedTuple

from datamodel_code_generator import PythonVersion

from .base import ConstraintsBase, DataModel, DataModelFieldBase

if TYPE_CHECKING:
    from collections.abc import Iterable

    from datamodel_code_generator import DataModelType
    from datamodel_code_generator.types import DataTypeManager as DataTypeManagerABC

DEFAULT_TARGET_PYTHON_VERSION = PythonVersion(f"{sys.version_info.major}.{sys.version_info.minor}")


class DataModelSet(NamedTuple):
    data_model: type[DataModel]
    root_model: type[DataModel]
    field_model: type[DataModelFieldBase]
    data_type_manager: type[DataTypeManagerABC]
    dump_resolve_reference_action: Callable[[Iterable[str]], str] | None
    known_third_party: list[str] | None = None


def _is_py312_or_later(target_python_version: PythonVersion) -> bool:
    return target_python_version in {
        PythonVersion.PY_312,
        PythonVersion.PY_313,
        PythonVersion.PY_314,
    }


def _get_type_alias_root_model(
    data_model_type: DataModelType,
    target_python_version: PythonVersion,
) -> type[DataModel]:
    from datamodel_code_generator import DataModelType  # noqa: PLC0415

    from .type_alias import (  # noqa: PLC0415
        TypeAliasAnnotation,
        TypeAliasTypeAliasType,
        TypeAliasTypeStatement,
    )

    if _is_py312_or_later(target_python_version):
        return TypeAliasTypeStatement
    if data_model_type == DataModelType.PydanticV2BaseModel:
        return TypeAliasTypeAliasType
    return TypeAliasAnnotation


def get_data_model_types(
    data_model_type: DataModelType,
    target_python_version: PythonVersion = DEFAULT_TARGET_PYTHON_VERSION,
    *,
    use_type_alias: bool = False,
) -> DataModelSet:
    from datamodel_code_generator import DataModelType  # noqa: PLC0415

    from . import dataclass, msgspec, pydantic, pydantic_v2, rootmodel, typed_dict  # noqa: PLC0415
    from .types import DataTypeManager  # noqa: PLC0415

    if use_type_alias:
        type_alias_root = _get_type_alias_root_model(data_model_type, target_python_version)

    if data_model_type == DataModelType.PydanticBaseModel:
        return DataModelSet(
            data_model=pydantic.BaseModel,
            root_model=type_alias_root if use_type_alias else pydantic.CustomRootType,
            field_model=pydantic.DataModelField,
            data_type_manager=pydantic.DataTypeManager,
            dump_resolve_reference_action=pydantic.dump_resolve_reference_action,
        )
    if data_model_type == DataModelType.PydanticV2BaseModel:
        return DataModelSet(
            data_model=pydantic_v2.BaseModel,
            root_model=type_alias_root if use_type_alias else pydantic_v2.RootModel,
            field_model=pydantic_v2.DataModelField,
            data_type_manager=pydantic_v2.DataTypeManager,
            dump_resolve_reference_action=pydantic_v2.dump_resolve_reference_action,
        )
    if data_model_type == DataModelType.DataclassesDataclass:
        return DataModelSet(
            data_model=dataclass.DataClass,
            root_model=type_alias_root if use_type_alias else rootmodel.RootModel,
            field_model=dataclass.DataModelField,
            data_type_manager=dataclass.DataTypeManager,
            dump_resolve_reference_action=None,
        )
    if data_model_type == DataModelType.TypingTypedDict:
        return DataModelSet(
            data_model=typed_dict.TypedDict,
            root_model=type_alias_root if use_type_alias else rootmodel.RootModel,
            field_model=(
                typed_dict.DataModelField
                if target_python_version.has_typed_dict_non_required
                else typed_dict.DataModelFieldBackport
            ),
            data_type_manager=DataTypeManager,
            dump_resolve_reference_action=None,
        )
    if data_model_type == DataModelType.MsgspecStruct:
        return DataModelSet(
            data_model=msgspec.Struct,
            root_model=type_alias_root if use_type_alias else msgspec.RootModel,
            field_model=msgspec.DataModelField,
            data_type_manager=msgspec.DataTypeManager,
            dump_resolve_reference_action=None,
            known_third_party=["msgspec"],
        )
    msg = f"{data_model_type} is unsupported data model type"
    raise ValueError(msg)  # pragma: no cover


__all__ = ["ConstraintsBase", "DataModel", "DataModelFieldBase"]
