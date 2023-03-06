#!/usr/bin/env python3

# Import packages
import os

import bis_scraper

# Import scripts
import lists

# Working directory to save files
path_data = "../../../bld/data/"
path_scrape = path_data + "raw"
path_df = path_data + "df"

# Create directories if doesn't exist
if not os.path.exists(path_data):
    os.makedirs(path_data)

if not os.path.exists(path_scrape):
    os.makedirs(path_scrape)

if not os.path.exists(path_df):
    os.makedirs(path_df)

# Create datelist
date_list = lists.date_list()

# Create list of institutions.
institutions = lists.institutions

# Call BIS scraper

# Call function that transforms pdf's into txts

# Call function that combines the dataset and pickle
combined = bis_scraper.construct_dataset(path_scrape)

combined.to_pickle(os.path.join(path_df, "merged_raw.pickle"))
