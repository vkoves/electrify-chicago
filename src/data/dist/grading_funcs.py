import pandas as pd
from scipy.stats import percentileofscore
from typing import List


# Default bins and letter grades for percentile grading:
bins = [0, 20, 40, 60, 80, 100]
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
        calc_func = lambda x: 100 - percentileofscore(vals, x, kind="weak")
    else:
        calc_func = lambda x: percentileofscore(vals, x, kind="weak")
    percent_scores: pd.Series = vals.apply(calc_func)
    grades[f"{field}PercentileGrade"] = percent_scores
    
    # Calculate letter grades (right threshold is included):
    letter_grades = pd.cut(
        percent_scores,
        bins=bins,
        labels=letter_grades,
        right=True
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
        _description_, by default energy_mix_grade_weights
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
    weighted_pct_scores.name = "EnergyMix"

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