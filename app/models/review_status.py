"""Module of the review status model
"""

from flask import current_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import synonym
from sqlalchemy.orm.exc import FlushError

from app import db

class ReviewStatus(db.Model):
    """The ReviewStatus model"""
    __tablename__ = 'reviewStatuses'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), unique=True)
    feedbacks = db.relationship('Feedback', backref='reviewStatus')

    @property
    def name(self) -> str:
        """The name getter"""
        return self._name

    @name.setter
    def name(self, name) -> None:
        if len(name) > 64:
            raise ValueError('exceed the name length limit of 64.')
        self._name = name

    name = synonym('_name', descriptor=name)

    def __repr__(self) -> str:
        return f'<ReviewStatus {self.name}>'

    @staticmethod
    def insert_review_status() -> None:
        """Insert default review statuses"""
        review_statuses = current_app.config.get('REVIEW_STATUSES')
        for name in review_statuses:
            try:
                review_status = ReviewStatus(name=name)
                db.session.add(review_status)
                db.session.commit()
            except (IntegrityError, FlushError) as exc:
                print(exc)