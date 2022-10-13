import sys
import threading
import time
import os
# if os.name == 'nt':
#     import msvcrt
import helpers.input_helper as input_helper
import helpers.serial_helper as serial_helper

wifi_ssid = 'ssid'
wifi_pwd = 'password'

# Use Ctrl-C to exit
EXIT_COMMAND = "\x03"

def serial_thread(port_name):
    """ Uses a separate thread for each serial port so multiple devices can be updated at the same time

    """
    confirm_ssid = False
    confirm_pwd = False
    serial_con = serial_helper.open_port(port_name)
    time.sleep(3)
    serial_con.write((f'$Wssid={wifi_ssid}\r\n').encode())
    time.sleep(1)
    serial_con.write((f'$Wpwd={wifi_pwd}\r\n').encode())
    time.sleep(1)
    serial_con.write(('$Wreset=1\r\n').encode())
    time.sleep(2)
    serial_con.write(('$Dflash=\r\n').encode())
    while 1:
        if serial_con.in_waiting:
            line = serial_helper.read_line(serial_con)
            # print(line)
            if line[0:6] == "WIFI_S":
                device_wifi_ssid = line[10:]
                if wifi_ssid != device_wifi_ssid:
                    print(f'Error writing WiFi SSID to {port_name}')
                confirm_ssid = True
            elif line[0:6] == "WIFI_P":
                device_wifi_pwd = line[9:]
                if wifi_pwd != device_wifi_pwd:
                    print(f"Error writing WiFi password to {port_name}")
                confirm_pwd = True
        # If SSID and password have been found, break while loop and end thread
        if confirm_ssid & confirm_pwd:
            break
        time.sleep(0.01) 

def main():
    print("")
    print("Update WiFi 1.0 (ctrl-c to quit)")
    print("")
    ports = serial_helper.select_port()
    s_threads = []
    input_helper.input_init()
    for port in ports:
        new_thread = threading.Thread(target=serial_thread, args=(port,))
        new_thread.daemon = True
        new_thread.start()
        s_threads.append(new_thread)
    print("")
    print("Please wait, this will take about 10 seconds...")

    try:
        while True:
            try:
                input_str = input_helper.check_input()
            except KeyboardInterrupt:
                input_helper.input_deinit()
                sys.exit()
            if input_str:
                if (input_str == EXIT_COMMAND):
                    print("Exiting serial monitor.")
                    break
            if len(threading.enumerate()) <= 2:
                print("")
                print("Finished, if there were any errors they will be displayed above.")
                input_helper.input_deinit()
                sys.exit()
            time.sleep(0.1)
    except KeyboardInterrupt:
        input_helper.input_deinit()
        sys.exit()
    

if (__name__ == '__main__'): 
    main()