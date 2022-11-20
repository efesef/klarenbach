import pandas as pd
import os
import re 
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

def measurement_location(df):
    """
    Returns dictionaries of KPI measurement definitions and cells where these definitions are stored.

    The way we find this is by looking up where BW data is stored and going two up and one to the right.
    """
    first_column = df.iloc[:, 0]

    bws = df.loc[first_column == "Baden-Württemberg", :].index

    locations = [(i - 2, 1) for i in bws]
    measurements = [{df.iloc[loc]: loc} for loc in locations]

    return measurements


def measurement_ranges(df):
    """
    Each worksheet can contains various measurements of a kpi.

    This function returns the ranges in which each measurement is stored in the sheet.

    It inputs a worksheet and outputs a dictionary of {measurement : data range} key value pairs.
    """
    measurements = measurement_location(df)

    measurement_df = pd.DataFrame(columns=["measurement", "range_start", "range_end"])

    for m in measurements:
        range_start = (list(m.values())[0][0] + 2, list(m.values())[0][1] - 1)
        range_end = (range_start[0] + 17), len(
            df.iloc[3, :]
        )  # end of range is row start + 17 and column determined by the length of the "year" row
        measurement_name = list(m.keys())[0]
        new_df = {
            "measurement": measurement_name,
            "range_start": range_start,
            "range_end": range_end,
        }

        measurement_df = measurement_df.append(new_df, ignore_index=True)

    return measurement_df


def df_to_pg(df, sheets, pg_uri):
    """
    Inputs: dataframe storing multiple excel worksheets - umweltreport_laender.xlsx
            sheets - list of all worksheets to ingest.
            Postgres connection uri.

    Output: writes each single KPI measurement to a PG db
    """
    engine = create_engine(pg_uri)

    for sheet in sheets:
        # each sheet contains data on a single kpi. each kpi might be represented in various measurements (totals, % etc.)
        # the first loop goes through each single sheet and extracts sheet specific data.
        try:
            table = df[sheet].iloc[1, 0]
            #print(f"Migrating sheet {table}")
            core_kpi = df[sheet].iloc[1, 1]
            column_name = df[sheet].iloc[3, 0:]

            measurements = measurement_ranges(df[sheet])
            # each kpi can be measured in different ways. this loop now extracts every single measurement present
            # in the sheet and writes each individual measurement to the pg db.
            for index, row in measurements.iterrows():
                data_range = df[sheet].iloc[
                    row["range_start"][0] : row["range_end"][0],
                    row["range_start"][1] : row["range_end"][1],
                ]
                data_range.columns = column_name
                data_range["table"] = table
                data_range["core_kpi"] = core_kpi
                data_range["measurement"] = row["measurement"]

                data_range = pd.melt(
                    data_range,
                    id_vars=["table", "core_kpi", "measurement", "Land"],
                    var_name="year",
                    value_name="value",
                )

                df.to_sql("umwelt_panels", engine)

        except Exception as err:
            pass
