# Import packages
import pandas as pd


# Create populism dataset
def get_populists():
    """This function creates a dataset at the country year level on populist leaders.

    Args:
        -

    Returns:
        dataset

    Source: Funke, Manuel, Moritz Schularick, and Christoph Trebesch. "Populist leaders and the economy." (2020).

    """
    ### create long dataset to merge with
    years = list(range(1997, 2024))
    countries = [
        "Argentina",
        "Australia",
        "Austria",
        "Belgium",
        "Bolivia",
        "Brazil",
        "Bulgaria",
        "Canada",
        "Chile",
        "China",
        "Colombia",
        "Croatia",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Ecuador",
        "Egypt",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Ireland",
        "Israel",
        "Italy",
        "Japan",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malaysia",
        "Malta",
        "Mexico",
        "Netherlands",
        "New Zealand",
        "Norway",
        "Paraguay",
        "Peru",
        "Philippines",
        "Poland",
        "Portugal",
        "Romania",
        "Russia",
        "Slovakia",
        "Slovenia",
        "South Africa",
        "South Korea",
        "Spain",
        "Sweden",
        "Switzerland",
        "Thailand",
        "Turkey",
        "United Kingdom",
        "United States",
        "Uruguay",
        "Venezuela",
        "ECB",
    ]

    df = pd.DataFrame(columns=["year", "country"])

    # loop through each year and country, and append to the dataframe
    for year in years:
        for country in countries:
            df = df.append({"year": year, "country": country}, ignore_index=True)

    ### read in populist episodes
    pop = [
        ["Argentina", "1991-1999", "Menem", "Right"],
        ["Argentina", "2003-2007", "Kirchner", "Left"],
        ["Argentina", "2007-2015", "Fernández", "Left"],
        ["Bolivia", "2006-2019", "Morales", "Left"],
        ["Brazil", "1990-1992", "Collor", "Right"],
        ["Bulgaria", "2009-2013", "Borisov", "Right"],
        ["Bulgaria", "2014-2017", "Borisov", "Right"],
        ["Bulgaria", "2017-2021", "Borisov", "Right"],
        ["Ecuador", "2007-2017", "Correa", "Left"],
        ["Greece", "1981-1989", "Papandreou", "Left"],
        ["Greece", "1993-1995", "Papandreou", "Left"],
        ["Greece", "2015-2019", "Tsipras", "Left"],
        ["Indonesia", "2014-2023", "Widodo", "Left"],
        ["Israel", "1996-1999", "Netanyahu", "Right"],
        ["Israel", "2009-2023", "Netanyahu", "Right"],
        ["Mexico", "2018-2023", "López Obrador", "Left"],
        ["Philippines", "2016-2022", "Duterte", "Right"],
        ["Poland", "2015-2023", "PiS (J. Kaczyński)(a)", "Right"],
        ["Slovakia", "2006-2010", "Fico", "Left"],
        ["Slovakia", "2012-2018", "Fico", "Left"],
        ["South Africa", "2009-2018", "Zuma", "Left"],
        ["South Korea", "2003-2008", "Roh", "Right"],
        ["Taiwan", "2000-2008", "Chen", "Right"],
        ["Thailand", "2001-2006", "Shinawatra", "Right"],
        ["Turkey", "2003-2023", "Erdoğan", "Right"],
        ["United States", "2017-2021", "Trump", "Right"],
        ["Venezuela", "2013-2023", "Maduro", "Left"],
    ]

    pop = pd.DataFrame(
        pop,
        columns=["country", "years", "leader", "political_affiliation"],
    )

    # split up the second variable into "year begin" and "year end"
    pop[["year_begin", "year_end"]] = pop["years"].str.split("-", expand=True)

    # drop the third variable
    pop = pop.drop(columns=["leader", "years"])

    # replace the fourth variable by a dummy "right" equal to 1 if the variable is "Right" and 0 if the variable is equal to "Left"
    pop["right"] = (pop["political_affiliation"] == "Right").astype(int)
    pop["left"] = (pop["political_affiliation"] == "Left").astype(int)
    pop = pop.drop(columns=["political_affiliation"])

    # bring into long format
    long_df = pd.DataFrame(columns=["country", "year", "right"])

    # Iterate over each row of the original DataFrame
    for _i, row in pop.iterrows():
        # Extract the relevant information from the row
        country = row["country"]
        year_begin = int(row["year_begin"])
        year_end = int(row["year_end"])
        right = row["right"]
        left = row["left"]

        # Iterate over each year in the range from year begin to year end
        for year in range(year_begin, year_end + 1):
            # Create a new row for this year and country
            new_row = {
                "country": country,
                "year": str(year),
                "right": right,
                "left": left,
            }

            # Add the new row to the long DataFrame
            long_df = long_df.append(new_row, ignore_index=True)

    long_df["pop"] = 1

    ### merge the empty country-year dataset and the list with populist episodes

    df = pd.merge(df, long_df, on=["year", "country"], how="outer")
    df.fillna(0, inplace=True)

    return df


