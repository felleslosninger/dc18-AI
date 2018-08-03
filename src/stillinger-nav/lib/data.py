import wget
import os


years_with_desc = [2002, 2015, 2016, 2017]
years_with_ads = list(range(2002, 2017 + 1))

def download_data(data_dir, start_year=2012, end_year=2017):
    for year in range(start_year, end_year + 1):
        filename_ads = ''.join([str(year), '_ads', '.csv'])
        filename_desc = ''.join([str(year), '_desc', '.csv'])
        ads_url = ''.join(['https://hotell.difi.no/download/nav/ledige-stillinger/', str(year), '?download'])
        desc_url = ''.join(['https://hotell.difi.no/download/nav/stillingstekster/', str(year), '?download'])
        
        if filename_ads not in os.listdir(os.path.join(data_dir)) and year in years_with_ads:
            wget.download(ads_url, out=os.path.join(data_dir, filename_ads))
            print(''.join(['Downloaded ads for ', str(year)]))
        if filename_desc not in os.listdir(os.path.join(data_dir)) and year in years_with_desc:
            wget.download(desc_url, out=os.path.join(data_dir, filename_desc))
            print(''.join(['Downloaded desc for ', str(year)]))