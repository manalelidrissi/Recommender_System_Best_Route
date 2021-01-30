class ItemBasedCollaborativeFiltering(RecommendationModel):
    name = RecommendationType.CF_ITEM_BASED

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
        self._analytics_repository = analytics_repository
        self._event_repository = event_repository
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
        model = KNNBasic(sim_options={"user_based": False})

        trained_model = model.fit(dataset)
        return trained_model

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

        if not item_id:
            logger.info("Item_id not provided: fallback to Multi-Criteria")
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
            inner_id = model.trainset.to_inner_iid(item_id)
        except ValueError as e:
            logger.warning(e)
            raise ItemNotFound()

        neighbors = model.get_neighbors(iid=int(inner_id), k=k * 10)
        item_ids = [model.trainset.to_raw_iid(n) for n in neighbors]

        # only display articles to user that he did not read yet
        if reader_id:
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

            item_ids = [a for a in item_ids if a not in viewed_items]

        if not item_ids:
            return []

        items = self._article_repository.get_list(user, item_ids)
        items = [a for a in items if a]
        if by_types:
            items = [a for a in items if a.type in by_types]

        if by_sources:
            items = [a for a in items if a.source.title in by_sources]

        items = items[:k]
        items = self._set_suggested_by(items)
        return items
