import pathlib
import tomllib
from typing import Final

from pydantic import BaseModel

from setup.config.api import ApiSettings
from setup.config.telegram_bot import TelegramBotSettings


class AppSettings(BaseModel):
    telegram_bot: TelegramBotSettings
    api: ApiSettings


SETTINGS_FILE_PATH: Final[pathlib.Path] = (
    pathlib.Path(__file__).parents[3] / "settings.toml"
)


def load_settings_from_toml_file(
    file_path: pathlib.Path = SETTINGS_FILE_PATH,
) -> AppSettings:
    config_toml = file_path.read_text(encoding="utf-8")
    config = tomllib.loads(config_toml)
    return AppSettings.model_validate(config)
