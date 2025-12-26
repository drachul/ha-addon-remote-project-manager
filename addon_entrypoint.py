#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


def _load_options(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        print(f"Failed to parse options JSON: {exc}", file=sys.stderr)
        return {}
    except OSError as exc:
        print(f"Failed to read options JSON: {exc}", file=sys.stderr)
        return {}


def _set_env_from_options(options: dict, option_key: str, env_key: str) -> None:
    if option_key not in options:
        return
    value = options.get(option_key)
    if value is None:
        return
    if isinstance(value, str) and value == "":
        return
    os.environ[env_key] = str(value)


def main() -> None:
    options = _load_options("/data/options.json")

    db_path = options.get("db_path") or "/data/state.db"
    os.environ["DB_PATH"] = str(db_path)
    try:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"Failed to create DB directory: {exc}", file=sys.stderr)
        sys.exit(1)
    os.environ.setdefault("APP_HOST", "0.0.0.0")
    os.environ.setdefault("APP_PORT", "8000")

    _set_env_from_options(options, "log_level", "APP_LOG_LEVEL")
    _set_env_from_options(options, "app_port", "APP_PORT")
    _set_env_from_options(options, "secret_seed", "SECRET_SEED")
    _set_env_from_options(options, "state_refresh_seconds", "STATE_REFRESH_SECONDS")
    _set_env_from_options(options, "update_refresh_seconds", "UPDATE_REFRESH_SECONDS")
    _set_env_from_options(options, "ssl_certfile", "SSL_CERTFILE")
    _set_env_from_options(options, "ssl_keyfile", "SSL_KEYFILE")
    _set_env_from_options(options, "ssl_ca_certs", "SSL_CA_CERTS")

    if not os.environ.get("SECRET_SEED"):
        print(
            "ERROR: secret_seed is required. Set it in the add-on configuration.",
            file=sys.stderr,
        )
        sys.exit(1)

    import uvicorn

    ssl_kwargs = {}
    ssl_certfile = os.environ.get("SSL_CERTFILE")
    ssl_keyfile = os.environ.get("SSL_KEYFILE")
    ssl_ca_certs = os.environ.get("SSL_CA_CERTS")
    if ssl_certfile and ssl_keyfile:
        ssl_kwargs["ssl_certfile"] = ssl_certfile
        ssl_kwargs["ssl_keyfile"] = ssl_keyfile
        if ssl_ca_certs:
            ssl_kwargs["ssl_ca_certs"] = ssl_ca_certs

    uvicorn.run(
        "app.main:app",
        host=os.environ.get("APP_HOST", "0.0.0.0"),
        port=int(os.environ.get("APP_PORT", "8000")),
        **ssl_kwargs,
    )


if __name__ == "__main__":
    main()
