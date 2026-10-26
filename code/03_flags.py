import pandas as pd
"""Dictionary flags for COVID-19 and AI mentions (title, abstract, author keywords)."""
df = pd.read_pickle('clean.pkl')
DICT = {
 'GenAI': r"chatgpt|generative ai\b|generative artificial intelligence|generative pre-trained|large language model|\bllms?\b|\bgpt\b|\bgpt-\d|\bgenai\b|\bgen-ai\b",
 'AI (broad)': r"artificial intelligence|\bai\b|machine learning|deep learning|neural network|large language model|\bllms?\b|chatgpt|generative ai\b|\bgpt\b|\bgpt-\d|natural language processing|chatbot",
 'ML/DL (pre-generative)': r"machine learning|deep learning|neural network",
 'COVID-19': r"covid|sars-cov-2|coronavirus|2019-ncov|\bpandemic|lockdown",
 'Misinformation': r"misinformation|disinformation|fake news|infodemic|conspiracy theor",
 'Open science': r"open access|open science|open data|\bfair principles|\bfair data|preprint",
 'Information literacy': r"information literacy|media literacy|digital literacy|\bai literacy",
}
for k,p in DICT.items(): df[k] = df.text.str.contains(p, regex=True)
df['GenAI'] &= ~((df.Year<=2022) & ~df.text.str.contains(r"\bgpt|large language model|\bllm", regex=True))  # guard early false hits
df[['EID']+list(DICT)].to_pickle('art_flags.pkl'); print(df[list(DICT)].mean().round(4).to_dict())
