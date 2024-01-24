from decimal import Decimal, Context

from pydantic import Field

INTEGRAL_PART_PLACES = 128
DECIMAL_PART_PLACES = 128
TOTAL_PLACES = INTEGRAL_PART_PLACES + DECIMAL_PART_PLACES


def get_pydantic_decimal_field() -> Decimal:
    return Field(max_digits=TOTAL_PLACES, decimal_places=DECIMAL_PART_PLACES)


def get_decimal(value: int | str) -> Decimal:
    return Decimal(value, context=Context(prec=TOTAL_PLACES))
