"""
Michelle Wang
utils.py: reusable functions that are called in sundash.py
"""

# import libraries
import pandas as pd


def read_file(filename, names):
    """ Read in a csv file into a dataframe

    Args:
        filename (str): name of file that you are interested in
        names (list): list of names for the headers
    Returns:
        df (pd.DataFrame): pandas dataframe of the dataset with no headers
    """
    # read csv file into pandas
    df = pd.read_csv(filename, names=names)

    return df


def filter_data(df, column_name, num_years):
    """ Filter data based on a column name so that it only includes data within the specified date range

    Args:
        df (pd.DataFrame): dataset for interest in pandas dataframe
        column_name (str): name of desired column
        num_years (tuple): desired date range

    Returns:
        df (pd.DataFrame): interested dataset with rows only within the specified date range
    """
    # filter out rows that are between the num_years date range
    df = df[df.loc[:, column_name].between(num_years[0], num_years[1])]

    return df
