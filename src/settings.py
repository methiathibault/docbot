from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	meilisearch_url: str = "http://0.0.0.0:7700"
	
settings=Settings()