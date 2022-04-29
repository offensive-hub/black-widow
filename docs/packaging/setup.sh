#!/bin/bash

if [[ "$1" = '-t' ]];then
  repo_url='https://test.pypi.org/legacy/'
else
  repo_url='https://pypi.org/'
fi

# Remove old build
rm -rf ./build/ ./dist/ ./src/black_widow.egg-info/

cp -f ./src/black_widow/README.md ./

# Make new build
python3 setup.py sdist bdist_wheel

# Upload new build
python3 -m twine upload --repository-url "$repo_url" dist/*

sudo pip3 uninstall black-widow

echo
echo "Install the new black-widow version"
echo
echo "Eg."
echo "  test:"
echo "    sudo pip3 install -i https://test.pypi.org/simple/ black-widow==1.8.0"
echo "  prod:"
echo "    sudo pip3 install -i https://pypi.org/simple/ black-widow==1.8.0"
echo
