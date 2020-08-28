#!/bin/sh
PYTHONPATH='src' luigi --module FactorCalculatorTask FactorCalculatorTask --runDate 2016-01-28 --multiFactor True --logging-conf-file /Users/mjtung/Projects/luigi-examples/example-mj/debug-macos/luigi-logging.conf --workers 10
