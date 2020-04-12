from packetlib import Packet

packet = Packet('packet.yaml')
packet.val1 = 0xaa
packet.val2 = 1
for i in packet.stream:
    print(f"0x{i:X}")

