from asyncio import AbstractEventLoop

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from blockchain_fee_logger.execution.execution import log_current_fee_for_blockchain
from blockchain_fee_logger.logger.logger import LoggerFactory
from blockchain_fee_logger.utils.enum_utils import Blockchain


def get_scheduler(
    event_loop: AbstractEventLoop, interval_seconds: int = 10
) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler({"apscheduler.event_loop": event_loop})
    trigger = IntervalTrigger(seconds=interval_seconds)
    for blockchain in Blockchain:
        scheduler.add_job(
            func=log_current_fee_for_blockchain, args=(blockchain,), trigger=trigger
        )
    return scheduler


def start_scheduler(scheduler: AsyncIOScheduler, event_loop: AbstractEventLoop) -> None:
    LoggerFactory.get_logger().info("The application is starting ...")
    scheduler.start()
    event_loop.run_forever()


def stop_scheduler(scheduler: AsyncIOScheduler, event_loop: AbstractEventLoop) -> None:
    LoggerFactory.get_logger().info("The application is stopping ...")
    scheduler.shutdown()
    event_loop.stop()
