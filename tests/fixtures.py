def get_mock_openalex_work():
    return {
        "id": "https://openalex.org/W123456789",
        "display_name": "A Sample Paper on Neural Networks",
        "best_oa_location": {
            "is_oa": True,
            "pdf_url": "https://arxiv.org/pdf/1234.56789.pdf",
            "landing_page_url": "https://arxiv.org/abs/1234.56789",
        },
    }


def get_mock_openalex_no_pdf():
    return {
        "id": "https://openalex.org/W987654321",
        "display_name": "A Paper Without a PDF",
        "best_oa_location": {
            "is_oa": True,
            "pdf_url": None,
            "landing_page_url": "https://arxiv.org/abs/1234.56789",
        },
    }
