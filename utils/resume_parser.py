import pdfplumber

def extract_text_from_pdf(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        return text

    except Exception as e:
        print("Error reading PDF:", e)
        return ""
