#!/bin/bash
# insta485db

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

FILE=var/insta485.sqlite3
if [ ! -f "$FILE" ]; then
  ./bin/insta485db create
fi

export FLASK_ENV=development
export FLASK_APP=insta485
flask run --host 0.0.0.0 --port 8000