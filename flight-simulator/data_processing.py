import pandas as pd
import numpy as np
import helper_functions as hfunc
import rocket_classes as rktClass
import constants as con

def import_and_clean_data(file_path, data_type):
    """
    Import and clean telemetry data from a CSV file.

    Args:
    - file_path (str): Path to the CSV file.
    - data_type (str): Type of data (e.g., 'telemetrum', 'telemega').

    Returns:
    - pd.DataFrame: Cleaned dataset.
    """
    if data_type == "telemetrum":
        skip_rows = 93
        drop_rows = 258
    elif data_type == "telemega":
        skip_rows = 80
        drop_rows = 216
    else:
        raise ValueError("Unsupported data type")

    dataset = pd.read_csv(file_path, skiprows=range(1, skip_rows))
    dataset = dataset.iloc[:-drop_rows].drop_duplicates().reset_index()
    dataset["time"] = dataset["time"] - dataset["time"][0]

    return dataset

def calculate_aerodynamic_parameters(dataset, rocket_config):
    """
    Calculate aerodynamic parameters for the dataset.

    Args:
    - dataset (pd.DataFrame): The dataset to process.
    - rocket_config (dict): Configuration parameters of the rocket.

    Returns:
    - pd.DataFrame: Dataset with calculated aerodynamic parameters.
    """
    rocket = rktClass.Rocket(**rocket_config)
    len_characteristic = rocket.L_rocket

    # Fix temperature (temperature readings were taken inside the av bay, which does not change at the same rate as the outside temperature)
    dataset["temperature"] = hfunc.temp_at_height(dataset["height"], dataset["temperature"].iloc[0]+273.15)
    # Calculate additional parameters
    dataset["air_density"] = dataset.apply(
        lambda x: hfunc.air_density_fn(x["pressure"], x["temperature"]), axis=1
    )
    dataset["q"] = dataset.apply(
        lambda x: 0.5 * x["air_density"] * pow(x["speed"], 2), axis=1
    )
    dataset["dynamic_viscosity"] = dataset["temperature"].apply(
        lambda x: hfunc.lookup_dynamic_viscosity(x)
    )
    dataset["reynolds_num"] = dataset.apply(
        lambda x: (x["air_density"] * x["speed"] * len_characteristic)
        / x["dynamic_viscosity"],
        axis=1,
    )
    dataset["mach_number"] = dataset.apply(
        lambda x: hfunc.mach_number_fn(x["speed"], x["temperature"]),
        axis=1,
    )

    return dataset

