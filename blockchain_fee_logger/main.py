from asyncio import get_event_loop, AbstractEventLoop
from functools import partial
from signal import signal, SIGINT, SIGTERM
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


def register_signal_handler(
    sigints: tuple[int, ...],
    event_loop: AbstractEventLoop,
    scheduler: AsyncIOScheduler,
) -> None:
    for sigint in sigints:
        handler = partial(signal_handler, event_loop=event_loop, scheduler=scheduler)
        signal(sigint, handler)
        asyncio_handler = partial(handler, signum=sigint, frame=None)
        event_loop.add_signal_handler(sigint, asyncio_handler)


def main() -> None:
    event_loop = get_event_loop()
    scheduler = get_scheduler(event_loop)
    register_signal_handler((SIGINT, SIGTERM), event_loop, scheduler)
    start_scheduler(scheduler, event_loop)


if __name__ == "__main__":
    main()
