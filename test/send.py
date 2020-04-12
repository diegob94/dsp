from packetlib import Packet

packet = Packet('packet.yaml')
packet.val1 = 0x12
packet.val2 = -1234567890
for i in packet.stream:
    print(f"0x{i:X}")

