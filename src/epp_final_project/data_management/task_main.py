#!/usr/bin/env python3

from epp_final_project.config import BLD
from epp_final_project.config import SRC

# Import packages
import os
import pytask

# Import scripts
import epp_final_project.data_management.functions as f

# Import packages
import os
import pandas as pd



##########################.
# Data cleaning & Pre-Processing (takes < 10 min)
##########################

@pytask.mark.depends_on(BLD / "data" / "raw" /"merged_raw.pickle")
@pytask.mark.produces(BLD / "data" / "raw" /"merged_processed.pickle") 
def task_cleaning(depends_on, produces):
    df = pd.read_pickle(depends_on)
    df_processed = f.data_proc(df)
    df_processed.to_pickle(produces)


##########################
# Generate variables
##########################

@pytask.mark.depends_on(BLD / "data" / "raw" /"merged_processed.pickle")
@pytask.mark.produces(BLD / "data" / "raw" /"merged_processed_vars.pickle") 
def task_generate_variables(depends_on, produces):
    df = pd.read_pickle(depends_on)
    df_variables = f.generate_variables(df)
    df_variables.to_pickle(produces)


##########################
### Merge other data at year-country level
##########################

@pytask.mark.depends_on(
    {
        "path_speech": BLD / "data" / "raw" /"merged_processed_vars.pickle",
        "path_cbi": SRC /  "data" /"CBIData_Romelli2022.xlsx"
    }
)
@pytask.mark.produces(BLD / "data" / "merged_final_ind.pickle") 
def task_merge_data(depends_on, produces):
    df = pd.read_pickle(depends_on["path_speech"])
    df_merged = f.merge_data(df, depends_on["path_cbi"])
    df_merged.to_pickle(produces)


##########################
### Collapse
##########################

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "data" / "merged_final_collapse.pickle") 
def task_collapse(depends_on, produces):
    df = pd.read_pickle(depends_on)
    df_grouped = f.collapse(df)
    df_grouped.to_pickle(produces)