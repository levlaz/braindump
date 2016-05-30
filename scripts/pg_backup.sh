#!/bin/bash

set -e

NOW=$(date +"%m-%d-%Y_%H:%M")

docker exec braindump_db_1 pg_dump -Ubraindump_admin -dbraindump -f /db/backups/$NOW.braindump.bak