import json
from datetime import date
import requests
import pandas as pd


def to_dataFrame(raw):
    dates = []
    names = []
    downloads = []
    for pkg in raw:
        for date in raw[pkg]:
            downloads.append(raw[pkg][date])
            names.append(pkg)
            dates.append(date)

    return pd.DataFrame({
        "date": dates,
        "name": names,
        "downloads": downloads}
    )


def get_downloads(request_type, value, from_date, until_date):

    print('feching...', request_type, value,
          from_date, until_date)

    res = requests.get(
        f"https://npm-stat.com/api/download-counts?{request_type}={value}&from={from_date}&until={until_date}"
    )

    print('fetched...', request_type, value,
          from_date, until_date, res.status_code)

    if res.status_code != 200:
        raise Exception(res.text)

    data = json.loads(res.text)

    return to_dataFrame(data)


def get_top10(df):
    top10_df = df[df["downloads"] > 0].groupby(["name"]).sum().sort_values(
        by=['downloads'], inplace=False, ascending=False).head(10)
    y = top10_df.values.tolist()
    x = top10_df.index.tolist()

    y = [x[0] for x in y]

    return x, y


def get_trends(df):
    df_trends = df.groupby(["date"]).sum()
    y = df_trends.values.tolist()
    x = df_trends.index.tolist()

    y = [x[0] for x in y]

    return x, y
