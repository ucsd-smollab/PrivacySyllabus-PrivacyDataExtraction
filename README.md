# PDF Privacy Keyword Extractor
This Python script extracts paragraphs containing specific privacy-related keywords from a PDF document. It categorizes the extracted paragraphs based on whether they relate to privacy protections or privacy threats. The results are saved into CSV files.

## Repquirements
- Python 3.x
- pandas library
- PyMuPDF library (also known as fitz)

## Usage
- Place your PDF file in the same directory as the script.
- Modify the pdf_path variable in the script to point to your PDF file.
- Run the script.


## Notes
- Ensure the PDF file is not encrypted or password-protected, as this script does not handle such files.
- Adjust the keyword lists (protections_keywords and threats_keywords) as needed to fit your specific requirements.