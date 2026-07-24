from fastapi import APIRouter, Depends, status, HTTPException

from app.backend.db_depends import get_db
from slugify import slugify
from app.schemas import CreateProduct
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from typing import Annotated
from app.models import Product
from app.models import Category



router = APIRouter(prefix='/products', tags=['products'])
dbsession = Annotated[Session, Depends(get_db)]

@router.get('/')
async def all_products(db: dbsession):
    products = db.scalars(select(Product).where(Product.is_active == True)).all()
    return products


@router.post('/create')
async def create_product(db: dbsession, new_product: CreateProduct):
    product = db.execute(insert(Product).values(name=new_product.name,
                                                slug=slugify(new_product.name),
                                                description=new_product.description,
                                                price=new_product.price,
                                                image_url=new_product.image_url,
                                                stock=new_product.stock,
                                                category_id=new_product.category,
                                                rating=0.0))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            'detail': 'Товар создан'}

@router.get('/{category_slug}')
async def product_by_category(db: dbsession, category_slug: str):
    category = db.scalar(select(Category).where(Category.is_active == True,
                                                   Category.slug==category_slug))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    subcategories = db.scalars(select(Category.id).where(Category.is_active == True,
                                                      Category.parent_id == category.id)).all()
    categories_ids = subcategories + [category.id]
    products_by_category = db.scalars(select(Product).where(Product.category_id.in_(categories_ids),
                                                            Product.stock > 0)).all()
    return products_by_category


@router.get('/detail/{product_slug}')
async def product_detail(db: dbsession, product_slug: str):
    product = db.scalar(
        select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0))
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return product

@router.put('/detail/{product_slug}')
async def update_product(db: dbsession, product_slug: str, update_product_model: CreateProduct):
    product_update = db.scalar(select(Product).where(Product.slug == product_slug))
    if product_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )

    db.execute(update(Product).where(Product.slug == product_slug).values(name=update_product_model.name,
                                                               description=update_product_model.description,
                                                               price=update_product_model.price,
                                                               image_url=update_product_model.image_url,
                                                               stock=update_product_model.stock,
                                                               category_id=update_product_model.category,
                                                               slug=slugify(update_product_model.name)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }


@router.delete('/delete')
async def delete_product(db: Annotated[Session, Depends(get_db)], product_id: int):
    product_delete = db.scalar(select(Product).where(Product.id == product_id))
    if product_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    db.execute(update(Product).where(Product.id == product_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }