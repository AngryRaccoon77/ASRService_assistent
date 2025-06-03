
from fastapi import APIRouter, UploadFile, File, HTTPException
from GigaAmService.app.services.transcription import process_audio_for_transcription, TranscriptionError

router = APIRouter()

@router.post("/transcribe", summary="Транскрибировать аудиофайл")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """
    Принимает аудиофайл (.wav) и возвращает его текстовую транскрипцию.
    """
    if not file.filename.endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Неверный формат файла. Пожалуйста, загрузите .wav файл."
        )

    try:
        # Делегируем всю работу сервисному слою
        transcription = process_audio_for_transcription(file)
        return {"transcription": transcription}

    except TranscriptionError as e:
        # Обрабатываем ошибку из сервисного слоя и возвращаем клиенту
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Обработка других непредвиденных ошибок
        raise HTTPException(status_code=500, detail=f"Произошла внутренняя ошибка: {str(e)}")