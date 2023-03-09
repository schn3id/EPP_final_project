# EPP Final Project (Valentin Kecht, Georg Schneider) 

## Overview

This project explores speeches held by central bankers and includes the following steps: 

- scrape all available speeches of central bankers provided by the [BIS](https://www.bis.org/cbspeeches/), extract the text and compile one dataset including all the data. The scraper is partly based on this [code](https://github.com/HanssonMagnus/scrape_bis). 
- clean and preprocess the data, including tokenization, removal of stop words and lemmatization. We also merge data of left- and right-wing populists as well as information on central bank independence. 
- the analysis explores descriptively how the discourse 1) has changed over the last 25 years, 2) varies across countries, 3) is influenced by populist governments, and 4) to what extent central bank independence moderates the latter effect


## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate epp_final_project
```

To build the project, type

```console
$ pytask
```

### Notes: 

- Both authors contributed equally to the project. 
- The project is exclusively written in python. Activating the environment should therefore be sufficient. 
- Scraping and processing the data for the whole period since 1997 takes several hours. To speed up the execution as proof of concept, we included the option to only retain speeches help on the first day of a month. To activate this option, you need to set the argument of function "..\scrape_bis\bis_scraper.py" (line 36) equal to 1 (currently activated).
- Detailed docstrings are contained in the function definitions themselves, not in the task_* files.
