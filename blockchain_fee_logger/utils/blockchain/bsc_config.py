from typing import Literal

from pydantic import BaseModel, Field

from blockchain_fee_logger.utils.enum_utils import Blockchain


class BscConfig(BaseModel):
    blockchain: Literal[Blockchain.BSC] = Field(default=Blockchain.BSC)
    transaction_gas_unit_limit: int
    base_fee_per_gas_unit_in_wei: int
