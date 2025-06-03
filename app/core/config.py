from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # Название модели GigaAM
    # Можно изменить на другие варианты: "v2_ctc", "ctc", "v2_rnnt", "v1_ctc", "v1_rnnt"
    MODEL_NAME: str = "v2_rnnt"

    # Путь для кэширования модели
    MODEL_DOWNLOAD_ROOT: str = "../model_cache"

    # Настройки сервера
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8081

settings = Settings()