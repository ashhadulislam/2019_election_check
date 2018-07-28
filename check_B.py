from flask import Flask, render_template, request, Markup
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def main(year):
    df=pd.read_excel("AllStates.xlsx",sheet_name=year)
    constituencies=df.Constituency.unique()
    df_b_win=pd.DataFrame()
    for constituency in constituencies:
        df_constituency=df[df["Constituency"]==constituency]
        if df_constituency.iloc[0]["Party"] in "BJP":
            df_b_win=df_b_win.append(df_constituency)
    df_b_win=df_b_win.reset_index(drop=True)
    df_b_win.to_csv(year+"_bjp_win.csv")


if __name__=="__main__":
    main("2014")
    main("2009")
    main("2004")