### Get dataframe that maps institutions to countries
def inst_to_country():
    """Returns dataframe that maps institutions to countries."""
    dict = {
        "central bank of argentina": "Argentina",
        "reserve bank of australia": "Australia",
        "central bank of the republic of austria": "Austria",
        "national bank of belgium": "Belgium",
        "central bank of bolivia": "Bolivia",
        "central bank of brazil": "Brazil",
        "bulgarian national bank": "Bulgaria",
        "bank of canada": "Canada",
        "central bank of chile": "Chile",
        "people's bank of china": "China",
        "central bank of colombia": "Colombia",
        "croatian national bank": "Croatia",
        "central bank of cyprus": "Cyprus",
        "czech national bank": "Czech Republic",
        "national bank of denmark": "Denmark",
        "central bank of ecuador": "Ecuador",
        "central bank of egypt": "Egypt",
        "bank of estonia": "Estonia",
        "bank of finland": "Finland",
        "bank of france": "France",
        "deutsche bundesbank": "Germany",
        "bank of greece": "Greece",
        "central bank of hungary": "Hungary",
        "central bank of iceland": "Iceland",
        "reserve bank of india": "India",
        "bank indonesia": "Indonesia",
        "central bank of ireland": "Ireland",
        "bank of israel": "Israel",
        "bank of italy": "Italy",
        "bank of japan": "Japan",
        "bank of latvia": "Latvia",
        "bank of lithuania": "Lithuania",
        "central bank of luxembourg": "Luxembourg",
        "central bank of malaysia": "Malaysia",
        "central bank of malta": "Malta",
        "bank of mexico": "Mexico",
        "netherlands bank": "Netherlands",
        "reserve bank of new zealand": "New Zealand",
        "central bank of norway": "Norway",
        "central bank of paraguay": "Paraguay",
        "central reserve bank of peru": "Peru",
        "central bank of the philippines": "Philippines",
        "bank of poland": "Poland",
        "bank of portugal": "Portugal",
        "national bank of romania": "Romania",
        "bank of russia": "Russia",
        "national bank of slovakia": "Slovakia",
        "bank of slovenia": "Slovenia",
        "south african reserve bank": "South Africa",
        "bank of korea": "South Korea",
        "bank of spain": "Spain",
        "sveriges riksbank": "Sweden",
        "swiss national bank": "Switzerland",
        "bank of thailand": "Thailand",
        "central bank of the republic of turkey": "Turkey",
        "bank of england": "United Kingdom",
        "board of governors of the federal reserve system": "United States",
        "federal reserve bank of kansas city": "United States",
        "federal reserve bank of new york": "United States",
        "federal reserve bank of san francisco": "United States",
        "federal reserve bank of boston": "United States",
        "federal reserve bank of chicago": "United States",
        "federal reserve bank of dallas": "United States",
        "federal reserve bank of minneapolis": "United States",
        "federal reserve bank of philadelphia": "United States",
        "federal reserve bank of atlanta": "United States",
        "federal reserve bank of richmond": "United States",
        "central bank of uruguay": "Uruguay",
        "central bank of venezuela": "Venezuela",
        "european central bank": "ECB",
    }

    cb_country = pd.DataFrame(dict.items(), columns=["institution", "country"])

    cb_country["institution"] = cb_country["institution"].astype(str)

    return cb_country
