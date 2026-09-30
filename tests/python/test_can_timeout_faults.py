"""
Automotive Python Test Suite - CAN Communication Faults & Sensor Disconnects
Validates graceful HMI degradation, fallback indicators, and DTC generation.
"""
import time
from simulator.can_signal_generator import CANSignalGenerator
from simulator.cluster_hmi_state_machine import ClusterHMIStateMachine


def test_ambient_temp_sensor_disconnect_timeout():
    """
    Requirement REQ-HMI-COMM-009:
    If Ambient Environment CAN message (0x120) is not received for > 500ms:
    1. Cluster must NOT crash or freeze.
    2. Outside temperature must display safe fallback notation ('--.-').
    3. Diagnostic Trouble Code U0100 must be recorded in ECU fault memory.
    """
    can_gen = CANSignalGenerator()
    cluster = ClusterHMIStateMachine()

    # Step 1: Transmit valid temperature message
    can_gen.set_signal("Outside_Temp_Raw", 18.5)
    frame = can_gen.transmit_message("0x120")
    cluster.process_can_frame(frame)
    assert cluster.displayed_temp_c == 18.5

    # Step 2: Inject Sensor Disconnect / CAN Bus Drop Fault
    can_gen.inject_fault("TIMEOUT", "0x120")

    # Step 3: Advance simulated time by 600ms (exceeding 500ms timeout threshold)
    current_time = time.time() + 0.6
    cluster.check_can_timeouts(current_time)

    # Step 4: Verify Graceful Degradation & Fallback
    assert cluster.displayed_temp_c is None, "Cluster failed to display fallback notation on CAN timeout!"
    assert "U0100" in cluster.active_dtcs, "Cluster failed to register DTC U0100 for lost communication!"


def test_tpms_sensor_disconnect_timeout():
    """
    Validates that loss of TPMS gateway CAN frame (0x160) logs DTC U0127.
    """
    can_gen = CANSignalGenerator()
    cluster = ClusterHMIStateMachine()

    frame = can_gen.transmit_message("0x160")
    cluster.process_can_frame(frame)

    # Simulate timeout
    current_time = time.time() + 0.7
    cluster.check_can_timeouts(current_time)

    assert "U0127" in cluster.active_dtcs
