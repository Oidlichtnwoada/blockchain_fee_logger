from decimal import Decimal

from blockchain_fee_logger.calculation.fee_calculation_result import (
    FeeCalculationResult,
)
from blockchain_fee_logger.logger.logger import LoggerFactory


class FeeCache:
    cache: dict[tuple[str, str], Decimal] = {}

    @classmethod
    def get_key_and_value_from_representation(
        cls, result: FeeCalculationResult
    ) -> tuple[tuple[str, str], Decimal]:
        return (
            (result.blockchain, result.unit),
            result.fee,
        )

    @classmethod
    def is_new_value(
        cls, fee_calculation_result: FeeCalculationResult, update_cache: bool = False
    ) -> bool:
        key, new_value = cls.get_key_and_value_from_representation(
            fee_calculation_result
        )
        if key not in cls.cache:
            is_new = True
        else:
            current_value = cls.cache[key]
            is_new = current_value != new_value
        if update_cache:
            cls.add_to_cache(fee_calculation_result)
        return is_new

    @classmethod
    def add_to_cache(cls, fee_calculation_result: FeeCalculationResult) -> None:
        key, value = cls.get_key_and_value_from_representation(fee_calculation_result)
        cls.cache[key] = value


def log_calculation_fee_result(result: FeeCalculationResult) -> None:
    if FeeCache.is_new_value(result, update_cache=True):
        LoggerFactory.get_logger().info(
            f"Fee for {result.blockchain} at {result.timestamp.isoformat()}: {result.fee} {result.unit}"
        )


def log_exception(exception: Exception) -> None:
    LoggerFactory.get_logger().error(
        f"The following exception has occurred: {repr(exception)}"
    )
