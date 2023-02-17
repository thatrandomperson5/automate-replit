from autoreplit import ReplitClient

client = ReplitClient()


async def getEthan():
    ethan = await client.getUserByName("not-ethan")
    print(f"Ethan's id: {ethan.id}")
    print(f"Ethan's follower count: {ethan.followerCount}")
    if ethan.isOnline:
        print("Ethan is online!")
    else:
        print(f"Ethan was last seen {ethan.lastSeen}")
    print(f"Ethan's roles: {ethan.roles}")
    print(f"All of ethan: {ethan}")


client.run(getEthan())
