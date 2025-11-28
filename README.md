# python-template

Template/boilerplate/reference project for a Python application (branches for different add-ons, e.g. like FastAPI)

1. Clone & copy
   ([cookiecutter](https://cookiecutter.readthedocs.io/en/stable/),
   [copier](https://copier.readthedocs.io/en/stable/))
   or use this repo via GitHub directly, see
   [create a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
2. Run `uv run pre-commit install`.
3. Delete `CHANGELOG.md` and reset version in `pyproject.toml` for your app.

## Branches

The base branch `main` includes only the most necessary parts of a python project:
* `git` config (gitignore for Python, gitattributes to ensure proper line endings in the repo)
* [uv](https://docs.astral.sh/uv/) setup (currently the fastest Python package manager (?))
* [ruff](https://docs.astral.sh/ruff/configuration/) for code formatting and linting
* [mypy](https://mypy.readthedocs.io/en/stable/) for static type checking
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
* `fastapi` - Webservice with [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)

## Local Development

### Run

```bash
LOG_LEVEL=TRACE LOG_JSON=True uv run python python_template/main.py
```

You can have the env variables in `.env.shared` or customize it on the command line.

Start FastAPI dev mode with auto-reload on changes:
```bash
uv run fastapi dev python_template/main.py
```

Interface:
- [/docs](http://localhost:8000/docs) (probes and metrics are excluded)
- [/live](http://localhost:8000/live)
- [/ready](http://localhost:8000/ready)
- [/metrics](http://localhost:8000/metrics)

## References

- [Ruff - Configuration](https://docs.astral.sh/ruff/configuration/)
- [Conventional Commits - Quickstart](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Angular - Commit Message Guidelines](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
- [commitizen - GitHub Actions](https://commitizen-tools.github.io/commitizen/tutorials/github_actions/)
- [mypy - cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [loguru - Switching from Standard Logging to Loguru](https://loguru.readthedocs.io/en/stable/resources/migration.html)

Other Templates:
- [FastAPI - Template](https://github.com/fastapi/full-stack-fastapi-template)
