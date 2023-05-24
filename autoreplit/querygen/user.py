from .querygen import OperationBase, QueryBase
from .utils import TypedField
from graphql_query import Variable, Argument


class UserQuery(QueryBase):
    id: TypedField[int]  #: User's id
    username: TypedField[str]  #: User's username
    image: TypedField[str]  #: User's pfp
    url: TypedField[str]  #: Path to the users profile
    followerCount: TypedField[int]  #: How many followers the user has
    followCount: TypedField[int]  #: How many people the user is following
    isFollowedByCurrentUser: TypedField[bool]  # Self explanitory
    isFollowingCurrentUser: TypedField[bool]
    isBlockedByCurrentUser: TypedField[bool]
    isBlockingCurrentUser: TypedField[bool]
    fullName: TypedField[str]  #: The user's full name
    hasPrivacyRole: TypedField[bool]  #: Replit students under the age of 13 (probably)
    userSubscriptionType: TypedField[
        str
    ]  #: User's plan, eg. ``"HACKER"``. ``None`` if the user has no plan

    #: A dictonary of roles, keys are the role key, eg. ``"MODERATOR"``.
    #: The values are of the :class:`.Role` class.
    # roles: Dict[str, Role]

    # publicRepls: List[BasicRepl]  #: A list of the user's public repl's ids.
    presenceStatus: None  #: :meta private:

    #: ``True`` if the user is online
    #:
    #: .. note::
    #:   Always ``False`` if no SID is provided.
    isOnline: TypedField[bool]

    #: Date-Time str of the users last status update.
    #:
    #: .. note::
    #:   Always ``None`` if no SID is provided.
    lastSeen: TypedField[str]
    bio: str  #: User description

    #: A dictonary of social contacts, keys are the social type, eg. ``"github"``.
    #: The values are of the :class:`.Social` class.
    # socials: Dict[str, Social]

    firstName: TypedField[str]
    lastName: TypedField[str]
    locale: TypedField[str]
    isVerified: TypedField[bool]
    displayName: TypedField[str]
    
    def __init__(self):
        usernameArg = Argument(
            name="username", value=Variable(name="username", type="String!")
        )
        super().__init__(name="userByUsername", arguments=[usernameArg])


class UserByUsername(OperationBase):
    user: UserQuery  # userByUsername

    def __init__(self):

        usernameVar = Variable(name="username", type="String!")
        super().__init__(
            type="query", name="UserByUsername", variables=[usernameVar], queries=[]
        )

