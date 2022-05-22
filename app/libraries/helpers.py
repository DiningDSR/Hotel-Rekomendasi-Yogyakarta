import pandas as pd
def addBintangHotel(data:list, hotel:list) -> list:
    df = pd.DataFrame(data)
    hotel = pd.DataFrame(hotel)
    df = pd.merge(df, hotel, how="inner", on="itemName")
    data = df.to_dict("records")

    del df
    return data