import asyncio, aiohttp, aiolimiter
from .querys import querys
from .classes.user import User
from .classes.basic import SimpleUser
from .classes.queryResult import QueryResult
from .classes.notifications import makeNotification, UnidentifiedNotif, CommonNotif
from .classes.repl import Repl
from dataclasses import dataclass
import traceback

# Typing
from types import CoroutineType
from .commonTyping import JsonType
from typing import Optional, Dict, Any, List, Callable
from functools import wraps


@dataclass
class CachedRequest:
    """A cached request for better preformance."""

    fut: asyncio.Future
    json: JsonType


class RequestError(Exception):
    """Replit api request error."""

    pass

def requiresSid(f: Callable) -> Callable:
    """Decorator to make a function require a sid to run."""
    @wraps(f)
    def inner(self, *args, **kwargs: Any) -> Any:
        if self.sid is None:
            raise ValueError("This method requries a sid in the client.")
        return f(self, *args, **kwargs)
    return inner

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
        self.limiter = aiolimiter.AsyncLimiter(5, 1)  # Current rate-limit is 5/s
        self.requestCache: List[CachedRequest] = []
        # self.activeRequestCalls: int = 0

    async def __clearCache(self) -> None:
        """Clear the cache and request data in groups of 5"""
        amount = min(5, len(self.requestCache))
        session = self.client
        rqs = self.requestCache[:amount]
        if len(rqs) == 0:
            return
        # print("Emptying cached objects")
        rjson = [rq.json for rq in rqs]
        async with session.post(
            "https://replit.com/graphql", json=rjson, headers=self.headers
        ) as response:
            # print("Request made")
            if response.status != 200:
                errText = await response.text()
                for rq in rqs:
                    # print("Resolving errored hash (L93)", hash(rq.fut))

                    rq.fut.set_exception(
                        RequestError(errText)
                    )  # Raise request errors for the batch
                    # assert rq.fut.done()
                    self.requestCache.remove(rq)
                # print("Futures Errored")
                # del self.requestCache[:amount]
                return

            json = await response.json()
            # print("Json parsed")
            # print("Packed and requested:", len(json), ". Futures left:", len(self.requestCache))
            for result, rq in zip(json, rqs):
                if not rq in self.requestCache[:amount]:
                    continue
                if "errors" in result:  # Raise other errors
                    # print(result["errors"])
                    # print("Resolving errored hash (L110)", hash(rq.fut))

                    rq.fut.set_exception(RequestError(result["errors"][0]["message"]))
                    # print(rq.fut.done())
                else:
                    # print("Resolving hash (L115)", hash(rq.fut))

                    rq.fut.set_result(result)
                # assert self.requestCache.find(rq.fut).done()
                self.requestCache.remove(rq)

            # del self.requestCache[:amount]

    async def __request(self) -> bool:
        """Request a cache clearing, returns false if the request was dissmissed."""
        # print("Request: Awaiting limiter", self.limiter.has_capacity())
        if len(self.requestCache) < 1:
            # print("Request Dismissed")
            return False
        await self.limiter.acquire()
        # print("Limiter aquired")
        if len(self.requestCache) > 0:
            # print("Clearing cache")
            await self.__clearCache()

            return True

        return False

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

    def __checkTask(self, task):
        task.remove_done_callback(self.__checkTask)
        exc = task.exception()
        if exc is not None:
            amount = min(5, len(self.requestCache))
            rqs = self.requestCache[:amount]
            for rq in rqs:

                err = RequestError("Failed to send end request: \n" + "".join(traceback.format_exception(exc)))
                # print("Resolving errored hash ", hash(rq.fut))
                rq.fut.set_exception(err)
                self.requestCache.remove(rq)
            raise exc
        # print("Task ended, current futures left: ", len(self.requestCache))

    def __gqlQuery(
        self, query: str, vars: JsonType, opname: Optional[str] = None
    ) -> asyncio.Future[JsonType]:
        # Query replit graphql
        json: Dict[str, Any] = {}
        if opname != None:
            json["operationName"] = opname
        json = {"query": query, "variables": vars}

        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self.requestCache.append(CachedRequest(fut, json))
        # print("Added to cache, now requesting")
        # print("Task created")
        task = loop.create_task(self.__request())
        task.add_done_callback(self.__checkTask)
        # await self.__request()
        return fut

    async def rawQuery(
        self, queryname: str, query: str, vars: JsonType = {}
    ) -> QueryResult:
        """Use a raw gql query on the api. Returns a QueryResult object.

        :param queryname: The name of the query, for example ``UserByUsername``
        :param query: The actual graphql query
        :param vars: The variable params passed to the query
        """
        json = await self.__gqlQuery(query, vars, queryname)
        # print(json)
        return QueryResult(queryname, json)

    async def getUserByName(self, name: str) -> User:
        """Get a user by name. Returns an user object."""
        query = querys["userByUsername"]
        result = await self.__gqlQuery(query, {"username": name}, "userByUsername")
        return User(result)

    @requiresSid
    async def getCurrentUser(self) -> SimpleUser:
        """Get the current user. Returns a ``SimpleUser``"""
        query = querys["currentUser"]
        result = await self.__gqlQuery(query, {}, "UpgradeModal")
        result = result["data"]["currentUser"]
        return SimpleUser(result["username"], result["id"])

    @requiresSid
    async def updatePresence(self) -> None:
        """Update your bot's presence, will set you to ``Online``"""
        query = querys["updatePresence"]
        await self.__gqlQuery(query, {}, "SitePresenceUpdate")


    async def getReplById(self, id: str) -> Repl:
        query = querys["repl"]
        result = await self.__gqlQuery(query, {"id": id}, "repl")
        return Repl(result)

    async def getReplByUrl(self, url: str) -> Repl:
        query = querys["repl"]
        result = await self.__gqlQuery(query, {"url": url}, "repl")
        return Repl(result)

    @requiresSid
    async def getNotifications(
        self, count: int = 10, seen: bool = False
    ) -> List[CommonNotif | UnidentifiedNotif]:
        """Get ``count`` amount of notifications for the current user."""
        query = querys["notifications"]
        result = await self.__gqlQuery(
            query, {"count": count, "seen": seen}, "notifications"
        )
        return makeNotification(result)
