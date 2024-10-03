import requests
import logging
import time
import os  # Import os to access environment variables


def download_pdf(pdf_url, save_path, delay, retries=3):
    if retries == 0:
        logging.error(f"Failed to download {pdf_url} after multiple retries.")
        return

    try:
        # Fetch email from environment variable directly
        user_agent_email = os.getenv(
            "OPENALEX_EMAIL", ""
        )  # Default to empty if not set
        headers = (
            {"User-Agent": f"gmap ({user_agent_email})"}
            if user_agent_email
            else {"User-Agent": "gmap"}
        )

        response = requests.get(pdf_url, stream=True, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as pdf_file:
                for chunk in response.iter_content(1024):
                    pdf_file.write(chunk)
            logging.info(f"Downloaded PDF to: {save_path}")
        elif response.status_code == 429:
            logging.warning("Rate limited. Retrying after a delay.")
            time.sleep(10)
            return download_pdf(
                pdf_url, save_path, delay, retries - 1
            )  # Decrease retries
        else:
            logging.error(
                f"Failed to download {pdf_url}. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file from {pdf_url}: {e}")
