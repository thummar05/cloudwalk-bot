import re
from app.utils.file_io import save_text


def clean_text(text: str) -> str:
    """Removes extra whitespace, scripts, special characters."""

    text = re.sub(r"\s+", " ", text)

    text = text.encode("ascii", "ignore").decode()

    return text.strip()


def clean_and_save(text, filename):
    cleaned = clean_text(text)
    save_text(f"data/cleaned/{filename}", cleaned)
    return cleaned



if __name__ == "__main__":
    clean_and_save()