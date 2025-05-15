import torch
import random
import pandas as pd

dataset_name = "bhive_ithemal_dataset_v3"
dataset = torch.load(dataset_name + ".pt")

print(len(dataset))

categories_df = pd.read_csv("./bhive/benchmark/categories.csv", names=["hex_code", "category"])

category_dict = {}
for i, row in categories_df.iterrows():
    code = row["hex_code"]
    category = row["category"]
    category_dict[code] = category

# split dataset into train/test
train_size = int(len(dataset) * 0.8)
train_dataset = dataset[:train_size]
test_dataset = dataset[train_size:]

# randomly upsample train data from categories 'Vec' and 'Scalar/Vec'
# no data from the original train set should be left out
# i.e. there will be all the original data and some duplicates

vec_code_ids = []
scalar_vec_code_ids = []
original_data = []
data_to_upsample = []
for i, data in enumerate(train_dataset):
    code_id = data[0]
    
    if code_id != '':
        category = category_dict[code_id]            

        if category == "Vec" or category == "Scalar/Vec":
            # print(f"Code ID: {code_id}, Category: {category}")
            data_to_upsample.append(data)

            if category == "Vec":
                vec_code_ids.append(code_id)
                if code_id not in list(categories_df["hex_code"]):
                    print(f"Code ID {code_id} not found in categories.csv")
            elif category == "Scalar/Vec":
                scalar_vec_code_ids.append(code_id)
    
    original_data.append(data)

print(f"Number of Vec code IDs: {len(vec_code_ids)}")
print("Number of unique Vec code IDs:", len(set(vec_code_ids)))
print(f"Number of Scalar/Vec code IDs: {len(scalar_vec_code_ids)}")
print("Number of unique Scalar/Vec code IDs:", len(set(scalar_vec_code_ids)))

print(f"Number of samples to upsample: {len(data_to_upsample)}")
# Get indices of samples to duplicate
# indices_to_add = random.choices(range(len(data_to_upsample)), k=len(data_to_upsample))
# samples_to_add = [data_to_upsample[i] for i in indices_to_add]

samples_to_add = data_to_upsample * 3
print(f"Number of samples added: {len(samples_to_add) - len(data_to_upsample)}")

upsampled_dataset = original_data + samples_to_add
print(f"Upsampled train dataset size: {len(upsampled_dataset)}")

new_dataset = upsampled_dataset + test_dataset
print(len(new_dataset))

# save new dataset
torch.save(new_dataset, dataset_name + "_upsampled.pt")
