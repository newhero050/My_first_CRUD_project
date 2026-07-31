from sqlalchemy import (Column, Integer, String, DateTime, Boolean,
                        ForeignKey, func)
from sqlalchemy.orm import relationship
from app.backend.db import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    comment = Column(String, nullable=False)
    comment_date = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='reviews')
    rating = relationship('Rating', back_populates='review')
    product = relationship('Product', back_populates='reviews')


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='ratings')
    review = relationship('Review', back_populates='rating', uselist=False)
    product = relationship('Product', back_populates='ratings')