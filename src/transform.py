import os
import pathlib
from pyspark.sql import SparkSession, Window, functions as pysparkF, DataFrame as pysparkDataFrame

def transform():
    spark = SparkSession.builder.appName("ELT-weather-data").getOrCreate()
    p = pathlib.Path.cwd().joinpath('res')

    for file in p.iterdir():
        print(file)
        df = spark.read.json(str(file), multiLine=True).drop('daily_units', 'generationtime_ms', 'utc_offset_seconds', 'timezone_abbreviation')
        df.show()
        df.printSchema()

        dailyDF = joinArrayColumns(
            df.select(pysparkF.expr('daily.*')), 
            ['time', 'weather_code', 
             'temperature_2m_min', 'temperature_2m_max', 
             'apparent_temperature_min', 'apparent_temperature_max', 
             'sunrise', 'sunset', 'daylight_duration', 'sunshine_duration', 
             'precipitation_sum', 'rain_sum', 'snowfall_sum', 'precipitation_hours'])
        dailyDF.printSchema()
        dailyDF.show()



    spark.stop()
    pass

def joinArrayColumns(df: pysparkDataFrame, columns : list['str']) -> pysparkDataFrame:
    if(len(columns) <= 1):
        return df
    
    ret = df.select(pysparkF.explode(columns[0]).alias(columns[0]))
    for col in columns:
        if(ret.columns.count(col) == 0):
            ret = joinDataFrames(ret, df.select(pysparkF.explode(col).alias(col)))
    return ret

def joinDataFrames(df1: pysparkDataFrame, df2: pysparkDataFrame) -> pysparkDataFrame:
    return df1.withColumn('id', pysparkF.monotonically_increasing_id()).join(df2.withColumn('id', pysparkF.monotonically_increasing_id()), 'id').drop('id')

if __name__ == "__main__":
    transform()