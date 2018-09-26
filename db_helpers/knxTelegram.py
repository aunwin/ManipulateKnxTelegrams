class KnxTelegram:
    sequence_number = None  # Not interesting - not included in cEMI
    timestamp = None  # Not interesting - not included in cEMI
    source_addr = None  # Byte 4:6
    destination_addr = None  # Byte 6:8
    apci = None  # Byte 9: (Bits 6:)
    tpci = None  # Byte 9: (Bits 0:6/8)
    priority = None  # Byte 2 (Bits 4:6)
    repeated = None  # Byte 2 (Bit 2:3)
    hop_count = None  # Byte 3 (Bits 1:4)
    apdu = None  # Bytes 9:
    payload_length = None  # Byte 8:9
    cemi = None  # value to be calculated/checked
    is_manipulated = None  # Not interesting - not included in cEMI
    attack_type_id = None  # Not interesting - not included in cEMI
