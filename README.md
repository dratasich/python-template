# python-template

Template/boilerplate/reference project for a Python application (branches for different add-ons, e.g. like FastAPI)

1. Clone&copy or use this via GitHub directly, see [create a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
2. Run `uv run pre-commit install`.

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
* [pre-commit](https://pre-commit.com/) config (enforcing all of the above)

You can include branches depending on your needs:
* TODO


## References

- [Ruff - Configuration](https://docs.astral.sh/ruff/configuration/)
- [Conventional Commits - Quickstart](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Angular - Commit Message Guidelines](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
- [commitizen - GitHub Actions](https://commitizen-tools.github.io/commitizen/tutorials/github_actions/)
- [mypy - cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

Other Templates:
- [FastAPI - Template](https://github.com/fastapi/full-stack-fastapi-template)
