import pytest
from unittest.mock import patch, MagicMock
from gmap.search import fetch_paper_by_title
from gmap.download import download_pdf
from tests.fixtures import get_mock_openalex_work, get_mock_openalex_no_pdf


@patch("requests.get")
@patch("gmap.search.download_pdf")
@patch("pyalex.Works.search")
@patch("fuzzywuzzy.fuzz.token_sort_ratio")
def test_fetch_paper_with_pdf(mock_fuzz, mock_search, mock_download_pdf, mock_requests):
    # Setup mock responses
    mock_fuzz.return_value = 90  # Fuzzy match similarity
    mock_search.return_value.get.return_value = [get_mock_openalex_work()]

    # Simulate a successful response from requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content = MagicMock(return_value=[b"test data"])
    mock_requests.return_value = mock_response

    # Call the function under test
    fetch_paper_by_title(
        "A Sample Paper on Neural Networks", output_dir="/tmp", min_similarity=80
    )

    # Ensure correct calls
    mock_search.assert_called_once_with("A Sample Paper on Neural Networks")
    mock_fuzz.assert_called_once()
    mock_download_pdf.assert_called_once_with(
        "https://arxiv.org/pdf/1234.56789.pdf", "/tmp/W123456789.pdf", 1
    )


@patch("gmap.download.download_pdf")
@patch("pyalex.Works.search")
@patch("fuzzywuzzy.fuzz.token_sort_ratio")
def test_fetch_paper_no_pdf(mock_fuzz, mock_search, mock_download_pdf):
    # Setup mock responses
    mock_fuzz.return_value = 90  # Fuzzy match similarity
    mock_search.return_value.get.return_value = [get_mock_openalex_no_pdf()]

    # Call the function under test
    fetch_paper_by_title("A Paper Without a PDF", output_dir="/tmp", min_similarity=80)

    # Ensure that download_pdf is not called because there's no PDF
    mock_download_pdf.assert_not_called()
