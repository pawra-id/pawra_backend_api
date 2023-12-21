from typing import Generic, List, TypeVar
from pydantic import BaseModel, conint
from pydantic.generics import GenericModel

T = TypeVar("T")

class PageParams(BaseModel):
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10

class PagedResponseSchema(GenericModel, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]

def paginate(page_params: PageParams, query, ResponseSchema: BaseModel) -> PagedResponseSchema[T]:
    paginated_query = query.offset((page_params.page - 1) * page_params.size).limit(page_params.size).all()
    print(paginated_query)
    
    return PagedResponseSchema(
        total = query.count(),
        page = page_params.page,
        size = page_params.size,
        results = [ResponseSchema.from_orm(result) for result in paginated_query]
    )