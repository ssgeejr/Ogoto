import os
import pandas as pd
import requests
from datetime import date

class Ogoto:
    def __init__(self):
        self.today = date.today()
        self.base_dir = "."  # Use current directory for portability
        self.today_file = os.path.join(self.base_dir, f"cisa_kev_{self.today}.csv")
        self.previous_file = os.path.join(self.base_dir, "cisa_kev_latest.csv")
        self.csv_url = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"


    def download_csv(self):
        print(f"Downloading KEV CSV from {self.csv_url}")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(self.csv_url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        with open(self.today_file, 'wb') as f:
            f.write(response.content)
        print(f"✅ Saved current CSV to {self.today_file}")

    def compare_csvs(self):
        if not os.path.exists(self.previous_file):
            print("ℹ️ No previous CSV to compare. Skipping diff.")
            return pd.DataFrame()

        new = pd.read_csv(self.today_file)
        old = pd.read_csv(self.previous_file)

        added = pd.merge(new, old, indicator=True, how='outer').query('_merge == "left_only"').drop('_merge', axis=1)
        return added

    def cleanup_previous_csv(self):
        if os.path.exists(self.previous_file):
            try:
                os.remove(self.previous_file)
                print(f"🧹 Removed old file: {self.previous_file}")
            except Exception as e:
                print(f"⚠️ Failed to remove {self.previous_file}: {e}")

    def run(self):
        self.download_csv()
        changes = self.compare_csvs()
        if not changes.empty:
            print(f"🚨 {len(changes)} new vulnerabilities found:")
            print(changes[['cveID', 'vendorProject', 'product', 'vulnerabilityName']])
        else:
            print("✅ No new vulnerabilities.")

        # Save today's CSV as latest and clean up
        os.replace(self.today_file, self.previous_file)
        print(f"📦 Updated reference CSV: {self.previous_file}")

        # Cleanup logic (temporary until DB support is added)
        #self.cleanup_previous_csv()
