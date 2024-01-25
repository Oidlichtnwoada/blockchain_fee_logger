from decimal import Decimal
from typing import Literal, get_args

from pydantic import BaseModel, Field, field_validator

from blockchain_fee_logger.utils.math_utils import get_pydantic_decimal_field
from blockchain_fee_logger.utils.request_utils import (
    checked_get_request_body_text,
)


class FeeDetails(BaseModel):
    usd: Literal["NaN"]
    satoshi: Decimal = get_pydantic_decimal_field()


class TotalFees(BaseModel):
    p2wpkh: FeeDetails
    p2sh_p2wpkh: FeeDetails = Field(alias="p2sh-p2wpkh")
    p2pkh: FeeDetails


class Estimate(BaseModel):
    sat_per_vbyte: Decimal = get_pydantic_decimal_field()
    total: TotalFees


TargetConfirmationMinutes = Literal["30", "60", "120", "180", "360", "720", "1440"]


class BtcFeeResponse(BaseModel):
    timestamp: int
    estimates: dict[TargetConfirmationMinutes, Estimate]

    @field_validator("estimates")
    @classmethod
    def estimates_must_contain_all_keys(
        cls, estimates: dict[TargetConfirmationMinutes, Estimate]
    ) -> dict[TargetConfirmationMinutes, Estimate]:
        if len(estimates) != len(get_args(TargetConfirmationMinutes)):
            raise ValueError(
                "The estimates must contain values for all confirmation minutes"
            )
        return estimates


ConfirmationProbabilityPercentage = Literal[50, 80, 90]


async def get_btc_fee_response(
    confirmation_probability_percentage: ConfirmationProbabilityPercentage,
) -> BtcFeeResponse:
    response_text = await checked_get_request_body_text(
        "https://bitcoiner.live/api/fees/estimates/latest",
        params={"confidence": confirmation_probability_percentage / 100},
    )
    return BtcFeeResponse.model_validate_json(response_text)
