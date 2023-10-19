from util.serializable import Serializable


class DetectorReport(Serializable):
    def to_json(self):
        return {
            "phi": str(self.phi),
            "probability": str(self.probability),
        }

    @classmethod
    def from_json(cls, json_data):
        pass

    def __init__(self, phi: float, probability: float):
        self.phi: float = phi
        self.probability: float = probability
