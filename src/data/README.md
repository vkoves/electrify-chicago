- [Data Folder](#data-folder)
  - [Python setup](#python-setup)
  - [Data Dist Folder](#data-dist-folder)
  - [File Explainers](#file-explainers)
    - [The Main/Holistic File - `building-benchmarks.csv`](#the-mainholistic-file---building-benchmarkscsv)
    - [The Historical File - `benchmarking-all-years.csv`](#the-historical-file---benchmarking-all-yearscsv)
    - [City-Wide Stats - `building-benchmark-stats.json`](#city-wide-stats---building-benchmark-statsjson)
    - [Property Type Stats - `building-statistics-by-property-type.json`](#property-type-stats---building-statistics-by-property-typejson)
    - [Available Property Types - `property-types.json`](#available-property-types---property-typesjson)

(Generated using VSCode extension "Markdown All In One")


# Data Folder

This folder is for all of our data processing, including:

- `/analysis` - Jupyter research notebooks
- `/debug` - more readable debug data from running the data pipeline
- `/dist` - the files generated from our data pipeline, used by the actual site
- `/scripts` - all our data processing scripts
- `/source` - input files to our data pipeline, typically the latest benchmarking data


## Python setup
Install virtual environments to manage dependencies according to the guide in [Electrify-Chicago/PythonDev.md](../../PythonDev.md)

## Data Dist Folder

This directory contains files used for the actual built site. These are committed, since the city
data (and our data pipeline) changes infrequently.

**Important!** To keep things clean, keep this directory minimal, and make sure all files are
auto-generated when you run the data pipeline - any manual custom information should live in our
JS files in Gridsome, not in the data pipeline.

## File Explainers

### The Main/Holistic File - `building-benchmarks.csv`

This file contains one row for each building, and contains information for the latest year they
submitted data. This file has the most columns, because it includes overall and by property type
rankings (e.g. #1 highest GHG in the city, #3 highest GHG among Office), but the fewest rows.

### The Historical File - `benchmarking-all-years.csv`

Contains one row for each building per year of data in the source data, with a limited set of
columns we track over time. This file has the most rows, and is only used on the building details
page to show historical trends in things like electric & gas use, emissions, etc.

### City-Wide Stats - `building-benchmark-stats.json`

Statistics on the overall data set of buildings across a number of properties, for example the
average GHG emissions, intensity, and gas use among all benchmark buildings.

### Property Type Stats - `building-statistics-by-property-type.json`

A larger JSON file of the same city-wide statistics, but by each property type. For example, the
average, min and max electric and gas use among buildings with type 'Office'.

### Available Property Types - `property-types.json`

The property types in benchmark data - for the front-end to show filters.
