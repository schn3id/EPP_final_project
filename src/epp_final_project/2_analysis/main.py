#!/usr/bin/env python3
"""
Outcomes already included:
    1. Frequencies of lemmas & occurrences of some topics
    2. Complexity
    3. Sentiment Analysis
Possible Other Outcomes:
    1. Ngrams
    2. Variables from Topic Modelling.

Q: Does Cb Communication change during populist governments?

Analysis:
    - Descriptives
    - reg outcome ~ political variable

"""

# Import packages
import os

import functions as f
import pandas as pd

# Working directory to save files
path_data = "../../../bld/data/"
path_df = path_data + "df"
path_plots = "../../../bld/plots"
path_tables = "../../../bld/tables"

# creating directories


f.make_folders([path_plots, path_tables])


# load the data

df = pd.read_pickle(os.path.join(path_df, "merged_final_ind.pickle"))


##########################
##########################
# Analysis
##########################
##########################

##########################
### Graphical Analysis
##########################

# Wordcloud

f.make_wordcloud(df).savefig(os.path.join(path_plots, "wordcloud.png"))

# historical development

f.make_historical_plots(df).savefig(os.path.join(path_plots, "historical_plots.png"))


# crosssectional plots
f.make_crosssectional_plots(df).savefig(
    os.path.join(path_plots, "crosssectional_plots.png"),
)


# crosssectional plots
f.make_politics_plots(df).savefig(os.path.join(path_plots, "politics_plots.png"))


f.make_cbi_pol_plot(df).savefig(os.path.join(path_plots, "politics_cbi_plot.png"))

f.make_cbi_speech_plot(df).savefig(os.path.join(path_plots, "cbi_speech_plot.png"))

f.run_regressions(df, path_tables)
