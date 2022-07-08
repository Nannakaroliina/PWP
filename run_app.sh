#!/bin/bash

# find the current path and set db location
db=$(pwd)/db/winebase.db
cd src/ || exit

# check if db exists, if not, create one
if [[ -f $db ]]; then
  echo "[INFO] Wine database already exists, let's continue..."
else
  echo "[INFO] Wine database does not exist, let's create one"
  echo "[INFO] Initialize database"
  flask create-tables
  echo "[INFO] Populating database"
  flask populate-database
  echo "[INFO] Database initialized and populated, let's continue..."
fi

flask run
