import sys
import time
import helpers.input_helper as input_helper
import helpers.serial_helper as serial_helper

# Use Ctrl-C to exit
EXIT_COMMAND = "\x03"

def main():
    print("")
    print("Serial Monitor 1.0 (ctrl-c to quit)")
    print("")
    port_name = serial_helper.select_port()[0]
    print("Opening " + port_name + "...")
    serial_con = serial_helper.open_port(port_name)
    time.sleep(1)

    # View the device settings
    serial_con.write('$Dflash=\r\n'.encode())

    input_helper.input_init()

    try:
        while (True):
            try:
                input_str = input_helper.check_input()
            except KeyboardInterrupt:
                input_helper.input_deinit()
                sys.exit()
            if input_str:
                if (input_str == EXIT_COMMAND):
                    print("Exiting...")
                    break
                else:
                    serial_con.write((input_str + "\r\n").encode())
            
            # Check input buffer
            if serial_con.in_waiting:
                line = serial_helper.read_line(serial_con)
                print(line)
            time.sleep(0.01) 
    except KeyboardInterrupt:
        input_helper.input_deinit()
        sys.exit()
    
    input_helper.input_deinit()

if (__name__ == '__main__'): 
    main()