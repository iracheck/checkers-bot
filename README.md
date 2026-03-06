# checkers-bot 🤖

__**WORK IN PROGRESS**__

A physical checkers-playing robot built by a team of engineers. The robot uses computer vision to read the board state, runs game logic and AI internally, and physically moves pieces using a robotic arm controlled via serial communication.

> **Status:** Early stage development; Board/robotic design, checkers logic & gameplay development

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
| Microcontroller | ESP32 (C) |
| Mechanical System | Custom robotic arm |
| Camera | TBA |
| Motors | TBA |
| Power Source | TBA |

---

## Project Structure

```
checkers-bot/
├── esp32/                   
│   ├── interface/          # Serial communication with Python brain
│   ├── control/            # Arm control firmware
├── docs/                   # Documentation and serial protocol spec
├── hardware/               # Design files, etc.
├── python/
│   ├── game/               # Board, pieces, game logic, AI
│   ├── computer_vision/    # OpenCV board detection
│   ├── interface/          # Serial communication with ESP32
│   ├── data_structures/    # Move sequences and other supporting structures
│   └── main.py             # Entry point
└── tests/                  # Unit tests for python
```

---

## Team

| Name | Role |
|---|---|
| Cristian Fabian | Electrical Engineer |
| Ira Check | Software Engineer |
| Zachary Brannigan | Mechanical Engineer |
| Connor Macalalad | Mechanical Engineer |

---

## Running the Project

*Setup instructions coming closer to project completion.*

```bash
cd python
python main.py
```

To run unit tests:

```bash
python -m pytest
```

---

## Roadmap

Software
- [x] Project structure and repository setup
- [x] Core game engine (board, pieces)
- [ ] Move validation and legal move generation
- [ ] Minimax AI with alpha-beta pruning
- [ ] LLM player mode (Minimax vs LLM)
- [ ] Serial communication protocol
- [ ] Computer vision board detection
- [ ] Full system integration
- [ ] Set up GitHub Action to automate unit tests

Mechanical
- [x] Theorize board setup/layout
- [ ] 3D model of Board
- [ ] 3D model of Robot

Electrical
- [ ] TBA
