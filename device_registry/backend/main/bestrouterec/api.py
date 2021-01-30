import os
import logging
import numpy as np

from flask_restplus import Namespace, Resource, abort
from flask_restplus._http import HTTPStatus
from injector import inject


logger = logging.getLogger(os.path.basename(__file__))

api = Namespace("recommendation", description="Recommendation API")

parser = api.parser()

@api.route("/")
class Rec:
    def execute_func():
        return('hello world')

# @api.doc(security="apikey")
# @api.route("")
# class Recommendation:
#     @api.marshal_list_with(recommendation_response_model(api))
#     @api.expect(recommendation_post_request(api))
#     def post(self):

#         trip_id = api.payload.get("trip_id")
#         reader_id = api.payload.get("user_id")
#         by_transports = api.payload.get("by_transports")
#         weights = api.payload.get("weights", {})
#         rec_model = api.payload.get("model")

#         if rec_model:
#             for model in models:
#                 if model.name == rec_model:
#                     model_class = model
        
#         logger.info(f"Selected model class {model_class}")

#         if model_class in [UserBasedCollaborativeFiltering, ItemBasedCollaborativeFiltering]:
#             train_model=model_class(repository=repository).train()
#             logger.info("model trained")


#         ranker = model_class(repository=repository)

#         try:
#             response = ranker.top_k(
#                 user=logged_in_user,
#                 reader_id=reader_id,
#                 item_id=item_id,
#                 content_language=content_config.content_language,
#                 k=limit,
#                 by_types=by_types,
#                 by_sources=by_sources,
#                 by_categories=by_categories,
#                 weights=weights,
#                 diversify=diversify,
#                 diversification_criteria=diversification_criteria,
#             )

#             return self._process_response(
#                 response=response,
#                 item_id=item_id,
#                 ranker=ranker,
#                 exp_name=exp_name,
#                 model_config_name=model_config_name,
#             )
#         except ModelNotFound:
#             abort(code=HTTPStatus.BAD_REQUEST, message="Trained Model not found. Please train the model first.")



#         )


# @api.doc(security="apikey")
# @api.route("/model/collaborative")
# class TrainCollaborativeModel(RecommendationResource):
#     @login_required
#     def post(self, logged_in_user, agents: int = 30, chunksize: int = 20):

#         cf_algorithms = [UserBasedCollaborativeFiltering, ItemBasedCollaborativeFiltering]
#         for algorithm in cf_algorithms:
#             instance = algorithm(
#                 ),
#             )

#             model = instance.train(user=logged_in_user, agents=agents, chunksize=chunksize)

#             storage.store_model(
#                 model=model,
#                 model_name=algorithm.name,
#                 public_id=logged_in_user.public_id,
#                 storage_provider=self._storage_provider,
#             )

#         # clear cache so that we can access the new model
#         storage.cf_model_cache.clear()

#         return {"message": "Model trained."}, 200
