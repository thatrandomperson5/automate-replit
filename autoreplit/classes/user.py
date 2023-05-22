from dataclasses import dataclass
from ..commonTyping import JsonType
from .queryResult import QueryResultBase
from .basic import BasicRepl
from typing import Dict, List, Optional


@dataclass
class Social:
    """Social contact object, like ``"github"``"""

    id: int
    url: str
    type: str


@dataclass
class Role:
    """A role object, provides role id, name, key and tagline. Keys are all caps."""

    id: str
    name: str
    key: str
    tagline: str


class User(QueryResultBase):
    """The user object. Contains user data."""

    id: int  #: User's id
    username: str  #: User's username
    image: str  #: User's pfp
    url: str  #: Path to the users profile
    followerCount: int  #: How many followers the user has
    followCount: int  #: How many people the user is following
    isFollowedByCurrentUser: bool  # Self explanitory
    isFollowingCurrentUser: bool
    isBlockedByCurrentUser: bool
    isBlockingCurrentUser: bool
    fullName: str  #: The user's full name
    hasPrivacyRole: bool  #: Replit students under the age of 13 (probably)
    userSubscriptionType: Optional[
        str
    ]  #: User's plan, eg. ``"HACKER"``. ``None`` if the user has no plan

    #: A dictonary of roles, keys are the role key, eg. ``"MODERATOR"``.
    #: The values are of the :class:`.Role` class.
    roles: Dict[str, Role]

    publicRepls: List[BasicRepl]  #: A list of the user's public repl's ids.
    presenceStatus: None  #: :meta private:

    #: ``True`` if the user is online
    #:
    #: .. note::
    #:   Always ``False`` if no SID is provided.
    isOnline: bool

    #: Date-Time str of the users last status update.
    #:
    #: .. note::
    #:   Always ``None`` if no SID is provided.
    lastSeen: Optional[str]
    bio: str  #: User description

    #: A dictonary of social contacts, keys are the social type, eg. ``"github"``.
    #: The values are of the :class:`.Social` class.
    socials: Dict[str, Social]

    firstName: Optional[str]
    lastName: Optional[str]
    locale: str
    isVerified: bool
    displayName: str

    __slots__ = locals()["__annotations__"].keys()

    def __makePublicRepls(self):
        pr = self.publicRepls
        self.publicRepls = []
        for item in pr["items"]:
            self.publicRepls.append(BasicRepl(item["id"], item["url"], item["title"]))

    def __makePresenceStatus(self):
        for k, v in self.presenceStatus.items():
            self.__setattr__(k, v)
        self.presenceStatus = None

    def __makeRoles(self):
        oroles = self.roles  # Old roles
        self.roles = {}
        for item in oroles:
            self.roles[item["key"]] = Role(
                item["id"], item["name"], item["key"], item["tagline"]
            )

    def __makeSocials(self):
        osocials = self.socials
        self.socials = {}
        for item in osocials:
            self.socials[item["type"]] = Social(item["id"], item["url"], item["type"])

    def __init__(self, data: JsonType, pathName: str = "userByUsername") -> None:
        super().__init__(pathName, data)
        self.__makePublicRepls()
        self.__makePresenceStatus()
        self.__makeRoles()
        self.__makeSocials()
