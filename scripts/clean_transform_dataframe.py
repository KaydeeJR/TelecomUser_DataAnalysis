import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer
import seaborn as sns

class CleanTransformDataframe:
    def calculate_percent_missing(self, dataframe):
        totalValCount = np.product(dataframe.shape)

        # Count number of missing values in each column
        missingValCount = dataframe.isnull().sum()

        # Calculate total number of missing values
        totalMissingValues = missingValCount.sum()

        # Calculate percentage of missing values
        print(round(
            ((totalMissingValues/totalValCount) * 100), 2), "% of values are missing.")
    
    def drop_column(self, dataframe, column)->pd.DataFrame:
        # drop NaN values from columns
        dataframe.dropna(subset=column,inplace=True)

    def plot_outliers(self, dataframe):
        col_list = self.get_numeric_columns(dataframe)
        df_no_id = dataframe.drop("Bearer Id",axis=1)
        for col in col_list:
            plt.figure()
            df_no_id.boxplot([col])

    def delete_outliers(self, dataframe)->pd.DataFrame:
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

    def fill_missing_values(self, dataframe,col_list)->pd.DataFrame:
        # fill with mean value of column
        mean_values_list = list(dataframe.drop(columns = col_list,axis=1).describe().iloc[1])
    
    def string_bearer_ids(self, dataframe, column)->pd.Series:
        return pd.Series(dataframe[column].value_counts().head(10).index, dtype="string")

    def bytes_to_GB(self, dataframe):
        dataframe.apply(lambda x:x/10**9)

    def ms_to_hours(self,dataframe):
        dataframe.apply(lambda x:x/3600000)

    def normalizer(dataframe):
        # Dataframe should not have NaN values
        norm = Normalizer()
        # normalize the exponential data with boxcox
        normalized_data = norm.fit_transform(dataframe)
        # plot both together to compare
        fig, ax=plt.subplots(1,2, figsize=(10, 5))
        sns.histplot(dataframe, ax=ax[0])
        ax[0].set_title("Original Data")
        sns.histplot(normalized_data, ax=ax[1])
        ax[1].set_title("Normalized data")