from datetime import date
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from twilio.rest import Client

# TODO: Fix pandas problem AWS
def main(event=None, context=None):
    options = Options()
    options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://timberupdate.com/timber-prices/')
    html = driver.page_source

    tables = pd.read_html(html)
    data = tables[1]

    driver.close()
    pine_price_string = data.iloc[19].to_string()
    pine_price = pine_price_string.splitlines()[1].split()[-1]
    
    account_sid =  os.environ['twilio_account_sid']
    auth_token = os.environ['twilio_auth_token']

    client = Client(account_sid, auth_token)
    client.messages.create(
        to=os.environ['phone_number_to'],
        from_="os.environ['phone_number_from']",
        body=f'Yellow Pine Price: {pine_price}\nDate: {date.today()}'
    )

if __name__ == '__main__':
    raise SystemExit(main())

