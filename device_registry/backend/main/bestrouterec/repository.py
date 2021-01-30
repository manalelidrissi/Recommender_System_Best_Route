from typing import List
from bestrouterec.document import db, Event


class Repository:

    """
    Base Repository for all SQLAlchemy databases
    """

    @classmethod
    def get_all(cls, obj , table) -> List[Event]:

        dic = obj.to_dict()
        filter_data = {key: value for (key, value) in dic.items() if value}
        query = db.session.query(table).filter_by(**filter_data).all()

        return query

    @classmethod
    def add_many(cls, objs):

        db.session.bulk_save_objects(objs)
        db.session.commit()

