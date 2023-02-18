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
```
**Note**: pass a sid to get better info