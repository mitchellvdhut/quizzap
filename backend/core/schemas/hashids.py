from typing import Any, Callable

from pydantic_core import core_schema
from core.helpers.hashids import encode, decode_single


class HashId(int):
    """Pydantic type for hashing integer"""

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        # calling handler(core_schema) here raises an exception
        json_schema = {}
        json_schema.update(type="string", format="binary")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value, schema):
        if not isinstance(value, int):
            raise TypeError('integer required')        
        return encode(value)
    

class DehashId(str):
    """Pydantic type for dehashing hash"""
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        # calling handler(core_schema) here raises an exception
        json_schema = {}
        json_schema.update(type="string", format="binary")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value, schema):
        if not isinstance(value, str):
            raise TypeError('hash required')
        
        return decode_single(value)
