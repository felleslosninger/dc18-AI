import pandas as pd
import os

# Load several datasets from csv and merge them
def load_datasets(data_dir=os.path.join('.', 'data'), start_year=2017, end_year=None):
    if not end_year:
        end_year = start_year
    df = pd.DataFrame()
    print("Loading datasets from year {0} to {1}".format(start_year, end_year))
    for year in range(start_year, end_year + 1):
        job_ads_filename = ''.join([str(year), '_ads.csv'])
        job_ads_desc_filename = ''.join([str(year), '_desc.csv'])

        df_ads = pd.read_csv(
            os.path.join(data_dir, job_ads_filename),
            sep=';'
        )

        df_ads_desc = pd.read_csv(
            os.path.join(data_dir, job_ads_desc_filename),
            sep=';'
        )

        # Merge datasets into one
        df = df.append(pd.merge(df_ads, df_ads_desc).rename(columns={'stillingsutlysning': 'stillingsbeskrivelse'}))

    return df