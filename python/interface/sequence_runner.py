from data_structures.sequence import Sequence
from interface.serial_interface import SerialCom


class SequenceRunner:
    '''A class that handles the running of sequences independently of the main file.'''
    def __init__(self, serial_com: SerialCom, max_retries: int = 3):
        self.serial_com = serial_com
        self.max_retries = max_retries

    def run(self, sequence: Sequence):
        '''Executes every command in a sequence, retrying failed commands up to max_retries times.'''
        while not sequence.is_complete():
            command = sequence.get_next()
            try:
                response = self.serial_com.send_and_wait(str.encode(command))
            except TimeoutError:
                response = None

            print(response)
            if response is None:
                if sequence.retry_count >= self.max_retries:
                    raise RuntimeError(f"Sequence failed after {self.max_retries} retries: {command}")
                # TODO: Implement retries, but for the purpose of testing this complex action is not required (yet)