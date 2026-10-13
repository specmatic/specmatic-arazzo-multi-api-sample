from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
import strawberry
from strawberry.fastapi import GraphQLRouter

from common.models import Product as ProductModel
from . import SessionDep


@strawberry.type
class Product:
    product_id: int
    name: str
    price: float
    inventory: int


@strawberry.type
class Query:
    @strawberry.field
    def products(self, info: strawberry.Info, location_code: str) -> list[Product]:
        session: Session = info.context["session"]
        statement = (
            select(ProductModel)
            .where(ProductModel.location_code == location_code)
            .options(selectinload(ProductModel.inventory_levels))
        )

        products = session.exec(statement).all()
        return [
            Product(
                name=product.name,
                price=product.price,
                product_id=product.product_id,
                inventory=product.inventory_levels.inventory,
            )

            for product in products
        ]

async def get_graphql_context(session: SessionDep) -> dict[str, Session]:
    return {"session": session}

schema = strawberry.Schema(query=Query)
graphql_router = GraphQLRouter(schema, context_getter=get_graphql_context)
