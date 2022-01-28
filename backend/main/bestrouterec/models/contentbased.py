from sklearn.metrics.pairwise import linear_kernel
import pandas as pd



class ContentBased:
    name = "content_based"

    def __init__(
        self,
        repository: Repository
    ):
        self._repository = repository

    def top_k(self, id_trip : str, passenger_id : str, k : int = 5):

        df = pd.read_csv("trips.csv")
        df = df[["user", "id_trip", "Rating_total"]]
        df_rating = df.pivot(index="id_trip", columns="user", values="Rating_total")
        df_rating = df_rating.fillna(0)
        users_ids = list(df["user"])
        user_trip_matrix = df_rating.to_numpy()
        cosine_sim = linear_kernel(user_trip_matrix, user_trip_matrix)
        sim_scores = list(enumerate(cosine_sim[id_trip]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[:k]
        trips_ids = [i[0] for i in sim_scores]
        trips=self._repository.get_list(user_id=passenger_id, items_ids=trips_ids)

        return trips