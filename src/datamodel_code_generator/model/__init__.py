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


def _create_type_alias_class(
    target_python_version: PythonVersion,
    use_pydantic_v2: bool,
) -> type[DataModel]:
    """Create a TypeAlias class with the appropriate Python version and Pydantic version settings."""
    from functools import partial  # noqa: PLC0415

    from .type_alias import TypeAlias  # noqa: PLC0415

    class TypeAliasWithVersion(TypeAlias):
        """TypeAlias class with Python version and Pydantic version pre-configured."""

        _python_version = target_python_version
        _use_pydantic_v2 = use_pydantic_v2

        def __init__(self, **kwargs: object) -> None:
            kwargs.setdefault("python_version", self._python_version)  # type: ignore[arg-type]
            kwargs.setdefault("use_pydantic_v2", self._use_pydantic_v2)  # type: ignore[arg-type]
            super().__init__(**kwargs)  # type: ignore[arg-type]

    return TypeAliasWithVersion


def get_data_model_types(
    data_model_type: DataModelType,
    target_python_version: PythonVersion = DEFAULT_TARGET_PYTHON_VERSION,
    *,
    use_type_alias: bool = False,
) -> DataModelSet:
    from datamodel_code_generator import DataModelType  # noqa: PLC0415

    from . import dataclass, msgspec, pydantic, pydantic_v2, rootmodel, typed_dict  # noqa: PLC0415
    from .types import DataTypeManager  # noqa: PLC0415

    if data_model_type == DataModelType.PydanticBaseModel:
        root_model: type[DataModel]
        if use_type_alias:
            root_model = _create_type_alias_class(target_python_version, use_pydantic_v2=False)
        else:
            root_model = pydantic.CustomRootType
        return DataModelSet(
            data_model=pydantic.BaseModel,
            root_model=root_model,
            field_model=pydantic.DataModelField,
            data_type_manager=pydantic.DataTypeManager,
            dump_resolve_reference_action=pydantic.dump_resolve_reference_action,
        )
    if data_model_type == DataModelType.PydanticV2BaseModel:
        if use_type_alias:
            root_model = _create_type_alias_class(target_python_version, use_pydantic_v2=True)
        else:
            root_model = pydantic_v2.RootModel
        return DataModelSet(
            data_model=pydantic_v2.BaseModel,
            root_model=root_model,
            field_model=pydantic_v2.DataModelField,
            data_type_manager=pydantic_v2.DataTypeManager,
            dump_resolve_reference_action=pydantic_v2.dump_resolve_reference_action,
        )
    if data_model_type == DataModelType.DataclassesDataclass:
        if use_type_alias:
            root_model = _create_type_alias_class(target_python_version, use_pydantic_v2=False)
        else:
            root_model = rootmodel.RootModel
        return DataModelSet(
            data_model=dataclass.DataClass,
            root_model=root_model,
            field_model=dataclass.DataModelField,
            data_type_manager=dataclass.DataTypeManager,
            dump_resolve_reference_action=None,
        )
    if data_model_type == DataModelType.TypingTypedDict:
        if use_type_alias:
            root_model = _create_type_alias_class(target_python_version, use_pydantic_v2=False)
        else:
            root_model = rootmodel.RootModel
        return DataModelSet(
            data_model=typed_dict.TypedDict,
            root_model=root_model,
            field_model=(
                typed_dict.DataModelField
                if target_python_version.has_typed_dict_non_required
                else typed_dict.DataModelFieldBackport
            ),
            data_type_manager=DataTypeManager,
            dump_resolve_reference_action=None,
        )
    if data_model_type == DataModelType.MsgspecStruct:
        if use_type_alias:
            root_model = _create_type_alias_class(target_python_version, use_pydantic_v2=False)
        else:
            root_model = msgspec.RootModel
        return DataModelSet(
            data_model=msgspec.Struct,
            root_model=root_model,
            field_model=msgspec.DataModelField,
            data_type_manager=msgspec.DataTypeManager,
            dump_resolve_reference_action=None,
            known_third_party=["msgspec"],
        )
    msg = f"{data_model_type} is unsupported data model type"
    raise ValueError(msg)  # pragma: no cover


__all__ = ["ConstraintsBase", "DataModel", "DataModelFieldBase"]
