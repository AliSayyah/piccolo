from __future__ import annotations
import typing as t

from piccolo.custom_types import Combinable
from piccolo.query.base import Query
from piccolo.query.mixins import WhereDelegate
from piccolo.querystring import QueryString

from .select import Select


class Count(Query):
    __slots__ = ("where_delegate",)

    def __init__(self, table: t.Type[Table]):
        self.table = table
        self.where_delegate = WhereDelegate()

    def where(self, where: Combinable) -> Count:
        self.where_delegate.where(where)
        return self

    async def response_handler(self, response) -> bool:
        return response[0]["count"]

    @property
    def querystrings(self) -> t.Sequence[QueryString]:
        select = Select(self.table)
        select.where_delegate._where = self.where_delegate._where
        return [
            QueryString(
                'SELECT COUNT(*) AS "count" FROM ({}) AS "subquery"',
                select.querystrings[0],
            )
        ]
