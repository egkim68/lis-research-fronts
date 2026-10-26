# LIS research fronts, 2016 to 2025

Code for "Journal and research-front dynamics in library and information science: Based on the SCImago category, 2016 to 2025" (*Journal of Librarianship and Information Science*, under review).

## Data

Scopus records cannot be shared and are not included. Run each query in `queries/` in Scopus Advanced Search and export the results as CSV (citation information, bibliographical information, abstract and keywords). Put the 2016 to 2025 files in one folder.

## Run

```bash
pip install -r requirements.txt
bash run_all.sh <folder with the CSV files> work
```

Results, tables, and figures are written to `work/`. Add the 2026 CSV file as a third argument to run the 2026 check. `eid_order.csv` keeps the record order of the reported run, which makes the clusters identical.

Python 3.13; about 7 GB of memory; about 30 minutes.

License: MIT.
