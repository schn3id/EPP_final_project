# EPP Final Project (Valentin Kecht, Georg Schneider) 

<<<<<<< HEAD
=======
## Overview

This project explores speeches held by central bankers and includes the following steps: 

- scrape all available speeches of central bankers provided by the [BIS](https://www.bis.org/cbspeeches/), extract the text and compile one dataset including all the data. The scraper is partly based on this [code](https://github.com/HanssonMagnus/scrape_bis). 
- clean and preprocess the data, including tokenization, removal of stop words and lemmatization. We also merge data of left- and right-wing populists as well as information on central bank independence. 
- the analysis explores descriptively how the discourse 1) has changed over the last 25 years, 2) varies across countries, 3) is influenced by populist governments, and 4) to what extent central bank independence moderates the latter effect
>>>>>>> f0727f14a2095517ca59309a8834fdea5001ee4b

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

<<<<<<< HEAD
## Overview

This project explores speeches held by central bankers and includes the following steps: 

- scrape all available speeches of central bankers provided by the [BIS](https://www.bis.org/cbspeeches/), extract the text and compile one dataset including all the data. The scraper is partly based on this [code](https://github.com/HanssonMagnus/scrape_bis). 
- clean and preprocess the data, including tokenization, removal of stop words and lemmatization. We also merge data of left- and right-wing populists as well as information on central bank independence. 
- the analysis explores descriptively how the discourse 1) has changed over the last 25 years, 2) varies across countries, 3) is influenced by populist governments, and 4) to what extent central bank independence moderates the latter effect
=======
### Notes: 

- The project is exclusively written in python. 
- 
- Scraping and processing the data for the whole period since 1997 takes several hours. To speed up the execution, you can shorten the period for the scraper in "..\scrape_bis\lists.py" (line 200) by e.g. setting the start year to 2023. 


>>>>>>> f0727f14a2095517ca59309a8834fdea5001ee4b
