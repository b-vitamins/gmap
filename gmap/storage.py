import os


def save_pdf(content, filename, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as file:
        file.write(content)
    return filepath
