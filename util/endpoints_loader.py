import json

from network.endpoint import Endpoint


def load_endpoints():
    with open("endpoints.json", "r") as file:
        endpoint_data = json.load(file)

    return [Endpoint.from_json(data) for data in endpoint_data]
