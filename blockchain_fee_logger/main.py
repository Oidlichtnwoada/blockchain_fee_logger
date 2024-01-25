import signal
from asyncio import get_event_loop, AbstractEventLoop
from functools import partial
from types import FrameType
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from blockchain_fee_logger.scheduler.scheduler import (
    get_scheduler,
    stop_scheduler,
    start_scheduler,
)


def signal_handler(
    signum: int,
    frame: Optional[FrameType],
    event_loop: AbstractEventLoop,
    scheduler: AsyncIOScheduler,
) -> None:
    stop_scheduler(scheduler, event_loop)


def main() -> None:
    event_loop = get_event_loop()
    scheduler = get_scheduler(event_loop)
    for sigint in (signal.SIGINT, signal.SIGTERM):
        handler = partial(signal_handler, event_loop=event_loop, scheduler=scheduler)
        signal.signal(sigint, handler)
        asyncio_handler = partial(handler, signum=sigint, frame=None)
        event_loop.add_signal_handler(sigint, asyncio_handler)
    start_scheduler(scheduler, event_loop)


if __name__ == "__main__":
    main()
