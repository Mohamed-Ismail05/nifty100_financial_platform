from pathlib import Path
import pandas as pd
import re

class DataValidator:

    def __init__(self):
        self.failures = []
    def log_failure(self,company_id,year,field,issue,severity):
        self.failures.append(
            {
                "company_id": company_id,
                "year": year,
                "field": field,
                "issue": issue,
                "severity": severity
            }
        )
    def load_data(self):
        base_path = Path("data/raw")
        self.companies = pd.read_excel(base_path / "companies.xlsx",header=1)
        self.pnl = pd.read_excel(base_path / "profitandloss.xlsx",header=1)
        self.balance = pd.read_excel(base_path / "balancesheet.xlsx",header=1)
        self.cashflow = pd.read_excel(base_path / "cashflow.xlsx",header=1)
        self.analysis = pd.read_excel(base_path / "analysis.xlsx",header=1)
        self.documents = pd.read_excel(base_path / "documents.xlsx",header=1)
        self.prosandcons = pd.read_excel(base_path / "prosandcons.xlsx",header=1)
        
        from normaliser import normalize_year
        self.pnl["year"] = self.pnl["year"].apply(normalize_year)
        self.balance["year"] = self.balance["year"].apply(normalize_year)
        self.cashflow["year"] = self.cashflow["year"].apply(normalize_year)
            # DQ-01
    def validate_company_pk(self):
        duplicates = self.companies[self.companies["id"].duplicated()]
        for _, row in duplicates.iterrows():
            self.log_failure(
                row["id"],
                None,
                "id",
                "Duplicate company primary key",
                "CRITICAL"
            )
    # DQ-02
    def validate_annual_pk(self):
        tables = {
            "profitandloss": self.pnl,
            "balancesheet": self.balance,
            "cashflow": self.cashflow
        }
        for table_name, df in tables.items():
            duplicates = df[
                df.duplicated(
                    subset=["company_id", "year"],
                    keep=False
                )
            ]
            for _, row in duplicates.iterrows():
                self.log_failure(
                    row["company_id"],
                    row["year"],
                    table_name,
                    "Duplicate company-year record",
                    "CRITICAL"
                )
    # DQ-03
    def validate_foreign_keys(self):
        valid_ids = set(self.companies["id"])
        child_tables = [
            self.pnl,
            self.balance,
            self.cashflow,
            self.analysis,
            self.documents,
            self.prosandcons
        ]
        for df in child_tables:
            invalid = df[~df["company_id"].isin(valid_ids)]
            for _, row in invalid.iterrows():
                self.log_failure(
                    row["company_id"],
                    row.get("year", None),
                    "company_id",
                    "Foreign key violation",
                    "CRITICAL"
                )
    # DQ-04
    def validate_balance_sheet(self):
        for _, row in self.balance.iterrows():
            assets = row["total_assets"]
            liabilities = row["total_liabilities"]
            if pd.notna(assets) and assets != 0:
                ratio = abs(assets - liabilities) / assets
                if ratio >= 0.01:
                    self.log_failure(
                        row["company_id"],
                        row["year"],
                        "total_assets",
                        "Balance sheet mismatch",
                        "WARNING"
                    )

    # DQ-05
    def validate_opm(self):
        for _, row in self.pnl.iterrows():
            sales = row["sales"]
            if sales > 0:
                calculated_opm = (row["operating_profit"]/ sales) * 100
                difference = abs(calculated_opm- row["opm_percentage"])
                if difference >= 2:
                    self.log_failure(
                        row["company_id"],
                        row["year"],
                        "opm_percentage",
                        "OPM cross-check failed",
                        "WARNING"
                    )

    # DQ-06
    def validate_sales(self):
        invalid = self.pnl[self.pnl["sales"] <= 0]
        for _, row in invalid.iterrows():
            self.log_failure(
                row["company_id"],
                row["year"],
                "sales",
                "Sales less than or equal to zero",
                "WARNING"
            )

    # DQ-07
    def validate_year_format(self):
        pattern = r"^\d{4}-\d{2}$|^TTM$"
        financial_tables = [self.pnl,self.balance,self.cashflow]
        for df in financial_tables:
            for _, row in df.iterrows():
                year_value = row["year"]
                # Missing year
                if pd.isna(year_value):
                    self.log_failure(
                        row["company_id"],
                        None,
                        "year",
                        "Missing year value",
                        "CRITICAL"
                    )
                    continue
                year_value = str(year_value).strip()
                # Invalid format
                if not re.match(pattern, year_value):
                    self.log_failure(
                        row["company_id"],
                        year_value,
                        "year",
                        "Invalid year format",
                        "CRITICAL"
                    )
    # DQ-08
    def validate_company_id(self):
        financial_tables = [self.pnl,self.balance,self.cashflow]
        for df in financial_tables:
            for _, row in df.iterrows():
                value = str(row["company_id"]).strip().upper()
                if (len(value) < 2 or len(value) > 12):
                    self.log_failure(
                        value,
                        row["year"],
                        "company_id",
                        "Ticker length out of range",
                        "CRITICAL"
                    )
        # DQ-09
    def validate_cashflow(self):
        for _, row in self.cashflow.iterrows():
            calculated = (row["operating_activity"]+row["investing_activity"]+
                row["financing_activity"]
            )

            difference = abs(calculated-row["net_cash_flow"])
            if difference > 10:
                self.log_failure(
                    row["company_id"],
                    row["year"],
                    "net_cash_flow",
                    "Net cash mismatch",
                    "WARNING"
                )

    # DQ-10
    def validate_fixed_assets(self):
        invalid = self.balance[self.balance["fixed_assets"] < 0]
        for _, row in invalid.iterrows():
            self.log_failure(
                row["company_id"],
                row["year"],
                "fixed_assets",
                "Negative fixed assets",
                "WARNING"
            )

    # DQ-11
    def validate_tax_rate(self):
        invalid = self.pnl[(self.pnl["tax_percentage"] < 0)|
            (
                self.pnl["tax_percentage"] > 60
            )
        ]
        for _, row in invalid.iterrows():
            self.log_failure(
                row["company_id"],
                row["year"],
                "tax_percentage",
                "Tax rate outside range",
                "WARNING"
            )

    # DQ-12
    def validate_dividend(self):

        invalid = self.pnl[self.pnl["dividend_payout"] > 200]
        for _, row in invalid.iterrows():
            self.log_failure(
                row["company_id"],
                row["year"],
                "dividend_payout",
                "Dividend payout exceeds limit",
                "WARNING"
            )

    # DQ-13
    def validate_urls(self):
        for _, row in self.documents.iterrows():
            url = str(row["Annual_Report"])
            if not (url.startswith("http://")or url.startswith("https://")):
                self.log_failure(
                    row["company_id"],
                    row["Year"],
                    "Annual_Report",
                    "Invalid report URL",
                    "WARNING"
                )

    # DQ-14
    def validate_eps(self):
        invalid = self.pnl[(self.pnl["net_profit"] > 0)
            &
            (self.pnl["eps"] <= 0)]
        for _, row in invalid.iterrows():
            self.log_failure(
                row["company_id"],
                row["year"],
                "eps",
                "EPS sign mismatch",
                "WARNING"
            )

    # DQ-15
    def validate_strict_balance(self):
        invalid = self.balance[
            self.balance["total_assets"]
            !=
            self.balance["total_liabilities"]
        ]

        for _, row in invalid.iterrows():
            self.log_failure(
                row["company_id"],
                row["year"],
                "balance_check",
                "Assets not equal liabilities",
                "INFO"
            )

    # DQ-16
    def validate_coverage(self):
        counts = (self.pnl.groupby("company_id")["year"].nunique())
        insufficient = counts[counts < 5]
        for company_id, years in insufficient.items():
            self.log_failure(
                company_id,
                None,
                "coverage",
                f"Only {years} years available",
                "WARNING"
            )

    def export_results(self):
        output_path = Path("output")
        output_path.mkdir(exist_ok=True)
        pd.DataFrame(self.failures).to_csv(output_path /"validation_failures.csv",index=False)
    def run(self):
        self.load_data()
        self.validate_company_pk()
        self.validate_annual_pk()
        self.validate_foreign_keys()
        self.validate_balance_sheet()
        self.validate_opm()
        self.validate_sales()
        self.validate_year_format()
        self.validate_company_id()
        self.validate_cashflow()
        self.validate_fixed_assets()
        self.validate_tax_rate()
        self.validate_dividend()
        self.validate_urls()
        self.validate_eps()
        self.validate_strict_balance()
        self.validate_coverage()

        self.export_results()

        print(f"Validation completed. "f"{len(self.failures)} issues found.")
if __name__ == "__main__":

    validator = DataValidator()
    validator.run()

    import pandas as pd

df = pd.read_csv("output/validation_failures.csv")
