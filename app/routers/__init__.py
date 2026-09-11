from fastapi import APIRouter

#v1 api_routers
from .auth import router as auth_router_v1
from .category import router as category_router_v1
from .permission import router as permission_router_v1
from .products import router as products_router_v1
from .reviews import router as reviews_router_v1

#v2 api_routers
from .products import router_v2 as products_router_v2

#v1
v1_routers = APIRouter(prefix='/api/v1')
v1_routers.include_router(auth_router_v1)
v1_routers.include_router(category_router_v1)
v1_routers.include_router(permission_router_v1)
v1_routers.include_router(products_router_v1)
v1_routers.include_router(reviews_router_v1)

#v2
v2_routers = APIRouter(prefix='/api/v2')
v2_routers.include_router(products_router_v2)
