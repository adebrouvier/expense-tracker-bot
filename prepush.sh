# Flake 8
echo 'flake8'
uv run flake8 --config=.flake8
# Pylint
echo '-------------------'
echo 'pylint'
uv run pylint */*.py --disable=missing-docstring --errors-only
# MyPy
echo '-------------------'
echo 'mypy'
uv run mypy tracker
# Tests
echo '-------------------'
echo 'tests'
uv run pytest -c pytest.ini --cov --cov-config .coveragerc
