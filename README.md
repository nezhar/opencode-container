# OpenCode Container

A Docker container with the OpenCode CLI pre-installed and ready to use.

This project mirrors the approach used in `claude-container` and `devstral-container`: run the CLI in an isolated environment with a persisted config directory and your local workspace mounted in `/workspace`.

## Quick Start

### Using the Helper Script (Recommended)

```bash
# Download and install
curl -o ~/.local/bin/opencode-container https://raw.githubusercontent.com/nezhar/opencode-container/main/bin/opencode-container
chmod +x ~/.local/bin/opencode-container

# Run OpenCode
opencode-container
```

Make sure `~/.local/bin` is in your PATH, or install system-wide with `sudo`:

```bash
sudo curl -o /usr/local/bin/opencode-container https://raw.githubusercontent.com/nezhar/opencode-container/main/bin/opencode-container
sudo chmod +x /usr/local/bin/opencode-container
```

### Using Docker Directly

```bash
docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "$HOME/.config/opencode-container:/config" \
  -v "$HOME/.local/share/opencode:/data" \
  -e "HOME=/config" \
  -e "OPENCODE_CONFIG_DIR=/config" \
  -e "XDG_DATA_HOME=/data" \
  nezhar/opencode-cli:latest
```

## Helper Script Options

```bash
opencode-container --help
opencode-container --pull
opencode-container --shell
opencode-container --auth-forward
opencode-container --auth-port 1455 --auth-forward
opencode-container "analyze the code"
opencode-container --proxy --proxy-provider openai --proxy-target https://api.openai.com
opencode-container --datasette --proxy-provider openai --proxy-target https://api.openai.com
opencode-container --proxy-all
```

## Optional API Logging

Enable API logging through a reverse proxy and store requests/responses in SQLite:

```bash
opencode-container --proxy \
  --proxy-provider openai \
  --proxy-target https://api.openai.com
```

Logs are stored at:

```
~/.config/opencode-container/proxy/logs.db
```

To explore logs in a web UI, start Datasette:

```bash
opencode-container --datasette \
  --proxy-provider openai \
  --proxy-target https://api.openai.com
```

Datasette is available at `http://localhost:8001`.

If your provider uses a different base path, override the base URL injected into OpenCode:

```bash
opencode-container --proxy \
  --proxy-provider openai \
  --proxy-target https://api.openai.com \
  --proxy-base-url http://opencode-proxy:8080/v1
```

### Intercept All Traffic (Forward Proxy)

To capture requests from multiple providers without changing OpenCode config:

```bash
opencode-container --proxy-all
```

This sets `HTTP_PROXY`/`HTTPS_PROXY` for the CLI container and trusts the mitmproxy CA.
If HTTPS requests fail on first run, re-run the command after the proxy generates its
CA files in `~/.config/opencode-container/proxy/certs`.

## Configuration

Configuration is stored on the host in:

```
~/.config/opencode-container
```

Credentials are stored on the host in:

```
~/.local/share/opencode/auth.json
```

These paths are mounted into the container as `/config` and `/data`, with `HOME=/config` and `XDG_DATA_HOME=/data`.

Proxy-related environment variables:

```
OPENCODE_PROXY_PROVIDER
OPENCODE_PROXY_TARGET
OPENCODE_PROXY_BASE_URL
OPENCODE_PROXY_DATA
OPENCODE_PROXY_MODE
OPENCODE_PROXY_PORT
OPENCODE_DATASETTE_PORT
OPENCODE_PROXY_IMAGE
OPENCODE_DATASETTE_IMAGE
```

## Auth Callback Port

If OpenCode starts a local auth server (default `127.0.0.1:1455`), publish it with:

```bash
opencode-container --auth-forward
```

If you need a different port:

```bash
opencode-container --auth-port 1455 --auth-forward
```

## Build Locally

```bash
docker compose build
```

## Related Projects

- `claude-container`
- `devstral-container`
