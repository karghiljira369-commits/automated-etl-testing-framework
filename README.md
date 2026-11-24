# Automated ETL Testing Framework

## Project Overview
A Python-based automated ETL data validation framework
designed to identify data quality problems in sales datasets.

## Technologies Used
- Python
- Pandas
- Pytest
- Git and GitHub
- CSV Data Processing

## Features
- Sales amount validation
- Missing customer detection
- Missing product detection
- Duplicate transaction ID detection
- Non-numeric amount detection
- Data quality summary reporting
- Automated testing using Pytest

## Project Structure
- data/ - Sample sales datasets
- src/ - Python validation programs
- tests/ - Automated Pytest test cases
- reports/ - Validation reports

## Installation

Create and activate a Python virtual environment.

Install dependencies:

    python -m pip install -r requirements.txt

## Run Validation

    python -m src.run_validation

## Run Automated Tests

    python -m pytest tests/test_validation.py -v

## Testing Results
- Total sample records: 14
- Valid records: 8
- Invalid records: 6
- Automated tests: 10 passed

## Future Enhancements
- SQL database validation
- Source-to-target reconciliation
- Advanced data quality rules
- HTML testing reports
- GitHub Actions CI/CD

## Project Type
Personal learning and portfolio project using sample data.