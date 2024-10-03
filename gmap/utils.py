def construct_arxiv_pdf_url(landing_page_url):
    if "arxiv.org/abs/" in landing_page_url:
        arxiv_id = landing_page_url.split("/abs/")[-1]
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return None
