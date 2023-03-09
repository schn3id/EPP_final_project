import os
from collections import Counter

import gensim
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from gensim import corpora  # Create Dictionary
from nltk.corpus import stopwords
from stargazer.stargazer import Stargazer


def make_frequencyplot(data, n=200):
    """Creates frequency plot from a random sample of documents to limit runtime.

    Parameters:
            data: the dataframe
            n: sample size

    Returns:
            a figure object

    """
    frequency_distribution = Counter(
        item for sublist in data["lemma_sep"] for item in sublist
    )
    most_common = frequency_distribution.most_common(20)

    fig = plt.figure()
    plt.barh(range(len(most_common)), [val[1] for val in most_common], align="center")
    plt.yticks(range(len(most_common)), [val[0] for val in most_common])
    return fig


def _make_labels_dict():
    """Creates a dict of labels for column names.

    Returns:
            a dict

    """
    clean_labels = [
        "Growth References",
        "Inflation References",
        "Inequality References",
        "Climate References",
        "Number of Words",
        "Flesch Reading Ease Index",
        "Automated Readability Index",
        "Gunning Fog Index",
        "Subjectivity Sentiments",
        "Polarization Sentiments",
    ]

    labels = [
        "growth_count",
        "inflation_count",
        "inequality_count",
        "climate_count",
        "num_words",
        "flesch_ease",
        "ari",
        "gunning_fog",
        "sent_subj",
        "sent_pol",
    ]

    return dict(zip(labels, clean_labels))


def make_historical_plots(data):
    """Creates plots over time of the main text attributes.

    Parameters:
            data: the dataframe

    Returns:
            a figure object

    """
    plot_data = (
        data[
            [
                "year",
                "growth_count",
                "inflation_count",
                "inequality_count",
                "climate_count",
                "num_words",
                "flesch_ease",
                "ari",
                "gunning_fog",
                "sent_subj",
                "sent_pol",
            ]
        ]
        .groupby("year")
        .agg("mean")
    )

    fig, ax = plt.subplots(5, 2, figsize=(8, 8))
    ax = ax.flatten()

    for i, measure in enumerate(plot_data.columns):
        ax[i].set_title(_make_labels_dict()[measure])
        ax[i].plot(plot_data.index, plot_data[measure])

    fig.tight_layout()
    return fig


def make_crosssectional_plots(data):
    """Creates plots over across countries/institutions of the main text attributes.

    Parameters:
            data: the dataframe

    Returns:
            a figure object

    """
    plot_data = (
        data[
            [
                "country",
                "growth_count",
                "inflation_count",
                "inequality_count",
                "climate_count",
                "num_words",
                "flesch_ease",
                "ari",
                "gunning_fog",
                "sent_subj",
                "sent_pol",
            ]
        ]
        .loc[
            data["country"].isin(
                [
                    "United States",
                    "Germany",
                    "ECB",
                    "China",
                    "United Kingdom",
                    "Japan",
                    "France",
                ],
            )
        ]
        .groupby("country")
        .agg("mean")
    )
    fig, ax = plt.subplots(5, 2, figsize=(8, 16))
    ax = ax.flatten()

    for i, measure in enumerate(plot_data.columns):
        plot_data = plot_data.sort_values(by=measure)
        ax[i].bar(plot_data.reset_index()["country"], plot_data[measure], width=0.3)
        ax[i].set_xticklabels(
            plot_data.reset_index()["country"],
            rotation=60,
            ha="right",
            rotation_mode="anchor",
        )
        ax[i].set_title(_make_labels_dict()[measure])

    fig.tight_layout()
    return fig


def make_politics_plots(data):
    """Creates plots across populist type governments of the main text attributes.

    Parameters:
            data: the dataframe

    Returns:
            a figure object

    """
    plot_data = (
        data[
            [
                "left",
                "right",
                "country",
                "growth_count",
                "inflation_count",
                "inequality_count",
                "climate_count",
                "num_words",
                "flesch_ease",
                "ari",
                "gunning_fog",
                "sent_subj",
                "sent_pol",
            ]
        ]
        .assign(
            pop=np.where(
                data["left"] == 1,
                "Populist Left",
                np.where(data["right"] == 1, "Populist Right", "Not Populist"),
            ),
        )
        .loc[~data["country"].isin(["ECB"])]
        .drop(["country", "left", "right"], axis=1)
        .groupby("pop")
        .agg("mean")
    )

    fig, ax = plt.subplots(5, 2, figsize=(6, 12))
    ax = ax.flatten()

    for i, measure in enumerate(plot_data.columns):
        ax[i].bar(plot_data.index, plot_data[measure], width=0.3)
        ax[i].set_xticklabels(
            plot_data.index,
            rotation=60,
            ha="right",
            rotation_mode="anchor",
        )
        ax[i].set_title(_make_labels_dict()[measure])

    fig.tight_layout()
    return fig


def make_cbi_pol_plot(data):
    """Creates plot of CB independence by populist government type.

    Parameters:
            data: the dataframe

    Returns:
            a figure object

    """
    plot_data = (
        data[["CBIE", "left", "right"]]
        .assign(
            populist=np.where(
                data["left"] == 1,
                "Populist Left",
                np.where(data["right"] == 1, "Populist Right", "Not Populist"),
            ),
        )[["populist", "CBIE"]]
        .groupby("populist")
        .agg("mean")
    )

    fig = plt.figure()
    plt.bar(plot_data.reset_index()["populist"], plot_data["CBIE"], width=0.3)

    return fig


