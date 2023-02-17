# Tests
import autoreplit, os

sid = os.getenv("sid")
client = autoreplit.ReplitClient(sid)


async def getEthan():
    ethan = await client.getUserByName("not-ethan")
    print(f"Ethan's id: {ethan.id}")
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


async def main():
    current = await client.getCurrentUser()
    print(f"Logged in as {current.username}")
    await client.updatePresence()
    user = await client.getUserByName(current.username)
    print(user.followerCount)
    print(user.socials["github"])
    print(user.id)
    assert user.isFollowedByCurrentUser == False
    # await getEthan()
    await notif()


print()
client.run(main())
