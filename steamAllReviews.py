# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('steam_games_clean.csv')

df['all_reviews'] = pd.to_numeric(df['all_reviews'], errors='coerce')
df.all_reviews.fillna(value=-1,inplace=True)

df.to_csv("steam_games_clean_v2.csv", index=False)