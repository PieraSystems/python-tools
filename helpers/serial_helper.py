import serial
import serial.tools.list_ports
import sys
import glob
import os
import logging


class TempPort:
    name = ""
    description = ""
    vid = 0
    pid = 0


def serial_ports():
    """ Lists serial port names (Mac & Linux)
        Modified version of https://stackoverflow.com/a/14224477/2489265

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            if port.startswith("/dev/tty.usb") or port.startswith("/dev/ttyUSB"):
                tempPort = TempPort()
                tempPort.name = port
                result.append(tempPort)
        except (OSError):
            pass
    return result


def serial_ports_win():
    """ Lists serial port names (Windows)

        :returns:
            A list of the serial ports available on the system
    """
    ports = serial.tools.list_ports.comports()
    result = []
    for port in ports:
        if isinstance(port.vid, int) and isinstance(port.pid, int):
            result.append(port)
    return result


def select_port():
    """ Gets list of serial ports and prompts user for selection

        :returns:
            Name of selected serial ports
    """
    if os.name == "nt":
        # it's windows
        ports = serial_ports_win()
    else:
        ports = serial_ports()
    if len(ports) == 0:
        input('No sensor found, make sure device is connected via USB and no other programs are using the COM port. Press any key to exit...')
        sys.exit()

    for index, port in enumerate(ports, start=1):
        print(" {}: {} ({}...) [{} {}]".format(
            index, port.name, port.description[:19], hex(port.vid), hex(port.pid)))
    print(" {}: ALL".format(len(ports) + 1))
    print("")
    port_names = []

    if len(sys.argv) > 1:
        if sys.argv[1].upper() == "ALL":
            for port in ports:
                port_names.append(port.name)
        else:
            port_names = [sys.argv[1].upper()]

    if not port_names:
        port_sel = input('Selection [1]: ')
        if not port_sel:
            port_names = [ports[0].name]
        elif int(port_sel.split()[0]) == len(ports) + 1:
            for port in ports:
                port_names.append(port.name)
        else:
            port_arr = port_sel.split()
            for port in port_arr:
                port_names.append(ports[int(port) - 1].name)
    else:
        print("Selected: " + sys.argv[1])

    return port_names


def open_port(port_name):
    """ Opens port_name using pySerial

        :returns:
            Serial object
    """
    return serial.Serial(port_name, 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, timeout=1, xonxoff=False, rtscts=False, write_timeout=1, dsrdtr=False, inter_byte_timeout=None)


def read_line(serial_con):
    """ Reads next line of serial output and attempts to decode bytes

        :returns:
            UTF-8 decoded string
    """
    ser_bytes = serial_con.readline()
    decoded_bytes = ""
    try:
        if ser_bytes:
            decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
    except UnicodeDecodeError:
        logging.debug("UnicodeDecodeError")
    return decoded_bytes
