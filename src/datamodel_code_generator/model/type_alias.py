from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.imports import Import
from datamodel_code_generator.model import DataModel


class TypeAliasModel(DataModel):
    """Renders a root model as a TypeAlias annotation (pre-3.12).

    Output example::

        MyType: TypeAlias = str
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAlias.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (
        Import(from_="typing_extensions", import_="TypeAlias"),
    )

    def __init__(self, **kwargs: Any) -> None:
        # TypeAlias models never have a base class
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


class NativeTypeAliasModel(DataModel):
    """Renders a root model using the native ``type`` statement (3.12+).

    Output example::

        type MyType = str
    """

    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasNative.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(self, **kwargs: Any) -> None:
        # Native type alias models never have a base class
        kwargs.pop("custom_base_class", None)
        super().__init__(**kwargs)


_PY_312_AND_LATER = {
    PythonVersion.PY_312,
    PythonVersion.PY_313,
    PythonVersion.PY_314,
}


def get_type_alias_model_class(
    target_python_version: PythonVersion,
) -> type[DataModel]:
    """Return the appropriate TypeAlias model class based on Python version."""
    if target_python_version in _PY_312_AND_LATER:
        return NativeTypeAliasModel
    return TypeAliasModel
