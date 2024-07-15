import pandas as pd

# Setting up dataframe
k_raw  = pd.read_csv("401k-history.csv")

# Function to convert strings to floats.. that have a comma in them
def convFloatFromString(string):
    str_no_comma = string.replace(',', '')
    str_float = float(str_no_comma)
    return str_float

# ----------------- Functions for Translations -----------------
def dateTranslation(date):
    repl_date = date.replace('/','-')
    split_date = repl_date.split('-')
    return split_date[2] + "-" + split_date[0] + "-" + split_date[1]

def codeTranslation(code):
    name_to_code = {
        "FID 500 INDEX": "FXAIX",
        "MFS MID CAP GRTH R4": "OTCJX",
        "JPM LG CAP GROWTH R6": "JLGMX",
        "AM CENT SM CAP GR R6": "ANODX",
        "FA BALANCED Z": "FZAAX",
        "J H TRITON N": "JGMNX",
        "TRP BLUE CHIP GRTH": "TRBCX"
    }

    return(name_to_code[code])

def actionTranslation(price, quantity):
    if price < 0:
        if quantity == 0.00:
            return "fee"
        return "sell"
    return "buy"

def feeTranslation(action, price):
    if action == "fee":
        return abs(price)
    return 0.00

def priceTranslation(price, quantity, action):
    if action == "fee":
        return 0.00
    if quantity != 0.00:
        stock_price = round(price/quantity, 2)
        return stock_price
    else:
        return price

def quantityTranslation(quantity):
    return abs(round(quantity, 2))
# --------------------------------------------------------------

# renaming some of the columns to what ghostfolio wants
k_new = k_raw.rename(columns={
    "Investment": "Code", 
    "Amount": "Price",
    "Shares/Unit": "Quantity",
    "Transaction Type": "Action"
})

# Date , Code , DataSource , Currency , Price , Quantity , Action , Fee , Note , Account
# inserting some columns that ghostfolio wants
k_new.insert(2, "DataSource", "YAHOO", allow_duplicates=True)
k_new.insert(3, "Currency", "USD", allow_duplicates=True)
k_new.insert(7, "Fee", 0.00, allow_duplicates=True)
k_new.insert(8, "Note", "", allow_duplicates=True)
k_new.insert(9, "Account", "401k", allow_duplicates=True)

# testing for now
#temp = k_new.head(340)

# setting price column to float from string
k_new.loc[:, 'Price'] = k_new['Price'].apply(lambda x: convFloatFromString(x))

# converting date '/' to '-'
k_new.loc[:, 'Date'] = k_new['Date'].apply(dateTranslation)

# converting str name of investment to the stock ticker code
k_new.loc[:, 'Code'] = k_new['Code'].apply(codeTranslation)

# converting the transaction type to actions: buy, sell, fee
k_new.loc[:, 'Action'] = k_new.apply(lambda x: actionTranslation(x['Price'],x['Quantity']), axis=1)

# converting the price to the fee if it is a fee ?
k_new.loc[:, 'Fee'] = k_new.apply(lambda x: feeTranslation(x['Action'],x['Price']), axis=1)

# converting price to the actual stock price instead of it adjusted to how much was bought
k_new.loc[:, 'Price'] = k_new.apply(lambda x: priceTranslation(x['Price'],x['Quantity'], x['Action']), axis=1)

# converting quantity to two decimal places and only positive numbers
k_new.loc[:, 'Quantity'] = k_new['Quantity'].apply(quantityTranslation)

#print(k_raw.head(20))
#print(temp)
k_new.to_csv('out.csv', index=False)