from fastapi import APIRouter, Depends, status, HTTPException

from app.backend.db_depends import get_db
from app.schemas import CreateReview
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.models import Review, Product, Rating
from app.routers.auth import get_current_user

router = APIRouter(prefix='/review', tags=['review'])
dbsession = Annotated[AsyncSession, Depends(get_db)]

@router.get('/')
async def all_reviews(db: dbsession):
    reviews = await db.scalars(select(Review).where(Review.is_active==True))
    return reviews.all()

@router.get('/{product_id}')
async def reviews_by_product(db: dbsession, product_id: int):
    reviews = await db.scalars(select(Review).where(Review.product_id == product_id,
                                                   Review.is_active == True))
    return reviews.all()


@router.post('/add_review/{product_id}')
async def add_review(db: dbsession, product_id: int, get_user: Annotated[dict, Depends(get_current_user)], review: CreateReview):
    user_id = get_user.get('id')

    product = await db.scalar(select(Product).where(Product.id == product_id, Product.is_active == True))
    if not product:
        raise HTTPException(status_code=404, detail='Товар не найден')

    new_rating = Rating(grade=review.grade,
                        user_id=user_id,
                        product_id=product_id)
    db.add(new_rating)
    await db.flush()

    new_review = Review(user_id=user_id,
                        product_id=product_id,
                        rating_id=new_rating.id,
                        comment=review.comment)
    db.add(new_review)

    average_rating_query = select(func.avg(Rating.grade)).where(Rating.product_id == product_id, Rating.is_active == True)
    average_rating = await db.scalar(average_rating_query)

    await db.execute(update(Product).where(Product.id == product_id).values(rating=average_rating))
    await db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            "detail": "Отзыв успешно добавлен"}

@router.delete('/delete_reviews/{review_id}')
async def delete_reviews(db: dbsession, review_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        review_delete = await db.scalar(select(Review).where(Review.id == review_id, Review.is_active == True))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав для удаления отзыва')
    if review_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Отзыв не найден')
    rating_id_to_delete = review_delete.rating_id

    await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
    await db.execute(update(Rating).where(Rating.id == rating_id_to_delete).values(is_active=False))
    product_id = review_delete.product_id
    average_rating_query = select(func.avg(Rating.grade)).where(Rating.product_id == product_id, Rating.is_active == True)
    average_rating = await db.scalar(average_rating_query)
    if average_rating is None:
        average_rating = 0.0
    await db.execute(update(Product).where(Product.id == product_id).values(rating=average_rating))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'detail': 'Отзыв успешно удалён!'}
