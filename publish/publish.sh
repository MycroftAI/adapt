#!/usr/bin/env bash

set -Ee # fail on error

# pypi and testpypi .python.org credential variables must be set
#TESTPYPI_USERNAME=
#TESTPYPI_PASSWORD=
#PYPI_USERNAME=
#PYPI_PASSWORD=

# set top of working directory
TOP=$(cd $(dirname $0)/.. && pwd -L)
echo "The working directory top is ${TOP}"

# set virtualenv root
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/adapt"}
echo "The virtualenv root location is ${VIRTUALENV_ROOT}"

# get latest release version
VERSION="$(basename $(git for-each-ref --format="%(refname:short)" --sort=-authordate --count=1 refs/tags) | sed -e 's/v//g')"
echo "The latest adapt release version is ${VERSION}"

# check out tagged version
git checkout release/v${VERSION}

# get setup.py version
PYPI_VERSION=$(python ${TOP}/setup.py --version)
echo "The adapt version found in setup.py is ${PYPI_VERSION}"

# verify release tag and setup.py version are equal
if [[ ${VERSION} != ${PYPI_VERSION} ]]; then
  echo "setup.py and release tag version are inconsistent."
  echo "please update setup.py and verify release"
  exit 1

fi

# clean virtualenv and remove previous test results
echo "Removing previous virtualenv and test results if they exist"
rm -rf ${VIRTUALENV_ROOT} TEST-*.xml

# create virtualenv
echo "Creating virtualenv"
virtualenv ${VIRTUALENV_ROOT}
# activate virtualenv
. ${VIRTUALENV_ROOT}/bin/activate

echo "Installing adapt requirements.txt"
# install adapt requirements
pip install -r requirements.txt

echo "Installing adapt test-requiremtns.txt"
# install adapt test runner requirements
pip install -r test-requirements.txt

# run unit tests
python run_tests.py

function replace() { # @Seanfitz is the bomb.com
  local FILE=$1
  local PATTERN=$2
  local VALUE=$3
  local TMP_FILE="/tmp/$$.replace"
  cat ${FILE} | sed -e "s/${PATTERN}/${VALUE}/g" > ${TMP_FILE}
  mv ${TMP_FILE} ${FILE}
}

echo "Creating ~/.pypirc from template"
PYPIRC_FILE=~/.pypirc
cp -v ${TOP}/publish/pypirc.template ${PYPIRC_FILE}
replace ${PYPIRC_FILE} %%PYPI_USERNAME%% ${PYPI_USERNAME}
replace ${PYPIRC_FILE} %%PYPI_PASSWORD%% ${PYPI_PASSWORD}
replace ${PYPIRC_FILE} %%TESTPYPI_USERNAME%% ${TESTPYPI_USERNAME}
replace ${PYPIRC_FILE} %%TESTPYPI_PASSWORD%% ${TESTPYPI_PASSWORD}
# make .pyric private
chmod -v 600 ${PYPIRC_FILE}

echo "Registering at pypitest.python.org"
python setup.py register -r pypitest
echo "Uploading to pypitest.python.org"
python setup.py sdist upload -r pypitest

echo "testing installation from testpypi.python.org"
PYPI_TEST_VIRTUALENV='/tmp/.virtualenv'
rm -Rvf ${PYPI_TEST_VIRTUALENV}
virtualenv ${PYPI_TEST_VIRTUALENV}
deactivate
. ${PYPI_TEST_VIRTUALENV}/bin/activate
pip install -r requirements.txt
pip install -i https://testpypi.python.org/pypi adapt-parser==${VERSION}
deactivate
rm -Rvf ${PYPI_TEST_VIRTUALENV}

. ${VIRTUALENV_ROOT}/bin/activate
echo "Registering at pypi.python.org"
python setup.py register -r pypi
echo "Uploading to pypi.python.org"
python setup.py sdist upload -r pypi
