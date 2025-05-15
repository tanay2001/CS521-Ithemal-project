import numpy as np
import pandas as pd

# Read categories.csv to get hex_code, category
categories_df = pd.read_csv("./bhive/benchmark/categories.csv", names=["hex_code", "category"])

# read hex_code_errors.csv to get hex_code, error
throughput_df = pd.read_csv("./hsw_validation_results.txt", 
                            names = ["hex_code", "predicted_throughput", "actual_throughput"]
                            )

throughput_df["error"] = (abs(throughput_df["predicted_throughput"] - throughput_df["actual_throughput"]))/throughput_df["actual_throughput"]

# Merge the two dataframes on hex_code
# merged_df = pd.merge(categories_df, throughput_df, on="hex_code", how="inner")
merged_df = pd.merge(throughput_df, categories_df, on="hex_code", how="inner")
print(merged_df.head())

# create a dict mapping category to avg error per category
category_errors = merged_df.groupby("category")["error"].mean().to_dict()
# create a dict mapping category to std error per category
category_errors_std = merged_df.groupby("category")["error"].std().to_dict()
# create a dict mapping category to count of errors per category
category_errors_count = merged_df.groupby("category")["error"].count().to_dict()

# print all category-wise errors in a well-formatted way
print(f"{'Category':<20} {'Avg Error':<20} {'Std Error':<20} {'Count':<20}")
for category, error in category_errors.items():
    std_error = category_errors_std[category]
    count = category_errors_count[category]
    print(f"{category:<20} {error:<20} {std_error:<20} {count:<20}")

# Save all category-wise errors in a csv file
category_errors_df = pd.DataFrame.from_dict(category_errors, orient="index", columns=["Avg Error"])
category_errors_std_df = pd.DataFrame.from_dict(category_errors_std, orient="index", columns=["Std Error"])
category_errors_count_df = pd.DataFrame.from_dict(category_errors_count, orient="index", columns=["Count"])
category_errors_df = category_errors_df.join(category_errors_std_df)
category_errors_df = category_errors_df.join(category_errors_count_df)
category_errors_df.to_csv("hsw_category_errors.csv")