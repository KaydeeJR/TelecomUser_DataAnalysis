import numpy as np
import pandas as pd


class CleanDataframe:
    def csv_to_dataframe(self, filePath: str) -> pd.DataFrame:
        dataframe = pd.read_csv(filePath.replace(" ", ""))
        return dataframe

    def calculate_percent_missing(self, dataframe):
        totalValCount = np.product(dataframe.shape)

        # Count number of missing values in each column
        missingValCount = dataframe.isnull().sum()

        # Calculate total number of missing values
        totalMissingValues = missingValCount.sum()

        # Calculate percentage of missing values
        print(round(
            ((totalMissingValues/totalValCount) * 100), 2), "% of values are missing.")


cleanDFClass = CleanDataframe()
dataframe = cleanDFClass.csv_to_dataframe(
    'D:/10XAcademy/TelecomUser_DataAnalysis/data/Week1_challenge_data_source.csv')