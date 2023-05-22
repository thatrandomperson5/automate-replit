from argparse import ArgumentParser
import json
from graphql.parser import GraphQLParser


def makeSchema(ast):
    print(ast)
    return dict()


def extractRequests(args):
    with open(args.request) as f:
        request = json.load(f)
    parser = GraphQLParser()
    query = parser.parse(request["query"])
    with open(args.response) as f:
        response = json.load(f)
    output = {
        "querySchema": makeSchema(query),
        "operationName": request["operationName"],
        "varSchema": dict(),
    }
    if args.output is None:
        with open("schema.json", "w") as f:
            json.dump(output, f, indent=4)
        print("Made schema.json")
    else:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=4)
        print(f"Made {args.output}")


def main():
    parser = ArgumentParser(
        prog="Schema Gen",
        description="Automatically convert GQL requests and results to a usable json format, and convert that to docs and code!",
    )
    subparsers = parser.add_subparsers()
    extract = subparsers.add_parser("extract")
    extract.add_argument("request")
    extract.add_argument("response")
    extract.add_argument("-o", "--output")
    extract.set_defaults(func=extractRequests)

    args = parser.parse_args()
    args.func(args)
