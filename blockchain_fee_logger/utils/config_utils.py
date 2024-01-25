from os import pardir
from os.path import dirname, join
from typing import Union

from pydantic import BaseModel, field_validator, Field

from blockchain_fee_logger.retrieval.blockchain.btc_fee_retrieval import (
    ConfirmationProbabilityPercentage,
    TargetConfirmationMinutes,
)
from blockchain_fee_logger.utils.enum_utils import Blockchain


class BitcoinConfig(BaseModel):
    blockchain: Blockchain = Field(default=Blockchain.Bitcoin)
    confirmation_probability_percentage: ConfirmationProbabilityPercentage
    transaction_virtual_bytes: int
    target_confirmation_minutes: TargetConfirmationMinutes


class BscConfig(BaseModel):
    blockchain: Blockchain = Field(default=Blockchain.BSC)
    transaction_gas_unit_limit: int
    base_fee_per_gas_unit_in_wei: int


BlockchainConfigUnion = Union[BitcoinConfig, BscConfig]

BlockchainConfigurations = dict[Blockchain, BlockchainConfigUnion]


class LoggerConfig(BaseModel):
    blockchain_configs: BlockchainConfigurations

    @field_validator("blockchain_configs")
    @classmethod
    def blockchain_type_must_match(
        cls, blockchain_configs: BlockchainConfigurations
    ) -> BlockchainConfigurations:
        for blockchain, blockchain_config in blockchain_configs.items():
            if blockchain != blockchain_config.blockchain:
                raise ValueError("Wrong blockchain configuration object")
        return blockchain_configs


def get_default_logger_config_json_file_path() -> str:
    return join(dirname(__file__), pardir, "default_config.json")


def get_logger_config_from_json_file(file_path: str) -> LoggerConfig:
    with open(file_path, "r") as file:
        content = file.read()
    return LoggerConfig.model_validate_json(content)
