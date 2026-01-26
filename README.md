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
opencode-container "analyze the code"
```

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

## Build Locally

```bash
docker compose build
```

## Related Projects

- `claude-container`
- `devstral-container`
