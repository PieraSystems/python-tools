from datetime import datetime
import os
import sys
import threading
import time
import helpers.input_helper as input_helper
import helpers.serial_helper as serial_helper

valid_keys = ["PC0.1", "PC0.3", "PC0.5", "PC1.0", "PC2.5", "PC5.0", "PC10",\
        "PM0.1", "PM0.3", "PM0.5", "PM1.0", "PM2.5", "PM5.0", "PM10",\
        "TEMP", "HUMID", "VOCAQI"]

# Use Ctrl-C to exit
EXIT_COMMAND = "\x03"

def serial_thread(port_name):
    serial_con = serial_helper.open_port(port_name)
    serial_num = ""
    file_name = ""
    f = 0
    while 1:
        if serial_con.in_waiting:
            line = serial_helper.read_line(serial_con)
            # print(line)
            serial_values = line.split(',')
            parsed_values = {}
            if not serial_num and (len(serial_values) >= 29):
                if  len(serial_values) == 43:
                    serial_num = serial_values[-1:][0]
                else: 
                    serial_num = serial_values[-2:][0]
                print("Found: ", serial_num)
                now = datetime.now()
                time_now = now.astimezone().strftime("%m%d%y-%H%M%S")
                file_name = "logs/{}-{}.csv".format(serial_num, time_now)
                f = open(file_name, "a")
                f.write( "Name,Time,PC0.1,PC0.3,PC0.5,PC1.0,PC2.5,PC5.0,PC10,PM0.1,PM0.3,PM0.5,PM1.0,PM2.5,PM5.0,PM10,Temp,RH,VOC\n")
                f.close()
            for index2, value in enumerate(serial_values):
                if value in valid_keys:
                    # print(serial_values[index2 + 1])
                    parsed_values[value] = serial_values[index2 + 1]
            if len(parsed_values) == 14:
                now = datetime.now()
                time_now = now.astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")
                timezone = now.astimezone().strftime("%Z")
                if timezone.startswith("Pacific Day"):
                    timezone = "PDT"
                f = open(file_name, "a")
                f.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},-274,-1,-1\n".format(serial_num,time_now + " " + timezone,\
                    parsed_values["PC0.1"],parsed_values["PC0.3"],parsed_values["PC0.5"],parsed_values["PC1.0"],parsed_values["PC2.5"],parsed_values["PC5.0"],parsed_values["PC10"],\
                    parsed_values["PM0.1"],parsed_values["PM0.3"],parsed_values["PM0.5"],parsed_values["PM1.0"],parsed_values["PM2.5"],parsed_values["PM5.0"],parsed_values["PM10"]))
                f.close()
            if len(parsed_values) == 17:
                now = datetime.now()
                time_now = now.astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")
                timezone = now.astimezone().strftime("%Z")
                if timezone.startswith("Pacific Day"):
                    timezone = "PDT"
                f = open(file_name, "a")
                f.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(serial_num,time_now + " " + timezone,\
                    parsed_values["PC0.1"],parsed_values["PC0.3"],parsed_values["PC0.5"],parsed_values["PC1.0"],parsed_values["PC2.5"],parsed_values["PC5.0"],parsed_values["PC10"],\
                    parsed_values["PM0.1"],parsed_values["PM0.3"],parsed_values["PM0.5"],parsed_values["PM1.0"],parsed_values["PM2.5"],parsed_values["PM5.0"],parsed_values["PM10"],\
                    parsed_values["TEMP"],parsed_values["HUMID"],parsed_values["VOCAQI"]))
                f.close()
        time.sleep(0.01) 

def main():
    if not os.path.exists("logs"):
        os.mkdir("logs")
    ports = serial_helper.select_port()
    input_helper.input_init()
    s_threads = []
    for port in ports:
        new_thread = threading.Thread(target=serial_thread, args=(port,))
        new_thread.daemon = True
        new_thread.start()
        s_threads.append(new_thread)
    print("")
    print("Logging output...")

    try:
        while True:
            try:
                input_str = input_helper.check_input()
            except KeyboardInterrupt:
                input_helper.input_deinit()
                sys.exit()
            if input_str:
                if (input_str == EXIT_COMMAND):
                    print("Exiting...")
                    break
            time.sleep(0.1)
    except KeyboardInterrupt:
        input_helper.input_deinit()
    
    
    

if (__name__ == '__main__'): 
    main()