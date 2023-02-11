# Flake 8
echo 'flake8'
pipenv run flake8 --config=.flake8
# Pylint
echo '-------------------'
echo 'pylint'
pipenv run pylint */*.py --disable=missing-docstring --errors-only
# MyPy
echo '-------------------'
echo 'mypy'
pipenv run mypy tracker
# Tests
echo '-------------------'
echo 'tests'
pipenv run pytest -c pytest.ini --cov --cov-config .coveragerc