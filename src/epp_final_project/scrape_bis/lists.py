# Import packages
import datetime as dt

# List of institutions.
institutions = [
    "People's Bank of China",
    "Bank Indonesia",
    "Bank of Albania",
    "Bank of Algeria",
    "Bank of Botswana",
    "Bank of Canada",
    "Bank of England",
    "Bank of Estonia",
    "Bank of Finland",
    "Bank of France",
    "Bank of Ghana",
    "Bank of Greece",
    "Bank of Guatemala",
    "Bank of Guyana",
    "Bank of Israel",
    "Bank of Italy",
    "Bank of Jamaica",
    "Bank of Japan",
    "Bank of Korea",
    "Bank of Latvia",
    "Bank of Lithuania",
    "Bank of Mauritius",
    "Bank of Mexico",
    "Bank of Morocco",
    "Bank of Mozambique",
    "Bank of Namibia",
    "Bank of Papua New Guinea",
    "Bank of Portugal",
    "Bank of Sierra Leone",
    "Bank of Slovenia",
    "Bank of Spain",
    "Bank of Tanzania",
    "Bank of Thailand",
    "Bank of Uganda",
    "Bank of Zambia",
    "Board of Governors of the Federal Reserve System",
    "Bulgarian National Bank",
    "Central Bank of Argentina",
    "Central Bank of Aruba",
    "Central Bank of Bahrain",
    "Central Bank of Barbados",
    "Central Bank of Belize",
    "Central Bank of Bolivia",
    "Central Bank of Bosnia and Herzegovina",
    "Central Bank of Brazil",
    "Central Bank of Chile",
    "Central Bank of Colombia",
    "Central Bank of Curaçao and Sint Maarten",
    "Central Bank of Cyprus",
    "Central Bank of Iceland",
    "Central Bank of Ireland",
    "Central Bank of Jordan",
    "Central Bank of Kenya",
    "Central Bank of Kuwait",
    "Central Bank of Luxembourg",
    "Central Bank of Malaysia",
    "Central Bank of Malta",
    "Central Bank of Nepal",
    "Central Bank of Nigeria",
    "Central Bank of Norway",
    "Central Bank of Samoa",
    "Central Bank of Seychelles",
    "Central Bank of Solomon Islands",
    "Central Bank of Sri Lanka",
    "Central Bank of The Bahamas",
    "Central Bank of Trinidad and Tobago",
    "Central Bank of Uruguay",
    "central bank of the Philippines",
    "Central Bank of the Republic of Kosovo",
    "Central Bank of the Republic of Turkey",
    "Bank of Russia",
    "Central Bank of the United Arab Emirates",
    "Croatian National Bank",
    "Czech National Bank",
    "National Bank of Denmark",
    "Deutsche Bundesbank",
    "Eastern Caribbean Central Bank",
    "European Central Bank",
    "Federal Reserve Bank of Atlanta",
    "Federal Reserve Bank of Boston",
    "Federal Reserve Bank of Chicago",
    "Federal Reserve Bank of Dallas",
    "Federal Reserve Bank of Kansas City",
    "Federal Reserve Bank of Minneapolis",
    "Federal Reserve Bank of New York",
    "Federal Reserve Bank of Philadelphia",
    "Federal Reserve Bank of Richmond",
    "Federal Reserve Bank of San Francisco",
    "Hong Kong Monetary Authority",
    "central bank of Hungary",
    "Maldives Monetary Authority",
    "Monetary Authority of Macao",
    "Monetary Authority of Singapore",
    "National Bank of Belgium",
    "National Bank of Cambodia",
    "National Bank of Romania",
    "National Bank of Serbia",
    "National Bank of Slovakia",
    "National Bank of Ukraine",
    "Central Bank of the Republic of Austria",
    "National Bank of North Macedonia",
    "Netherlands Bank",
    "Reserve Bank of Australia",
    "Reserve Bank of Fiji",
    "Reserve Bank of India",
    "Reserve Bank of Malawi",
    "Reserve Bank of New Zealand",
    "Reserve Bank of Vanuatu",
    "Saudi Arabian Monetary Agency",
    "South African Reserve Bank",
    "State Bank of Pakistan",
    "Sveriges Riksbank",
    "Swiss National Bank",
    "Board of Governors of the US Federal Reserve System",
    "Bank of Sweden",
    "Board of the US Federal Reserve System",
    "US Federal Reserve System",
    "European Monetary Institute",
    "Bank for International Settlements",
    "Norges Bank",
    "Board of Governors of the US Federal Reserve",
    "Nederlandsche Bank",
    "Banque de France",
    "International Monetary Fund",
    "Austrian National Bank",
    "Governors of the U.S. Federal Reserve System",
    "Swedish Central Bank",
    "Board of the U S Federal Reserve System",
    "Bank of South Africa",
    "Banque nationale suisse",
    "Hong Kong Monetary",
    "Oesterreichische Nationalbank",
    "Sveriges Riskbank",
    "Bank of India",
    "National Bank of the Republic of Macedonia",
    "National Bank of the Republic of North Macedonia",
    "ECB",
    "Authority of Ireland",
    "Bank of Turkey",
    "Bank of Poland",
    "Bank of China",
    "Board of Governors of the federal reserve",
    "Board of governors of the us fed",
    "Australian Reserve Bank",
    "Sveriges Risksbank",
    "Federal Reserve Board",
    "Austrian Nationalbank",
    "Bank of Australia",
    "Board of Governors of the US Fed",
    "Federal Reserve System",
]

# In several speehes the name of the FED is different
# The ones in institutions_us are also included in institutions
# One alternative to write out all combinations would ofc be to only use, e.g.,
# "federal reserve" or similar and then it would catch all.
inst_us = [
    "board of governors of the federal reserve system",
    "board of governors of the us federal reserve system",
    "board of the us federal reserve system",
    "us federal reserve system",
    "board of governors of the us federal reserve",
    "governors of the u.s. federal reserve system",
    "board of the u s federal reserve system",
    "board of governors of the federal reserve",
    "board of governors of the us fed",
    "federal reserve board",
    "board of governors of the us fed",
    "federal reserve system",
]

inst_swe = [
    "sveriges riksbank",
    "bank of sweden",
    "sveriges riskbank",
    "swedish central bank",
    "sveriges risksbank",
]

inst_austria = [
    "central bank of the republic of austria",
    "austrian national bank",
    "oesterreichische nationalbank",
    "austrian nationalbank",
]

# Create List of Dates
def date_list(small):
    """
    Returns:
        date_list: list of dates in format 210101,
        from 970106 (first BIS speech) to today.

    Args: 
        small: returns on the first day of the month to speed up computation
    """
    
    today = dt.date.today()
    start = dt.date(1997, 1, 6)
    date_list = []

    if small == 1:
        # Start at the first day of the start month
        day = dt.date(start.year, start.month, 1)

        while day <= today:
            # Add the current day to the list
            date_list.append(day.strftime("%y%m%d"))
            
            # Move to the first day of the next month
            if day.month == 12:
                day = dt.date(day.year + 1, 1, 1)
            else:
                day = dt.date(day.year, day.month + 1, 1)

    else: 

        delta = today - start

        for i in range(delta.days + 1):
            day = start + dt.timedelta(days=i)
            day = day.strftime("%y%m%d")
            date_list.append(day)

    return date_list
