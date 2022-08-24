from configparser import Interpolation
import numpy as np
import pandas as pd
import sklearn as sk


class CleanDataframe:
    def csv_to_dataframe(self, filePath: str) -> pd.DataFrame:
        dataframe = pd.read_csv(filePath.replace(" ", ""))
        return dataframe

    def get_numeric_columns(self, df)->list:
        return list(df.select_dtypes(exclude=['object']).columns)

    def calculate_percent_missing(self, dataframe):
        totalValCount = np.product(dataframe.shape)

        # Count number of missing values in each column
        missingValCount = dataframe.isnull().sum()

        # Calculate total number of missing values
        totalMissingValues = missingValCount.sum()

        # Calculate percentage of missing values
        print(round(
            ((totalMissingValues/totalValCount) * 100), 2), "% of values are missing.")
    
    def drop_empty_bearer_ids(self, dataframe)->pd.DataFrame:
        # bearer ids are unique and empty values cannot be filled up using the mean
        dataframe.dropna(subset=["Bearer Id"],inplace=True)

    def detect_and_delete_outliers(self, dataframe)->pd.DataFrame:
        # using IQR.
        # fixing outliers first so they do not interfere with the value of mean
        col_list = self.get_numeric_columns(df=dataframe)
        col_list.remove("Bearer Id")
        upper_lim={}
        lower_lim={}
        for col in col_list:
            # calculating IQR for each column
            q1 = np.percentile(dataframe[col],25,method='midpoint')
            q3 = np.percentile(dataframe[col],75, method = 'midpoint')
            IQR = q3 - q1
            upper_lim = np.where(dataframe[col]>=(q3+1.5*IQR))
            lower_lim = np.where(dataframe[col]<=(q1-1.5*IQR))
        # deleting outliers
        dataframe.drop(upper_lim[0],inplace=True)
        dataframe.drop(lower_lim[0],inplace=True)
        return dataframe



    def fill_missing_values(self, dataframe)->pd.DataFrame:
        # fill with mean value of column
        col_list = self.get_numeric_columns(df=dataframe)
        col_list.remove("Bearer Id")
        mean_values_list = list(dataframe.drop("Bearer Id",axis=1).describe().iloc[1])


