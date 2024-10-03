import argparse
import logging
import os
from .search import fetch_paper_by_title


def main():
    # Argument parser for the command-line interface
    parser = argparse.ArgumentParser(
        description=(
            "Get Me A Paper (gmap): Fetch scholarly papers by title using OpenAlex"
        )
    )
    parser.add_argument("title", type=str, help="The title of the paper to fetch")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save the downloaded PDF",
    )
    parser.add_argument(
        "--name", type=str, default="", help="Optional name for the saved PDF file"
    )
    parser.add_argument(
        "--min-similarity",
        type=int,
        default=80,
        help="Minimum title similarity to consider (default: 80)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1,
        help="Delay between API requests (default: 1 second)",
    )
    parser.add_argument(
        "--log", action="store_true", help="Enable logging (to file or console)"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=os.path.expanduser("~/gmap.log"),
        help="File to write logs to if --log is specified. Defaults to '~/gmap.log'",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Run in quiet mode (suppress non-critical console output)",
    )

    args = parser.parse_args()

    # Logging setup based on --log and --log-file
    if args.log:
        logging.basicConfig(
            filename=args.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info(f"Logging initiated, writing logs to {args.log_file}")
    else:
        # No logging unless --log is specified
        logging.basicConfig(
            level=logging.CRITICAL
        )  # Suppresses everything except critical logs

    # Call the main function to fetch and download the paper
    fetch_paper_by_title(
        args.title, args.output_dir, args.name, args.min_similarity, args.delay
    )


if __name__ == "__main__":
    main()
