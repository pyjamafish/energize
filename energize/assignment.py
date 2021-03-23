"""
Get the temperature values of all rooms on AHS' third floor,
initialize a DataFrame from them, and export the DataFrame to csv.
"""

import sys
from importlib import resources

import pandas as pd

from energize import building_data_requests as bdr


def get_third_floor_meters():
    """
    Read the CSV file of AHS temperature meters
    and return the rows with meters located on the third floor.
    """
    with resources.open_text("energize.data", "ahs_air.csv") as f:
        meters_df = pd.read_csv(f)
    return meters_df.loc[meters_df["Label"].str.startswith("3")]


def to_bulk_request(meters_df):
    """
    Convert a dataframe to a bulk request
    to the Building Energy Gateway.
    """
    meters_df.drop(columns=["CO2"], inplace=True)
    meters_df.rename(
        columns={
            "Label": "label",
            "Facility": "facility",
            "Temperature": "instance"
        },
        inplace=True
    )
    return meters_df.to_dict("records")


def main():
    bulk_request = to_bulk_request(get_third_floor_meters())
    response = bdr.get_bulk(bulk_request)
    df = pd.DataFrame(response["rsp_list"])
    df.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    main()
