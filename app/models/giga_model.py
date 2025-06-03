# app/models/giga_model.py

import gigaam
from GigaAmService.app.core.config import settings


class GigaModel:
    """
    Класс-обертка для модели транскрипции GigaAM.
    Гарантирует, что модель загружается только один раз.
    """
    _model = None

    def __init__(self):
        if GigaModel._model is None:
            print(f"Загрузка модели '{settings.MODEL_NAME}'...")
            GigaModel._model = gigaam.load_model(
                model_name=settings.MODEL_NAME,
                download_root=settings.MODEL_DOWNLOAD_ROOT
            )
            print("Модель успешно загружена.")

    def transcribe(self, file_path: str) -> str:
        """
        Выполняет транскрипцию аудиофайла.

        :param file_path: Путь к аудиофайлу.
        :return: Распознанный текст.
        """
        if GigaModel._model is None:
            raise RuntimeError("Модель не была загружена. Проверьте инициализацию.")


        result = GigaModel._model.transcribe(file_path)
        return result


giga_model_instance = GigaModel()