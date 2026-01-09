import json
import PyPDF2


def read_file(file):
    """
    Reads text from a PDF or TXT file.
    """

    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            return text

        except Exception:
            raise Exception("Error reading the PDF file")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception(
            "Unsupported file format. Only PDF and TXT files are supported."
        )


def get_table_data(quiz_str):
    """
    Converts quiz JSON string into table-friendly data.
    """

    try:
        # Convert quiz string to dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate over quiz dictionary
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option} -> {option_value}"
                    for option, option_value in value["options"].items()
                ]
            )
            correct = value["correct"]

            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

        return quiz_table_data

    except Exception as e:
        raise Exception("Error converting quiz JSON to table data") from e
