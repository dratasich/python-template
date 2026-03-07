# Contributing

Yeah! Please go for it :)

## Environment Setup

```bash
uv run pre-commit install  # install git hooks (commit-msg, pre-commit, pre-push)
# this implicitly also runs a `uv sync` installing the dependencies
```

The virtual environment is managed by `uv` and lives in `.venv/`.

## Common Commands

| Task         | Command                                                 |
| ------------ | ------------------------------------------------------- |
| Run app      | `LOG_LEVEL=TRACE uv run python python_template/main.py` |
| Run tests    | `uv run pytest tests/unit`                              |
| Lint (check) | `uv run ruff check .`                                   |
| Lint (fix)   | `uv run ruff check --fix .`                             |
| Format       | `uv run ruff format .`                                  |
| Type check   | `uv run ty check .`                                     |

Instead of running the steps separately, you can
`uv run pre-commit run --all-files`.

## Code Style

- **Formatter:** `ruff format` (Black-compatible, 88-char line length, double quotes)
- **Linter:** `ruff` with rules `E`, `F`, `UP`, `B`, `SIM`, `I` (isort included)
- **Type checker:** `ty` (not mypy — do not add mypy)

Run the pre-commit hooks before committing and pushing.

## Project Structure

- Source code lives in `python_template/`
  (its not [clean architecture](https://gist.github.com/ygrenzinger/14812a56b9221c9feca0b3621518635b) but the structure follows it more or less)
- Tests live in `tests/unit/`; no integration tests on the main branch
- Prefer classes over "just-methods" (imo makes it easier to test).
- All tool configuration lives in `pyproject.toml` — do not create separate config files (no `setup.py`, `pytest.ini`, `.flake8`, etc.)

## Dependencies

- Add runtime dependencies: `uv add <package>`
- Add dev dependencies (for typing, tests, etc.): `uv add --group dev <package>`
- Always commit the updated `uv.lock` alongside `pyproject.toml`
- Do **not** create `requirements.txt` files

Dependencies can be updated all together with `uv lock --upgrade`
(at least in a separate commit, better in a separate PR).

## Configuration

- App config is in `python_template/config.py` using `pydantic-settings`
- Env files: `.env.shared` (committed, non-secret), `.env.secret` (gitignored, secrets)
- Never hardcode secrets or commit `.env.secret`

## Commits

Follow **Conventional Commits** (enforced by pre-commit `commit-msg` hook):

```
<type>(<optional scope>): <description>

Types: feat, fix, build, ci, docs, perf, refactor, style, test, chore
```

Examples:

```
feat(config): add MY_VAR env variable
fix(db): handle disconnected db on read
test(config): add test for list parsing
```

- Commits to `main` trigger automated version bumping and changelog generation via commitizen
- Do not manually edit `CHANGELOG.md` or bump the version in `pyproject.toml`

## Pre-commit Hooks

| Stage        | Hook                                                                                               |
| :----------- | :------------------------------------------------------------------------------------------------- |
| `commit-msg` | conventional commit message validation                                                             |
| `pre-commit` | trailing whitespace, EOF fixer, YAML check, large file check, ruff-format, ruff, uv-lock, ty check |
| `pre-push`   | pytest unit tests                                                                                  |

If the `uv-lock` hook fails, run `uv lock` and stage the updated `uv.lock`.

## Testing Guidelines

- Write tests in `tests/unit/` using `pytest`
- Use fixtures from `conftest.py` (`db_mock`, `repo`, `caplog`)
  (add more fixtures if needed,
  add `conftest.py` in subdirectories if fixtures are for a sub package only)
- Loguru logs are captured via the custom `caplog` fixtures
  (use it the same way as pytest's built-in `caplog`)
- Mock external dependencies (DB, HTTP clients)
  (unit tests must not require live services)
- Aim for tests that are fast and isolated
