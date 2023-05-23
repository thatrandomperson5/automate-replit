# Tests
import autoreplit, os, asyncio

sid = os.getenv("sid")
client = autoreplit.ReplitClient(sid)


transformer = """
query Repl($id: String, $url: String) {
repl(id: $id, url: $url) {
...on Repl {
  id
  title
  slug
}
}}"""


async def tRaw(id: str):
    repl = await client.rawQuery("repl", transformer, {"id": id})
    print(repl)


async def getEthan():
    ethan = await client.getUserByName("not-ethan")
    print(f"Ethan's id: {ethan.id}")
    print(f"Ethan's bio: {ethan.bio}")
    print(f"Ethan's follower count: {ethan.followerCount}")
    if ethan.isOnline:
        print("Ethan is online!")
    else:
        print(f"Ethan was last seen {ethan.lastSeen}")
    print(f"Ethan's roles: {ethan.roles}")
    print(ethan)


async def notif():
    notifs = await client.getNotifications(20, True)
    for item in notifs:
        print(item)


async def repl():
    print("Getting repl")
    r = await client.getReplByUrl("/@dragonhunter1/ChooseNim")
    print(r)
    assert r.url == (await client.getReplById(r.id)).url


async def main():
    current = await client.getCurrentUser()
    print(f"Logged in as {current.username}")
    await client.updatePresence()
    user = await client.getUserByName(current.username)
    print(user.followerCount)
    print(user.socials["github"])
    print(user.id)
    assert user.isFollowedByCurrentUser == False
    await getEthan()
    await notif()
    print(len(user.publicRepls))
    await repl()
    await asyncio.gather(*[tRaw(repl.id) for repl in user.publicRepls])
    print("Tests done!")


print()
client.run(main())
