import pandas as pd
from scipy.stats import percentileofscore
from typing import List


bins = [0, 20, 40, 60, 80, 100]
letter_grades = ["F", "D", "C", "B", "A"]


def generate_percentile_grade(
        df: pd.DataFrame, 
        year: int, 
        field: str,
        bins: List[int] = bins,
        letter_grades: List[str] = letter_grades,
    ) -> pd.DataFrame:
    """For each building record from `df` of year `year, translate numerical 
    valus in the `field` column into a percentile grade and it's letter grade 
    equivalent. Each letter grade (A to F) has 20% of records. E.g. percentile 
    grade of 56.37 means this building is better than 56.37% of records in `df` 
    for that `year`.

    Parameters
    ----------
    df : pd.DataFrame
        Input building records
    year : int
        Year to calculate grades for
    field : str
        Name of column to calculate grades for
    bins : List[int]
        Integers denoting boundaries between letter grades
    letter_grades : List[str]
        Letter grades corresponding to the bins
    Returns
    -------
    grades : pd.DataFrame
        Percentile and letter grades, with ID and year columns for reference. 
        Original Index is also preserved.

    """
    grades: pd.DataFrame = df.loc[
        df["DataYear"] == year,
        ["ID", "DataYear", field]
    ]
    
    col_vals: pd.Series = grades.loc[:, field]

    # Calculate percentile-based score out 100:
    percent_scores: pd.Series = col_vals.apply(
        lambda x: 100 - percentileofscore(col_vals, x, kind="weak")
    )
    grades[f"{field}PercentileGrade"] = percent_scores
    
    # Calculate letter grades (right threshold is inlcuded):
    letter_grades = pd.cut(
        percent_scores,
        bins=bins,
        labels=letter_grades,
        right=True
    )
    grades[f"{field}LetterGrade"] = letter_grades

    return grades
    # df_current.loc[:, ["GHGIntensityLetterGrade"]] = pd.cut(
    #     df_current["GHGIntensityPercentileGrade"],
    #     bins=bins,
    #     labels=letter_grades,
    #     right=True
    # )