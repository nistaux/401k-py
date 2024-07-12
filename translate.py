import pandas as pd

# dict for str names to ticker codes
name_to_code = {
    "FID 500 INDEX": "FXAIX",
    "MFS MID CAP GRTH R4": "OTCJX",
    "JPM LG CAP GROWTH R6": "JLGMX",
    "AM CENT SM CAP GR R6": "ANODX",
    "FA BALANCED Z": "FZAAX",
    "J H TRITON N": "JGMNX",
    "TRP BLUE CHIP GRTH": "TRBCX"
}

# Setting up dataframe
k_raw  = pd.read_csv("401k-history.csv")

# Functions for Translations
def codeTranslation(Code):
    return(name_to_code[Code])

# renaming some of the columns to what ghostfolio wants
k_new = k_raw.rename(columns={
    "Investment": "Code", 
    "Amount": "Price",
    "Shares/Unit": "Quantity",
    "Transaction Type": "Action"
})

# inserting some columns that ghostfolio wants
k_new.insert(2, "DataSource", "YAHOO", allow_duplicates=True)
k_new.insert(3, "Currency", "USD", allow_duplicates=True)
k_new.insert(6, "Fee", 0.00, allow_duplicates=True)
k_new.insert(7, "Note", "", allow_duplicates=True)
k_new.insert(8, "Account", "401k", allow_duplicates=True)

# testing for now
temp = k_new.head(20)
temp['Code'] = temp['Code'].apply(codeTranslation)

print(temp)