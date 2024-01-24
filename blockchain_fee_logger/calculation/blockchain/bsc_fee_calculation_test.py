from pendulum import UTC, DateTime

from blockchain_fee_logger.calculation.blockchain.bsc_fee_calculation import (
    calculate_bsc_fee,
)
from blockchain_fee_logger.calculation.fee_calculation_result import (
    FeeCalculationResult,
)
from blockchain_fee_logger.retrieval.blockchain.bsc_fee_retrieval import BscFeeResponse
from blockchain_fee_logger.utils.enum_utils import Blockchain, Unit
from blockchain_fee_logger.utils.math_utils import get_decimal


def test_calculate_bsc_fee() -> None:
    sample_bsc_fee_response = BscFeeResponse.model_validate_json(
        """{
    "jsonrpc": "2.0",
    "id": 1,
    "result": "0xb2d05e00"
}"""
    )
    response_datetime = DateTime.now(tz=UTC)
    fee_calculation_result = calculate_bsc_fee(
        sample_bsc_fee_response,
        response_datetime,
        transaction_gas_unit_limit=55_000,
        base_fee_per_gas_unit_in_wei=0,
    )
    expected_fee_calculation_result = FeeCalculationResult(
        blockchain=Blockchain.BSC.value,
        unit=Unit.BNB.value,
        timestamp=response_datetime,
        fee=get_decimal("0.000165"),
    )
    assert fee_calculation_result == expected_fee_calculation_result
