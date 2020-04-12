#include <stdio.h>
#include <stdint.h>
#include "tmp/packet.h"

void printpacket(Packet packet){
    printf("val1: %15d 0x%02X\n", packet.fields.val1, packet.fields.val1);
    printf("val2: %15d 0x%08X\n", packet.fields.val2, packet.fields.val2);
}

int main(){
    Packet packet;
    printf("sizeof(packet) %ld\n", sizeof(packet));
    packet.fields.val1 = 0x12;
    packet.fields.val2 = -1234567890;
    printpacket(packet);
    for(int i = 0; i < sizeof(packet.stream); i++){
        printf("depacket.stream[%d] = 0x%02X;\n", i, packet.stream[i]);
    }
    Packet depacket;
    depacket.stream[0] = 0x12;
    depacket.stream[1] = 0x2E;
    depacket.stream[2] = 0xFD;
    depacket.stream[3] = 0x69;
    depacket.stream[4] = 0xB6;
    printpacket(depacket);
}
