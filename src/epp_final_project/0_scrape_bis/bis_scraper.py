# Import packages
import datetime as dt
import glob
import os
import string

# Import lists
import lists
import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup as bs

### Function for scraping the data


def bis_scraper(wd, institutions, date_list):
    """Scrapes all available speeches on the BIS homepage.

    Args:
        wd: string
        institutions: list of strings
        date_list: list of dates in format 210101

    Output:
        File with Metadata
        pdf's with speeches

    """
    # Create list of the alphabet
    letters = list(string.ascii_lowercase)

    # Define url from where to get text data
    url = "https://www.bis.org/review/r"
    end_pdf = ".pdf"
    end_htm = ".htm"

    for date in date_list:
        for inc in letters:

            response = requests.get(url + date + inc + end_htm)

            # Check if file already exists
            file_path_check = os.path.join(wd, date + inc + ".pdf.txt")

            if not os.path.exists(file_path_check):

                if response.status_code == 200:
                    try:
                        # Creating a Beautiful Soup object with appropriate parser.
                        soup = bs(response.content, "html.parser")

                        # Retrieve author data
                        try:
                            meta_name = soup.find_all(
                                "a",
                                {"class": "authorlnk dashed"},
                            )
                            meta_name = meta_name[0].text
                        except:
                            meta_name = "NA"

                        # Retrieve meta data
                        extratitle = soup.find(id="extratitle-div")

                        # Create a string with meta data
                        meta = extratitle.text
                        meta = meta.strip()  # remove white space

                        # Match institution with meta data
                        inst = []
                        for item in institutions:
                            if item.lower() in meta.lower():  # case insensitive
                                inst.append(item.lower())  # append all matching inst.

                        # If one institution was in the list proceed further
                        if len(inst) == 1:
                            inst = inst[0]

                        # If multiple institutions were in the extra title, choose
                        # the one that comes first in the meta information
                        elif len(inst) > 1:
                            index_list = []
                            for i in inst:
                                index_list.append(meta.lower().find(i))
                            min_value = min(index_list)
                            inst = inst[index_list.index(min_value)]

                        # Correct some institution names, because they are written
                        # wrong on the BIS website for some (all lower case here)
                        # us
                        if inst in lists.inst_us:
                            inst = lists.inst_us[0]
                        # norway
                        if inst == "norges bank":
                            inst = "central bank of norway"
                        # france
                        if inst == "banque de france":
                            inst = "bank of france"
                        # sweden
                        if inst in lists.inst_swe:
                            inst = "sveriges riksbank"
                        # netherlands
                        if inst == "nederlandsche bank":
                            inst = "netherlands bank"
                        # austria
                        if inst in lists.inst_austria:
                            inst = "central bank of the republic of austria"
                        # south africa
                        if inst == "bank of south africa":
                            inst = "south african reserve bank"
                        # hong kong
                        if inst == "hong kong monetary":
                            inst = "hong kong monetary authority"
                        # india
                        if inst == "bank of india":
                            inst = "reserve bank of india"
                        # macedonia
                        if (
                            inst == "national bank of the republic of macedonia"
                            or inst
                            == "national bank of the republic of north macedonia"
                        ):
                            inst = "national bank of north macedonia"
                        # european cental bank
                        if inst == "ecb":
                            inst = "european central bank"
                        # ireland
                        if inst == "authority of ireland":
                            inst = "central bank of ireland"
                        # turkey
                        if inst == "bank of turkey":
                            inst = "central bank of the republic of turkey"
                        # china
                        if inst == "bank of china":
                            inst = "people's bank of china"
                        # australia
                        if (
                            inst == "australian reserve bank"
                            or inst == "bank of australia"
                        ):
                            inst = "reserve bank of australia"

                        # Create string for outputting meta data
                        file_meta = os.path.join(wd, "meta_data.txt")

                        # Create Date Time format
                        date_hr = dt.datetime.strptime(
                            date,
                            "%y%m%d",
                        )  # datetime object
                        date_hr = dt.datetime.strftime(
                            date_hr,
                            "%Y-%m-%d",
                        )  # convert to "%Y-%m-%d"

                        # use "a" instead of "w" to append
                        with open(file_meta, "a", encoding="utf-8") as f:
                            f.write(
                                date
                                + inc
                                + ", "
                                + date_hr
                                + ", "
                                + meta_name
                                + ", "
                                + inst
                                + ": "
                                + meta
                                + "\n",
                            )

                        # Now download and save pdf
                        response_pdf = requests.get(url + date + inc + end_pdf)

                        file_speech = os.path.join(wd, date + inc + ".pdf")

                        with open(file_speech, "wb") as f:
                            f.write(response_pdf.content)

                    except:
                        pass

                # Break inner loop if no more speeches for that day
                elif response.status_code == 404:
                    break


### Function for transforming the data in txt files


def pdf_to_txt(wd):
    """Transfers txt files to pdfs, deletes pdf.

    Args:
        wd: string where pdf's are stored

    """
    files = list(glob.glob(wd + "/*.pdf"))

    for file in files:

        try:
            # Extract text from pdf
            text = textract.process(file)  # type bytes
            text = text.decode("utf-8")  # decode to type str

            # Create new file name
            file_name = os.path.basename(file)

            # Save list of strings to file
            path_file_out = os.path.join(wd, file_name + ".txt")

            with open(path_file_out, "w") as f:
                f.write(text)

            f.close()
            os.remove(file)

        except Exception:
            pass


### Function that combines everything into one dataset


def construct_dataset(wd):
    """Constructs dataset containing all speeches from meta_data and individual
    textfiles.

    Args: working directory with scraped data

    Output: combined dataset

    """
    # Load file
    with open(os.path.join(wd, "meta_data.txt").replace("\\", "/")) as f:
        df = f.readlines()
    df = pd.DataFrame(df, columns=["column_name"])

    # Extract some information
    df[["filename", "date", "name", "residual"]] = df["column_name"].str.split(
        ",",
        3,
        expand=True,
    )

    # Split each cell into two columns based on ":"
    df[["institution", "meta_data"]] = df["residual"].str.split(":", 1, expand=True)

    # Drop some variables
    df = df.drop(["column_name", "residual"], axis=1)

    # initialize empty speech string
    df["speech"] = ""

    # loop over filenames and load corresponding text file
    for i, filename in enumerate(df["filename"]):
        try:
            with open(os.path.join(wd, filename + ".pdf.txt")) as file:
                text = file.read()
                df.at[i, "speech"] = text
        except:
            pass

    return df
