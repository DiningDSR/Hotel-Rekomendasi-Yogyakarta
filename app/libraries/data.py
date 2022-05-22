import pandas as pd

class Dataprep:
    def __init__(self, data1, data2=None) -> None:
        self.data1 = data1
        self.data2 = data2

    def pivot_data(self):
        df1 = pd.DataFrame(self.convert_hotel())
        df2 = pd.DataFrame(self.convert_rating())
        df = pd.merge(df1, df2, how="inner", on="itemId")
        df['user'] = df['user'].str.lower()
        df = df.pivot_table(index='itemName', columns='user', values='rating').fillna(0)
        return df

    def convert_hotel(self):
        data = [{ 
            "_id": i.id,
            "itemId": i.itemId,
            "itemName": i.itemName,
            "bintang": i.bintang
        } for i in self.data1]
        return data

    def convert_rating(self):
        data = [{ 
            "_id": i.id,
            "user": i.user,
            "rating": i.rating,
            "itemId": i.itemId, 
            "created_at": i.created_at
        } for i in self.data2]
        return data