# EPP Final Project (Valentin Kecht, Georg Schneider) 


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

## Overview

This project explores speeches held by central bankers and includes the following steps: 

- scrape all available speeches of central bankers provided by the [BIS](https://www.bis.org/cbspeeches/), extract the text and compile one dataset including all the data. The scraper is partly based on this [code](https://github.com/HanssonMagnus/scrape_bis). 
- clean and preprocess the data, including tokenization, removal of stop words and lemmatization. We also merge data of left- and right-wing populists as well as information on central bank independence. 
- the analysis explores descriptively how the discourse 1) has changed over the last 25 years, 2) varies across countries, 3) is influenced by populist governments, and 4) to what extent central bank independence moderates the latter effect