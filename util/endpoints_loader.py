import json

from network.endpoint import Endpoint
from util.singletone import Singleton


class EndpointsLoader(metaclass=Singleton):

    def __init__(self):
        load_endpoints_map = self.load_endpoints()
        self.endpoints = load_endpoints_map['endpoints']
        self.cluster_id = load_endpoints_map['cluster_id']

    @staticmethod
    def load_endpoints():
        with open("endpoints.json", "r") as file:
            endpoint_data = json.load(file)

        ep = list([Endpoint.from_json(data) for data in endpoint_data["endpoints"]])

        return {"endpoints": ep, "cluster_id": endpoint_data["cluster_id"]}
