"""Merge the Scopus CSV exports (one per publication year) into all.pkl.
Usage: python 00_merge_exports.py <folder with Scopus CSV files> [eid_order.csv]
Record order affects the randomized SVD and the Leiden algorithm. To reproduce the
published results exactly, pass eid_order.csv, which fixes the order of records used
in the paper. Without it, records are sorted by EID (results then differ slightly;
see the robustness section of the paper)."""
import sys, glob, pandas as pd
files = sorted(glob.glob(sys.argv[1].rstrip('/') + '/*.csv'))
df = pd.concat([pd.read_csv(f, dtype=str) for f in files]).drop_duplicates('EID')
if len(sys.argv) > 2:
    order = pd.read_csv(sys.argv[2], dtype=str).EID
    missing = set(order) - set(df.EID)
    if missing: print('warning:', len(missing), 'records in eid_order.csv are not in the exports')
    df = df.set_index('EID').reindex([e for e in order if e not in missing]).reset_index()
else:
    df = df.sort_values('EID').reset_index(drop=True)
    df[['EID']].to_csv('eid_order.csv', index=False)
df.to_pickle('all.pkl'); print(len(files), 'files,', len(df), 'unique records')
