import pandas as pd, re, numpy as np
from journal_tiers import TIERS, norm
df = pd.read_pickle("all.pkl").reset_index(drop=True)
df['jn'] = df['Source title'].map(norm)
miss = sorted(set(df.jn) - set(TIERS)); print('unmapped (discontinued titles not on the 2025 list, dropped)', miss, int((~df.jn.isin(TIERS)).sum()), 'records')
df = df[df.jn.isin(TIERS)].reset_index(drop=True)
df['tier'] = df.jn.map(lambda j: TIERS[j][0]); df['domain'] = df.jn.map(lambda j: TIERS[j][1])
df['Year'] = df.Year.astype(int)
keep = ['Article','Review','Conference paper','Data paper','Short survey']
print(df['Document Type'].value_counts().to_dict())
df = df[df['Document Type'].isin(keep)].copy()
def clean_abs(a):
    if not isinstance(a, str) or a.startswith('[No abstract'): return ''
    a = re.split(r'\s©|\s\(C\)\s|Copyright ©', a)[0]
    a = re.sub(r'(\d+(st|nd|rd|th) )?Annual Meeting of the Association for Information Science.*$', '', a)
    a = re.sub(r'This briefing is prepared by an independent writer[^.]*\.', '', a)
    a = re.sub(r'The briefing saves busy executives[^.]*\.', '', a)
    a = re.sub(r'(Purpose|Design/methodology/approach|Findings|Originality/value|Research limitations/implications|Practical implications|Social implications)\s*:', ' ', a)
    a = re.sub(r'\[(Purpose/Significance|Method/Process|Results?/Conclusions?|Objective|Methods?|Results?|Conclusions?|Limitations?)\]', ' ', a)
    return a
df['abs'] = df.Abstract.map(clean_abs)
df['kw'] = df['Author Keywords'].fillna('')
df['text'] = (df.Title.fillna('') + '. ' + df['abs'] + ' ' + df.kw.str.replace(';', ' ')).str.lower()
df['cites'] = pd.to_numeric(df['Cited by'], errors='coerce').fillna(0)
df['nauth'] = df['Author(s) ID'].fillna('').map(lambda s: len([x for x in s.split(';') if x.strip()]))
df['jname'] = df.groupby('jn')['Source title'].transform(lambda s: s.value_counts().index[0])
print(len(df), df.groupby(['Year','tier']).size().unstack())
print('no abstract share', (df['abs']=='').mean())
df.to_pickle('clean.pkl')
