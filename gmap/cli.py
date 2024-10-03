import argparse
import logging
from .search import fetch_paper_by_title


def main():
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
        "--quiet",
        action="store_true",
        help="Run in quiet mode (suppress non-error logs)",
    )

    args = parser.parse_args()

    # Setup logging based on --quiet flag
    if args.quiet:
        logging.basicConfig(level=logging.CRITICAL)  # Only show critical errors
    else:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    # Call the main function to fetch and download the paper
    fetch_paper_by_title(
        args.title, args.output_dir, args.name, args.min_similarity, args.delay
    )


if __name__ == "__main__":
    main()
