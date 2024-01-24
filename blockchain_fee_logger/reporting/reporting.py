from blockchain_fee_logger.calculation.fee_calculation_result import (
    FeeCalculationResult,
)
from blockchain_fee_logger.logger.logger import LoggerFactory


def log_calculation_fee_result(result: FeeCalculationResult) -> None:
    LoggerFactory.get_logger().info(
        f"Fee for {result.blockchain} at {result.timestamp.isoformat()}: {result.fee} {result.unit}"
    )


def log_exception(exception: Exception) -> None:
    LoggerFactory.get_logger().error(
        f"The following exception has occurred: {repr(exception)}"
    )
