import logging
from pyalex import Works
from fuzzywuzzy import fuzz
from .download import download_pdf
from .utils import construct_arxiv_pdf_url
import os
import time
import pyalex  # Ensure pyalex is imported to set its configuration


def fetch_paper_by_title(
    title, output_dir=".", pdf_name="", min_similarity=80, delay=1
):
    openalex_email = os.getenv("OPENALEX_EMAIL")

    if openalex_email:
        pyalex.config.email = openalex_email
        pyalex.config.max_retries = 3
        pyalex.config.retry_backoff_factor = 0.1
        pyalex.config.retry_http_codes = [429, 500, 503]

    try:
        logging.info(f"Searching for papers with title: {title}")
        print(f"Searching for papers with title: {title}")
        works = Works().search(title).get()
    except Exception as e:
        logging.error(f"Error during query: {e}")
        print(f"Error during query: {e}")
        return

    if not works:
        logging.info("No papers found with the given title.")
        print("No papers found with the given title.")
        return

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
            print("Skipping entry with missing title")

    if best_match and highest_similarity >= min_similarity:
        logging.info(
            f"Best match: {best_match['display_name']} (Similarity: {highest_similarity}%)"
        )
        print(
            f"Best match: {best_match['display_name']} (Similarity: {highest_similarity}%)"
        )

        oa_location = best_match.get("best_oa_location")
        if oa_location and oa_location.get("is_oa"):
            pdf_url = oa_location.get("pdf_url")
            landing_page_url = oa_location.get("landing_page_url")

            if "arxiv.org" in landing_page_url and not pdf_url:
                logging.info(
                    f"ArXiv paper detected, constructing PDF URL from landing page: "
                    f"{landing_page_url}"
                )
                pdf_url = construct_arxiv_pdf_url(landing_page_url)

            if pdf_url:
                # Use pdf_name if provided, otherwise fallback to work_id
                work_id = best_match["id"].split("/")[-1]
                final_pdf_name = f"{pdf_name}.pdf" if pdf_name else f"{work_id}.pdf"
                save_path = os.path.join(output_dir, final_pdf_name)

                time.sleep(delay)
                download_pdf(pdf_url, save_path, delay)
            else:
                logging.info(
                    "No direct PDF link available, but open access at "
                    f"{landing_page_url}"
                )
                print(
                    "No direct PDF link available, but open access at "
                    f"{landing_page_url}"
                )
        else:
            logging.info("No open access PDF available for the best match.")
            print("No open access PDF available for the best match.")
    else:
        logging.info(
            f"No close matches found for the title '{title}' (Best match similarity: {highest_similarity}%)"
        )
        print(
            f"No close matches found for the title '{title}' (Best match similarity: {highest_similarity}%)"
        )
