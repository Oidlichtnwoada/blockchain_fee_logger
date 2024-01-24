import time

from pendulum import DateTime, UTC

from blockchain_fee_logger.calculation.blockchain.btc_fee_calculation import (
    calculate_btc_fee,
)
from blockchain_fee_logger.calculation.fee_calculation_result import (
    FeeCalculationResult,
)
from blockchain_fee_logger.retrieval.blockchain.btc_fee_retrieval import BtcFeeResponse
from blockchain_fee_logger.utils.enum_utils import Blockchain, Unit
from blockchain_fee_logger.utils.math_utils import get_decimal


def test_calculate_btc_fee() -> None:
    current_timestamp = int(time.time())
    current_datetime = DateTime.fromtimestamp(current_timestamp, tz=UTC)
    sample_btc_fee_response = BtcFeeResponse.model_validate_json(
        """{
    "timestamp": %i,
    "estimates": {
        "30": {
            "sat_per_vbyte": 41.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5781.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 6806.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 9266.0
                }
            }
        },
        "60": {
            "sat_per_vbyte": 39.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5499.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 6474.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 8814.0
                }
            }
        },
        "120": {
            "sat_per_vbyte": 36.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5076.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5976.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 8136.0
                }
            }
        },
        "180": {
            "sat_per_vbyte": 36.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5076.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5976.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 8136.0
                }
            }
        },
        "360": {
            "sat_per_vbyte": 34.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 4794.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5644.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 7684.0
                }
            }
        },
        "720": {
            "sat_per_vbyte": 33.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 4653.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5478.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 7458.0
                }
            }
        },
        "1440": {
            "sat_per_vbyte": 33.0,
            "total": {
                "p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 4653.0
                },
                "p2sh-p2wpkh": {
                    "usd": "NaN",
                    "satoshi": 5478.0
                },
                "p2pkh": {
                    "usd": "NaN",
                    "satoshi": 7458.0
                }
            }
        }
    }
}"""
        % current_timestamp
    )
    fee_calculation_result = calculate_btc_fee(
        sample_btc_fee_response,
        transaction_virtual_bytes=140,
        target_confirmation_minutes="30",
    )
    expected_fee_calculation_result = FeeCalculationResult(
        blockchain=Blockchain.Bitcoin.value,
        unit=Unit.BTC.value,
        timestamp=current_datetime,
        fee=get_decimal("0.0000574"),
    )
    assert fee_calculation_result == expected_fee_calculation_result
