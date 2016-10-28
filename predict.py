import pandas as pd
from scrub_data_no_dummies import scrub_df

def predict(d_obj, model, tab):
    df = pd.DataFrame.from_dict(d_obj)
    df_row = scrub_df(df)

    y = model.predict_proba(df_row.values)

    d = {}
    d['raw_input'] = df.values
    d['input'] = df_row.values
    d['prediction'] = y

    # tab.insert_one(d)

    return y[0][1]
