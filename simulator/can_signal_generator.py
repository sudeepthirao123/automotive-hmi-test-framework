"""
CAN Signal Generator & Fault Injection Engine
Simulates automotive bus traffic for HMI validation (Vector CANoe / PeakCAN style).
"""
import time
from typing import Dict, Any, List, Optional


class CANSignalGenerator:
    def __init__(self):
        self.active_signals: Dict[str, Any] = {
            # Ambient (0x120)
            "Outside_Temp_Raw": 20.0,
            "Ice_Warning_Request": False,
            # Powertrain (0x140)
            "Vehicle_Speed_Kmh": 0.0,
            "Engine_Speed_RPM": 800,
            "Gear_Position": "P",
            "Ignition_Terminal_State": "KL15_ON",
            # TPMS (0x160)
            "FL_Pressure_kPa": 230,
            "FR_Pressure_kPa": 230,
            "RL_Pressure_kPa": 230,
            "RR_Pressure_kPa": 230,
            "FL_Temp_C": 25.0,
            "FR_Temp_C": 25.0,
            "RL_Temp_C": 25.0,
            "RR_Temp_C": 25.0,
            # Telltales (0x180)
            "Seatbelt_Warning_Lamp": "OFF",
            "Airbag_Warning_Lamp": "OFF",
            "Brake_System_Lamp": "OFF",
            "ESC_OFF_Lamp": "OFF",
            "Check_Engine_Lamp": "OFF"
        }
        self.message_last_tx: Dict[str, float] = {}
        self.fault_injections: Dict[str, Any] = {}
        self.can_trace_log: List[Dict[str, Any]] = []

    def set_signal(self, signal_name: str, value: Any):
        """Sets a signal value with timestamp recording."""
        self.active_signals[signal_name] = value
        self.record_can_event("SIGNAL_SET", signal_name, value)

    def inject_fault(self, fault_type: str, target_signal: str, params: Optional[Dict[str, Any]] = None):
        """
        Injects real-world automotive failure scenarios:
        - 'TIMEOUT': Stops transmitting the CAN message
        - 'OUT_OF_BOUNDS': Sends physically impossible values (e.g. 444 bar TPMS)
        - 'NEEDLE_DESYNC': Creates desynchronization between speed digital and analog readout
        - 'DATE_INVALID': Injects impossible calendar date (e.g. 30.02.2021)
        """
        self.fault_injections[target_signal] = {
            "type": fault_type,
            "params": params or {},
            "active": True
        }
        self.record_can_event("FAULT_INJECTED", target_signal, fault_type)

    def clear_faults(self):
        """Clears all active fault injections."""
        self.fault_injections.clear()
        self.record_can_event("FAULTS_CLEARED", "ALL", None)

    def transmit_message(self, message_id: str) -> Dict[str, Any]:
        """Simulates transmission of a CAN frame onto the bus."""
        now = time.time()
        self.message_last_tx[message_id] = now
        
        frame = {
            "timestamp": now,
            "can_id": message_id,
            "signals": {}
        }

        # Check for timeout fault
        if "TIMEOUT" in [f["type"] for f in self.fault_injections.values()]:
            frame["status"] = "DROPPED_BY_FAULT_INJECTION"
            return frame

        # Populate payload
        for sig, val in self.active_signals.items():
            if sig in self.fault_injections and self.fault_injections[sig]["type"] == "OUT_OF_BOUNDS":
                frame["signals"][sig] = self.fault_injections[sig]["params"].get("override_value", val)
            else:
                frame["signals"][sig] = val

        frame["status"] = "TRANSMITTED_OK"
        return frame

    def record_can_event(self, action: str, signal: str, value: Any):
        entry = {
            "timestamp": time.time(),
            "action": action,
            "signal": signal,
            "value": value
        }
        self.can_trace_log.append(entry)

    def export_trace_log(self) -> List[Dict[str, Any]]:
        return self.can_trace_log
