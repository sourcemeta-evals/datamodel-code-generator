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


def _get_type_alias_root_model(
    data_model_type: DataModelType,
    target_python_version: PythonVersion,
) -> type[DataModel]:
    """Select the appropriate type alias model class based on output type and Python version."""
    from datamodel_code_generator import DataModelType  # noqa: PLC0415

    from . import type_alias  # noqa: PLC0415

    is_pydantic_v2 = data_model_type == DataModelType.PydanticV2BaseModel
    is_pydantic_v1 = data_model_type == DataModelType.PydanticBaseModel

    if target_python_version.has_type_statement:
        # Python 3.12+: use native `type` statement for all output types
        return type_alias.TypeStatement

    if is_pydantic_v2:
        # Pydantic v2 + Python 3.9-3.11: use TypeAliasType from typing_extensions
        return type_alias.TypeAliasTypeModel

    # Pydantic v1 or non-Pydantic + Python 3.9-3.11: use TypeAlias annotation
    if target_python_version.has_type_alias_in_typing and not is_pydantic_v1:
        # Python 3.10+: TypeAlias from typing
        return type_alias.TypeAliasAnnotation

    # Python 3.9 or Pydantic v1: TypeAlias from typing_extensions
    return type_alias.TypeAliasAnnotationExt


def get_data_model_types(
    data_model_type: DataModelType,
    target_python_version: PythonVersion = DEFAULT_TARGET_PYTHON_VERSION,
    use_type_alias: bool = False,
) -> DataModelSet:
    from datamodel_code_generator import DataModelType  # noqa: PLC0415

    from . import dataclass, msgspec, pydantic, pydantic_v2, rootmodel, typed_dict  # noqa: PLC0415
    from .types import DataTypeManager  # noqa: PLC0415

    result: DataModelSet
    if data_model_type == DataModelType.PydanticBaseModel:
        result = DataModelSet(
            data_model=pydantic.BaseModel,
            root_model=pydantic.CustomRootType,
            field_model=pydantic.DataModelField,
            data_type_manager=pydantic.DataTypeManager,
            dump_resolve_reference_action=pydantic.dump_resolve_reference_action,
        )
    elif data_model_type == DataModelType.PydanticV2BaseModel:
        result = DataModelSet(
            data_model=pydantic_v2.BaseModel,
            root_model=pydantic_v2.RootModel,
            field_model=pydantic_v2.DataModelField,
            data_type_manager=pydantic_v2.DataTypeManager,
            dump_resolve_reference_action=pydantic_v2.dump_resolve_reference_action,
        )
    elif data_model_type == DataModelType.DataclassesDataclass:
        result = DataModelSet(
            data_model=dataclass.DataClass,
            root_model=rootmodel.RootModel,
            field_model=dataclass.DataModelField,
            data_type_manager=dataclass.DataTypeManager,
            dump_resolve_reference_action=None,
        )
    elif data_model_type == DataModelType.TypingTypedDict:
        result = DataModelSet(
            data_model=typed_dict.TypedDict,
            root_model=rootmodel.RootModel,
            field_model=(
                typed_dict.DataModelField
                if target_python_version.has_typed_dict_non_required
                else typed_dict.DataModelFieldBackport
            ),
            data_type_manager=DataTypeManager,
            dump_resolve_reference_action=None,
        )
    elif data_model_type == DataModelType.MsgspecStruct:
        result = DataModelSet(
            data_model=msgspec.Struct,
            root_model=msgspec.RootModel,
            field_model=msgspec.DataModelField,
            data_type_manager=msgspec.DataTypeManager,
            dump_resolve_reference_action=None,
            known_third_party=["msgspec"],
        )
    else:
        msg = f"{data_model_type} is unsupported data model type"
        raise ValueError(msg)  # pragma: no cover

    return _apply_type_alias_override(result, data_model_type, target_python_version, use_type_alias)


def _apply_type_alias_override(
    result: DataModelSet,
    data_model_type: DataModelType,
    target_python_version: PythonVersion,
    use_type_alias: bool,
) -> DataModelSet:
    """Override root_model in the DataModelSet if use_type_alias is enabled."""
    if not use_type_alias:
        return result
    root_model = _get_type_alias_root_model(data_model_type, target_python_version)
    return result._replace(root_model=root_model)


__all__ = ["ConstraintsBase", "DataModel", "DataModelFieldBase"]
