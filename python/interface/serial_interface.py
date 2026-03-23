import serial
import serial.tools.list_ports
from time import sleep
from meta import SUPPORTED_DEVICES

class SerialCom:
    '''SerialCom is a pyserial wrapper that helps send and recieve data from the robotic arm.'''

    def __init__(self):
        self.ser: serial.Serial | None = None
        self.port = None
        self.device: str | None = None
        self.message_queue: list[bytes] = []
        pass

    def send_command(self, command: bytes):
        '''Sends a command to the connected microcontroller.'''
        if self.ser is None:
            raise RuntimeError("Tried to send a message to a serial device that does not exist!")            
        
        self.ser.write(command + b"\n")

    def block_until_recieved(self, timeout = 2000):
        '''Block the program from continuing until a response is recieved. Defaults to a 2000 millisecond timeout before it breaks the loop.'''
        pass

    def get_message(self):
        messages = self.ser.read_all()

        self.message_queue += messages

    def open(self):
        if self.ser is not None:
            self.ser.close()

        if self.port is None:
            raise RuntimeError("No port selected.")
        
        self.ser = serial.Serial(self.port, 9600)

    def close(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None

    def find_robot(self):
        self.port = self.find_valid_serial_device()
        self.device = self.port.description

        self.ser = serial.Serial(self.port.device, 9600)

    def find_valid_serial_device(self): 
        '''Returns the *FIRST* valid microcontroller (esp32, arduino uno) that might be the checkers robot. 
        
        If there are multiple microcontrollers connected, it might not find the correct one. Always plug in the robot first so that it attaches to the earliest serial device.'''
        found_port = None

        print("Connect the robot, if it is not already connected.\nSearching for device.", end = "")
        for attempts in range(0, 20):
            print(end=".")
            if found_port is not None:
                break
            ports = self.get_ports()
            for port in ports:
                if not found_port:
                    for supported_device in SUPPORTED_DEVICES.keys():
                        if supported_device[0] == port.vid and supported_device[1] == port.pid:
                            found_port = port
            sleep(1)
        
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