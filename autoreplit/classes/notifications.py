from ..commonTyping import JsonType
from .user import SimpleUser
from .queryResult import QueryResultBase
from typing import List, Optional, cast
from warnings import warn
from .comments import BasicComment


class CommonNotif(QueryResultBase):
    """The most common stucture for notifications. Look at ``notifications.gql`` for more details."""

    id: str  #: Notification id
    timeCreated: str  #: Time the notification was created
    seen: bool  #: If the user saw the notification
    creator: SimpleUser  #: The notification's creator
    replComment: Optional[
        BasicComment
    ]  #: The linked comment, if the type is a comment notif
    type: str  #: Notif type
    url: Optional[str]  #: Notif url

    __slots__ = locals()["__annotations__"].keys()

    def __init__(self, json: JsonType) -> None:
        json["type"] = json["__typename"]
        del json["__typename"]
        super().__init__(None, json)
        self.creator = SimpleUser(
            cast(JsonType, self.creator)["username"], cast(JsonType, self.creator)["id"]
        )
        if not self.replComment is None:
            self.replComment = BasicComment(cast(JsonType, self.replComment))


class UnidentifiedNotif(QueryResultBase):
    """Unidentified notification. Will produce a warning, please featrue request support for the unidentified type."""

    def __init__(self, json: JsonType) -> None:
        json["type"] = json["__typename"]
        del json["__typename"]
        super().__init__(None, json)


def makeNotification(json: JsonType) -> List[QueryResultBase]:
    """Sort and type notif's."""
    data = json["data"]["notifications"]["items"]
    result: List[QueryResultBase] = []
    for item in data:
        match item["__typename"]:
            case "ReplCommentCreatedNotification" | "ReplCommentReplyCreatedNotification" | "ReplCommentMentionNotification" | "NewFollowerNotification":
                result.append(CommonNotif(item))
            case _:
                warn(f"Unwrapped and Unidentified notif {item['__typename']}")
                result.append(UnidentifiedNotif(item))
    return result
