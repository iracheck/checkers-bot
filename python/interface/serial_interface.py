import serial
import serial.tools.list_ports
from time import sleep
from meta import SUPPORTED_DEVICES

class SerialCom:
    '''SerialCom is a pyserial wrapper that exposes information more relevant to the Checkers robot, and helps '''

    devices = [
        {'name': 'Arduino Uno', 'vid': '0x2341', 'pid': '0x0043'},
        # {'ESP32', 'TODO: FILL THIS IN'}
    ]

    def __init__(self):
        self.ser = None
        self.port = None
        self.device = None
        pass

    def send_command(self, command: str):
        '''Sends a string as a command.'''
        pass

    def block_until_recieved(self, timeout = 2000):
        '''Block the program from continuing until a response is recieved. Defaults to a 2000 millisecond timeout before it breaks the loop.'''
        pass

    def get_message(self):
        pass

    def open(self):
        if self.ser is None:
            serial.Serial()

    def close(self):
        pass

    def find_robot(self):
        self.port = self.find_valid_serial_device()
        self.device = self.port.description

        self.ser = serial.Serial(self.port.device, 9600)

    def find_valid_serial_device(self): 
        '''Returns the *FIRST* valid serial device that might contain '''
        found_port = None

        print("Searching for device", end = "")
        for attempts in range(0, 10):
            if found_port is not None:
                break
            print(".", end="")
            ports = self.get_ports()
            for port in ports:
                if not found_port:
                    for supported_device in SUPPORTED_DEVICES.keys():
                        if supported_device[0] == port.vid and supported_device[1] == port.pid:
                            found_port = port
            print()
            sleep(1)
            print(f"Found {port.description} as a potential match!")
        
        return found_port

        #TODO: Make it so, if a potentially valid device is found, it tries to ping it to see if the firmware is loaded onto it

    def list_ports(self):
        ports = self.get_ports()

        print("Ports:")
        for port in ports:
            print(f"Device: {port.device}")
            print(f"Description: {port.description}")
            print(f"Hardware ID: {port.hwid}")
            print("-" * 20)

    def get_ports(self):
        return serial.tools.list_ports.comports()