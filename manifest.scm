;; manifest.scm - Guix manifest to provide a development environment for gmap

(specifications->manifest
  '("python"
    "poetry"
    "python-pytest"
    "python-pytest-cov"
    "python-pyalex"
    "python-fuzzywuzzy"
    "python-requests"
    "python-black"
    "python-flake8"))
