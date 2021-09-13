import requests

""" 
REQUESTS DATA FROM FOLLOWING WEBSITES:
 """

def request_data(url):
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8', errors='ignore')

    return decoded_content

def get_italyRetail():
    url = 'http://sdmx.istat.it/sdmxws/rest/data/IT1%2C120_337%2C1.2/M.RTD_TURN3.99.TOTAL.N.1.IT?format=csv'
    italyRetail_content_csv = request_data(url).splitlines()
    
    return italyRetail_content_csv 

def get_italyZinc():
    #Domain to request data
    url2 = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/'
    query = 'sts_inpr_m?precision=1&geo=IT&unit=I15&s_adj=NSA&indic_bt=PROD&nace_r2=C2443'
    italyZinc_content_json = request_data(url2+query)

    return italyZinc_content_json

def get_germanyRetail():
    url3 = 'https://www.destatis.de/static/de_/opendata/data/einzelhandel_umsatz_wirtschaftszweige_preisbereinigt_originalwert.csv'
    germanyRetail_content_csv = request_data(url3).splitlines()

    return germanyRetail_content_csv





