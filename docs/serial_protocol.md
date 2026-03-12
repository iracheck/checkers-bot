# Serial Protocol for the Checkers Robot
The checkers robot uses serial communication (originating from an external brain) to communicate with the ESP32 that controls the motors which actually move the arm. It does this by receiving one command at a time and verifying its completion with `DONE` or reporting a failure with `ERROR`. The host machine does not send any new information until one of these codes are received,  resulting in minimal processing done on the ESP32 and maintaining the Python code as the universal source of truth for the robot.

## Command Format
Each command is sent as a single-line string with spaces as separators for arguments. The parsing is terminated on a newline.
`[COMMAND] [arg1] [arg2] [arg3]`
Examples:
`MOVE_TO 120 75 30`
`MAGNET_ON`
`MAGNET_OFF`
`WAIT 200`

## Commands
### HOME
Usage: `HOME`
*Returns the arm to its predefined "zeroed" position-- intended to be somewhere that is out of the way of the board and camera vision.*
**Notes**:

 - May or may not automatically disable magnet, depending on final implementation

### MOVE_TO
Usage: `MOVE_TO x y z`
*Moves the arm to the designated `(x,y,z)` coordinate.*
**Notes**:
-   Coordinate meaning is defined elsewhere in the motion system.

-   The micro controller is responsible only for execution, not coordinate interpretation beyond motion control. To reiterate: all logic is handled within the Python brain.

**Parameters**:
 - `x`: base rotation
 - `y`: board depth
 - `z`: vertical height

### WAIT
Usage: `WAIT ms`
*Waits for a designated period of time, before continuing. Can be used for other (debug) purposes such as measuring latency or debugging the serial protocol.*

**Parameters**:
 - `ms`: delay in milliseconds

### MAGNET_ON
Usage: `MAGNET_ON`
*Enables the electromagnet*

### MAGNET_OFF
Usage: `MAGNET_OFF`
*Disables the electromagnet*

## Responses
### DONE  
Example: `DONE`  
*Indicates that the command was successfully received and completed without detected error.*
### ERROR
Example: `ERROR [reason]`  
  
*Indicates an error that happened, and gives a code relating to its nature*
**Possible reasons include**:  
- INVALID_COMMAND  
- BAD_ARGUMENT_COUNT  
- BAD_ARGUMENT_VALUE  
- MOTION_FAILURE  
- TIMEOUT (>3 seconds to return `DONE` or other message)

