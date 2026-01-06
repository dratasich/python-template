# python-template

[![test](https://github.com/dratasich/python-template/actions/workflows/test.yml/badge.svg)](https://github.com/dratasich/python-template/actions/workflows/test.yml)
[![license](https://img.shields.io/github/license/dratasich/python-template)](LICENSE)

Template/boilerplate/reference project for a Python application (branches for different add-ons, e.g. FastAPI)

1. Create a repository from this template in [GitHub directly](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
   or copy
   (e.g. with [copier](https://copier.readthedocs.io/en/stable/))
3. Run `uv run pre-commit install`.
4. Delete `CHANGELOG.md` and reset version in `pyproject.toml` for your app.

## Branches

The base branch `main` includes only the most necessary parts of a python project:
* `git` config (gitignore for Python, gitattributes to ensure proper line endings in the repo)
* [uv](https://docs.astral.sh/uv/) setup (currently the fastest Python package manager (?))
* [ruff](https://docs.astral.sh/ruff/configuration/) for code formatting and linting
* [ty](https://docs.astral.sh/ty/) for static type checking
* [commitizen](https://commitizen-tools.github.io/commitizen/) for structured commits (= [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)) enabling automatic versioning and changelog update
  ```bash
  # bump version (in `pyproject.toml` and update `CHANGELOG.md`)
  # ideally this is performed by your pipeline (e.g., on PR merge)
  cz bump  --yes --annotated-tag --check-consistency
  ```
* [pytest](https://docs.pytest.org/en/stable/) - yes, even for python notebooks ;)
* simple and optional json logging with [loguru](https://github.com/Delgan/loguru)
* [pre-commit](https://pre-commit.com/) config (enforcing all of the above)

You can include branches depending on your needs:
* `devcontainers` - Develop within a [devcontainer](https://containers.dev/)
   (nice to have when you use AI agents or don't have admin rights
   to install all the stuff you need - `docker` or `podman` required though)
* `docker` - Dockerfile and a GitHub action / workflow to build the image
* `fastapi` - Webservice with [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)

## Local Development

### Run

```bash
LOG_LEVEL=TRACE uv run python python_template/main.py
```

You can have the env variables in `.env.shared` or customize it on the command line.

## References

- [Ruff - Configuration](https://docs.astral.sh/ruff/configuration/)
- [Conventional Commits - Quickstart](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Angular - Commit Message Guidelines](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
- [commitizen - GitHub Actions](https://commitizen-tools.github.io/commitizen/tutorials/github_actions/)
- [loguru - Switching from Standard Logging to Loguru](https://loguru.readthedocs.io/en/stable/resources/migration.html)
- [Using uv in docker](https://docs.astral.sh/uv/guides/integration/docker/#getting-started)

Other Templates:
- [FastAPI - Template](https://github.com/fastapi/full-stack-fastapi-template)
- [Python uv](https://github.com/a5chin/python-uv)
- [substrate](https://github.com/superlinear-ai/substrate) - awesome copier template with very similar tools
- [copier-uv](https://github.com/pawamoy/copier-uv)
