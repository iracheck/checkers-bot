from queue import Queue
from data_structures import Command

class Sequence:
    '''A sequence is similar to a queue but much less advanced, as the requirements for this project are significantly lower, but still want the functionality of pulling from the first element in the list.'''
    def __init__(self, size = 32):
        self.commands = []
        self.completed = 0
        self.retry_count = 0

    def get_next(self) -> Command:
        '''Returns the next item in the sequence'''
        self.completed += 1
        return self.commands[self.completed]
    
    def _advance(self) -> int:
        '''Advances to the next index. The same as doing self.completed += 1'''
        self.completed += 1
        return self.completed
    
    def retry(self, index = None) -> Command:
        '''Retries the last given command, or the one at the specified index. Defaults to the previously executed Command.
        
        Returns the next move.'''
        if index is None:
            index = self.completed - 1
        return self.get_next(index)

    def retry(self, index = 0) -> int:
        '''Restarts from the given index. Defaults to starting from the very beginning
        
        Returns the new number of retries.'''
        self.completed = 0
        self.retry_count += 1

        if self.retry_count >= 2:
            print(f"[WARNING] This command has been retried {self.retry_count} times.\nCommand: {self.commands}")
        
        return self.retry_count
    
