#!/usr/bin/env python3


# Import packages
import re

import nltk
import pandas as pd
import textstat
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Download nltk packages
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")

# Import scripts
import populist_data

# Working directory to save files
path_data = "../../../bld/data/"
path_bld = path_data + "df"


##########################
# Data cleaning & Pre-Processing (takes < 10 min)
##########################


def data_proc(df):
    """Preprocesses the dataset (casefold, remove stop words, tokenize, lemmatize).

    Args:
        - dataframe

    """
    # Read date
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    # Apply casefold (all lowercase and eliminate special characters)
    df["speech_clean"] = df["speech"].apply(lambda x: x.casefold())

    # Remove all special characters and numericals
    def clean(text):
        text = re.sub("[^A-Za-z]+", " ", text)
        return text

    df["speech_clean"] = df["speech_clean"].apply(clean)

    # remove stop words
    stop_words = set(stopwords.words("english"))
    stop_words.update(["would", "also", "one", "new"])
    df["speech_clean"] = df["speech_clean"].apply(
        lambda x: " ".join([word for word in x.split() if word not in (stop_words)]),
    )

    # tokenize
    df["token"] = df["speech_clean"].apply(word_tokenize)

    # lemmatize (creates two different versions, one comma-separated and the other one not)
    lemmatizer = WordNetLemmatizer()

    df["lemma_sep"] = df["token"].apply(
        lambda lst: [lemmatizer.lemmatize(word) for word in lst],
    )

    def lemmatize(data):
        lemma_rew = " "
        for word in data:
            lemma = word
            lemma_rew = lemma_rew + " " + lemma
        return lemma_rew

    df["lemma"] = df["lemma_sep"].apply(lemmatize)

    return df


##########################
##########################


def generate_variables(df):
    ### Tracking Issues over Time
    # Define a function to count occurrences of a word in a list
    def count_keywords(keywords, lst):
        count = 0
        for word in lst:
            if word in keywords:
                count += 1
        return count

    # Apply the function for different keywords
    keywords = ["growth", "economic"]
    df["growth_count"] = df["lemma_sep"].apply(lambda x: count_keywords(keywords, x))

    keywords = ["inflation", "price"]
    df["inflation_count"] = df["lemma_sep"].apply(lambda x: count_keywords(keywords, x))

    keywords = ["inequality", "distribution"]
    df["inequality_count"] = df["lemma_sep"].apply(
        lambda x: count_keywords(keywords, x),
    )

    keywords = ["environment", "climate", "green"]
    df["climate_count"] = df["lemma_sep"].apply(lambda x: count_keywords(keywords, x))

    ### Complexity Stats

    # Number of Words
    df["num_words"] = df["speech"].apply(lambda x: len(x.split()))

    # Some Readability Scores
    df["flesch_ease"] = df["speech"].apply(textstat.flesch_reading_ease)
    df["flesch_grade"] = df["speech"].apply(textstat.flesch_kincaid_grade)
    df["ari"] = df["speech"].apply(textstat.automated_readability_index)
    df["gunning_fog"] = df["speech"].apply(textstat.gunning_fog)

    ### Sentiment Analysis
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    df["sent_subj"] = df["lemma"].apply(getSubjectivity)
    df["sent_pol"] = df["lemma"].apply(getPolarity)

    return df


##########################
### Merge other data at year-country level
##########################


def merge_data(speech_df):
    speech_df["institution"] = speech_df["institution"].astype("str")
    speech_df["institution"] = speech_df["institution"].str.replace(" ", "", 1)
    speech_df["year"] = speech_df["year"].astype("int64")

    ## Get other datasets
    populists = populist_data.get_populists()
    cb_to_country = populist_data.inst_to_country()
    pop_df = pd.merge(populists, cb_to_country, on="country", how="right")
    pop_df["institution"] = pop_df["institution"].astype("str")
    pop_df["year"] = pop_df["year"].astype("int64")

    ## Merge datasets
    merged_df = pd.merge(speech_df, pop_df, on=["year", "institution"], how="inner")

    cbi_df = (
        pd.read_excel("../data/CBIData_Romelli2022.xlsx", sheet_name="CBI Indices")[
            ["year", "CBIE", "Country"]
        ]
        .rename(columns={"Country": "country"})
        .set_index(["country", "year"])
    )

    merged_df = pd.merge(
        merged_df.reset_index().set_index(["country", "year"]),
        cbi_df,
        left_index=True,
        right_index=True,
        how="left",
    ).reset_index()

    ### Save processed variables
    # Define the columns to be kep
    cols = [
        "year",
        "country",
        "lemma_sep",
        "growth_count",
        "inflation_count",
        "inequality_count",
        "climate_count",
        "num_words",
        "flesch_ease",
        "flesch_grade",
        "ari",
        "gunning_fog",
        "sent_subj",
        "sent_pol",
        "right",
        "left",
        "pop",
        "CBIE",
    ]

    # Save dataset as-is for descriptives
    merged_df = merged_df[cols]

    return merged_df


##########################
### Collapse
##########################


def collapse(df):
    cols = [
        "growth_count",
        "inflation_count",
        "inequality_count",
        "climate_count",
        "num_words",
        "flesch_ease",
        "flesch_grade",
        "ari",
        "gunning_fog",
        "sent_subj",
        "sent_pol",
        "right",
        "left",
        "pop",
    ]

    grouped_df = df.groupby(["year", "country"])[cols].mean().reset_index()

    return grouped_df
