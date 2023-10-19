from enum import Enum


class MessageCodes(Enum):
    UNKNOWN = "UNK"

    GOSSIP_SYNC_CODE = "GSM"
    GOSSIP_ACK_CODE = "GAM"
    GOSSIP_ACK_CONFIRM_CODE = "GACM"

    INFO_REQUEST = "IRQM"

    INFO_RESPONSE = "IRSM"

    @staticmethod
    def from_str(label: str):
        if label in ('UNKNOWN', 'UNK'):
            return MessageCodes.UNKNOWN
        elif label in ('GOSSIP_SYNC_CODE', 'GSM'):
            return MessageCodes.GOSSIP_SYNC_CODE
        elif label in ('GOSSIP_ACK_CODE', 'GAM'):
            return MessageCodes.GOSSIP_ACK_CODE
        elif label in ('GOSSIP_ACK_CONFIRM_CODE', 'GACM'):
            return MessageCodes.GOSSIP_ACK_CONFIRM_CODE
        elif label in ('INFO_REQUEST', 'IRQM'):
            return MessageCodes.INFO_REQUEST

        return MessageCodes.UNKNOWN
