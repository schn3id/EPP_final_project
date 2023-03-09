import os

import gensim
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from gensim import corpora  # Create Dictionary
from nltk.corpus import stopwords
from stargazer.stargazer import Stargazer
from wordcloud import WordCloud


def _make_folders(paths):
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)


def make_wordcloud(data, n=200):
    """Creates wordcloud plot from a random sample of documents to limit runtime.

    Parameters:
            data: the dataframe
            n: sample size

    Returns:
            a figure object

    """
    # combine words from n speeches, if we use all it would take forever
    text = " ".join(str(x) for x in data["lemma_sep"].sample(n=n, random_state=1))

    # make wordcloud plot
    wordcloud = WordCloud(background_color="white", height=3000, width=3000).generate(
        text,
    )

    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

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


def run_regressions(data, path_tables):
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
    with open(os.path.join(path_tables, "regressions_part1.tex"), "w") as f:
        f.write(stargazer.render_latex())

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
    with open(os.path.join(path_tables, "regressions_part2.tex"), "w") as f:
        f.write(stargazer.render_latex())


def make_topic_analysis_plots(data, figpath):
    """Fits topic analysis model and creates plots with wordclouds per topic.

    Parameters:
            data: the dataframe with a column lemma_sep
            figpath: a path where figures are saved

    Returns:
            none (saves figure as side effect)

    """
    sample = data["lemma_sep"].to_list()

    id2word = corpora.Dictionary(sample)  # Create Corpus
    texts = sample  # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]  # View

    num_topics = 4  # Build LDA model

    lda_model = gensim.models.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=num_topics,
    )

    cols = [
        color for name, color in mcolors.TABLEAU_COLORS.items()
    ]  # more colors: 'mcolors.XKCD_COLORS'

    stop_words = stopwords.words("english")
    cloud = WordCloud(
        stopwords=stop_words,
        background_color="white",
        width=2500,
        height=1800,
        max_words=10,
        colormap="tab10",
        color_func=lambda *args, **kwargs: cols[i],
        prefer_horizontal=1.0,
    )

    topics = lda_model.show_topics(formatted=False)

    fig, axes = plt.subplots(2, 2, figsize=(8, 8), sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title("Topic " + str(i), fontdict={"size": 16})
        plt.gca().axis("off")

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.tight_layout()
    plt.show()
    fig.savefig(os.path.join(figpath, "topic_wordclouds.png"))
