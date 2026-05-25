from queue import Queue
from data_structures import Command
from game.move import Move

class Sequence:
    def __init__(self):
        self.commands = []
        self.completed = 0
        self.retry_count = 0

    def get_next(self) -> Command:
        '''Returns the next item in the sequence'''
        command = self.commands[self.completed]
        self._advance()
        return command
    
    def _advance(self) -> int:
        '''Advances to the next index. The same as doing self.completed += 1 but it returns the new index.'''
        self.completed += 1
        return self.completed
    
    def retry(self, index = None) -> Command:
        '''Retries the last given command, or the one at the specified index. Defaults to the previously executed Command.
        
        Returns the next move.'''
        if index is None:
            index = self.completed - 1
        self.completed = index
        return self.get_next()

    def restart(self, index = 0) -> int:
        '''Restarts from the given index. Defaults to starting from the very beginning
        
        Returns the new number of retries.'''
        self.completed = 0
        self.retry_count += 1

        if self.retry_count >= 2:
            print(f"[WARNING] This command has been retried {self.retry_count} times.\nCommand: {self.commands}")
        
        return self.retry_count
    
    def from_move(self, move: Move):
        '''Creates a sequence given a move-- essentially, devises a sequence of mechanical movements in order to complete each step of the move.'''
        #TODO: Implement this when the mechanical engineers finish their tasks
        pass
