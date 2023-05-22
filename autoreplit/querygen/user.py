from .querygen import OperationBase, QueryBase
from graphql_query import Variable


class UserQuery(QueryBase):
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

