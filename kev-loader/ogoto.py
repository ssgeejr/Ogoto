import os
import pandas as pd
import requests
import mysql.connector
from datetime import date
from saturn import Saturn

class Ogoto:
    def __init__(self):
        self.today = date.today()
        self.base_dir = "."
        self.today_file = os.path.join(self.base_dir, f"cisa_kev_{self.today}.csv")
        self.previous_file = os.path.join(self.base_dir, "cisa_kev_latest.csv")
        self.csv_url = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv"

    def download_csv(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.csv_url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        with open(self.today_file, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved: {self.today_file}")

    def compare_csvs(self):
        if not os.path.exists(self.previous_file):
            print("No previous CSV to compare.")
            return pd.DataFrame()

        new = pd.read_csv(self.today_file)
        old = pd.read_csv(self.previous_file)

        new = new.dropna(subset=["cveID"])
        old = old.dropna(subset=["cveID"])

        new["cveID"] = new["cveID"].astype(str).str.strip()
        old["cveID"] = old["cveID"].astype(str).str.strip()

        added_ids = set(new["cveID"]) - set(old["cveID"])
        return new[new["cveID"].isin(added_ids)]

    def cleanup_previous_csv(self):
        if os.path.exists(self.previous_file):
            os.remove(self.previous_file)
            print(f"Removed: {self.previous_file}")

    def update_daily_changes(self, changes):
        print("Preparing to insert new changes into the database...")
        saturn = Saturn()
        db_host = saturn.get_value("DBHOST") or "db"
        db_user = saturn.get_db_uname()
        db_pass = saturn.get_db_pword()
        db_name = saturn.get_db()

        try:
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_name
            )
            print("✅ Connected to the database.")
            # Future logic to insert `changes` will go here
            connection.close()
        except mysql.connector.Error as err:
            print(f"❌ Database connection error: {err}")

    def run(self):
        self.download_csv()
        changes = self.compare_csvs()
        if not changes.empty:
            print(f"Found {len(changes)} new CVEs:")
            print(changes[["cveID", "vendorProject", "product", "vulnerabilityName"]])
            self.update_daily_changes(changes)
        else:
            print("No new vulnerabilities.")

        os.replace(self.today_file, self.previous_file)
        print(f"Set {self.previous_file} as the new baseline.")
        # self.cleanup_previous_csv()
