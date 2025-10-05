import esp32
import machine

p = esp32.Partition.find(esp32.Partition.TYPE_DATA, label='nvs')[0]

for x in range(int(p.info()[3] / 4096)):
    p.writeblocks(x, bytearray(4096))

machine.reset()
