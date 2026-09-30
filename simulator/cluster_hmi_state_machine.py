"""
Cluster HMI State Machine & Rendering Logic
Simulates the automotive Instrument Cluster firmware (Qt/QML/Android Automotive based).
Handles:
- Outside Temperature & Snowflake Ice Warning with Hysteresis
- TPMS Monitoring & Unit Conversion (Metric kPa vs Imperial bar)
- Speedometer Digital vs Analog Needle Calculation
- ISO 2575 Safety Telltales & Lamp Test
- CAN Timeout Fallback & Diagnostic Trouble Code (DTC) Generation
"""
import time
from typing import Dict, Any, List, Optional
from datetime import datetime


class ClusterHMIStateMachine:
    def __init__(self, mode: str = "PRODUCTION_STRICT"):
        self.mode = mode  # "PRODUCTION_STRICT" or "INJECT_BUGS"
        self.ignition_state = "KL15_ON"
        self.system_units = "METRIC"  # METRIC or IMPERIAL
        self.language = "DE"          # "EN", "DE", "FR"

        # Display States
        self.displayed_speed_digital = 0.0
        self.displayed_needle_angle_deg = 0.0
        self.displayed_temp_c = 20.0
        self.snowflake_telltale = False
        self.displayed_tpms: Dict[str, Dict[str, Any]] = {
            "FL": {"pressure": 230, "unit": "kPa", "temp": 25.0},
            "FR": {"pressure": 230, "unit": "kPa", "temp": 25.0},
            "RL": {"pressure": 230, "unit": "kPa", "temp": 25.0},
            "RR": {"pressure": 230, "unit": "kPa", "temp": 25.0}
        }
        self.active_telltales: Dict[str, str] = {}
        self.active_dtcs: List[str] = []
        self.last_can_rx_timestamp: Dict[str, float] = {}
        self.timeout_threshold_s = 0.5  # 500ms CAN timeout

    def process_can_frame(self, frame: Dict[str, Any]):
        """Processes an incoming CAN frame and updates HMI display state."""
        now = time.time()
        can_id = frame.get("can_id")
        self.last_can_rx_timestamp[can_id] = now
        signals = frame.get("signals", {})

        # 0x140: Powertrain Dynamics
        if can_id == "0x140":
            speed_kmh = signals.get("Vehicle_Speed_Kmh", 0.0)
            self.update_speedometer(speed_kmh)

        # 0x120: Ambient Environment
        elif can_id == "0x120":
            temp_raw = signals.get("Outside_Temp_Raw", 20.0)
            self.update_temperature_display(temp_raw)

        # 0x160: TPMS
        elif can_id == "0x160":
            self.update_tpms_display(signals)

        # 0x180: Safety Telltales
        elif can_id == "0x180":
            self.update_telltales(signals)

    def update_temperature_display(self, raw_temp: float):
        """
        Updates outside temperature & snowflake warning.
        Standard Automotive Specification:
        - Trigger ON when temperature drops below 5.0°C (<= 4.9°C).
        - Extinguish OFF when temperature rises strictly above 6.0°C (Hysteresis Band).
        - In 'INJECT_BUGS' mode: Replicates Image 1 bug where snowflake is ON at 13.0°C!
        """
        self.displayed_temp_c = raw_temp

        if self.mode == "INJECT_BUGS":
            # Defect: Snowflake forced ON at 13.0°C
            if abs(raw_temp - 13.0) < 0.1:
                self.snowflake_telltale = True
                return

        # Correct Automotive Logic with Hysteresis
        if raw_temp < 5.0:
            self.snowflake_telltale = True
        elif raw_temp >= 6.0:
            self.snowflake_telltale = False
        # If between 5.0 and 5.9, retain previous state (Hysteresis Memory)

    def update_speedometer(self, speed_kmh: float):
        """
        Calculates digital speed and analog needle angle.
        Dial range: 0 to 200 (scale: 0 km/h = 0 deg, 200 km/h = 240 deg).
        In 'INJECT_BUGS' mode: Replicates Image 1 bug (Digital=100 MPH, Needle=72)!
        """
        if self.system_units == "IMPERIAL":
            speed_val = speed_kmh * 0.621371
        else:
            speed_val = speed_kmh

        self.displayed_speed_digital = round(speed_val, 1)

        if self.mode == "INJECT_BUGS" and speed_val >= 99.0:
            # Defect: Needle desynchronized (stuck at 72)
            self.displayed_needle_angle_deg = 72.0 * (240.0 / 200.0)
        else:
            self.displayed_needle_angle_deg = min(240.0, speed_val * (240.0 / 200.0))

    def update_tpms_display(self, signals: Dict[str, Any]):
        """
        Renders TPMS values.
        In 'INJECT_BUGS' mode: Replicates Image 1 bug (FR tire displays 444 bar in kPa mode)!
        """
        for pos in ["FL", "FR", "RL", "RR"]:
            pressure_raw = signals.get(f"{pos}_Pressure_kPa", 230)
            temp_raw = signals.get(f"{pos}_Temp_C", 25.0)

            unit = "kPa" if self.system_units == "METRIC" else "psi"

            if self.mode == "INJECT_BUGS" and pos == "FR":
                # Defect: Displays 'bar' unit with extreme 444 value
                unit = "bar"
                pressure_raw = 444

            self.displayed_tpms[pos] = {
                "pressure": pressure_raw,
                "unit": unit,
                "temp": temp_raw
            }

    def update_telltales(self, signals: Dict[str, Any]):
        """Updates ISO 2575 safety telltale states."""
        for lamp, state in signals.items():
            self.active_telltales[lamp] = state

    def check_can_timeouts(self, current_time: float):
        """
        Validates loss of CAN communication.
        Automotive requirement: If no frame received within 500ms:
        - Freeze display must be prevented.
        - Display safe fallback (e.g. '--.- °C').
        - Log DTC U0100 (Lost Communication with ECU).
        """
        for can_id, last_tx in list(self.last_can_rx_timestamp.items()):
            if (current_time - last_tx) > self.timeout_threshold_s:
                if can_id == "0x120":
                    self.displayed_temp_c = None  # '--.-'
                    if "U0100" not in self.active_dtcs:
                        self.active_dtcs.append("U0100")
                elif can_id == "0x160":
                    for pos in self.displayed_tpms:
                        self.displayed_tpms[pos]["pressure"] = None
                    if "U0127" not in self.active_dtcs:
                        self.active_dtcs.append("U0127")

    def validate_date(self, date_str: str) -> bool:
        """
        Validates Gregorian calendar date format (DD.MM.YYYY).
        Prevents impossible dates like '30.02.2021'.
        """
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True
        except ValueError:
            return False
