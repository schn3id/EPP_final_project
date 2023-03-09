#!/usr/bin/env python3


# Import packages
# Import packages
import os

import epp_final_project.analysis.functions as f
import pandas as pd
import pytask
from epp_final_project.config import BLD

# Working directory to save files

# creating directories


@pytask.mark.produces({"path_plots": BLD / "plots", "path_tables": BLD / "tables"})
def task_create_folders(produces):
    if not os.path.exists(produces["path_data"]):
        os.makedirs(produces["path_data"])
    if not os.path.exists(produces["path_scrape"]):
        os.makedirs(produces["path_scrape"])


# load the data


# make plots and tables
@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "wordcloud.png")
def task_make_frequency_plot(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_frequency_plot(df).savefig(produces)


f.make_historical_plots(df).savefig(os.path.join(path_plots, "historical_plots.png"))


f.make_crosssectional_plots(df).savefig(
    os.path.join(path_plots, "crosssectional_plots.png"),
)


f.make_politics_plots(df).savefig(os.path.join(path_plots, "politics_plots.png"))


f.make_cbi_pol_plot(df).savefig(os.path.join(path_plots, "politics_cbi_plot.png"))

f.make_cbi_speech_plot(df).savefig(os.path.join(path_plots, "cbi_speech_plot.png"))

f.run_regressions(df, path_tables)

f.make_topic_analysis_plots(df, path_plots)
