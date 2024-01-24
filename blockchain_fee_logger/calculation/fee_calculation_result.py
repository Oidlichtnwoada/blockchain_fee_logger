from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from blockchain_fee_logger.utils.math_utils import get_pydantic_decimal_field


class FeeCalculationResult(BaseModel):
    blockchain: str
    unit: str
    timestamp: datetime
    fee: Decimal = get_pydantic_decimal_field()
