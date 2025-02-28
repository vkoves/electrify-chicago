import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
from typing import List

from src.data.scripts.utils import get_data_file_path


data_directory = "dist"
data_in_file_historical = "benchmarking-all-years.csv"
data_in_file_historical_path = get_data_file_path(
    data_directory, data_in_file_historical
)


# Default bins and letter grades for percentile grading: (note the last bin is 101 so perfect scores
# get an A)
bins = [0, 20, 40, 60, 80, 101]
letter_grades = ["F", "D", "C", "B", "A"]

# Default weights for each energy source in the energy mix grade:
energy_mix_grade_weights = {
    "ElectricityUse": 2,
    "NaturalGasUse": 0.5,
    "DistrictSteamUse": 1,
    "DistrictChilledWaterUse": 1,
    "AllOtherFuelUse": 0,
}

def generate_percentile_grade(
    vals: pd.Series,
    reverse: bool = False,
    bins: List[int] = bins,
    letter_grades: List[str] = letter_grades,
) -> pd.DataFrame:
    """For each building record from `vals`, translate numerical
    values into a percentile grade and it's letter grade
    equivalent. E.g. percentile
    grade of 56.37 means this building is better than 56.37% of records in
    `vals`.

    Parameters
    ----------
    vals : pd.Series
    reverse : bool
        If True, lower values are better. If False, higher values are better.
    bins : List[int]
        Integers denoting boundaries between letter grades.
    letter_grades : List[str]
        Letter grades corresponding to the bins.

    Returns
    -------
    grades : pd.DataFrame
        Percentile and letter grades, with ID and year columns for reference.
        Original Index is also preserved.

    """
    field = vals.name
    grades = pd.DataFrame(index=vals.index)

    # Calculate percentile-based score out 100:
    if reverse:
        def calc_func(x):
            return 100 - percentileofscore(vals, x, kind="weak")
    else:
        def calc_func(x):
            return percentileofscore(vals, x, kind="weak")
    percent_scores: pd.Series = vals.apply(calc_func)
    grades[f"{field}PercentileGrade"] = percent_scores

    # Calculate letter grades (right threshold is included):
    letter_grades = pd.cut(
        percent_scores,
        bins=bins,
        labels=letter_grades,
        right=True,
        include_lowest=True,
    )
    grades[f"{field}LetterGrade"] = letter_grades

    return grades


def generate_energy_int_grade(
    df: pd.DataFrame,
    year: int,
    cols_to_keep: List[str] = ["ID", "DataYear"],
    bins: List[int] = bins,
    letter_grades: List[str] = letter_grades,
):
    """Generate percentile and letter grades for `GHGIntensity` field.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing building records.
    year : int
        Year to filter records by.
    cols_to_keep : List[str]
        Columns to keep from `df`.
    bins : List[int]
        Integers denoting boundaries between letter grades.
    letter_grades : List[str]
        Letter grades corresponding to the bins.

    Returns
    -------
    ghg_intensity_res : pd.DataFrame
        Percentile and letter grades for `GHGIntensity` field. Uses `df`'s
        index. `cols_to_keep` are also included.

    """
    relevant_cols: pd.DataFrame = df.loc[
        df["DataYear"] == year,
        cols_to_keep,
    ]

    ghg_intensity: pd.Series = df.loc[
        df["DataYear"] == year,
        "GHGIntensity",
    ]

    ghg_intensity_grades_df: pd.DataFrame = generate_percentile_grade(
        vals=ghg_intensity,
        reverse=True,
        bins=bins,
        letter_grades=letter_grades,
    )

    ghg_intensity_res = pd.merge(
        relevant_cols,
        ghg_intensity_grades_df,
        left_index=True,
        right_index=True,
    )

    return ghg_intensity_res


