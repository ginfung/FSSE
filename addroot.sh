# adding the current project path to PYTHONPATH.
# this script can be called at any folder
# command : source addpath.sh

#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="${PYTHONPATH}:$DIR"