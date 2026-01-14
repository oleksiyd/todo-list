from dataclasses import dataclass
from enum import StrEnum

KEY_ALL="all"
KEY_PENDING="pending"
KEY_COMPLETED="completed"
KEY_CREATED_AT="createdAt"
KEY_DUE_DATE="dueDate"
KEY_TITLE="title"
KEY_ASC="asc"
KEY_DESC="desc"

class Status(StrEnum):
    ALL = KEY_ALL
    PENDING = KEY_PENDING
    COMPLETED = KEY_COMPLETED


class SortKey(StrEnum):
    CREATED_AT = KEY_CREATED_AT
    DUE_DATE = KEY_DUE_DATE
    TITLE = KEY_TITLE


class Order(StrEnum):
    ASC = KEY_ASC
    DESC = KEY_DESC


@dataclass(frozen=True)
class ListOptions:
    status: Status = Status.ALL
    sort: SortKey = SortKey.CREATED_AT
    order: Order = Order.DESC
