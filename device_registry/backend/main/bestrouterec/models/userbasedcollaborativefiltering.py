from surprise import Dataset, Reader
from surprise import KNNBasic
data = Dataset.load_from_df(df2, Reader(rating_scale=(1, 5)))
data = data.build_full_trainset()

model = KNNBasic(sim_options={"user_based": False})
trained_model = model.fit(data)

from collections import defaultdict

from surprise import SVD
from surprise import Dataset


def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# First train an SVD algorithm on the movielens dataset.
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

top_n = get_top_n(predictions, n=10)

# Print the recommended items for each user
for uid, user_ratings in top_n.items():
    print(uid, [iid for (iid, _) in user_ratings])

from collections import defaultdict

from surprise import Dataset
from surprise import SVD
from surprise.model_selection import KFold


def precision_recall_at_k(predictions, k=10, threshold=3.5):
    """Return precision and recall at k metrics for each user"""

    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():

        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        # When n_rec_k is 0, Precision is undefined. We here set it to 0.

        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0

        # Recall@K: Proportion of relevant items that are recommended
        # When n_rel is 0, Recall is undefined. We here set it to 0.

        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

    return precisions, recalls


data = Dataset.load_builtin('ml-100k')
kf = KFold(n_splits=5)
algo = SVD()

for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    precisions, recalls = precision_recall_at_k(predictions, k=5, threshold=4)

    # Precision and recall can then be averaged over all users
    print(sum(prec for prec in precisions.values()) / len(precisions))
    print(sum(rec for rec in recalls.values()) / len(recalls))

import io  # needed because of weird encoding of u.item file

from surprise import KNNBaseline
from surprise import Dataset
from surprise import get_dataset_dir


def read_item_names():
    """Read the u.item file from MovieLens 100-k dataset and return two
    mappings to convert raw ids into movie names and movie names into raw ids.
    """

    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]

    return rid_to_name, name_to_rid


# First, train the algortihm to compute the similarities between items
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)

# Read the mappings raw id <-> movie name
rid_to_name, name_to_rid = read_item_names()

# Retrieve inner id of the movie Toy Story
toy_story_raw_id = name_to_rid['Toy Story (1995)']
toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)

# Retrieve inner ids of the nearest neighbors of Toy Story.
toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, k=10)

# Convert inner ids of the neighbors into names.
toy_story_neighbors = (algo.trainset.to_raw_iid(inner_id)
                       for inner_id in toy_story_neighbors)
toy_story_neighbors = (rid_to_name[rid]
                       for rid in toy_story_neighbors)

print()
print('The 10 nearest neighbors of Toy Story are:')
for movie in toy_story_neighbors:
    print(movie)

import os

from surprise import SVD
from surprise import Dataset
from surprise import dump


data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()

algo = SVD()
algo.fit(trainset)

# Compute predictions of the 'original' algorithm.
predictions = algo.test(trainset.build_testset())

# Dump algorithm and reload it.
file_name = os.path.expanduser('~/dump_file')
dump.dump(file_name, algo=algo)
_, loaded_algo = dump.load(file_name)

# We now ensure that the algo is still the same by checking the predictions.
predictions_loaded_algo = loaded_algo.test(trainset.build_testset())
assert predictions == predictions_loaded_algo
print('Predictions are the same')

from surprise import Dataset
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import KFold


data = Dataset.load_builtin('ml-100k')

algo = SVD()

trainset = data.build_full_trainset()
algo.fit(trainset)

testset = trainset.build_testset()
predictions = algo.test(testset)
# RMSE should be low as we are biased
accuracy.rmse(predictions, verbose=True)  # ~ 0.68 (which is low)

import random

from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import GridSearchCV


# Load the full dataset.
data = Dataset.load_builtin('ml-100k')
raw_ratings = data.raw_ratings

# shuffle ratings if you want
random.shuffle(raw_ratings)

# A = 90% of the data, B = 10% of the data
threshold = int(.9 * len(raw_ratings))
A_raw_ratings = raw_ratings[:threshold]
B_raw_ratings = raw_ratings[threshold:]

data.raw_ratings = A_raw_ratings  # data is now the set A

# Select your best algo with grid search.
print('Grid Search...')
param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005]}
grid_search = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3)
grid_search.fit(data)

algo = grid_search.best_estimator['rmse']

# retrain on the whole set A
trainset = data.build_full_trainset()
algo.fit(trainset)

# Compute biased accuracy on A
predictions = algo.test(trainset.build_testset())
print('Biased accuracy on A,', end='   ')
accuracy.rmse(predictions)

