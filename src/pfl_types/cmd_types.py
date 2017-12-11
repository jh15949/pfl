# This file enumerates the possible actions for each
# subsystem server. Note that certain commands (POWER_ON, etc)
# are shared between all subsystems, and are implemented in the
# software bus header instead

from enum import Enum

CommsCmd = Enum('CommsCmd',
    ' '.join(
    ['EXTEND_ANT',   # Extend antenna
    'RETRACT_ANT',   # Retract antenna
    'SEND_TLM_PKT',  # Send formatted telemetry packet to ground
    'RECV_TLM_PKT'   # Receive telemetry packet from ground
    ])
)

ADCSCmd = Enum('ADCSCmd',
    ' '.join(
    ['GET_STATE',        # Reply with packet containing pointing angle and position
    'IS_TUMBLING',       # Return whether or not the craft is still tumbling
    'COILS_ON'           # Power on magcoils to detumble
    'COILS_OFF'          # Power off magcoils
    'DETUMBLE',          # Detumble spacecraft during deployment phase
    'POINT',             # Point spacecaft at specified angle
    'TRACK',             # Track object
    'GET_SUN_SENSOR_POS' # Get sun sensor telemetry
    ])
)

LogCmd = Enum('LogCmd',
    ' '.join(
    ['GET_LEVEL',        # Return a formatted packet containing all logs at a level
    'GET_LINES',         # Return a formatted packet with N most recent entries
    'ADD_LINES',         # Add a list of lines to the log storage
    'GET_TLM'            # Return all unsent logs marked as telemetry
    'GET_STATE'          # Get the state of all operations, persists after poweroff
    'SET_STATE'          # Set the state of all operations, persists after poweroff
    ])
)

CDHCmd = Enum('CDHCmd',
    ' '.join(
    ['SYNC_CLOCKS',      # Send out a heartbeat to sync all subsystem clocks
    'EXEC_CMD'           # For emergencies: run a shell command
    ])
)

PowerCmd = Enum('PowerCmd',
    ' '.join(
    ['GET_STATUS' ,      # Return bus and battery voltage and current
    'LOW_POWER'          # Returns whether or not power is low
    ])
)

StorageCmd = Enum('StorageCmd',
    ' '.join(
    ['STORE',            # Store object blob
    'LOAD',              # Load blob as object
    ])
)
