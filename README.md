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
| Game Logic & AI | Python 3.11 |
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

---

## Running the Project
Before running the project, ensure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

Then change directory into `/python/`
```bash
cd python
```

The usage to run the program is as follows:
```bash
python main.py [player1] [player2] --r --d
```

`player`: The PlayerType that is occupying that slot. Player1 is WHITE and Player2 is BLACK. WHITE player goes first.
Valid args: 
- ai[`depth`] e.g. ai5, ai3 -- *depth is an integer which represents the search depth for minimax. Higher values will take longer but result in a generally more intelligent opponent.*
- human
- google

`--debug` (`--d`): Runs the program in debug (verbose) mode

`--recalibrate` (`--r`): Reruns the recalibration process, overwriting the existing calibration.

### Examples

```bash
python main.py ai3 ai3 --r
```
*Runs an evenly matched, fully automated game after running the calibration process.*

```bash
python main.py ai3 human
```
*Plays a human vs AI game on difficulty level 3 on an existing calibrated board (or calibrates one, if one is not already calibrated)*

```bash
python main.py gemini ai1 --d --r
```
*Plays a game having Gemini LLM face against an easy ai in verbose mode.*

### LLM Setup
To play against an LLM, you must have a valid API key for that LLM. These will be placed within a `.env` file that you must create yourself. You can paste the text below in as a template:
```env
GEMINI_API_KEY=[PASTE_API_KEY_HERE]
```

### Calibration

When the program starts, if no existing calibration is saved for the camera it will ask you to recalibrate. Optionally, run `--recalibrate` (`--r`) in program args OR delete the `calibration.json` file, to rerun the calibration process.

**INSTRUCTIONS**: When calibrating, you must start at the top left and move clockwise to select the four corners. Always select the four corners around the physical spaces for the pieces, not the physical edge of the board. After doing this, you will recieve a preview. Ensure that it is atleast mostly aligned (a few pixels off is okay), and if it is not, press 'r' to try again.

### Unit Tests
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
