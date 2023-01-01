from dataclasses import dataclass
from typing import Any, Optional, Union
from pydantic import BaseModel


@dataclass
class ExcelSettingDefinition:
    strings_to_numbers: bool = False
    strings_to_formulas: bool = True
    strings_to_urls: bool = True
    nan_inf_to_errors: bool = False
    default_date_format: str = None
    remove_timezone: bool = False
    use_future_functions: bool = False
    max_url_length: int = 0


@dataclass
class ExcelFormatDefinition:
    key: str
    value: object
    column_index: Union[int, None] = None


@dataclass
class ExcelHeaderInfoDefinition:
    name: str
    type: str
    column_width: Optional[float] = 20


@dataclass
class ExcelHeaderDefinition:
    headers: list[ExcelHeaderInfoDefinition]
    formats: Union[list[ExcelFormatDefinition], None] = None
    default_column_width: Optional[float] = 20
    default_row_height: Optional[float] = 20


@dataclass
class ExcelWorksheetDefinition:
    name: str
    definition: ExcelHeaderDefinition
    data: object
    formats: Union[list[ExcelFormatDefinition], None] = None
    start_row: Union[int, None] = 1
    start_column: Union[int, None] = 0
    translations: Union[dict[str, str], None] = None


@dataclass
class ExcelRequest:
    filename: str
    data: list[ExcelWorksheetDefinition]
    global_settings: Union[ExcelSettingDefinition, None] = None
