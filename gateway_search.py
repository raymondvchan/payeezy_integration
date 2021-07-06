'''
Description: Simple script to download transactions from Payeezy and update OMS with the transaction information
Documentation support for Payeezy Gateway Search:
https://support.payeezy.com/hc/en-us/articles/203731129-First-Data-Payeezy-Gateway-Search-and-Reporting-API
'''

import config
from datetime import datetime, timedelta
from io import StringIO
import pandas as pd
import requests

time_format = "%Y-%m-%d %H:%M:%S"
current_time = datetime(
    year=datetime.now().year, 
    month=datetime.now().month,
    day=datetime.now().day,
    hour=datetime.now().hour
)
start_date = current_time - timedelta(minutes = config.search_interval)
end_date = start_date + timedelta(minutes=config.search_interval-1) + timedelta(seconds=59)
headers = {'Accept': 'text/search-v3+csv'}
params = {
    'start_date': start_date.strftime(time_format),
    'end_date': end_date.strftime(time_format)
}

print(current_time.strftime(time_format), start_date.strftime(time_format), end_date.strftime(time_format))

resp = requests.get(config.url, params=params, headers=headers, auth=(config.userid, config.password))

if resp.status_code == 401:
    print('User/Pass expired')
if resp.status_code == 400:
    print('Bad Request / Arguments')
if resp.status_code == 500:
    print('Payeezy Server Error')      
if resp.status_code == 200:
    print('Request successful')    
    df = pd.read_csv(StringIO(resp.text))

    if (len(df) > 0) or (not(df.empty)):
        print('Results found to process')
    else:
        print('No results to process')

print('end of script')
