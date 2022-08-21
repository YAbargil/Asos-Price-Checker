import json
import pandas as pd
import requests as requests
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter



def checkCountry(p_id,code,curr,h):
    price_endpoint = f"https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={p_id}&store={code}&currency={curr}"
    return requests.get(price_endpoint, headers=h).json()[0]['productPrice']['current']['text'],requests.get(price_endpoint, headers=h).json()[0]['productPrice']['current']['value']


checker = {
    "ROW": ["Israel", "GBP"],
    "_ROW": ["Hong Kong", "HKD"],
    "COM": ["United Kingdom", "GBP"],
    "AU": ["Chrismas Island", "GBP"],

}
c = CurrencyConverter()


def checkItem(url):
    codes = list(checker.keys())
    prices = list()
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    product_url = url
    l=list()
    page = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser").find("script", type="application/ld+json")
    product_data = json.loads(soup.string)
    #print("Found item :", product_data['name'])
    l.append(f"Found item : {product_data['name']}")
    p_id = product_data['productID']
    df = pd.DataFrame()
    df['Country'] = " "
    df['Price'] = " "
    df['ILS Price'] = " "

    for i in range(len(checker)):
        currCode = codes[i].strip("_")
        currPrice, currPrice_ILS = checkCountry(p_id, currCode, checker[codes[i]][1], headers)
        prices.append(currPrice)
        df.loc[i] = [checker[codes[i]][0], currPrice, c.convert(currPrice_ILS, checker[codes[i]][1], "ILS")]
    prices = df.sort_values('ILS Price')
    prices = prices['ILS Price'].tolist()
    l.append(df.to_string(index=False))
    #print(df)
    lowest_price = prices[0]
    lowest = "{:.2f}".format(lowest_price)
    lowest = float(lowest)
    min_tax = c.convert(75, 'USD', 'ILS')
    #print("Lowest price is :", lowest)
    l.append(f"Lowest price is : {lowest}")
    #print("After IL17 Coupon :", round(lowest * 0.83))
    l.append(f"After IL17 Coupon : {round(lowest * 0.83)}")
    #print("Dont forget that above", round(min_tax), " ILS You'll pay tax")
    l.append(f"Dont forget that above {round(min_tax)}  ILS You'll pay tax")
    #print(l)
    return l
