from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", case_sensitive=True)

    PROJECT_NAME: str
    ENV: str = "dev"

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER_NAME: str
    DB_PASSWORD: str

    def get_database_url(self, is_async: bool = False) -> str:
        if is_async:
            return (f"postgresql+asyncpg://"
                    f"{self.DB_USER_NAME}"
                    f":{self.DB_PASSWORD}"
                    f"@{self.DB_HOST}"
                    f":{self.DB_PORT}"
                    f"/{self.DB_NAME}")

        else:
            return (f"postgresql://"
                    f"{self.DB_USER_NAME}"
                    f":{self.DB_PASSWORD}"
                    f"@{self.DB_HOST}"
                    f":{self.DB_PORT}"
                    f"/{self.DB_NAME}")

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
