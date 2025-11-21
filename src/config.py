from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    # Discord
    DISCORD_TOKEN: str
    BOT_PREFIX: str = ""

    # Sentry
    DSN: str

    # Enviroment
    PRODUCTION: bool = False


Settings = _Settings(__env_file=".env")  # type: ignore
