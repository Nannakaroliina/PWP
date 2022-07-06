#!/bin/bash

cd src/ || exit
# delete tables
flask delete-tables
cd ../
# delete database
rm -rf db/winebase.db