def make_cbi_speech_plot(data):
    """Creates plots across CB dependence status of the main text attributes.

    Parameters:
            data: the dataframe

    Returns:
            a figure object

    """
    plot_data = data.reset_index()[
        [
            "left",
            "right",
            "country",
            "growth_count",
            "inflation_count",
            "inequality_count",
            "climate_count",
            "num_words",
            "flesch_ease",
            "ari",
            "gunning_fog",
            "sent_subj",
            "sent_pol",
        ]
    ]
    plot_data["cbi_bin"] = np.where(data["CBIE"] >= 0.4, 1, 0)
    plot_data = (
        plot_data.loc[~data.reset_index()["country"].isin(["ECB"])]
        .drop(["left", "right"], axis=1)
        .groupby("cbi_bin")
        .agg("mean")
    )

    plot_data.index = plot_data.index.map({0: "Dep. CB", 1: "Indep. CB"})

    fig, ax = plt.subplots(5, 2, figsize=(6, 12))
    ax = ax.flatten()

    for i, measure in enumerate(plot_data.columns):
        ax[i].bar(plot_data.index, plot_data[measure])
        ax[i].set_xticklabels(
            plot_data.index,
            rotation=60,
            ha="right",
            rotation_mode="anchor",
        )
        ax[i].set_title(_make_labels_dict()[measure])

    fig.tight_layout()
    return fig


def run_regressions_1(data, table_1):
    """Creates tables for speech attribute on politics and CB dependence regressions.

    Parameters:
            data: the dataframe
            path_tables: the path where tables are stored

    Returns:
            none (saves 2 tex files as side effect)

    """
    data_cl = data.reset_index().dropna()

    model_growth_count = sm.OLS.from_formula(
        "growth_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_inflation_count = sm.OLS.from_formula(
        "inflation_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_inequality_count = sm.OLS.from_formula(
        "inequality_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_climate_count = sm.OLS.from_formula(
        "climate_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_num_words = sm.OLS.from_formula(
        "num_words ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_flesch_ease = sm.OLS.from_formula(
        "flesch_ease ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    sm.OLS.from_formula(
        "flesch_grade ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_ari = sm.OLS.from_formula("ari ~  CBIE*left + CBIE*right", data=data_cl).fit(
        cov_type="cluster",
        cov_kwds={"groups": data_cl["country"]},
    )
    model_gunning_fog = sm.OLS.from_formula(
        "gunning_fog ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_sent_subj = sm.OLS.from_formula(
        "sent_subj ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_sent_pol = sm.OLS.from_formula(
        "sent_pol ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})

    stargazer = Stargazer(
        [
            model_growth_count,
            model_inflation_count,
            model_climate_count,
            model_inequality_count,
        ],
    )

    stargazer.title("Political Determinants of CB Topics")
    stargazer.covariate_order(
        ["CBIE", "left", "CBIE:left", "right", "CBIE:right", "Intercept"],
    )
    stargazer.dependent_variable_name("Dependent variables:")
    stargazer.custom_columns(
        ["Growth Count", "Inflation Count", "Climate Count", "Inequality Count"],
        [
            len(stargazer.models) // 4,
            len(stargazer.models) // 4,
            len(stargazer.models) // 4,
            len(stargazer.models) // 4,
        ],
    )
    with open(table_1, "w") as f:
        f.write(stargazer.render_latex())

def run_regressions_2(data, table_2):
    """Creates tables for speech attribute on politics and CB dependence regressions.

    Parameters:
            data: the dataframe
            path_tables: the path where tables are stored

    Returns:
            none (saves 2 tex files as side effect)

    """
    data_cl = data.reset_index().dropna()

    model_growth_count = sm.OLS.from_formula(
        "growth_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_inflation_count = sm.OLS.from_formula(
        "inflation_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_inequality_count = sm.OLS.from_formula(
        "inequality_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_climate_count = sm.OLS.from_formula(
        "climate_count ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_num_words = sm.OLS.from_formula(
        "num_words ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_flesch_ease = sm.OLS.from_formula(
        "flesch_ease ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    sm.OLS.from_formula(
        "flesch_grade ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_ari = sm.OLS.from_formula("ari ~  CBIE*left + CBIE*right", data=data_cl).fit(
        cov_type="cluster",
        cov_kwds={"groups": data_cl["country"]},
    )
    model_gunning_fog = sm.OLS.from_formula(
        "gunning_fog ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_sent_subj = sm.OLS.from_formula(
        "sent_subj ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})
    model_sent_pol = sm.OLS.from_formula(
        "sent_pol ~  CBIE*left + CBIE*right",
        data=data_cl,
    ).fit(cov_type="cluster", cov_kwds={"groups": data_cl["country"]})



    stargazer = Stargazer(
        [
            model_num_words,
            model_flesch_ease,
            model_ari,
            model_gunning_fog,
            model_sent_subj,
            model_sent_pol,
        ],
    )

    stargazer.title("Political Determinants of CB Communication Style")
    stargazer.covariate_order(
        ["CBIE", "left", "CBIE:left", "right", "CBIE:right", "Intercept"],
    )
    stargazer.dependent_variable_name("Dependent variables:")
    stargazer.custom_columns(
        list(_make_labels_dict())[4:],
        [
            len(stargazer.models) // 6,
            len(stargazer.models) // 6,
            len(stargazer.models) // 6,
            len(stargazer.models) // 6,
            len(stargazer.models) // 6,
            len(stargazer.models) // 6,
        ],
    )
    with open(table_2, "w") as f:
        f.write(stargazer.render_latex())

