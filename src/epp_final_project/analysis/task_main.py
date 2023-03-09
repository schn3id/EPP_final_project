#!/usr/bin/env python3

from epp_final_project.config import BLD
from epp_final_project.config import SRC

# Import packages
import os

import epp_final_project.analysis.functions as f
import pandas as pd
import pytask
from epp_final_project.config import BLD

##########################
# Generate directories for plots and tables if not existing
##########################

@pytask.mark.produces({"path_plots": BLD / "plots", "path_tables": BLD / "tables"})
def task_create_folders(produces):
    if not os.path.exists(produces["path_plots"]):
        os.makedirs(produces["path_plots"])
    if not os.path.exists(produces["path_tables"]):
        os.makedirs(produces["path_tables"])

##########################
# Generate plot of most frequent words
##########################

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "wordcloud.png")
def task_make_frequencyplot(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_frequencyplot(df).savefig(produces)

##########################
# Plot evolution of some topics over time
##########################

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "historical_plots.png")
def task_make_historical_plots(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_historical_plots(df).savefig(produces)

##########################
# Plot frequency of some topics across countries
##########################

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "crosssectional_plots.png")
def task_make_crosssectional_plots(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_crosssectional_plots(df).savefig(produces)

##########################
# Plot by populism indicator
##########################

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "politics_plots.png")
def task_make_politics_plots(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_politics_plots(df).savefig(produces)

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "politics_cbi_plot.png")
def task_make_cbi_pol_plot(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_cbi_pol_plot(df).savefig(produces)


@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "cbi_speech_plot.png")
def task_make_cbi_speech_plot(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_cbi_speech_plot(df).savefig(produces)

##########################
# Output regression tables
##########################

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces( BLD / "tables" / "table_1.tex")
def task_run_regressions_part1(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.run_regressions_1(df, produces)

@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces( BLD / "tables" / "table_2.tex")
def task_run_regressions_part2(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.run_regressions_2(df, produces)

