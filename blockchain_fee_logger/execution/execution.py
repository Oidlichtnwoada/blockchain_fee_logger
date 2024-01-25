from asyncio import TimeoutError

from aiohttp.client_exceptions import ClientError
from pydantic import ValidationError

from blockchain_fee_logger.calculation.blockchain.bsc_fee_calculation import (
    calculate_bsc_fee,
)
from blockchain_fee_logger.calculation.blockchain.btc_fee_calculation import (
    calculate_btc_fee,
)
from blockchain_fee_logger.reporting.reporting import (
    log_calculation_fee_result,
    log_exception,
)
from blockchain_fee_logger.retrieval.blockchain.bsc_fee_retrieval import (
    get_bsc_fee_response,
)
from blockchain_fee_logger.retrieval.blockchain.btc_fee_retrieval import (
    get_btc_fee_response,
)
from blockchain_fee_logger.utils.config_utils import (
    BlockchainConfigUnion,
    BscConfig,
    BitcoinConfig,
)


async def log_current_fee_for_blockchain(
    blockchain_config: BlockchainConfigUnion,
) -> None:
    try:
        match blockchain_config:
            case BitcoinConfig():
                btc_fee_response = await get_btc_fee_response(
                    confirmation_probability_percentage=blockchain_config.confirmation_probability_percentage
                )
                calculation_result = calculate_btc_fee(
                    btc_fee_response,
                    transaction_virtual_bytes=blockchain_config.transaction_virtual_bytes,
                    target_confirmation_minutes=blockchain_config.target_confirmation_minutes,
                )
            case BscConfig():
                bsc_fee_response, response_datetime = await get_bsc_fee_response()
                calculation_result = calculate_bsc_fee(
                    bsc_fee_response,
                    response_datetime,
                    transaction_gas_unit_limit=blockchain_config.transaction_gas_unit_limit,
                    base_fee_per_gas_unit_in_wei=blockchain_config.base_fee_per_gas_unit_in_wei,
                )
            case _:
                raise ValueError("Unsupported blockchain")
    except (ClientError, TimeoutError, ValidationError) as e:
        log_exception(e)
        return
    log_calculation_fee_result(calculation_result)
