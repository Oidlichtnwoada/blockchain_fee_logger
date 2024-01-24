import signal

from blockchain_fee_logger.scheduler.scheduler import (
    get_scheduler,
    stop_scheduler,
    start_scheduler,
)


def main() -> None:
    scheduler = get_scheduler()
    for sigint in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sigint, lambda signum, frame: stop_scheduler(scheduler))
    start_scheduler(scheduler)


if __name__ == "__main__":
    main()
