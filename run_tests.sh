#!/bin/bash
test=$(pwd)/test/unit/

pytest --cov src test
# --cov-report html