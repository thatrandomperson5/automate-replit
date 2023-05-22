from .basic import SimpleUser, BasicRepl
from ..commonTyping import JsonType
from .queryResult import QueryResultBase
from typing import Optional


class Repl(QueryResultBase):
    id: str
    isProject: bool
    isPrivate: bool
    isStarred: bool
    title: str
    slug: str
    imageUrl: str
    folderId: str
    isRenamed: bool
    commentCount: int
    likeCount: int
    currentUserDidLike: bool
    templateCategory: str
    wasPosted: bool
    wasPublished: bool
    layoutState: str
    language: str
    owner: SimpleUser
    origin: BasicRepl
    lang: JsonType  # Not yet wrapped
    iconUrl: str
    templateLabel: str
    url: str
    inviteUrl: Optional[str]
    multiplayerInvites: JsonType
    rootOriginReplUrl: str
    timeCreated: str
    timeUpdated: str
    isOwner: bool
    config: JsonType
    hostedUrl: str
    hostedUrlDotty: str
    hostedUrlDev: str
    hostedUrlNoCustom: str
    terminalUrl: str
    currentUserPermissions: JsonType
    database: JsonType
    template: JsonType
    isProjectFork: bool
    isModelSolution: bool
    isModelSolutionFork: bool
    workspaceCta: str
    commentSettings: JsonType
    publicForkCount: int
    runCount: int
    isAlwaysOn: bool
    isBoosted: bool
    tags: JsonType
    lastPublishedAt: str
    multiplayers: JsonType
    nixedLanguage: str
    publishedAs: str
    attachments: JsonType
    description: str
    markdownDescription: str
    hasExplainCode: bool
    hasGenerateCode: bool
    templateInfo: JsonType
    domains: JsonType
    replViewSettings: JsonType
    isTutorial: bool

    __slots__ = locals()["__annotations__"].keys()

    def __init__(self, data: JsonType, pathName: str = "repl") -> None:
        super().__init__(pathName, data)
