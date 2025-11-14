"""
Merge imputed values from ChicagoEnergyBenchmarking_Imputed.csv into the historical
benchmarking data (benchmarking-all-years.csv).

For any missing values in the historical data, check if an imputed value exists and add it
along with a flag indicating it was imputed.

This runs as part of the data pipeline after clean_and_split_data creates the initial
historical dataset.
"""

import pandas as pd
from pathlib import Path


def run():
    """Merge imputed data into the historical benchmarking dataset."""

    # File paths
    historical_path = Path("src/data/dist/benchmarking-all-years.csv")
    imputed_path = Path("src/data/source/ChicagoEnergyBenchmarking_Imputed.csv")
    output_path = historical_path  # Overwrite the historical file

    print("Loading historical benchmarking data...")
    df_historical = pd.read_csv(historical_path)

    print("Loading imputed data...")
    df_imputed = pd.read_csv(imputed_path)

    print(f"Historical data: {len(df_historical)} rows")
    print(f"Imputed data: {len(df_imputed)} rows")

    # Mapping from historical column names (GraphQL-formatted) to imputed column names (snake_case)
    column_mapping = {
        "ElectricityUse": "electricity_use_kbtu",
        "NaturalGasUse": "natural_gas_use_kbtu",
        "TotalGHGEmissions": "total_ghg_emissions_metric_tons_co2e",
        "GHGIntensity": "ghg_intensity_kg_co2e_sq_ft",
        "SourceEUI": "source_eui_kbtu_sq_ft",
        "SiteEUI": "site_eui_kbtu_sq_ft",
        "DistrictSteamUse": "district_steam_use_kbtu",
        "DistrictChilledWaterUse": "district_chilled_water_use_kbtu",
    }

    # Create a column to track which fields were imputed (comma-separated)
    df_historical["ImputedFields"] = ""

    # Merge on building ID and year
    # Select only the columns we need from imputed data
    imputed_cols_to_merge = ["id", "data_year"] + list(column_mapping.values())
    df_imputed_subset = df_imputed[imputed_cols_to_merge].copy()

    # Rename the imputed columns to have _imputed suffix BEFORE merging
    rename_dict = {imp_col: f"{imp_col}_imputed" for imp_col in column_mapping.values()}
    df_imputed_subset = df_imputed_subset.rename(columns=rename_dict)

    df_merged = df_historical.merge(
        df_imputed_subset,
        left_on=["ID", "DataYear"],
        right_on=["id", "data_year"],
        how="left",
    )

    # For each field, check if original is missing and imputed exists
    imputed_count = 0
    imputed_rows = 0

    for hist_col, imp_col in column_mapping.items():
        if hist_col in df_historical.columns:
            imp_col_name = f"{imp_col}_imputed"

            # Find rows where historical value is null but imputed value exists
            if imp_col_name not in df_merged.columns:
                print(f"  Warning: {imp_col_name} not found in merged data, skipping")
                continue

            mask = (df_merged[hist_col].isna()) & (df_merged[imp_col_name].notna())

            if mask.sum() > 0:
                # Fill the missing values with imputed values
                df_merged.loc[mask, hist_col] = df_merged.loc[mask, imp_col_name]

                # Track which fields were imputed (comma-separated list)
                df_merged.loc[mask, "ImputedFields"] = df_merged.loc[
                    mask, "ImputedFields"
                ].apply(lambda x: f"{x},{hist_col}" if x else hist_col)

                imputed_count += mask.sum()
                print(f"  Filled {mask.sum()} missing values for {hist_col}")

    # Count how many rows had at least one imputed field
    imputed_rows = (df_merged["ImputedFields"] != "").sum()

    # Drop the temporary imputed columns
    cols_to_drop = ["id", "data_year"] + [
        f"{col}_imputed" for col in column_mapping.values()
    ]
    df_merged = df_merged.drop(
        columns=[col for col in cols_to_drop if col in df_merged.columns]
    )

    # Save the merged data
    print(f"\nTotal values imputed: {imputed_count}")
    print(f"Rows with imputed data: {imputed_rows}")
    print(f"Saving to {output_path}...")
    df_merged.to_csv(output_path, index=False)
    print("Done!")


if __name__ == "__main__":
    run()
