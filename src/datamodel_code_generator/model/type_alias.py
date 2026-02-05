from typing import ClassVar
from datamodel_code_generator.imports import Import, IMPORT_ANNOTATED, IMPORT_TYPE_ALIAS_BACKPORT
from datamodel_code_generator.model import DataModel
from datamodel_code_generator.types import chain_as_tuple

class TypeAlias(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "TypeAliasAnnotation.jinja2"
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = (IMPORT_TYPE_ALIAS_BACKPORT,)

    @property
    def imports(self) -> tuple[Import, ...]:
        imports = super().imports
        if self.fields and (self.fields[0].annotated or self.fields[0].field):
            imports = chain_as_tuple(imports, (IMPORT_ANNOTATED,))
        return imports
