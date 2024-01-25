from pendulum import DateTime

from blockchain_fee_logger.calculation.fee_calculation_result import (
    FeeCalculationResult,
)
from blockchain_fee_logger.retrieval.blockchain.bsc_fee_retrieval import BscFeeResponse
from blockchain_fee_logger.utils.enum_utils import Blockchain, Unit
from blockchain_fee_logger.utils.math_utils import get_decimal


def calculate_bsc_fee(
    bsc_fee_response: BscFeeResponse,
    response_datetime: DateTime,
    transaction_gas_unit_limit: int,
    base_fee_per_gas_unit_in_wei: int,
) -> FeeCalculationResult:
    priority_fee_per_gas_unit_in_wei = int(bsc_fee_response.result, 16)
    fee_per_gas_unit_in_wei = (
        base_fee_per_gas_unit_in_wei + priority_fee_per_gas_unit_in_wei
    )
    transaction_fee_bnbs = (
        get_decimal(transaction_gas_unit_limit)
        * fee_per_gas_unit_in_wei
        / get_decimal(10) ** 18
    )
    return FeeCalculationResult(
        blockchain=Blockchain.BSC.value,
        unit=Unit.BNB.value,
        timestamp=response_datetime,
        fee=transaction_fee_bnbs,
    )
