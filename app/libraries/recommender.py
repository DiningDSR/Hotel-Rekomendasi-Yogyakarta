from sklearn.neighbors import NearestNeighbors

def get_user_rating(df, user):
  """
  df: DataFrame of rating table
  user: name of user
  """
  return df[df[user] > 0][user].index.tolist()

def recommend_hotels(df, df1, user, num_recommended_hotel):
  """
  df: origin dataframe
  df1: syncronized dataframe
  num_recommended_hotel: the number of recommended hotel
  """
  recommended_hotel = {}
  for m in df[df[user] == 0].index.tolist():
    index_df = df.index.tolist().index(m)
    predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
    recommended_hotel[m] = predicted_rating

  sorted_rm = [{"itemName": k, "rating": v} for k, v in sorted(recommended_hotel.items(), 
      key=lambda item: item[1], reverse=True)[:num_recommended_hotel]]

  return sorted_rm

def hotels_recommender(df, user, num_neighbors=15, num_recommendation=15):
  """
  df: origin dataframe
  user: the name of user
  num_neighbors: the number of neighbors
  num_recommendation: the number of recommendation be returned
  """
  df1 = df.copy()

  number_neighbors = num_neighbors

  knn = NearestNeighbors(metric='cosine', algorithm='brute')
  knn.fit(df.values)
  distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

  user_index = df.columns.tolist().index(user)

  for m,t in list(enumerate(df.index)):
    if df.iloc[m, user_index] == 0:
      sim_hotels = indices[m].tolist()
      hotels_distances = distances[m].tolist()
    
      if m in sim_hotels:
        id_hotels = sim_hotels.index(m)
        sim_hotels.remove(m)
        hotels_distances.pop(id_hotels) 

      else:
        sim_hotels = sim_hotels[:num_neighbors-1]
        hotels_distances = hotels_distances[:num_neighbors-1]
            
      hotels_similarity = [1-x for x in hotels_distances]
      hotels_similarity_copy = hotels_similarity.copy()
      nominator = 0

      for s in range(0, len(hotels_similarity)):
        if df.iloc[sim_hotels[s], user_index] == 0:
          if len(hotels_similarity_copy) == (number_neighbors - 1):
            hotels_similarity_copy.pop(s)
          
          else:
            hotels_similarity_copy.pop(s-(len(hotels_similarity)-len(hotels_similarity_copy)))
            
        else:
          nominator = nominator + hotels_similarity[s]*df.iloc[sim_hotels[s],user_index]
          
      if len(hotels_similarity_copy) > 0:
        if sum(hotels_similarity_copy) > 0:
          predicted_r = nominator/sum(hotels_similarity_copy)
        
        else:
          predicted_r = 0

      else:
        predicted_r = 0
        
      df1.iloc[m,user_index] = predicted_r

  return recommend_hotels(df, df1, user,num_recommendation)