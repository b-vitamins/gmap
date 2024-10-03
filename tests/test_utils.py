from gmap.utils import construct_arxiv_pdf_url


def test_construct_arxiv_pdf_url():
    url = "https://arxiv.org/abs/1234.56789"
    expected_pdf_url = "https://arxiv.org/pdf/1234.56789.pdf"
    assert construct_arxiv_pdf_url(url) == expected_pdf_url


def test_construct_arxiv_pdf_url_invalid():
    url = "https://example.com/somepaper"
    assert construct_arxiv_pdf_url(url) is None
