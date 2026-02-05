# Plugin CLI (Third-party plugins)

## Overview

This document describes the `inkypi` command-line interface (CLI) subcommands used to install, uninstall, and list plugins.

The CLI is installed by the InkyPi installer as `/usr/local/bin/inkypi` and routes plugin operations to `/usr/local/inkypi/cli/inkypi-plugin`.

## Prerequisites

- InkyPi installed via `install/install.sh` (the installer places the `inkypi` executable into `/usr/local/bin`).
- `git` available on the system (required to clone plugin repositories).

## Command reference

### `inkypi plugin install`

Install a plugin from a Git repository:

```bash
inkypi plugin install <plugin_id> <git_repository_url>
```

Operational details:

- Plugin files are installed into `/usr/local/inkypi/src/plugins/<plugin_id>`.
- The repository must contain a top-level directory named `<plugin_id>`.
- A sparse checkout is used to copy only the `<plugin_id>` directory into the destination.
- If `/usr/local/inkypi/src/plugins/<plugin_id>/requirements.txt` exists, dependencies are installed into the InkyPi virtual environment located at `/usr/local/inkypi/venv_inkypi`.
- The `inkypi.service` systemd unit is restarted at the end of the install.

### `inkypi plugin uninstall`

Uninstall a plugin:

```bash
inkypi plugin uninstall <plugin_id>
```

Operational details:

- The plugin directory `/usr/local/inkypi/src/plugins/<plugin_id>` is removed.
- The `inkypi.service` systemd unit is restarted at the end of the uninstall.

### `inkypi plugin list`

List installed plugins:

```bash
inkypi plugin list
```

Output columns:

- `PLUGIN`
- `NAME`
- `TYPE` (`builtin` or `third_party`)
- `REPOSITORY`

Listing behavior:

- Plugins are discovered by scanning `/usr/local/inkypi/src/plugins/*`.
- The `base_plugin` directory is skipped.
- Entries without `plugin-info.json` are skipped.
- Plugin metadata is read from `plugin-info.json` fields `display_name` and `repository`.
- `jq` is used to parse `plugin-info.json`.

## Troubleshooting

# Plugin CLI (Third-party plugins)

## Overview

This document describes the `inkypi` command-line interface (CLI) subcommands used to install, uninstall, and list plugins.

The CLI is installed by the InkyPi installer as `/usr/local/bin/inkypi` and routes plugin operations to `/usr/local/inkypi/cli/inkypi-plugin`.

## Prerequisites

- InkyPi installed via `install/install.sh` (the installer places the `inkypi` executable into `/usr/local/bin`).
- `git` available on the system (required to clone plugin repositories).

## Command reference

### `inkypi plugin install`

Install a plugin from a Git repository:

```bash
inkypi plugin install <plugin_id> <git_repository_url>
```

Operational details:

- Plugin files are installed into `/usr/local/inkypi/src/plugins/<plugin_id>`.
- The repository must contain a top-level directory named `<plugin_id>`.
- A sparse checkout is used to copy only the `<plugin_id>` directory into the destination.
- If `/usr/local/inkypi/src/plugins/<plugin_id>/requirements.txt` exists, dependencies are installed into the InkyPi virtual environment located at `/usr/local/inkypi/venv_inkypi`.
- The `inkypi.service` systemd unit is restarted at the end of the install.

### `inkypi plugin uninstall`

Uninstall a plugin:

```bash
inkypi plugin uninstall <plugin_id>
```

Operational details:

- The plugin directory `/usr/local/inkypi/src/plugins/<plugin_id>` is removed.
- The `inkypi.service` systemd unit is restarted at the end of the uninstall.

### `inkypi plugin list`

List installed plugins:

```bash
inkypi plugin list
```

Output columns:

- `PLUGIN`
- `NAME`
- `TYPE` (`builtin` or `third_party`)
- `REPOSITORY`

Listing behavior:

- Plugins are discovered by scanning `/usr/local/inkypi/src/plugins/*`.
- The `base_plugin` directory is skipped.
- Entries without `plugin-info.json` are skipped.
- Plugin metadata is read from `plugin-info.json` fields `display_name` and `repository`.
- `jq` is used to parse `plugin-info.json`.

## Troubleshooting

### "Plugins directory does not exist"

Verify that `/usr/local/inkypi/src/plugins` exists.

This directory is created by the installation process by linking `src/` into `/usr/local/inkypi/src`.

### "Virtual environment not found"

The install command installs Python dependencies from a plugin-local `requirements.txt` into `/usr/local/inkypi/venv_inkypi`.

If the virtual environment is missing, run the installer:

```bash
sudo bash install/install.sh
```

### "Plugin '<plugin_id>' does not exist in the repo"

The plugin repository must contain a directory that exactly matches `<plugin_id>` at the repository root.

## Reference

- Plugin build guide: [Building InkyPi Plugins](./building_plugins.md)
