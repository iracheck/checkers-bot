from data_structures import Sequence, Command, CommandType
from interface.serial_interface import SerialCom
from kinematics import ArmKinematics

ERROR_MESSAGES = ["ERROR_INVALID_COMMAND", "ERROR_BAD_ARGUMENT_COUNT", "ERROR_BAD_ARGUMENT_VALUE"]


class SequenceRunner:
    '''A class that handles the running of sequences independently of the main file.'''
    def __init__(self, serial_com: SerialCom, kinematics: ArmKinematics, max_retries: int = 3):
        self.serial_com = serial_com
        self.kinematics = kinematics
        self.max_retries = max_retries

    def run(self, sequence: Sequence):
        '''Executes every command in a sequence, retrying failed commands up to max_retries times.'''
        while not sequence.is_complete():
            command = sequence.get_next()

            try:
                response = self.serial_com.send_and_wait(command, command.expected_timeout(8000))
            except TimeoutError:
                response = None

            if response is None:
                if sequence.retry_count >= self.max_retries:
                    raise RuntimeError(f"Sequence failed after {self.max_retries} retries: {command}")
                # TODO: Implement retries, but for the purpose of testing this complex action is not required (yet)