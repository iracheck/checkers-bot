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
        self._read_buffer = b""
        self.DEBUG = debug

        if connect:
            self.connect()
            self.send_and_wait("PING", 15000)

    def send_command(self, command: bytes):
        '''Sends a command to the connected microcontroller.'''
        if self.ser is None:
            raise RuntimeError("Tried to send a message to a serial device that does not exist!")            
        
        self.ser.write(command + b"\n")

    def send_and_wait(self, command: bytes, timeout = 2000):
        '''Sends a command (in bytes) and waits for a response back from the robot. This essentially just combines the send_command() and block_until_recieved() methods.'''

        if isinstance(command, str):
            command = str.encode(command)

        self.send_command(command)
        return self.block_until_recieved(timeout)

    def block_until_recieved(self, timeout = 6000) -> str:
        '''Block the program from continuing until a response is recieved. Defaults to a 2000 millisecond timeout before it breaks the loop.'''
        start = time()
        while True:
            message = self.get_message()
            if message is not None:
                return message.decode().strip()
            
            if (time() - start) * 1000 > timeout:
                return
            sleep(0.01)

    def get_message(self) -> bytes:
        data = self.ser.read_all()

        if data:
            self._read_buffer += data

        if b"\n" not in self._read_buffer:
            return None

        split_buf = self._read_buffer.split(b"\n", 1)

        self._read_buffer = split_buf[1]
        return split_buf[0]

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
            sleep(3)

        return True

    def _find_valid_serial_device(self): 
        '''Returns the *FIRST* valid microcontroller (esp32, arduino uno) that might be the checkers robot. 
        
        The method tries to ping the microcontroller and recieve a response, so it may take some time if you have many serial devices connected at one time.'''
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

                            self.connect(found_port)
                            response = self.send_and_wait("PING\n")
                            if response == "PONG!":
                                print("\nSuccessfully connected to " + SUPPORTED_DEVICES[supported_device])
                                return port
                            
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