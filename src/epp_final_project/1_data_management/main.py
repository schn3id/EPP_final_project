#!/usr/bin/env python3

# Import packages
import os

import functions
import pandas as pd

# Working directory to save files
path_data = "../../../bld/data/"
path_bld = path_data + "df"

##########################
# Data cleaning & Pre-Processing (takes < 10 min)
##########################
# Read pickled file
df = pd.read_pickle(os.path.join(path_bld, "merged_raw.pickle"))

# Run preprocessing
df_processed = functions.data_proc(df)

# Save processed dataset
df_processed.to_pickle(os.path.join(path_bld, "merged_processed.pickle"))

##########################
##########################

### Read data
df = pd.read_pickle(os.path.join(path_bld, "merged_processed.pickle"))

# Run variable generation
df_variables = functions.generate_variables(df)

# Save dataset
df_variables.to_pickle(os.path.join(path_bld, "merged_processed_vars.pickle"))

##########################
### Merge other data at year-country level
##########################

## Read data
df = pd.read_pickle(os.path.join(path_bld, "merged_processed_vars.pickle"))

## Merge data
df_merged = functions.merge_data(df)

# Save dataset
df_merged.to_pickle(os.path.join(path_bld, "merged_final_ind.pickle"))

##########################
### Collapse
##########################

## Read data
df = pd.read_pickle(os.path.join(path_bld, "merged_final_ind.pickle"))

## Collapse data
df_grouped = functions.collapse(df)

## Save dataset
df_grouped.to_pickle(os.path.join(path_bld, "merged_final_collapse.pickle"))
