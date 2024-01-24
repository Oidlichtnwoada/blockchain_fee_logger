from decimal import Context, setcontext

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from blockchain_fee_logger.execution.execution import log_current_fee_for_blockchain
from blockchain_fee_logger.logger.logger import LoggerFactory
from blockchain_fee_logger.utils.enum_utils import Blockchain


def get_scheduler(interval_seconds: int = 10, workers: int = 32) -> BlockingScheduler:
    executors = {
        "default": ThreadPoolExecutor(max_workers=workers),
    }
    background_scheduler = BlockingScheduler(executors=executors)
    trigger = IntervalTrigger(seconds=interval_seconds)
    for blockchain in Blockchain:
        background_scheduler.add_job(
            func=log_current_fee_for_blockchain, args=(blockchain,), trigger=trigger
        )
    return background_scheduler


def start_scheduler(scheduler: BaseScheduler) -> None:
    LoggerFactory.get_logger().info("The application is starting ...")
    setcontext(Context(prec=128))
    scheduler.start()


def stop_scheduler(scheduler: BaseScheduler) -> None:
    LoggerFactory.get_logger().info("The application is stopping ...")
    scheduler.shutdown()
