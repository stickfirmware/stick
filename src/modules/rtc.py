class BM8563:
    def __init__(self, i2c, addr=0x51):
        self.i2c = i2c
        self.addr = addr

    def bcd2dec(self, bcd):
        return (bcd // 16) * 10 + (bcd % 16)

    def dec2bcd(self, dec):
        return (dec // 10) * 16 + (dec % 10)

    def get_time(self):
        data = self.i2c.readfrom_mem(self.addr, 0x02, 7)
        seconds = self.bcd2dec(data[0] & 0x7F)
        minutes = self.bcd2dec(data[1] & 0x7F)
        hours = self.bcd2dec(data[2] & 0x3F)
        day = self.bcd2dec(data[3] & 0x3F)
        weekday = self.bcd2dec(data[4] & 0x07)
        month = self.bcd2dec(data[5] & 0x1F)
        year = self.bcd2dec(data[6]) + 2000
        return (year, month, day, weekday, hours, minutes, seconds, 0)
    
    def set_time(self, datetime_tuple):
        year, month, day, weekday, hours, minutes, seconds, _ = datetime_tuple
        year -= 2000
        data = bytes([
            self.dec2bcd(seconds),
            self.dec2bcd(minutes),
            self.dec2bcd(hours),
            self.dec2bcd(day),
            self.dec2bcd(weekday),
            self.dec2bcd(month),
            self.dec2bcd(year)
        ])
        self.i2c.writeto_mem(self.addr, 0x02, data)
