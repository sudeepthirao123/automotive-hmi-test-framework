"""
Robot Framework Custom HMI Library
Bridges Robot test keywords with the CAN Signal Generator and Cluster HMI State Machine.
"""
from simulator.can_signal_generator import CANSignalGenerator
from simulator.cluster_hmi_state_machine import ClusterHMIStateMachine
from simulator.dlt_logger import DLTLogger


class robot_hmi_library:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.can_gen = CANSignalGenerator()
        self.cluster = ClusterHMIStateMachine(mode="PRODUCTION_STRICT")
        self.dlt = DLTLogger()

    def initialize_cluster_test_bench(self):
        self.can_gen = CANSignalGenerator()
        self.cluster = ClusterHMIStateMachine()
        self.dlt.log("TEST", "BENCH", "INFO", "Cluster Test Bench Initialized successfully")

    def shutdown_test_bench(self):
        self.dlt.log("TEST", "BENCH", "INFO", "Cluster Test Bench Shutdown")

    def vehicle_can_simulation_is_active(self):
        return True

    def system_units_are_set_to(self, unit_system: str):
        self.cluster.system_units = unit_system
        self.dlt.log("HMI", "CONF", "INFO", f"System units set to {unit_system}")

    def outside_temperature_signal_is_injected(self, temp_val):
        temp_float = float(temp_val)
        self.can_gen.set_signal("Outside_Temp_Raw", temp_float)
        frame = self.can_gen.transmit_message("0x120")
        self.cluster.process_can_frame(frame)
        self.dlt.log("CAN", "TEMP", "INFO", f"Injected Outside_Temp_Raw: {temp_float}°C")

    def snowflake_telltale_status_should_be(self, expected_status: str):
        expected_bool = (expected_status.upper() == "ON")
        actual_bool = self.cluster.snowflake_telltale
        if actual_bool != expected_bool:
            actual_str = "ON" if actual_bool else "OFF"
            self.dlt.log("FAIL", "TEMP", "ERROR", f"Snowflake mismatch! Expected {expected_status}, got {actual_str}")
            raise AssertionError(f"Snowflake state mismatch! Expected: {expected_status}, Actual: {actual_str}")

    def displayed_outside_temperature_should_be(self, expected_val):
        expected_float = float(expected_val)
        if abs(self.cluster.displayed_temp_c - expected_float) > 0.05:
            raise AssertionError(f"Temp mismatch: Expected {expected_float}, got {self.cluster.displayed_temp_c}")

    def tpms_can_signals_injected(self, **kwargs):
        for k, v in kwargs.items():
            self.can_gen.set_signal(f"{k}_Pressure_kPa", int(v))
        frame = self.can_gen.transmit_message("0x160")
        self.cluster.process_can_frame(frame)

    def all_four_wheels_should_display_unit(self, expected_unit: str):
        for pos, data in self.cluster.displayed_tpms.items():
            if data["unit"] != expected_unit:
                raise AssertionError(f"Wheel {pos} unit mismatch: Expected {expected_unit}, got {data['unit']}")

    def wheel_unit_should_be(self, wheel_pos: str, expected_unit: str):
        actual_unit = self.cluster.displayed_tpms[wheel_pos]["unit"]
        if actual_unit != expected_unit:
            raise AssertionError(f"Wheel {wheel_pos} unit mismatch: Expected {expected_unit}, got {actual_unit}")

    def wheel_pressure_should_not_exceed_maximum_physical_limit(self, wheel_pos: str, max_limit: int):
        val = self.cluster.displayed_tpms[wheel_pos]["pressure"]
        if val > int(max_limit):
            raise AssertionError(f"Wheel {wheel_pos} pressure {val} exceeds physical safety maximum {max_limit}!")

    def vehicle_speed_can_signal_injected(self, speed_kmh):
        val = float(speed_kmh)
        self.can_gen.set_signal("Vehicle_Speed_Kmh", val)
        frame = self.can_gen.transmit_message("0x140")
        self.cluster.process_can_frame(frame)

    def displayed_digital_speed_should_be(self, expected_speed):
        exp = float(expected_speed)
        act = self.cluster.displayed_speed_digital
        if abs(act - exp) > 0.5:
            raise AssertionError(f"Speed digital mismatch: Expected {exp}, got {act}")

    def analog_needle_calculated_speed_should_match_digital_readout(self, tolerance=1.0):
        # Convert needle angle (0-240 deg) back to speed (0-200 scale)
        needle_speed = self.cluster.displayed_needle_angle_deg * (200.0 / 240.0)
        digital = self.cluster.displayed_speed_digital
        if abs(needle_speed - digital) > float(tolerance):
            raise AssertionError(f"Speed needle desync! Needle indicates {needle_speed:.1f}, but digital readout is {digital:.1f}")

    def ignition_state_changes_to(self, state: str):
        self.cluster.ignition_state = state
        self.can_gen.set_signal("Ignition_Terminal_State", state)

    def telltale_status_should_be(self, lamp_name: str, expected_state: str):
        act = self.cluster.active_telltales.get(lamp_name, "OFF")
        if act != expected_state:
            raise AssertionError(f"Telltale {lamp_name} mismatch: Expected {expected_state}, got {act}")
