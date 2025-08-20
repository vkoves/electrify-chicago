# Data Update Checklist

Quick checklist for updating to a new year's data.

## Required Steps

- [ ] **Download new data** from [Chicago Energy Benchmarking Data Portal](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/about_data)
- [ ] **Replace source data** - Update `src/data/source/ChicagoEnergyBenchmarking.csv` with the new file
- [ ] **Run data processing**:
  ```bash
  docker-compose run --rm electrify-chicago python3 run_all.py
  ```
- [ ] **Regenerate Python test data**:
  ```bash
  docker-compose run --rm electrify-chicago bash create_test_data.sh
  ```
- [ ] **Update FE latest year constant** in `src/constants/globals.vue` (change `LatestDataYear`)
- [ ] **Run tests and fix failures**:
  ```bash
  docker-compose run --rm electrify-chicago python -m pytest
  ```
- [ ] **Regenerate social images**:
  ```bash
  yarn gen-fresh-social-imgs
  ```
- [ ] **Update Release Notes** - Add data update section to `src/pages/ReleaseNotes.vue`

## Common Test Fixes Needed

- **Column mismatches**: Update expected column lists if data structure changed
- **Count mismatches**: Adjust expected record counts in test files
- **Year expectations**: Update hardcoded years in test assertions
- **Ward changes**: Update expected ward assignments if buildings moved
