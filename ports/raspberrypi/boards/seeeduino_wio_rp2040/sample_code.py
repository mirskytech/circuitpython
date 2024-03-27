from adafruit_bus_device.spi_device import SPIDevice
from digitalio import DigitalInOut, Direction
import board
import busio


class ESPAT:

    STATION_MODE = 1
    SOFT_AP_MODE = 2

    def __init__(self, mode=STATION_MODE):

        self.mode = mode

        self.wifi_handshake = DigitalInOut(board.ESP_HANDSHAKE)
        self.wifi_handshake.direction = Direction.OUTPUT

        self.wifi_reset = DigitalInOut(board.ESP_RESET)
        self.wifi_reset.direction = Direction.OUTPUT

        self.wifi_enable = DigitalInOut(board.ESP_ENABLE)
        self.wifi_enable.direction = Direction.OUTPUT

        self.wifi_power = DigitalInOut(board.ESP_POWER)
        self.wifi_power.direction = Direction.OUTPUT

        self.cs = DigitalInOut(board.ESP_CS)
        self.cs.direction = Direction.OUTPUT

        self.spi_bus = busio.SPI(board.ESP_CLK, MISO=board.ESP_MISO, MOSI=board.ESP_MOSI)
        self.spi_device = SPIDevice(self.spi_bus, self.cs, baudrate=200000)

    def power_on(self):
        """
        https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/mod_wifi_spi.c#L349
        """

        self.wifi_handshake.value = True
        self.wifi_enable.value = True
        self.wifi_reset.value = True

        # select chip
        self.cs.value = False

        # enable (?) power
        self.wifi_power.value = False

        self.wifi_handshake.switch_to_input()
        self.cs.value = True

        print("power on sequence complete")

    def wifi_init(self):
        # https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/wifi_spi.c#L1339
        raise NotImplementedError()

    def power_off(self):
        raise NotImplementedError()

    # AT over SPI message commands
    # MASTER_WRITE_DATA_TO_SLAVE = 2
    # MASTER_READ_DATA_FROM_SLAVE = 3
    # MASTER_WRITE_STATUS_TO_SLAVE = 1
    # MASTER_READ_STATUS_FROM_SLAVE = 4

    def send_at_command(self):
        """
            WIP : hardcoded AT\r\n sequence
        """
        # https://github.com/espressif/esp-at/tree/master/examples/at_spi_master/spi/esp32_c_series

        # handshake (ready) signal should be low before a request
        assert(not self.wifi_handshake.value)

        master_requests_send_to_slave = bytearray(b'\x01\x00\x00\xFE\x01\x04\x00')
        master_request_slave_status = bytearray(b'\x02\x04\x00\x00\x00\x00\x00')

        # STEP 1 : Master requests to send data
        # _note_ the `with` block handles verifying SPI lock and properly
        #        setting/unsetting CS, so all communication can't be within a single block
        with self.spi_device as spi:
            # TODO : set length of send based on size of data to be sent (currently fixed length because AT command)
            spi.write(master_requests_send_to_slave)

        # STEP 2a: ESP pulls up handshake pin
        print("wait for handshake")
        # TODO: add timeout error
        while not self.wifi_handshake.value:
            pass

        # STEP 2b: ESP requests slave status and reads the status value
        with self.spi_device as spi:
            spi.write(master_request_slave_status)
            slave_read = bytearray(7)
            spi.readinto(slave_read)

            # STEP 2c: check if slave status is ok (0x2)
            if not slave_read[3] & 0x2:
                raise ConnectionError('slave not ready')

        master_send_at_command = bytearray(b'\x03\x00\x00\x41\x54\0D\0A')  # AT\r\n
        master_send_done_command = bytearray(b'\07\x00\x00')

        # STEP 2d: master sends data (in this case AT command)
        # TODO : expand into loop for other data send
        with self.spi_device as spi:
            spi.write(master_send_at_command)

        # STEP 2e: master sends done command
        with self.spi_device as spi:
            spi.write(master_send_done_command)

        # STEP 3a: master reads slave status
        with self.spi_device as spi:
            spi.write(master_request_slave_status)
            slave_read = bytearray(7)
            spi.readinto(slave_read)
            if not slave_read[3] & 0x1:
                raise ConnectionError('slave not ready to send data')

            assert(slave_read[4] & 0x1)  # slave sequence numberd

            # TODO: use length to determine the number of reads needed in step 3b
            assert( (slave_read[5] << 1 | slave_read[6]) & 0x0400)  # slave data (in this case length)

        master_read_data_command = bytearray(b'\x04\x00\x00\x00\x00\x00\x00')
        master_read_done_command = bytearray(b'\x08\x00\x00')

        # STEP 3b: master read data
        with self.spi_device as spi:
            spi.write(master_read_data_command)
            slave_read = bytearray(7)
            spi.readinto(slave_read)

            # graphic shows b'\x00\x00\x00\x41\x54\x0D\x0A' which is AT\r\n,
            # but I think it should be b'\x4F\x4Bx\x0D\x0A' (OK\r\n)
            print(slave_read)

        # STEP 3c: master signals read is complete
        with self.spi_device as spi:
            spi.write(master_read_done_command)

    def send_command(self):
        # https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/wifi_spi.c#L753
        raise NotImplementedError()


if __name__ == "__main__":
    print("\n\ninitializing...\n")

    esp8285 = ESPAT()

    esp8285.power_on()
    esp8285.send_at_command()

print("\ncomplete\n")
