import shutil
import tempfile
import os
from fastapi import UploadFile
from GigaAmService.app.models.giga_model import giga_model_instance

class TranscriptionError(Exception):
    """Кастомное исключение для ошибок транскрипции."""
    pass

def process_audio_for_transcription(file: UploadFile) -> str:
    """
    Основная бизнес-логика: сохраняет аудио во временный файл,
    транскрибирует его и удаляет временный файл.

    :param file: Загруженный файл из FastAPI.
    :return: Строка с транскрипцией.
    :raises TranscriptionError: В случае ошибки в процессе.
    """
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        transcription_text = giga_model_instance.transcribe(temp_file_path)
        if transcription_text is None or transcription_text.strip() == "":
            raise TranscriptionError("Не удалось распознать текст из аудио.")
        return transcription_text

    except Exception as e:
        raise TranscriptionError(f"Ошибка во время обработки аудио: {str(e)}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)