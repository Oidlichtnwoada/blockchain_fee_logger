from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FeeCalculationResult(BaseModel):
    blockchain: str
    unit: str
    timestamp: datetime
    fee: Decimal
