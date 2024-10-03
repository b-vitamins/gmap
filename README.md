
# GMAP - Get Me A Paper

**GMAP** is a command-line tool designed to fetch academic papers by their titles. It leverages the OpenAlex API to search for scholarly works and download their PDFs directly to your specified directory.

## Features

- **Accurate paper retrieval**: Search and fetch academic papers by title.
- **Download PDFs**: Obtain the PDFs of academic papers, if available.
- **Fuzzy matching**: Ensures accurate results even if the title is not an exact match.
- **Customizable download options**: Specify the output directory, filename, and similarity threshold.
- **Quiet mode**: Suppress non-error logs for a cleaner output.

## Installation

Install **GMAP** using [Poetry](https://python-poetry.org/docs/):

```bash
git clone https://github.com/b-vitamins/gmap.git
cd gmap
poetry install
```

## Usage

To use **GMAP**, simply run the following command:

```bash
gmap "Title of the Paper"
```

### Command-line Options

- `title` (required): The title of the paper you want to fetch.
- `--output-dir`: Specify the directory where the downloaded PDF will be saved (default: current directory).
- `--name`: Optionally specify the name for the saved PDF file.
- `--min-similarity`: Set the minimum title similarity threshold (default: 80).
- `--delay`: Set a delay between API requests to avoid rate limiting (default: 1 second).
- `--log`: Enable logging to track detailed information during execution.
- `--log-file`: Specify the file to write logs to if logging is enabled (default: `~/gmap.log`).
- `--quiet`: Enable quiet mode to suppress non-critical console output.

### Example

```bash
gmap "Simplicial Hopfield networks" --output-dir="/home/b/downloads"
```

Output:

```
Searching for papers with title: Simplicial Hopfield networks
Best match: Simplicial Hopfield networks (Similarity: 100%)
Downloaded PDF to: /home/b/downloads/W4376122733.pdf
```

## Configuration

**GMAP** uses the email address specified in the `OPENALEX_EMAIL` environment variable for API requests. If this variable is not set, no email will be provided in the User-Agent header.

To configure the email address:

```bash
export OPENALEX_EMAIL="your-email@example.com"
```

## Dependencies

**GMAP** depends on the following libraries:

- `requests`: Handles HTTP requests.
- `fuzzywuzzy`: Provides fuzzy string matching functionality.
- `pyalex`: Python client for interacting with the OpenAlex API.

For development:

- `pytest`: Test framework for writing and running tests.
- `pytest-cov`: Measures test coverage.
- `flake8`: Ensures compliance with style guides.
- `black`: Automatic code formatting.

## Testing

Run the test suite using:

```bash
poetry run pytest --cov=gmap
```

This will execute the tests and generate a coverage report.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [OpenAlex](https://openalex.org/): for providing the academic paper data that powers **GMAP**.
- [arXiv](https://arxiv.org/): for offering access to a vast collection of open access papers, enabling direct downloads of research articles in various scientific fields, especially through their long-standing open access initiative.