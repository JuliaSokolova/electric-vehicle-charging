import pyspark as ps
from pyspark.sql.functions import udf
from pyspark.sql import functions as F
import json
import numpy as np
import pandas as pd

# Create spark session
spark = (ps.sql.SparkSession
         .builder
         .master('local[4]')
         .appName('julia_json')
         .getOrCreate())
sc = spark.sparkContext


def get_data(file_path='./data/acndata_sessions_3years.json'):
    '''
    Reads .json file.
    Breaks data into two tables - charging and users.
    Saves tables as .csv.
    '''
    spark_df_all = spark.read.json(sc.wholeTextFiles().values(file_path))
    # creating a table with information about charging sessions
    charging = spark_df_all.drop('userInputs')
    charging = charging.toPandas()
    # creatint a table with information about users
    user_input_0 = spark_df_all[['userInputs']]
    user_input = user_input_0.na.drop()
    rdd = user_input.rdd.map(list)
    rdd1 = rdd.flatMap(lambda x: x[0])
    users = spark.createDataFrame(rdd1)
    users = users.toPandas()

    return charging, users


def update_users_datetime(filepath='./data/users.csv'):
    '''
    Changes data type for colums with day, time to datetime.
    '''
    users_to_clean = pd.read_csv(filepath)
    users_to_clean['Modified'] = pd.to_datetime(
        users_to_clean.modifiedAt,
        infer_datetime_format=True)
    users_to_clean['Departure'] = pd.to_datetime(
        users_to_clean.requestedDeparture,
        infer_datetime_format=True)
    users = users_to_clean.drop(columns=[
        'requestedDeparture',
        'modifiedAt',
        'Unnamed: 0'])
    return users


def update_charging_datetime(filepath='./data/charging.csv'):
    charging_to_clean = pd.read_csv('./data/charging.csv')
    charging_to_clean['ConnectionTime'] = pd.to_datetime(
        charging_to_clean.connectionTime,
        infer_datetime_format=True)
    charging_to_clean['DisconnectTime'] = pd.to_datetime(
        charging_to_clean.disconnectTime,
        infer_datetime_format=True)
    charging_to_clean['DoneCharging'] = pd.to_datetime(
        charging_to_clean.doneChargingTime,
        infer_datetime_format=True)
    charging = charging_to_clean.drop(
        columns=[
            'connectionTime',
            'disconnectTime',
            'doneChargingTime',
            'Unnamed: 0'])
    return charging

if __name__ == "__main__":
    charging.to_csv('charging.csv')
    users.to_csv('users.csv')
    print ('Files users.csv, charging.csv are created.')
