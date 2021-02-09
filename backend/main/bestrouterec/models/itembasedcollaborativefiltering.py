from bestrouterec.repository import Repository
from bestrouterec.data import dataset
from surprise import KNNBasic
from datetime import datetime 
from typing import List
from bestrouterec.document import Event, Trip
class ItemBasedCollaborativeFiltering(RecommendationModel):
    name = "item_based"

    def __init__(
        self,
        repository: Repository
    ):
        self._repository = repository

    @timeit
    def train(self, user: User, agents: int = 30, chunksize: int = 20):

        dataset = dataset(repository=self._repository)
        model = KNNBasic(sim_options={"user_based": False})

        trained_model = model.fit(dataset)
        return trained_model

    @timeit
    def top_k(
        self,
        departure_point: User,
        arrival_point: str,
        passenger_id: str,
        trip_id:str,
        departure_time:datetime,
        k: int = 5,
        by_transports: List[str] = None,
        model=None,
        **kwargs,
    ) -> List:


        inner_id = model.trainset.to_inner_iid(trip_id)
        neighbors = model.get_neighbors(iid=int(inner_id), k=k * 10)
        item_ids = [model.trainset.to_raw_iid(n) for n in neighbors]

        if passenger_id:
            past_trips = set([action.item_id for action in self.repository.get_top(obj=Event(user_id=passenger_id), table=Event)])

            if trip_id:
                past_trips.add(trip_id)

            trips_ids = [a for a in trips_ids if a not in past_trips]

        if not trips_ids:
            return []

        trips = self._repository.get_list(user_id=passenger_id, items_ids=trips_ids)
        trips = [a for a in trips if a]
        if by_transports:
            trips = [a for a in trips if a.transport in by_transports]

        trips = trips[:k]
        return trips
