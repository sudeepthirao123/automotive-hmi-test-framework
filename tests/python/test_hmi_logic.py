"""
Automotive Python Test Suite - HMI Core Logic & Calendar Boundary Validation
"""
from simulator.cluster_hmi_state_machine import ClusterHMIStateMachine


def test_calendar_date_boundary_validation():
    """
    Validates calendar boundary handling to catch impossible dates like '30.02.2021'.
    """
    cluster = ClusterHMIStateMachine()

    # Valid Leap Year Date
    assert cluster.validate_date("29.02.2020") is True

    # Valid Non-Leap Year Date
    assert cluster.validate_date("28.02.2021") is True

    # Invalid Boundary Date (Audi Cluster Image 1 Defect)
    assert cluster.validate_date("30.02.2021") is False, "Calendar engine allowed February 30th!"


def test_metric_to_imperial_speed_conversion():
    """
    Validates that vehicle speed correctly converts when changing system units.
    """
    cluster = ClusterHMIStateMachine()

    # 100 km/h in Metric mode
    cluster.system_units = "METRIC"
    cluster.update_speedometer(100.0)
    assert cluster.displayed_speed_digital == 100.0

    # 100 km/h converted to Imperial (should be ~62.1 MPH)
    cluster.system_units = "IMPERIAL"
    cluster.update_speedometer(100.0)
    assert cluster.displayed_speed_digital == 62.1
