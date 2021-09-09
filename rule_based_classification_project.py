# Importing Libraries

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

# Importing Data

df = pd.read_csv("datasets/persona.csv")

# Data Understanding

df.shape  # Dimension of dataframe

df.dtypes  # Data type of each variable

df.info  # Print a concise summary of a DataFrame

df.head()  # First 5 observations of dataframe

df.tail()  # Last 5 observations of dataframe

df.isnull().sum()  # Get number of Null values in a dataframe

# Data Manipulation

# Nununiqe values of SOURCE and PRICE
df["SOURCE"].nunique()
df["PRICE"].nunique()

# Let's apply aggregation operations according to COUNTRY and SOURCE

df.groupby("COUNTRY").agg({"PRICE": "sum"})

df.groupby("SOURCE").agg({"PRICE": "count"})

df.groupby("COUNTRY").agg({"PRICE": "mean"})

df.groupby("SOURCE").agg({"PRICE": "mean"})

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

# Average of PRİCE by COUNTRY, SOURCE, SEX, AGE
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})

# The average PRİCE found in the previous step is assigned to agg_df, sorted from high to low.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)

agg_df.reset_index(inplace=True)  # We need to define the names that occur in the index as variables.

# A new categorical variable was created for AGES with similar characteristics due to the fact that there were too many breaks in the AGE variable
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins=[0, 18, 23, 30, 40, agg_df["AGE"].max()], labels=["0_18", "19_23", "24_30", "31_40", "41_" + str(agg_df["AGE"].max())])

# Add a new variable to the dataframe
agg_df["customers_level_based"] = [str(row[0]).upper() + "_" + str(row[1]).upper() + "_" + str(row[2]).upper() + "_" + str(row[5]).upper()for row in agg_df.values]

# Choose the variables we will use to create level-based customers
agg_df = agg_df[["customers_level_based", "PRICE"]]


# There will be many similar, we need to deduplicate the same segments by selecting them.
agg_df["customers_level_based"].value_counts()
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df = agg_df.reset_index()  # We need to define the names that occur in the index as variables.

agg_df["customers_level_based"].value_counts()  # After the operation, there is one from each segment

# The level-based customers created were divided into 4 segments, from high to low, according to PRİCE.
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "min", "max", "sum"]})

# Prediction
# A 25 years old male from Turkey who is an IOS user It is desired to determine how much the user can earn on average.

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]









