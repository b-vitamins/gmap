import argparse
from unittest.mock import patch
from gmap.cli import main


@patch("gmap.cli.fetch_paper_by_title")
@patch("argparse.ArgumentParser.parse_args")
def test_main(mock_parse_args, mock_fetch_paper):
    # Mocking argparse to simulate command-line inputs
    mock_parse_args.return_value = argparse.Namespace(
        title="A Sample Paper",
        output_dir="/tmp",
        name="",
        min_similarity=80,
        delay=1,
        quiet=False,
        log=False,  # Add this missing argument
        log_file=None,  # Add this missing argument (you can set a default)
    )

    # Run the CLI main function
    main()

    # Ensure fetch_paper_by_title was called with the right arguments
    mock_fetch_paper.assert_called_once_with("A Sample Paper", "/tmp", "", 80, 1)
