import asyncio, aiohttp, aiolimiter
from .querys import querys
from .classes.user import User, SimpleUser
from .classes.queryResult import QueryResult, QueryResultBase
from .classes.notifications import makeNotification

# Typing
from types import CoroutineType
from .commonTyping import JsonType
from typing import Optional, Dict, Any, List


class RequestError(Exception):
    """Replit api request error."""

    pass


class ReplitClient:
    """The replit client object.
    This class is the centerpiece or the library,
    almost all of the functions are of this class.
    This should be the only object you need to import.

    :param sid: The replit account's secure ID, kind of like a token. Required for most actions but not all.
    """

    def __makeCookie(self) -> Dict[str, Optional[str] | int]:
        # Make the cookie needed to acess replit
        return {
            "connect.sid": self.sid,
            "replit_authed": 1,
        }
        # return f"connect.sid={self.sid}; replit_authed=1; replit_authed=1;"

    def __init__(self, sid: Optional[str] = None) -> None:  # Sid not always needed.
        self.sid = sid
        self.headers = {  # Headers needed to acess replit.
            "User-Agent": "replit",
            "Origin": "https://replit.com",
            "Referrer": "https://replit.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.8",
            "content-type": "application/json",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-requested-with": "XMLHttpRequest",
        }
        self.limiter = aiolimiter.AsyncLimiter(5)  # Current rate-limit is 5/s

    async def start(self) -> None:
        """Start the client, needs to be used first, before any other functions.

        .. warning::
           Never use with :meth:`autoreplit.ReplitClient.run`
        """
        cookies: Any = self.__makeCookie()
        self.client = aiohttp.ClientSession(cookies=cookies)

    async def close(self) -> None:
        """Close the client, needs to be run after everything is done.

        .. warning::
           Never use with :meth:`autoreplit.ReplitClient.run`
        """
        await self.client.close()

    def run(self, mainfunc: CoroutineType) -> None:
        """Run Coroutine mainfunc so that a replit client works withing.

        Uses a combination of :meth:`asyncio.run`, :meth:`autoreplit.ReplitClient.start` and
        :meth:`autoreplit.ReplitClient.close`
        """

        async def inner():
            await self.start()
            try:
                await mainfunc
            finally:
                await self.close()

        asyncio.run(inner())

    async def __gqlQuery(
        self, query: str, vars: JsonType, opname: Optional[str] = None
    ) -> JsonType:
        # Query replut graphql
        json: Dict[str, Any] = {}
        if opname != None:
            json["operationName"] = opname
        json = {"query": query, "variables": vars}
        session = self.client
        await self.limiter.acquire()  # Rate-limit
        async with session.post(
            "https://replit.com/graphql", json=json, headers=self.headers
        ) as response:
            if response.status != 200:
                raise RequestError(await response.text())  # Raise request errors
            json = await response.json()
            if "errors" in json:  # Raise other errors
                raise RequestError(json["errors"]["message"])
            return json

    async def rawQuery(
        self, queryname: str, query: str, vars: JsonType = {}
    ) -> QueryResult:
        """Use a raw gql query on the api. Returns a QueryResult object.

        :param queryname: The name of the query, for example ``UserByUsername``
        :param query: The actual graphql query
        :param vars: The variable params passed to the query
        """
        json = await self.__gqlQuery(query, vars, queryname)
        return QueryResult(queryname, json)

    async def getUserByName(self, name: str) -> User:
        """Get a user by name. Returns an user object."""
        query = querys["userByUsername"]
        result = await self.__gqlQuery(query, {"username": name}, "userByUsername")
        return User(result)

    async def getCurrentUser(self) -> SimpleUser:
        """Get the current user. Returns a ``SimpleUser``"""
        query = querys["currentUser"]
        result = await self.__gqlQuery(query, {}, "UpgradeModal")
        result = result["data"]["currentUser"]
        return SimpleUser(result["username"], result["id"])

    async def updatePresence(self) -> None:
        """Update your bot's presence, will set you to ``Online``"""
        query = querys["updatePresence"]
        await self.__gqlQuery(query, {}, "SitePresenceUpdate")

    async def getNotifications(
        self, count: int = 10, seen: bool = False
    ) -> List[QueryResultBase]:
        query = querys["notifications"]
        result = await self.__gqlQuery(
            query, {"count": count, "seen": seen}, "notifications"
        )
        return makeNotification(result)
