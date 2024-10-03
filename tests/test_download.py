import pytest
from unittest.mock import patch, MagicMock
from gmap.download import download_pdf


@patch("requests.get")
def test_download_pdf_success(mock_get):
    # Mocking a successful response from requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_content = MagicMock(return_value=[b"test data"])
    mock_get.return_value = mock_response

    # Call the function under test with mocked environment variable
    with patch.dict("os.environ", {"OPENALEX_EMAIL": "test@example.com"}):
        download_pdf("http://example.com/test.pdf", "/tmp/test.pdf", delay=1)

    # Ensure requests.get was called correctly
    mock_get.assert_called_once_with(
        "http://example.com/test.pdf",
        stream=True,
        headers={"User-Agent": "gmap (test@example.com)"},
        timeout=10,
    )


@patch("requests.get")
def test_download_pdf_rate_limited(mock_get):
    # Mock a rate-limited response (429)
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_get.return_value = mock_response

    # Call the function under test with mocked environment variable
    with patch.dict("os.environ", {"OPENALEX_EMAIL": "test@example.com"}):
        with patch("time.sleep") as mock_sleep:
            download_pdf("http://example.com/test.pdf", "/tmp/test.pdf", delay=1)

    # Ensure sleep was called 3 times (for 3 retries)
    assert mock_sleep.call_count == 3  # Update to expect 3 calls
    mock_sleep.assert_called_with(10)  # Ensure the delay between retries is correct
