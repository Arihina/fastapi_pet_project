from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    ADMIN_PASSWORD: str
    STOREKEEPER_PASSWORD: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def admin_password(self):
        return self.ADMIN_PASSWORD

    @property
    def storekeeper_password(self):
        return self.STOREKEEPER_PASSWORD

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
