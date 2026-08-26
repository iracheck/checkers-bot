# checkers-bot

__**WORK IN PROGRESS**__

A physical checkers-playing robot built by a team of engineers. The robot uses computer vision to read the board state, runs game logic and AI internally, and physically moves pieces using a robotic arm controlled via serial communication.

> **Status:** Late stage development

---

## How It Works

1. A webcam reads the physical board using computer vision (OpenCV)
2. The detected board state is compared against an internal authority board to validate the human's move
3. The AI (minimax with alpha-beta pruning) calculates the best response
4. A move command is sent over serial to the ESP32 microcontroller
5. The robotic arm executes the move on the physical board

---

## Tech Stack

| Layer | Technology |
|---|---|
| Game Logic & AI | Python |
| Computer Vision | Python, OpenCV |
| Serial Communication | Python (pyserial) |
| Microcontroller | Arduino/ESP32 (C/C++) |
| Mechanical System | Custom robotic arm |
| Camera | TBA |
| Motors | TBA |
| Power Source | TBA |

---

## Project Structure

```
checkers-bot/
├── firmware/               # arduino control software-- robotic arm control
├── docs/                   # Documentation and serial protocol spec
├── hardware/               # Design files, etc.
├── python/
│   ├── game/               # Board, pieces, game logic, AI
│   ├── computer_vision/    # OpenCV board detection
│   ├── interface/          # Serial communication with ESP32
│   ├── tests/              # Unit tests
│   ├── data_structures/    # Move sequences and other supporting structures
│   └── main.py             # Entry point
└── requirements.txt        # Dependencies 
```

---

## Team

| Name | Role |
|---|---|
| Ira Check | Software Engineer |
| Zachary Brannigan | Mechanical Engineer |
| Connor Macalalad | Consulting |

---

## Running the Project

*Improved setup instructions coming upon project completion.*

```bash
cd python
python main.py [player1] [player2]
```

Player types include: AI[depth], Google, Human<br>

When the program starts, if no existing calibration is saved for the camera it will ask you to recalibrate. Optionally, run `--recalibrate` in program args to change calibration, OR delete the `calibration.json` file.

When calibrating, you must start at the top left and move clockwise to select the four corners. Always select the four corners around the physical spaces for the pieces, not the physical edge of the board.

To run unit tests:

```bash
python -m pytest
```

---

## Roadmap

Software
- [x] Project structure and repository setup
- [x] Core game engine (board, pieces)
- [x] Move validation and legal move generation
- [x] Minimax AI with alpha-beta pruning
- [x] LLM player mode (Minimax vs LLM)
- [x] Serial communication protocol
- [ ] Computer vision board detection
- [ ] Inverse kinematics
- [ ] Full system integration
- [x] Set up GitHub Action to automate unit tests

Robotic Arm
- [x] Functioning robotic arm
- [ ] Arm firmware
- [ ] Failure detection/redundancy

Documentation
- [x] Write serial protocpl docs
- [ ] Demo instructions
- [ ] Calibration instructions
- [ ] Mechanical design documentation
