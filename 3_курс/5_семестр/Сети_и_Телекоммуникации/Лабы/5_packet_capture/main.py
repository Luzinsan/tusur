from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
import time
import binascii

# будем отправлять данные сами себе
ip, mac = '192.168.43.44', '00:F4:8D:EF:72:8D'
# dst_port – порт получателя, src_port – порт отправителя
dst_port, src_port = 11111, 11110
# packet_count - количество отправляемых пакетов, n - счетчик пакетов
packet_count, n = 1000, 1
# Формирование тестовых данных
gen_data = [f'{i:02x}' for i in range(1, 129)]
gen_data_str = ''.join(gen_data)

while n <= packet_count:
    # Добавление текущего времени в начало паекты данных
    curr_t = time.localtime()
    h, m, s = curr_t.tm_hour, curr_t.tm_min, curr_t.tm_sec
    # Формирование итоговых данных для отправки
    data = binascii.unhexlify(f'{h:02x}{m:02x}{s:02x}{gen_data_str}')
    # Формирование и отправка UDP-пакета
    sendp(Ether(dst=mac)/
          IP(dst=ip)/
          UDP(sport=src_port, dport=dst_port, chksum=0x0000)/
          data)
    # Задержка на 0.1 сек
    time.sleep(0.1)
    n += 1
