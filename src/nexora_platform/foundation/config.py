"""Application settings shared by Nexora platform modules."""

from functools import lru_cache

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url


class Settings(BaseSettings):
    """Environment-backed application configuration."""

    app_name: str = "Nexora Team 5 Platform"
    app_env: str = "development"
    debug: bool = False
    database_url: str | None = Field(default=None, repr=False)
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: SecretStr | None = Field(default=None, repr=False)
    postgres_host: str | None = None
    postgres_port: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """Ignore malformed ambient DEBUG values so dotenv settings can apply."""

        def valid_environment_settings() -> dict[str, object]:
            values = env_settings()
            debug_value = values.get("debug")
            accepted = {"1", "0", "true", "false", "yes", "no", "on", "off"}
            if isinstance(debug_value, str) and debug_value.strip().lower() not in accepted:
                values.pop("debug", None)
            return values

        return (
            init_settings,
            valid_environment_settings,
            dotenv_settings,
            file_secret_settings,
        )

    @model_validator(mode="after")
    def resolve_database_url(self) -> "Settings":
        """Resolve DATABASE_URL or validate it against complete PG_* values."""
        component_values = (
            self.postgres_db,
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
        )
        has_components = any(value is not None for value in component_values)
        complete_components = all(value is not None for value in component_values)

        component_url = None
        if complete_components:
            component_url = URL.create(
                "postgresql+psycopg",
                username=self.postgres_user,
                password=self.postgres_password.get_secret_value(),
                host=self.postgres_host,
                port=self.postgres_port,
                database=self.postgres_db,
            )

        if self.database_url:
            if has_components and not complete_components:
                raise ValueError("Provide all POSTGRES_* values when using them with DATABASE_URL")
            if component_url is not None:
                configured_url = make_url(self.database_url)
                if configured_url.drivername == "postgresql":
                    configured_url = configured_url.set(drivername="postgresql+psycopg")
                if configured_url != component_url:
                    raise ValueError("DATABASE_URL conflicts with POSTGRES_* settings")
            return self

        if component_url is None:
            if has_components:
                raise ValueError("Provide all POSTGRES_* values to construct DATABASE_URL")
            return self

        self.database_url = component_url.render_as_string(hide_password=False)
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached settings instance for this process."""
    return Settings()
