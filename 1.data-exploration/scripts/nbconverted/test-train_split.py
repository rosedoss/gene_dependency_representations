#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pathlib
import numpy as np
import pandas as pd
sys.path.insert(0, "../0.data-download/scripts/")
from data_loader import load_data
from sklearn.model_selection import train_test_split


# In[2]:


# load all of the data 
data_directory = "../0.data-download/data/"
dfs = load_data(data_directory, adult_or_pediatric = "all")
dependency_df = dfs[1]
sample_df = dfs[0]


# In[3]:


# assign age_categories and sex columns to the dependency dataframe as a single column
presplit_dependency_df = dependency_df.assign(age_and_sex = sample_df.age_categories.astype(str) + "_" + sample_df.sex.astype(str))
presplit_dependency_df


# In[4]:


groups = sample_df.groupby("age_categories")
df_list = []
for name, df in groups:
    
    # only looking for samples that contain Adult or Pediatric information
    if name == "Adult" or name == "Pediatric":
        df_list.append(df)
        
# merge dataframes through concatentation 
new_df = pd.concat(df_list, axis=0)
new_df.reset_index(drop=True)


# In[5]:


# creating a sample data frame that onl contains the desired information of sex and age category
ref_df = new_df[["DepMap_ID", "sex", "age_categories"]]
ref_df.reset_index(drop=True)
ref_df = ref_df.set_index("DepMap_ID")
ref_df = ref_df.sort_index(ascending=True)
ref_df = ref_df.reset_index()


# In[6]:


# searching for similar IDs FROM the PEDIATRIC-samples IN the gene_dependency df
PA_dependency_IDs = ref_df["DepMap_ID"].tolist()

PA_IDs = set(PA_dependency_IDs) & set(presplit_dependency_df["DepMap_ID"].tolist())

# creating a new gene dependency data frame containing only PEDIATRIC samples
PA_dependency_df = presplit_dependency_df.loc[presplit_dependency_df["DepMap_ID"].isin(PA_IDs)].reset_index(drop=True)


# In[7]:


#split the data based on age category and sex
train_df, test_df = train_test_split(
    PA_dependency_df, 
    test_size = .15, 
    stratify= PA_dependency_df.age_and_sex
)


# In[8]:


# save the TESTING dataframe 
test_df = test_df.reset_index(drop=True)
testing_df_output = pathlib.Path("../0.data-download/data/VAE_test_df.csv")
test_df.to_csv(testing_df_output)
test_df


# In[9]:


# save the TRAINING dataframe 
train_df = train_df.reset_index(drop=True)
training_df_output = pathlib.Path("../0.data-download/data/VAE_train_df.csv")
train_df.to_csv(training_df_output)
train_df

