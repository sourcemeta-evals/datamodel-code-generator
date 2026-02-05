from __future__ import annotations

import sys
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, NamedTuple

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


def _create_type_alias_model_factory(
    python_version: PythonVersion,
    use_pydantic_v2: bool,
) -> type[DataModel]:
    """Create a TypeAliasModel factory with the given python_version and use_pydantic_v2."""
    from .type_alias import TypeAliasModel  # noqa: PLC0415

    class TypeAliasModelWithVersion(TypeAliasModel):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(
                python_version=python_version,
                use_pydantic_v2=use_pydantic_v2,
                **kwargs,
            )

    return TypeAliasModelWithVersion


def get_data_model_types(
    data_model_type: DataModelType,
    target_python_version: PythonVersion = DEFAULT_TARGET_PYTHON_VERSION,
    use_type_alias: bool = False,
) -> DataModelSet:
    from datamodel_code_generator import DataModelType  # noqa: PLC0415

    from . import dataclass, msgspec, pydantic, pydantic_v2, rootmodel, typed_dict  # noqa: PLC0415
    from .types import DataTypeManager  # noqa: PLC0415

    if data_model_type == DataModelType.PydanticBaseModel:
        type_alias_model = _create_type_alias_model_factory(target_python_version, False)
        return DataModelSet(
            data_model=pydantic.BaseModel,
            root_model=type_alias_model if use_type_alias else pydantic.CustomRootType,
            field_model=pydantic.DataModelField,
            data_type_manager=pydantic.DataTypeManager,
            dump_resolve_reference_action=pydantic.dump_resolve_reference_action,
        )
    if data_model_type == DataModelType.PydanticV2BaseModel:
        type_alias_model = _create_type_alias_model_factory(target_python_version, True)
        return DataModelSet(
            data_model=pydantic_v2.BaseModel,
            root_model=type_alias_model if use_type_alias else pydantic_v2.RootModel,
            field_model=pydantic_v2.DataModelField,
            data_type_manager=pydantic_v2.DataTypeManager,
            dump_resolve_reference_action=pydantic_v2.dump_resolve_reference_action,
        )
    if data_model_type == DataModelType.DataclassesDataclass:
        type_alias_model = _create_type_alias_model_factory(target_python_version, False)
        return DataModelSet(
            data_model=dataclass.DataClass,
            root_model=type_alias_model if use_type_alias else rootmodel.RootModel,
            field_model=dataclass.DataModelField,
            data_type_manager=dataclass.DataTypeManager,
            dump_resolve_reference_action=None,
        )
    if data_model_type == DataModelType.TypingTypedDict:
        type_alias_model = _create_type_alias_model_factory(target_python_version, False)
        return DataModelSet(
            data_model=typed_dict.TypedDict,
            root_model=type_alias_model if use_type_alias else rootmodel.RootModel,
            field_model=(
                typed_dict.DataModelField
                if target_python_version.has_typed_dict_non_required
                else typed_dict.DataModelFieldBackport
            ),
            data_type_manager=DataTypeManager,
            dump_resolve_reference_action=None,
        )
    if data_model_type == DataModelType.MsgspecStruct:
        type_alias_model = _create_type_alias_model_factory(target_python_version, False)
        return DataModelSet(
            data_model=msgspec.Struct,
            root_model=type_alias_model if use_type_alias else msgspec.RootModel,
            field_model=msgspec.DataModelField,
            data_type_manager=msgspec.DataTypeManager,
            dump_resolve_reference_action=None,
            known_third_party=["msgspec"],
        )
    msg = f"{data_model_type} is unsupported data model type"
    raise ValueError(msg)  # pragma: no cover


__all__ = ["ConstraintsBase", "DataModel", "DataModelFieldBase"]
