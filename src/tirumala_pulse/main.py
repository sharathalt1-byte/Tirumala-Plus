import argparse

from tirumala_pulse.services.backfill_service import (
    BackfillService,
)
from tirumala_pulse.services.etl_service import (
    ETLService,
)
from tirumala_pulse.utils.logger import get_logger

logger = get_logger(__name__)


def main():

    parser = argparse.ArgumentParser(description="Tirumala Pulse ETL")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Daily ETL

    subparsers.add_parser(
        "etl",
        help="Run daily ETL",
    )

    # Historical Backfill

    backfill = subparsers.add_parser(
        "backfill",
        help="Run historical backfill",
    )

    backfill.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Limit pages processed.",
    )

    backfill.add_argument(
        "--reset",
        action="store_true",
        help="Reset checkpoint before running.",
    )

    args = parser.parse_args()

    if args.command == "etl":

        logger.info("Running Daily ETL")

        ETLService().run()

    elif args.command == "backfill":

        logger.info("Running Historical Backfill")

        BackfillService().run(
            max_pages=args.max_pages,
            reset_checkpoint=args.reset,
        )


if __name__ == "__main__":
    main()
