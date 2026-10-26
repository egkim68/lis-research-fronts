import numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
import frontlib as L
from fronts2 import features, df, C
Y=L.Y
typ=L.typ
F,_=features(C['r20.0'].values, df.bal, minsize=60); F['type']=F.apply(typ,axis=1)
L.df['fine']=C['r20.0'].values; F['terms']=F.cluster.map(L.ctfidf('fine',F.cluster.tolist()))
F.to_pickle('fronts_fine.pkl')
print(len(F), F.type.value_counts().to_dict())
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',75); pd.set_option('display.max_rows',300)
x=F[F.type.isin(['Emergent','Growing'])&((F.core+F.adj)>=50)].sort_values('g_share',ascending=False)
print(x[['cluster','type','size','s2017','s2020','s2025','g_share','g_lo','core','adj','genai','ai','covid','top_journal','top_journal_share','terms']].round(1).to_string())