# Compute unbiased accuracy on B
testset = data.construct_testset(B_raw_ratings)  # testset is now the set B
predictions = algo.test(testset)
print('Unbiased accuracy on B,', end=' ')
accuracy.rmse(predictions)

import random
import numpy as np

my_seed = 0
random.seed(my_seed)
np.random.seed(my_seed)

class UserBasedCollaborativeFiltering(RecommendationModel):
    name = RecommendationType.CF_USER_BASED

    def __init__(
        self,
        storage_provider: AbstractStorageProvider,
        article_repository: ArticleRepository,
        analytics_repository: AnalyticsRepository,
        event_repository: EventRepository,
        fallback: RecommendationModel,
        **kwargs,
    ):
        self._storage_provider = storage_provider
        self._article_repository = article_repository
        self._event_repository = event_repository
        self._analytics_repository = analytics_repository
        self._fallback = fallback

    @timeit
    def train(self, user: User, agents: int = 30, chunksize: int = 20):

        dataset = data.prepare_reader_item_dataset(
            user=user,
            article_repository=self._article_repository,
            event_repository=self._event_repository,
            agents=agents,
            chunksize=chunksize,
        )
        model = KNNBasic(sim_options={"user_based": True})

        trained_model = model.fit(dataset)
        return trained_model

    def unique(self, sequence):
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]

    @timeit
    def top_k(
        self,
        user: User,
        content_language: str,
        reader_id: str,
        item_id: str,
        weights: dict = None,
        k: int = 5,
        by_types: List[str] = None,
        by_sources: List[str] = None,
        by_categories: List[str] = None,
        **kwargs,
    ) -> List[ArticleMetaData]:
        # cannot make any use based recs if user is not given ...
        if not reader_id:
            logger.info("reader_id not provided or anonymous user: fallback to Multi-Criteria")
            return self._fallback.top_k(
                user=user,
                content_language=content_language,
                reader_id=reader_id,
                item_id=item_id,
                k=k,
                weights=weights,
            )

        model = storage.load_model(self._storage_provider, model_name=self.name, public_id=user.public_id)

        try:
            inner_id = model.trainset.to_inner_uid(reader_id)
        except ValueError as e:
            logger.warning(e)
            raise ItemNotFound()

        neighbors = sorted(model.get_neighbors(iid=int(inner_id), k=5), reverse=True)

        names = [model.trainset.to_raw_uid(n) for n in neighbors]
        logger.info(f"Top {k} neighbors: {names}")

        item_ids = [model.trainset.ur[n] for n in neighbors]
        item_ids = self.unique([item[0] for sublist in item_ids for item in sublist])
        item_ids = [model.trainset.to_raw_iid(item_id) for item_id in item_ids]

        viewed_items = set(
            [
                action.item_id
                for action in self._event_repository.get_top(
                    event=DomainEvent(user_public_id=user.public_id, reader_id=reader_id, type=EventType.VIEWED),
                    sort=True,
                    sort_attribute=DomainEvent.timestamp,
                )
            ]
        )

        if item_id:
            viewed_items.add(item_id)

        item_ids = [i for i in item_ids if i not in viewed_items]

        items = self._article_repository.get_list(user, item_ids)
        items = [a for a in items if a]
        if by_types:
            items = [a for a in items if a.type in by_types]

        if by_sources:
            items = [a for a in items if a.source.title in by_sources]

        items = [i for i in items if i][:k]
        items = self._set_suggested_by(items)
        return items

    def _get_top_model(self, user, model, reader_id, k):
        test_set = self._build_anti_testset(model, reader_id)

        # TODO: these predictions need to be persisted as well after each model training
        predictions = model.test(test_set)
        top_n = self._get_top_n(predictions, n=k * 20)
        if reader_id in top_n:
            top_predictions = top_n[reader_id]
            ids = [prediction[0] for prediction in top_predictions if prediction]
            items = self._article_repository.get_list(user, ids)
            return items
        else:
            return []

    def _build_anti_testset(self, model, reader_id: str):
        """
        This is a modification of the build_anti_testset method of the trainset class.

        It only returns unrated items for a given `reader_id` instead of iterating over all users.

        :param model:
        :param reader_id:
        :return:
        """
        user_items = set([j for (j, _) in model.trainset.ur[reader_id]])
        test_set = [
            (reader_id, model.trainset.to_raw_iid(i), model.trainset.global_mean)
            for i in model.trainset.all_items()
            if i not in user_items
        ]
        return test_set

    def _get_top_n(self, predictions, n=10):
        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n
