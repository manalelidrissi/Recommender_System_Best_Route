from typing import List
from bestrouterec.document import db, Trip


class Repository:

    """
    Base Repository for all SQLAlchemy databases
    """

    @classmethod
    def get_all(cls, obj , table) -> List:

        dic = obj.to_dict()
        filter_data = {key: value for (key, value) in dic.items() if value}
        query = db.session.query(table).filter_by(**filter_data).all()

        return query

    @classmethod
    def get_top(cls, obj , table, limit_value : int = 10) -> List:

        dic = obj.to_dict()
        filter_data = {key: value for (key, value) in dic.items() if value}
        query = db.session.query(table).filter_by(**filter_data).limit(limit_value).all()

        return query

    @classmethod
    def add_many(cls, objs):

        db.session.bulk_save_objects(objs)
        db.session.commit()

    @classmethod
    def get_list(cls, user_id, items_ids) -> List:

        query = db.session.query(Trip).filter_by(user_id=user_id).filter(Trip.trip_id.in_(items_ids)).all()

        return query
