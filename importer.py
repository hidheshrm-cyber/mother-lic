import zipfile
import os

def extract_zip(zip_path):

    extract_folder = "extracted"

    os.makedirs(
        extract_folder,
        exist_ok=True
    )

    with zipfile.ZipFile(
        zip_path,
        'r'
    ) as zip_ref:

        zip_ref.extractall(
            extract_folder
        )

    return extract_folder
