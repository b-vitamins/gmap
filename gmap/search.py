import logging
from pyalex import Works
from fuzzywuzzy import fuzz
from .download import download_pdf
from .utils import construct_arxiv_pdf_url
import os
import time
import pyalex  # Ensure pyalex is imported to set its configuration


# Function to fetch a paper by title from OpenAlex and download the PDF if available
def fetch_paper_by_title(
    title, output_dir=".", pdf_name="", min_similarity=80, delay=1
):
    # Fetch email from environment variable
    openalex_email = os.getenv("OPENALEX_EMAIL")

    # Set up PyAlex configuration if email is provided
    if openalex_email:
        pyalex.config.email = openalex_email
        pyalex.config.max_retries = 3  # Set the number of retries
        pyalex.config.retry_backoff_factor = 0.1  # Delay between retries
        pyalex.config.retry_http_codes = [429, 500, 503]  # Retry on these HTTP codes

    try:
        logging.info(f"Searching for papers with title: {title}")
        works = Works().search(title).get()
    except Exception as e:
        logging.error(f"Error during query: {e}")
        return

    if not works:
        logging.info("No papers found with the given title.")
        return

    # Perform fuzzy matching on the titles to find the closest match
    best_match = None
    highest_similarity = 0
    for work in works:
        work_title = work.get("display_name")
        if work_title:
            similarity = fuzz.token_sort_ratio(work_title.lower(), title.lower())
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = work
        else:
            logging.warning("Skipping entry with missing title")

    # Check if the match is good enough
    if best_match and highest_similarity >= min_similarity:
        logging.info(
            f"Best match: {best_match['display_name']} "
            f"(Similarity: {highest_similarity}%)"
        )

        # Check for open access PDF
        oa_location = best_match.get("best_oa_location")
        if oa_location and oa_location.get("is_oa"):
            pdf_url = oa_location.get("pdf_url")
            landing_page_url = oa_location.get("landing_page_url")

            # Handle ArXiv-specific logic
            if "arxiv.org" in landing_page_url and not pdf_url:
                logging.info(
                    f"ArXiv paper detected, constructing PDF URL from landing page: "
                    f"{landing_page_url}"
                )
                pdf_url = construct_arxiv_pdf_url(landing_page_url)

            if pdf_url:
                # Save using OpenAlex Work ID
                work_id = best_match["id"].split("/")[
                    -1
                ]  # Extract the Work ID from the OpenAlex URI
                save_path = os.path.join(output_dir, f"{work_id}.pdf")

                # Download with a delay to avoid rate limiting
                time.sleep(delay)
                download_pdf(pdf_url, save_path, delay)
            else:
                logging.info(
                    "No direct PDF link available, but open access at "
                    f"{landing_page_url}"
                )

        else:
            logging.info("No open access PDF available for the best match.")
    else:
        logging.info(
            f"No close matches found for the title '{title}' "
            f"(Best match similarity: {highest_similarity}%)"
        )
