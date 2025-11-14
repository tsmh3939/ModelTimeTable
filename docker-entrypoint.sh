#!/bin/bash
set -e

python cleanup.py

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

python setup.py

python example.py

exec python app.py