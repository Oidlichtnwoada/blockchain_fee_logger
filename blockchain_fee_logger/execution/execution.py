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
from blockchain_fee_logger.utils.enum_utils import Blockchain


async def log_current_fee_for_blockchain(blockchain: Blockchain) -> None:
    try:
        match blockchain:
            case Blockchain.Bitcoin:
                btc_fee_response = await get_btc_fee_response()
                calculation_result = calculate_btc_fee(btc_fee_response)
            case Blockchain.BSC:
                bsc_fee_response, response_datetime = await get_bsc_fee_response()
                calculation_result = calculate_bsc_fee(
                    bsc_fee_response, response_datetime
                )
            case _:
                raise ValueError("Unsupported blockchain")
    except (ClientError, TimeoutError, ValidationError) as e:
        log_exception(e)
        return
    log_calculation_fee_result(calculation_result)
