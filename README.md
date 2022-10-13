# python-tools
Collection of Python scripts for interacting with Canaree and IPS sensors.

## Requirements
- Python v3.7
- pySerial (`pip install pyserial`)

## Usage
Monitor sensor output and send commands:
```
python monitor.py
```

Update WiFi settings, you can edit **wifi_ssid** and **wifi_pwd** in *update_wifi.py*:
```
python update_wifi.py
```

Log data to a file. Expects an IPS-7100/Canaree with default serial output to parse data correctly:
```
python logger.py
```

## Tips
See *update_wifi.py* for an example of how to use threading so you can communicate with multiple sensors at the same time.

You can send UART commands to a sensor like this:
```
serial_con.write(('$Dflash=\r\n').encode())
time.sleep(1)
```
Make sure to include a delay between commands. See the latest IPS or Canaree datasheet for a list of UART commands: https://pierasystems.com/