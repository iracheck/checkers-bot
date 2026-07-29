import serial
import serial.tools.list_ports
from time import sleep, time
from meta import SUPPORTED_DEVICES

class SerialCom:
    '''SerialCom is a pyserial wrapper that helps send and recieve data from the robotic arm.'''

    def __init__(self, connect=False, debug=False):
        self.ser: serial.Serial | None = None
        self.port = None
        self.device: str | None = None
        self.message_queue: list[bytes] = []
        self.DEBUG = debug

        if connect:
            self.connect()
            self.send_and_wait("PING", 15000)

    def encode(self, message: str, send = False) -> bytes:
        '''Encodes a message, and optionally sends the encoded message through the serial bus.'''
        msg = str.encode(message)

        if send:
            self.send_command(msg)

        return msg

    def send_command(self, command: bytes):
        '''Sends a command to the connected microcontroller.'''
        if self.ser is None:
            raise RuntimeError("Tried to send a message to a serial device that does not exist!")            
        
        self.ser.write(command + b"\n")

    def send_and_wait(self, command: bytes, timeout = 2000):
        '''Sends a command (in bytes) and waits for a response back from the robot. This essentially just combines the send_command() and block_until_recieved() methods.'''

        if isinstance(command, str):
            command = self.encode(command)

        self.send_command(command)
        return self.block_until_recieved(timeout)

    def block_until_recieved(self, timeout = 6000) -> bytes:
        '''Block the program from continuing until a response is recieved. Defaults to a 2000 millisecond timeout before it breaks the loop.'''
        start = time()
        while True:
            if self.ser.in_waiting:
                return self.get_message()
            if (time() - start) * 1000 > timeout:
                return
            sleep(0.01)

    def get_message(self) -> list[str] | None:
        message = self.ser.read_all()

        message = message.decode()

        if len(message) > 0:
            if self.DEBUG: print(message)
            return message
        else:
            return None

    def open(self):
        if self.ser is not None:
            self.ser.close()

        if self.port is None:
            raise RuntimeError("No port selected.")
        
        self.ser = serial.Serial(self.port.device, 9600)
        return self.ser

    def close(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None

        return self.ser is None

    def connect(self, port = None) -> bool:
        '''Connect to a given port, or if no port is provided, search for a potentially valid connected serial device.'''
        if port is None: 
            self.port = self._find_valid_serial_device()
        else:
            self.port = port

        self.device = self.port.description

        ser = self.open()

        if ser is not None:
            print("Found a potentially valid serial device. Please wait.")
            sleep(3)

        return True

    def _find_valid_serial_device(self): 
        '''Returns the *FIRST* valid microcontroller (esp32, arduino uno) that might be the checkers robot. 
        
        If there are multiple microcontrollers connected, it might not find the correct one. Always plug in the robot first so that it attaches to the earliest serial device.'''
        found_port = None

        print("Connect the robot, if it is not already connected.\nSearching for device.", end = "")
        for attempt in range(0, 20):
            print(".", end="", flush=True)

            if found_port is not None:
                break

            ports = self.get_ports()
            for port in ports:
                if not found_port:
                    for supported_device in SUPPORTED_DEVICES.keys():
                        if supported_device[0] == port.vid and supported_device[1] == port.pid:
                            found_port = port
            sleep(0.5)
        print("\n")

        if found_port is None:
            raise RuntimeError("Could not find a connected robot.")
        
        return found_port


    # debug
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