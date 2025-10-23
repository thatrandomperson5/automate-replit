# NOTICE: This project will likley no longer be maintained

# Automate Replit
[![Documentation Status](https://readthedocs.org/projects/automate-replit/badge/?version=latest)](https://automate-replit.readthedocs.io/en/latest/?badge=latest)


Automate replit actions with this replit api wrapper!

## Docs
Documentation for this library can be found [here](https://automate-replit.readthedocs.io/en/docs/)

## Source
Source can be found [here](https://github.com/thatrandomperson5/automate-replit)

## Example
```py
from autoreplit import ReplitClient

client = ReplitClient()

async def getUser():
    user = await client.getUserByName("username")
    print(f"User's id: {user.id}")
    print(f"User's follower count: {user.followerCount}")
    if user.isOnline:
        print("User is online!")
    else:
        print(f"User was last seen {user.lastSeen}")
    print(f"User's roles: {user.roles}")
    print(f"All of user: {user}")

client.run(getUser())
```
**Note**: pass a sid to get better info
