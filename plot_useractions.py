#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 21:43:03 2018

@author: joe
"""
import pandas as pd
import matplotlib

df = pd.read_csv("useractions.csv")
df = pd.concat([df,pd.get_dummies(df["type"])])
df = df.groupby(by = ["timestamp"]).count().reset_index()
df = df.set_index("timestamp")
df = df[['view','convert','trigger']]
df.plot()
