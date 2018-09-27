from db_helpers import knxTelegram as dbTelegram
import baos_knx_parser as knx
import binascii


def set_hop_count(value, cemi):
    if value > 7 | value < 0:
        raise OverflowError('No hopecount smaler than 0 or larger than 7 allowed!')
    hop = (value)
    daf = (get_destintation_address_flag(cemi) << 3)
    hopcnt_daf_nipple = (hop | daf)

    additional_length = parse_length_of_additional_info(cemi)

    position = 6 + additional_length * 2    # 2 nipple pro additional Byte

    cemi = replace_nipple(position, hopcnt_daf_nipple, cemi)

    return cemi

def get_destintation_address_flag(cemi):
    parsed_telegram = knx.parse_knx_telegram(binascii.a2b_hex(cemi))
    return parsed_telegram.dest.is_group_address()

def replace_nipple(position, value, cemi):
    #todo get this crap done propperly! Ugly code will hunt you down! Zoombies are comming for ugly coders first! *uargh*
    mutable_cemi = bytearray(cemi)
    mutable_cemi[position] = ord((str(hex(value))[2]).upper()) #turn integer into hex = '0x?' -> Cut off '0x' -> capitalize Letter
    # possible alternative way might be something along the lines of
    #new_cemi = cemi[0:2] + bytes(int('1', 16)) + cemi[3:]

    cemi = (bytes(mutable_cemi))
    return cemi

def parse_length_of_additional_info(cemi):
    return int(cemi[2:4], 16)
