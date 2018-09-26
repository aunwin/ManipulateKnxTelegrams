from db_helpers import knxTelegram as dbTelegram
import baos_knx_parser as knx
import binascii


def setHopCount(value, cemi):
    parsedTelegram = knx.parse_knx_telegram(binascii.a2b_hex(cemi))
    print(parsedTelegram.to_binary())
    return cemi
