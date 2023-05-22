from autoreplit.querygen.user import UserByUsername

query = UserByUsername().user.id
print(query.render())
