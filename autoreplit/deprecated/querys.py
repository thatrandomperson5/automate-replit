from pathlib import Path


def readFile(path: str | Path) -> str:
    path = Path(path)
    root = Path(__file__)
    path = root.parent / path
    with open(path, "r") as f:
        return f.read()


querys = {
    "userByUsername": readFile("gql/userByUsername.gql"),
    "updatePresence": readFile("gql/updatePresence.gql"),
    "currentUser": readFile("gql/currentUser.gql"),
    "notifications": readFile("gql/notifications.gql"),
    "repl": readFile("gql/repl.gql"),
}
