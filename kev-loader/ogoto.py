import os
import pandas as pd
import requests
from datetime import date

class Ogoto:
    def __init__(self):
        self.today = date.today()
        self.base_dir = "/tmp/ogoto"
        os.makedirs(self.base_dir, exist_ok=True)
        self.today_file = os.path.join(self.base_dir, f"cisa_kev_{self.today}.csv")
        self.previous_file = os.path.join(self.base_dir, "cisa_kev_latest.csv")
        self.csv_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"

    def download_csv(self):
        print(f"Downloading KEV CSV from {self.csv_url}")
        response = requests.get(self.csv_url)
        response.raise_for_status()
        with open(self.today_file, 'wb') as f:
            f.write(response.content)
        print(f"Saved current CSV to {self.today_file}")

    def compare_csvs(self):
        if not os.path.exists(self.previous_file):
            print("No previous CSV to compare. Skipping diff.")
            return pd.DataFrame()

        new = pd.read_csv(self.today_file)
        old = pd.read_csv(self.previous_file)

        added = pd.merge(new, old, indicator=True, how='outer').query('_merge == "left_only"').drop('_merge', axis=1)
        return added

    def run(self):
        self.download_csv()
        changes = self.compare_csvs()
        if not changes.empty:
            print(f"🚨 {len(changes)} new vulnerabilities found:")
            print(changes[['cveID', 'vendorProject', 'product', 'vulnerabilityName']])
        else:
            print("✅ No new vulnerabilities.")
        # Replace previous file
        os.replace(self.today_file, self.previous_file)
