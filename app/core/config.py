from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Clothing Category Identifier"
    API_V1_STR: str = "/api/v1"
    
    # 환경 변수로 모델 경로 등 관리 가능
    MODEL_NAME: str = "mobilenet_v2"

    class Config:
        case_sensitive = True

settings = Settings()
