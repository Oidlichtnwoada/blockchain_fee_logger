from pendulum import DateTime, UTC

from blockchain_fee_logger.calculation.fee_calculation_result import (
    FeeCalculationResult,
)
from blockchain_fee_logger.retrieval.blockchain.btc_fee_retrieval import (
    BtcFeeResponse,
    TargetConfirmationMinutes,
)
from blockchain_fee_logger.utils.enum_utils import Blockchain, Unit
from blockchain_fee_logger.utils.math_utils import get_decimal


def calculate_btc_fee(
    btc_fee_response: BtcFeeResponse,
    transaction_virtual_bytes: int = 140,
    target_confirmation_minutes: TargetConfirmationMinutes = "30",
) -> FeeCalculationResult:
    unix_timestamp = btc_fee_response.timestamp
    sat_per_vbyte = btc_fee_response.estimates[
        target_confirmation_minutes
    ].sat_per_vbyte
    transaction_fee_btcs = (
        sat_per_vbyte * transaction_virtual_bytes / get_decimal(10) ** 8
    )
    return FeeCalculationResult(
        blockchain=Blockchain.Bitcoin.value,
        unit=Unit.BTC.value,
        timestamp=DateTime.fromtimestamp(unix_timestamp, tz=UTC),
        fee=transaction_fee_btcs,
    )
