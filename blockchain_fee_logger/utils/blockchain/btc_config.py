from typing import Literal

from pydantic import BaseModel, Field

from blockchain_fee_logger.retrieval.blockchain.btc_fee_retrieval import (
    ConfirmationProbabilityPercentage,
    TargetConfirmationMinutes,
)
from blockchain_fee_logger.utils.enum_utils import Blockchain


class BitcoinConfig(BaseModel):
    blockchain: Literal[Blockchain.Bitcoin] = Field(default=Blockchain.Bitcoin)
    confirmation_probability_percentage: ConfirmationProbabilityPercentage
    transaction_virtual_bytes: int
    target_confirmation_minutes: TargetConfirmationMinutes
