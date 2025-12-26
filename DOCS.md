# Remote Project Manager

Manage remote Docker Compose projects over SSH using the bundled web UI/API.

## Configuration

Add-on options (in the UI):

- `app_port`: Port the service listens on inside the container (default: 8000).
- `db_path`: Path to the SQLite DB (default: `/data/state.db`). Use `/share/...` to store it in the shared HA folder.
- `log_level`: App logging verbosity (`info` default).
- `secret_seed`: Required. Used to hash passwords and sign tokens. Use 32+ random characters.
- `state_refresh_seconds`: Interval to refresh project status (default: 300).
- `update_refresh_seconds`: Interval to refresh update checks (default: 720).
- `ssl_certfile`: Optional path to TLS certificate (e.g. `/ssl/fullchain.pem`).
- `ssl_keyfile`: Optional path to TLS key (e.g. `/ssl/privkey.pem`).
- `ssl_ca_certs`: Optional CA bundle path.

Notes:
- The database path defaults to `/data/state.db`, which persists across add-on restarts/upgrades.
- If you change `app_port`, update `ingress_port` and `ports` in `config.yaml` before building the add-on so ingress/port mapping match.
- TLS is enabled only when both `ssl_certfile` and `ssl_keyfile` are provided.
- `state_refresh_seconds` and `update_refresh_seconds` can be set to `0` to disable periodic refresh.

## Access

- Ingress: Open the add-on from Home Assistant to use ingress.
- Direct access: `http://<home_assistant_host>:8000/`.

## Authentication

Default credentials are created on first startup:

- Username: `admin`
- Password: `changemenow`

Update or create users from the Configuration section in the UI. Keep `secret_seed` private and change it only if you are prepared to reset credentials.

## Backups

Backups run on the managed hosts. Ensure those hosts have the required tools installed:

- For `protocol=ssh`: `sshpass` and `rsync` on the managed host.
- For `protocol=rsync`: `rsync` on the managed host and an rsync daemon on the backup server.

## Ports

- `8000/tcp` exposes the web UI and API.

## Support

Upstream project: https://github.com/drachul/remote-project-manager
