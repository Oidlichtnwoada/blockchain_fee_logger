from pendulum import DateTime, UTC
from pydantic import BaseModel, field_validator

from blockchain_fee_logger.utils.request_utils import (
    checked_post_request_body_text,
)


class BscFeeResponse(BaseModel):
    id: int
    jsonrpc: str
    result: str

    @field_validator("result")
    @classmethod
    def result_must_be_a_valid_integer(cls, result: str) -> str:
        _ = int(result, 16)
        return result


async def get_bsc_fee_response() -> tuple[BscFeeResponse, DateTime]:
    response_datetime = DateTime.now(tz=UTC)
    response_text = await checked_post_request_body_text(
        "https://bsc.publicnode.com",
        json={
            "id": 1,
            "jsonrpc": "2.0",
            "method": "eth_maxPriorityFeePerGas",
            "params": [],
        },
    )
    return BscFeeResponse.model_validate_json(response_text), response_datetime
