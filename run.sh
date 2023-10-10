#!/bin/bash

set -e

export $(sed 's/#.*//g' .env | xargs)
exec python manage.py "$@"
