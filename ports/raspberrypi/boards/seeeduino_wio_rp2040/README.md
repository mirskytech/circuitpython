Thanks to all for previous investigations!


### References

- https://forum.seeedstudio.com/t/trying-to-port-circuitpython-to-wio-rp2040/262857
- https://www.pcbway.com/project/shareproject/The_Adventures_of_Porting_Circuitpython_to_Wio_RP2040_71757d3b.html

### Datasheets

- https://www.espressif.com/sites/default/files/documentation/0a-esp8285_datasheet_en.pdf

### Connections

I created a circuitpython branch (soon to be a pull request) for the wio2040 port:

https://github.com/adafruit/circuitpython/commit/7a90ad3aa430ad70d4cc8faf8f92bcfc884a111e

included in the commit is a schematic received from seeed with the connections between the 2040 and the 8285, most
notably the spi connection between signals, confirming findings from previously referenced posts:


- GPIO8 --> HSPI_MISO
- GPIO9 --> HSPI_CS
- GPIO10 --> HSPI_CLK
- GPIO11 --> HSPI_MOSI

Other signals are further clarified:
- RST is GPIO22 (connected to 8285 reset)
- WAKEUP is GPIO23 (connected to the XPD_DCDC on the 8285 for deep-sleep wakeup)
- ENABLE is GPIO24 (connected to 8285 enable)
- POWER is GPIO25 (enables/disables power to the entire 8285, presumably because even when ENABLE is low, the 8285 draws power)


### Power On Sequence

The power on / initialization sequence for the 8285:

https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/mod_wifi_spi.c#L349

To decode:

21 is the handshake signal
22 is wifi reset
24 is wifi enable
25 is wifi power
SPI_CS is GPIO9

so the power on sequence seems to be:

handshake, reset, enable are set to high
chip is selected (cs to low)
power is low **
handshake changed to input
cs is deselected (cs to high)

eInit is then called which sends a variety of AT commands.

https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/wifi_spi.c#L1339

** Note: this would seem to disable the esp8285 based on the schematic? TBD

the circuitpython equivalent:

```circuitpython
import board
import digitalio

wifi_handshake = digitalio.DigitalInOut(board.ESP_HANDSHAKE)
wifi_handshake.direction = digitalio.Direction.OUTPUT

wifi_reset = digitalio.DigitalInOut(board.ESP_RESET)
wifi_reset.direction = digitalio.Direction.OUTPUT
wifi_reset.value = False

wifi_enable = digitalio.DigitalInOut(board.ESP_ENABLE)
wifi_enable.direction = digitalio.Direction.OUTPUT


wifi_power = digitalio.DigitalInOut(board.ESP_POWER)
wifi_power.direction = digitalio.Direction.OUTPUT

cs = digitalio.DigitalInOut(board.ESP_CS)
cs.direction = digitalio.Direction.OUTPUT


wifi_handshake.value = True  # GP21
wifi_enable.value = True  # GP24
wifi_reset.value = True # GP22

cs.value = False # SPI_CS
wifi_power.value = False  #GP25

wifi_handshake.direction = digitalio.Direction.INPUT
cs.value = True # SPI_CS

```

### Sending AT commands over SPI

SPI is faster than UART in communication with the 8285, but requires a few more steps to send an AT command and receive a response.

The sequence is explained here: https://docs.espressif.com/projects/esp-at/en/release-v2.2.0.0_esp32c3/Compile_and_Develop/How_to_implement_SPI_AT.html

As implemented by Seeed in micropython's source code: https://github.com/IsQianGe/rp2040-spi/blob/master/ports/rp2/wifi_spi.c#L753

#### Work In Progress

Using the basic [AT command send/receive](https://github.com/espressif/esp-at/tree/master/examples/at_spi_master/spi/esp32_c_series) sequence to test connection:

- [pin initialization sequence](sample_code.py#L12)
- [power on es8285 sequence](sample_code.py#L34)
- [send AT command and read response](sample_code.py#L67)

