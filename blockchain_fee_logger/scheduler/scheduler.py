from asyncio import AbstractEventLoop

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from blockchain_fee_logger.execution.execution import log_current_fee_for_blockchain
from blockchain_fee_logger.logger.logger import LoggerFactory
from blockchain_fee_logger.utils.config_utils import LoggerConfig
from blockchain_fee_logger.utils.request_utils import SessionFactory


def get_scheduler(
    event_loop: AbstractEventLoop,
    logger_config: LoggerConfig,
) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler({"apscheduler.event_loop": event_loop})
    trigger = IntervalTrigger(seconds=logger_config.check_interval_seconds)
    for blockchain_config in logger_config.blockchain_configs.values():
        scheduler.add_job(
            func=log_current_fee_for_blockchain,
            args=(blockchain_config,),
            trigger=trigger,
        )
    return scheduler


def clear_all_jobs(scheduler: AsyncIOScheduler) -> None:
    scheduler.pause()
    scheduler.remove_all_jobs()
    scheduler.resume()


def start_scheduler(scheduler: AsyncIOScheduler, event_loop: AbstractEventLoop) -> None:
    LoggerFactory.get_logger().info("The application is starting ...")
    scheduler.start()
    event_loop.run_forever()


async def scheduler_teardown(
    scheduler: AsyncIOScheduler, event_loop: AbstractEventLoop
) -> None:
    await SessionFactory.close_session()
    scheduler.shutdown()
    event_loop.stop()


def stop_scheduler(scheduler: AsyncIOScheduler, event_loop: AbstractEventLoop) -> None:
    LoggerFactory.get_logger().info("The application is stopping ...")
    clear_all_jobs(scheduler)
    scheduler.add_job(func=scheduler_teardown, args=(scheduler, event_loop))
