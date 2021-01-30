#Take a sample of the "trips" dataframe
df = trips.head(1000)
df2 = df[["user", "id_trip", "Rating_total"]]
df_rating = df.pivot(index="id_trip", columns="user", values="Rating_total")
df_rating = df_rating.fillna(0)
users_ids = list(df["user"])
user_trip_matrix = df_rating.to_numpy()
user_trip_matrix.shape
user_trip_matrix

#Train the model : collaborative, content_based, hybrid
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(user_trip_matrix, user_trip_matrix)

cosine_sim.shape

def top_k(id_trip, cosine_sim, k):

    df = 
    sim_scores = list(enumerate(cosine_sim[id_trip]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:k]
    trips_ids = [i[0] for i in sim_scores]
    return trips_ids

top_k(97, cosine_sim, 5)