def apply_grade_func_all_years(df, func):
    """Generate grades for all years in the `df` dataset using a given `func`
    to grade each year.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing building records.

    Returns
    -------
    grades_all_years_df : pd.DataFrame
        Grades for all years in the `df` dataset.
        ["ID", "DataYear", "GHGIntensity"] are also included for reference.

    """
    all_years = df["DataYear"].unique()
    grades_all_years = []
    for year in all_years:
        grades_df = func(
            df=df, year=year
        )
        grades_all_years.append(grades_df)

    grades_all_years_df = pd.concat(
        grades_all_years
    )
    return grades_all_years_df


def generate_energymix_grade(
    df: pd.DataFrame,
    year: int,
    cols_to_keep: List[str] = ["ID", "DataYear"],
    energy_mix_grade_weights: dict = energy_mix_grade_weights,
    bins: List[int] = bins,
    letter_grades: List[str] = letter_grades,
):
    """Generate percentile and letter grades for each building
    based on energy mix fields.
    First, energy use percentage for each building per source is calculated.
    Second, weights are applied to each energy source percentage to
    calculate a weighted sum for percentages for each building. Then these
    weighted sums are converted to percentile and letter grades.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing building records.
    year : int
        Year to filter records by.
    cols_to_keep : List[str]
        Columns to keep from `df`.
    energy_mix_grade_weights : dict, optional
        Weights to use, by default energy_mix_grade_weights
    bins : List[int]
        Integers denoting boundaries between letter grades.
    letter_grades : List[str]
        Letter grades corresponding to the bins.

    Returns
    -------
    energy_mix_grades : pd.DataFrame
        Percentile and letter grades for energy mix. Uses `df`'s index.
        `cols_to_keep` are also included.

    """
    relevant_cols: pd.DataFrame = df.loc[
        df["DataYear"] == year,
        cols_to_keep,
    ]

    energy_source_cols = [
        "ElectricityUse",
        "NaturalGasUse",
        "DistrictSteamUse",
        "DistrictChilledWaterUse",
        "AllOtherFuelUse"
    ]
    energy_use_df: pd.DataFrame = df.loc[
        df["DataYear"] == year,
        energy_source_cols,
    ]

    total_energy_use_per_bldg: pd.Series = energy_use_df.sum(1)

    # Energy use kBtu percentage within each building for this year:
    energy_use_pct_df = energy_use_df.div(
        total_energy_use_per_bldg,
        axis="index"
    ) * 100

    # Calculate weighted energy mix grade:
    weighted_pct_scores: pd.Series = energy_use_pct_df.mul(
        energy_mix_grade_weights
    ).sum(1)
    weighted_pct_scores.name = "EnergyMixWeightedPctSum"

    # Generate percentile and letter grades:
    energy_mix_grades: pd.DataFrame = generate_percentile_grade(
        weighted_pct_scores,
        reverse=False,
        bins=bins,
        letter_grades=letter_grades,
    )

    # Attach weighted percent scores for reference:
    energy_mix_grades = pd.merge(
        weighted_pct_scores,
        energy_mix_grades,
        left_index=True,
        right_index=True,
    )

    # Add grades to columns to keep:
    energy_mix_grades = pd.merge(
        relevant_cols,
        energy_mix_grades,
        left_index=True,
        right_index=True,
    )

    return energy_mix_grades


