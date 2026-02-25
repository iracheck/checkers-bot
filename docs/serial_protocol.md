## ARM_INPUT (Python → ESP32)

| Command | Format | Description |
|---|---|---|
| Move | `M x1 y1 x2 y2` | Move piece from (x1,y1) to (x2,y2) |
| Kill | `K x y` | Remove piece at (x,y) from board |
| Shutdown | `X` | Emergency stop |
| Reset | `R` | Return arm to home position |

## ARM_OUTPUT (ESP32 → Python)

| Response | Format | Description |
|---|---|---|
| Done | `DONE` | Command executed successfully |
| Error | `ERR code` | Command failed with error code |
| Ready | `READY` | Arm initialized and ready |