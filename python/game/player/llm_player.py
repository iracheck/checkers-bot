from enum import Enum

from game.player.player import Player
from game.board import Board
from game.move import Move
from time import sleep

import os
from dotenv import load_dotenv

from google import genai

class LLMType(Enum):
    OPENAI = "CHATGPT"
    GOOGLE = "GEMINI"
    ANTHROPIC = "CLAUDE"
    XAI = "GROK"

class LLMPlayer(Player):
    def __init__(self, llm_type: LLMType, color="B"):
        super().__init__(color=color)

        self.llm_type = llm_type
        self.client = self.initialize_llm()

        if self.client is None:
            raise RuntimeError("Tried to initialize a LLMPlayer, but the type was not recognized.")


    def get_move(self, board: Board, turn: int) -> Move:
        indexed_moves = self.index_moves(board)
        message = self.assemble_message(board, indexed_moves)

        invalid_move = True

        while invalid_move:
            if self.is_gemini():
                msg = self.query_gemini(message, print_response=True)

                try:
                    msg = int(msg)
                except:
                    print("[WARNING] Gemini returned an invalid response.")
                    continue
                if msg == 0 or msg > len(indexed_moves):
                    raise RuntimeError("LLM returned an invalid string.")
                


            elif self.is_chatgpt():
                #TODO: Implement chatgpt
                raise NotImplementedError("This LLM is not yet implemented.")
            elif self.is_claude():
                #TODO: Implement claude
                raise NotImplementedError("This LLM is not yet implemented.")
            elif self.is_grok():
                #TODO: Implement grok
                raise NotImplementedError("This LLM is not yet implemented.")
            else:
                raise RuntimeError("Tried to get a move from an LLMPlayer that does not have an assigned LLMType or API key.")
            
        return indexed_moves[msg]
    

    def index_moves(self, board: Board) -> dict:
        valid_moves = board.get_every_legal(self.color)
        indexed_moves = {}
        index = 0

        for move in valid_moves:
            if len(valid_moves[move]) == 0:
                continue

            for option in valid_moves[move]:
                index += 1
                indexed_moves[index] = option

        return indexed_moves
    
    
    def assemble_message(self, board: Board, indexed_moves: dict) -> str:
        msg = f"""You are playing a game of checkers as player {self.color}. Here is the current board state:\n\n
        {board}\n\n 
        Here are the following moves you have avaliable: \n
        {indexed_moves}\n\n
        To choose a move, return only the index of the move you'd like to make (e.g. 1). Do not give an explanation. If there are no moves possible, return 0."""
        
        return msg
        
    def initialize_llm(self):
        load_dotenv()
        
        client = None
        if self.is_gemini():
            print("Trying to initialize a Gemini client...")
            key = os.getenv("GEMINI_API_KEY")
            return genai.Client(api_key=key)
        
    def query_gemini(self, prompt: str, llm_model="gemini-2.5-flash-lite", print_response=False):
        if not self.is_gemini():
            print("Tried to query Gemini when Gemini is not the active model.")
            return None

        response = self.client.models.generate_content(model=llm_model, contents=prompt)

        if print_response:
            print(response.text)
        
        return response.text
        
    def is_chatgpt(self) -> bool:
        return self.llm_type == LLMType.OPENAI
    
    def is_gemini(self) -> bool:
        return self.llm_type == LLMType.GOOGLE
    
    def is_claude(self) -> bool:
        return self.llm_type == LLMType.ANTHROPIC
    
    def is_grok(self) -> bool:
        return self.llm_type == LLMType.XAI
        
