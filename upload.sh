rm -rf build/
rm -rf dist/
source testenv/bin/activate
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/*
