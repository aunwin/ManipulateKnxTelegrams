from db_helpers import knxTelegram as dbTelegram
import baos_knx_parser as knx
import binascii


def set_hop_count(value, cemi):
    if value > 7 | value < 0:
        raise AssertionError('No hopecount smaler than 0 or larger than 7 allowed!')
    hop = (value)
    daf = (get_destintation_address_flag(cemi) << 3)
    hopcnt_daf_nipple = (hop | daf)

    additional_length = parse_length_of_additional_info(cemi)

    position = 6 + additional_length * 2    # 2 nipple pro additional Byte

    cemi = replace_nipple(position, hopcnt_daf_nipple, cemi)

    return cemi

#todo WIP - do not use this function
def set_src_address(src_address, cemi):

    area, line, device = src_address.split('.')
    area = int(area)
    line = int(line)
    device = int(device)

    if area > 15 | line > 15 | device > 255 | area < 0 | line < 0 | device < 0:
        raise AssertionError(f'Invalid src_address. Area = ({area}) or Line = ({line}) or Device = ({device}) value out of bounds!')

    device1 = device // 16
    device2 = device % 16

    additional_length = parse_length_of_additional_info(cemi)
    position = 8 + additional_length * 2    # 2 Nipple pro additional Byte

    new_cemi = bytearray(cemi)

    new_cemi[position] = ord((str(hex(area))[2]).upper()) #turn integer into hex = '0x?' -> Cut off '0x' -> capitalize Letter
    new_cemi[position+1] = ord((str(hex(line))[2]).upper()) #turn integer into hex = '0x?' -> Cut off '0x' -> capitalize Letter
    new_cemi[position+2] = ord((str(hex(device1))[2]).upper()) #turn integer into hex = '0x?' -> Cut off '0x' -> capitalize Letter
    new_cemi[position+3] = ord((str(hex(device2))[2]).upper()) #turn integer into hex = '0x?' -> Cut off '0x' -> capitalize Letter

    return bytes(new_cemi)

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
