#!/usr/bin/env python3


# Import packages
# Import packages
import os

import epp_final_project.analysis.functions as f
import pandas as pd
import pytask
from epp_final_project.config import BLD

# creating directories


@pytask.mark.produces({"path_plots": BLD / "plots", "path_tables": BLD / "tables"})
def task_create_folders(produces):
    if not os.path.exists(produces["path_plots"]):
        os.makedirs(produces["path_plots"])
    if not os.path.exists(produces["path_tables"]):
        os.makedirs(produces["path_tables"])


# load the data


# make plots and tables
@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "wordcloud.png")
def task_make_frequencyplot(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_frequencyplot(df).savefig(produces)


@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "historical_plots.png")
def task_make_historical_plots(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_historical_plots(df).savefig(produces)


@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(BLD / "plots" / "crosssectional_plots.png")
def task_make_crosssectional_plots(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.make_crosssectional_plots(df).savefig(produces)


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


@pytask.mark.depends_on(BLD / "data" / "merged_final_ind.pickle")
@pytask.mark.produces(
    {
        "table_1": BLD / "tables" / "table_1.tex",
        "table_2 ": BLD / "tables" / "table_2.tex",
    },
)
def task_run_regressions(depends_on, produces):
    df = pd.read_pickle(depends_on)
    f.run_regressions(df, produces["table_1"], produces["table_2"])
