from fastapi import FastAPI, UploadFile, File, HTTPException
import gigaam
import shutil
import os
import tempfile

# Создаем приложение FastAPI
app = FastAPI()

# Загружаем модель один раз при запуске приложения
model_name = "v2_rnnt"  # Можно изменить на другие варианты: "v2_ctc", "ctc", "v2_rnnt", "v1_ctc", "v1_rnnt"
model = gigaam.load_model(model_name, download_root='model_cache')


# Определяем endpoint для транскрипции аудио
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    git clone https://github.com/salute-developers/GigaAM.git
    Принимает аудиофайл через POST запрос и возвращает его транскрипцию.

    Args:
        file (UploadFile): Загружаемый аудиофайл.

    Returns:
        dict: Словарь с ключом "transcription" и текстом транскрипции.

    Raises:
        HTTPException: Если транскрипция не удалась.
    """
    temp_file_path = None
    try:
        # Создаем временный файл для сохранения загруженного аудио
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        # Выполняем транскрипцию
        transcription = model.transcribe(temp_file_path)

        # Возвращаем результат
        return {"transcription": transcription}

    except Exception as e:
        # В случае ошибки возвращаем HTTP 500 с описанием
        raise HTTPException(status_code=500, detail=f"Транскрипция не удалась: {str(e)}")

    finally:
        # Удаляем временный файл после обработки
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)