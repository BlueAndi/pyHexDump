#!/bin/bash
pytest tests -v --cov=./src/pyHexDump --cov-report=html:coverage_report
