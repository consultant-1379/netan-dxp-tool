#!/usr/bin/env bash

#  COPYRIGHT Ericsson 2019
#  The copyright to the computer program(s) herein is the property of
#  Ericsson Inc. The programs may be used and/or copied only with written
#  permission from Ericsson Inc. or in accordance with the terms and
#  conditions stipulated in the agreement/contract under which the
#  program(s) have been supplied.

trap 'catch' ERR

catch() {
  echo "ERROR: An error has occurred, the installation has been aborted."
  exit 1
}

# The name of the tool, with no file extension.
TOOL_NAME="dxp"

GIT_PATH=`which git` || \
{ echo "ERROR: Could not find git."; exit 127; }

# Get the directory where git is located, in order to copy the tool to the same place as git.
GIT_DIR=`dirname  ${GIT_PATH}`

# Creates the executable file for the tool in the 'dist' directory.
pyinstaller --onefile src/${TOOL_NAME}.py || \
{ echo "ERROR: Please install pyinstaller with 'pip install pyinstaller'."; exit 127; }

# Copy the executable file to the git directory.
cp dist/${TOOL_NAME}.exe ${GIT_DIR}/ || \
{ echo "ERROR: You should run this script with administrative privileges."; exit 126; }
