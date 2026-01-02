# Dev Container Configuration

This directory contains the development container configuration.

## Usage

### VS Code

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open the project in VS Code
3. Press `F1` and select "Dev Containers: Reopen in Container"
4. Wait for the container to build and dependencies to install (takes some minutes)

To use `podman` instead of `docker`,
search the VSCode settings for `docker` and adapt the path(s) to `podman`.

### PyCharm

PyCharm Professional supports dev containers natively:

1. Open the project in PyCharm
2. PyCharm will detect the `.devcontainer/devcontainer.json` file
3. Click "Create Dev Container and Mount Sources" when prompted
4. PyCharm will build the container and configure the Python interpreter automatically

Alternatively, you can manually set it up:

1. Go to **Settings** → **Build, Execution, Deployment** → **Docker**
2. Add a Docker server connection if not already configured
3. Go to **Settings** → **Project** → **Python Interpreter**
4. Click the gear icon → **Add Interpreter** → **On Docker**
5. Select the dev container image or build from the Dockerfile
6. PyCharm will configure the interpreter and sync dependencies

## Customization

Edit `devcontainer.json` to:
- Add more VS Code extensions in `customizations.vscode.extensions`
- Change Python version by modifying the image tag (e.g., `python3.13-trixie`)
- Forward ports for web services in `forwardPorts`
- Add environment variables in `containerEnv`
- Install additional system packages in `postCreateCommand`

## Container Resources

Dev container performance depends on available CPU, memory, and disk resources.

- macOS/Windows (Podman Machine): Increase VM limits when builds/tests feel slow.
  - Check current settings:
    - `podman machine inspect`
  - Raise limits (example: 4 CPUs, 4GB RAM, 60GB disk):
    - `podman machine set --cpus 4 --memory 4096 --disk-size 60`
    - `podman machine stop && podman machine start`
- Linux (native Podman): Containers use host resources by default.

## References

- [containers.dev](https://containers.dev/)
- [VSCode - DevContainers](https://code.visualstudio.com/docs/devcontainers/containers)
- [PyCharm - DevContainer](https://www.jetbrains.com/help/pycharm/connect-to-devcontainer.html)
