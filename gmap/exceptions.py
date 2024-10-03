class PaperNotFoundError(Exception):
    """Custom exception when a paper is not found by OpenAlex or other services."""

    pass


class DownloadError(Exception):
    """Custom exception for download failures."""

    pass
