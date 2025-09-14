import requests
import pandas as pd
import os

# Call the API
url = "https://disease.sh/v3/covid-19/countries"
response = requests.get(url)
data = response.json()

# Convert all data (no filtering)
df = spark.createDataFrame(pd.DataFrame(data))

# Rename columns
df = df.withColumnRenamed('country', 'Country') \
       .withColumnRenamed('cases', 'TotalCases') \
       .withColumnRenamed('todayCases', 'TodayCases') \
       .withColumnRenamed('deaths', 'TotalDeaths') \
       .withColumnRenamed('todayDeaths', 'TodayDeaths') \
       .withColumnRenamed('recovered', 'Recovered') \
       .withColumnRenamed('active', 'Active') \
       .withColumnRenamed('critical', 'Critical') \
       .withColumnRenamed('tests', 'TotalTests') \
       .withColumnRenamed('population', 'Population') \
       .withColumnRenamed('continent', 'Continent')

# Set up Azure storage access
storagename = os.environ['MY_STORAGE']
my_key = os.environ['MY_KEY']
spark.conf.set(
    f"fs.azure.account.key.{storagename}.blob.core.windows.net",
    my_key
)

# Save as Parquet in Azure Blob
df.write.mode("overwrite").parquet(
    f"wasbs://{'coviddata'}@{storagename}.blob.core.windows.net/raw/covid"
)

print(" Data for All countries saved successfully.")