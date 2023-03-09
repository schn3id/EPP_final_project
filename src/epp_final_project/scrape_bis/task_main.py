#!/usr/bin/env python3

from epp_final_project.config import BLD
from epp_final_project.config import SRC

# Import packages
import os
import pytask

# Import scripts
import epp_final_project.scrape_bis.bis_scraper as f

##########################
# Call BIS scraper 
##########################
@pytask.mark.produces(
    {
        "path_data": BLD / "data",
        "path_scrape": BLD / "data" / "raw" /"pdf"
    }
)
def task_bis_scraper(produces):
    if not os.path.exists(produces["path_data"]):
        os.makedirs(produces["path_data"])
    if not os.path.exists(produces["path_scrape"]):
        os.makedirs(produces["path_scrape"])
    f.bis_scraper(produces["path_scrape"])


##########################
# Call function that transforms pdf's into txts 
##########################

@pytask.mark.depends_on(BLD / "data" / "raw" /"pdf") 
@pytask.mark.produces(BLD / "data" / "raw"/"txt") 
def task_pdf_to_txt(depends_on, produces):
    if not os.path.exists(produces):
        os.makedirs(produces)
    f.pdf_to_txt(depends_on, produces)

##########################
# Call function that combines the dataset and pickle
##########################

@pytask.mark.depends_on(
    {
        "path_txt": BLD / "data" / "raw"/"txt",
        "path_meta": BLD / "data" / "raw" /"pdf"
    }
)
@pytask.mark.produces(BLD / "data" / "raw" /"merged_raw.pickle") 
def task_construct_dataset(depends_on, produces):
    combined = f.construct_dataset(depends_on["path_txt"], depends_on["path_meta"])
    combined.to_pickle(produces)