def calculate_building_submission_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the submission rate per building (percentage of years submitted).

    Args:
        df (pd.DataFrame): The DataFrame with building and year data.
        building_id_col (str): The name of the building ID column.
        status_col (str): The name of the status column.
        not_submitted_val (str): The value indicating a building is not submitted.

    Returns:
        pd.DataFrame: A DataFrame with building IDs and their submission rates as a SubmissionRate
            column
    """

    def calculate_metrics(group):
        total_years = len(group)
        # TODO: Refactor not submitted to be no GHG Intensity, since that's our true count
        not_submitted_count = (group['ReportingStatus'] == 'Not Submitted').sum()
        submitted_years = total_years - not_submitted_count

        if total_years == 0:
            submission_rate = 0.0
        else:
            submission_rate = (submitted_years / total_years) * 100

        return pd.Series({'submission_rate': submission_rate, 'not_submitted_count': not_submitted_count})

    submission_rates = df.groupby('ID').apply(calculate_metrics).reset_index()

    print('submission_rates', submission_rates.head())

    return submission_rates


def generate_consistent_reporting_grade(
    df: pd.DataFrame,
    bins: List[int] = bins,
):
    """
    Generate grades for consistent reporting, based on how many records are missing for each
    building.

    NOTE: This is not a relative percentile like the other grades, because there's a perfect score,
    and we don't care about the average performance. If you report all years, you get a 100%, if you
    report 1/5, you get a 20%.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing historical building records.
    bins : List[int]
        Integers denoting boundaries between letter grades. Right threshold is
        included.

    Returns
    -------
    not_submitted_count_df : pd.DataFrame
        Number of missing records and corresponding letter grades for each
        building ID.

    """
    df = df.copy()

    # Relevant columns:
    df = df.loc[:, ["ID", "DataYear", "ReportingStatus"]]

    # Calculate number of missing records for each building:
    submission_rates_df = calculate_building_submission_rate(df)

    # Calculate grades based on how many records are missing for each building:
    submission_rates_df['SubmittedRecordsGrade'] = pd.cut(
        submission_rates_df['submission_rate'],
        bins=bins,
        include_lowest=True,
        labels=letter_grades,
        right=False,
    )

    # Rename for consistent format:
    submission_rates_df.rename(
        columns={
            'not_submitted_count': 'MissingRecordsCount',
            'submission_rate': 'MissingRecordsCountPercentileGrade'
        }, inplace=True
    )

    submission_rates_df.reset_index(inplace=True)

    print('submission_rates_df', submission_rates_df.head())

    # submission_rates_df.insert(
    #     2, "MissingRecordsCountPercentileGrade", percentiles
    # )

    return submission_rates_df


def grade_ghg_intensity_energy_mix_all_years(building_data: pd.DataFrame):
    """Generate grades for all years in the dataset based on GHG intensity and
    energy mix.

    Parameters
    ----------
    building_data : pd.DataFrame
        The buildings records dataset

    Returns
    -------
    df : pd.DataFrame
        Grades for all years in the dataset based on GHG intensity and energy
        mix, merged with the original dataset.

    """
    # Generate grades for GHG intensity:
    ghg_intensity_grades_all_years = apply_grade_func_all_years(
        df=building_data,
        func=generate_energy_int_grade,
    )

    # Generate grades for energy mix:
    energy_mix_grades_all_years = apply_grade_func_all_years(
        df=building_data,
        func=generate_energymix_grade,
    )

    # Merge grades:
    grades_all_years_df = pd.merge(
        ghg_intensity_grades_all_years,
        energy_mix_grades_all_years,
        on=["ID", "DataYear"],
    )

    # Add to the original dataset:
    df = pd.merge(
        building_data,
        grades_all_years_df,
        on=["ID", "DataYear"],
    )

    return df


def grade_buildings(building_data):
    # Generate grades for all years for GHG Intensity and Energy Mix:
    graded_df = grade_ghg_intensity_energy_mix_all_years(
        building_data=building_data,
    )

    # Generate grades for consistent reporting (not missing records):
    df_historical = pd.read_csv(data_in_file_historical_path)
    consistent_reporting_grades = generate_consistent_reporting_grade(df_historical)
    graded_df = pd.merge(
        left=graded_df,
        right=consistent_reporting_grades,
        how="left",
        on="ID",
    )

    # Overall numerical grade, average of all percentile grades:
    graded_df["AvgPercentileGrade"] = graded_df[
        [
            "GHGIntensityPercentileGrade",
            "EnergyMixWeightedPctSumPercentileGrade",
            "MissingRecordsCountPercentileGrade"
        ]
    ].mean(axis=1)

    # Overall letter grade:
    graded_df["AvgPercentileLetterGrade"] = pd.cut(
        graded_df["AvgPercentileGrade"],
        bins=bins,
        labels=letter_grades,
        right=True
    )

    graded_df["AvgPercentileLetterGradeQuintiles"] = pd.cut(
        graded_df["AvgPercentileGrade"],
        bins=5,
        labels=letter_grades,
        right=True
    )

    return graded_df
