import os

from dotenv import load_dotenv


def str_to_bool(s: str | None, *, default: bool = False, var_name: str = "VERIFY_SSL") -> bool:
    if s is None:
        return default

    value = s.strip().lower()
    if value in {"1", "true", "yes", "y", "on", "oui", "o"}:
        return True
    if value in {"0", "false", "no", "n", "off", "non", ""}:
        return False

    raise ValueError(f"{var_name} invalide: {s!r}")


def load_api_env() -> tuple[bool, str | None, str | None, str | None]:
    load_dotenv()
    verify_ssl = str_to_bool(os.getenv("VERIFY_SSL"), default=True)
    discogs_key = os.getenv("DISCOGS_KEY")
    discogs_secret = os.getenv("DISCOGS_SECRET")
    data_dir = os.getenv("DATA_DIR")
    return verify_ssl, discogs_key, discogs_secret, data_dir