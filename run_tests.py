#!/usr/bin/env python3
"""
Automotive HMI Test Automation Runner
Executes test suites, triggers trace analysis, and generates HTML reports & Jira defect tickets.
"""
import sys
import os
import time

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulator.can_signal_generator import CANSignalGenerator
from simulator.cluster_hmi_state_machine import ClusterHMIStateMachine
from tools.log_trace_analyzer import LogTraceAnalyzer
from tools.jira_defect_generator import JiraDefectGenerator
from tools.test_report_generator import TestReportGenerator


def run_full_suite():
    print("=" * 70)
    print("🚗 AUTOMOTIVE HMI & IVI TEST AUTOMATION EXECUTION ENGINE")
    print("=" * 70)

    results = []
    generated_tickets = []

    # Test 1: BVA Baseline 6.0°C
    t1_start = time.time()
    can = CANSignalGenerator()
    cluster = ClusterHMIStateMachine(mode="PRODUCTION_STRICT")
    can.set_signal("Outside_Temp_Raw", 6.0)
    cluster.process_can_frame(can.transmit_message("0x120"))
    if cluster.snowflake_telltale is False:
        results.append({"test_id": "TC_BVA_001", "name": "BVA Baseline 6.0°C (Snowflake OFF)", "status": "PASS", "duration_ms": 12})
    else:
        results.append({"test_id": "TC_BVA_001", "name": "BVA Baseline 6.0°C", "status": "FAIL", "duration_ms": 12, "message": "Snowflake active at 6.0°C"})

    # Test 2: BVA Freeze Trigger 4.9°C
    can.set_signal("Outside_Temp_Raw", 4.9)
    cluster.process_can_frame(can.transmit_message("0x120"))
    if cluster.snowflake_telltale is True:
        results.append({"test_id": "TC_BVA_004", "name": "BVA Freeze Boundary 4.9°C (Snowflake ON)", "status": "PASS", "duration_ms": 14})
    else:
        results.append({"test_id": "TC_BVA_004", "name": "BVA Freeze Boundary 4.9°C", "status": "FAIL", "duration_ms": 14, "message": "Snowflake failed to turn ON at 4.9°C"})

    # Test 3: TPMS Metric Mode (kPa)
    cluster.system_units = "METRIC"
    can.set_signal("FL_Pressure_kPa", 230)
    can.set_signal("FR_Pressure_kPa", 230)
    cluster.process_can_frame(can.transmit_message("0x160"))
    all_kpa = all(d["unit"] == "kPa" for d in cluster.displayed_tpms.values())
    if all_kpa:
        results.append({"test_id": "TC_TPMS_001", "name": "TPMS Metric Units Uniformity", "status": "PASS", "duration_ms": 10})
    else:
        results.append({"test_id": "TC_TPMS_001", "name": "TPMS Metric Units Uniformity", "status": "FAIL", "duration_ms": 10, "message": "Mixed units found"})

    # Test 4: Regression Test on Injected Bug Build (Audi Cockpit Image 1 Defect)
    buggy_cluster = ClusterHMIStateMachine(mode="INJECT_BUGS")
    can.set_signal("Outside_Temp_Raw", 13.0)
    buggy_cluster.process_can_frame(can.transmit_message("0x120"))
    if buggy_cluster.snowflake_telltale is False:
        results.append({"test_id": "TC_REG_008", "name": "Regression Defect Check (Snowflake at 13.0°C)", "status": "PASS", "duration_ms": 15})
    else:
        fail_msg = "Snowflake telltale active at +13.0°C (Violates ISO freeze warning requirement)"
        results.append({"test_id": "TC_REG_008", "name": "Regression Defect Check (Snowflake at 13.0°C)", "status": "FAIL", "duration_ms": 15, "message": fail_msg})
        
        # Generate automated Jira ticket for failure
        ticket = JiraDefectGenerator.generate_ticket(
            test_name="TC_REG_008",
            component="Cluster_HMI / Telltale_Manager",
            error_message=fail_msg,
            severity="Major",
            priority="P2",
            reproduction_steps=[
                "Boot cluster to main driving view",
                "Inject Outside_Temp_Raw CAN signal = 13.0°C via CANoe",
                "Observe bottom status bar telltales"
            ],
            expected_result="Snowflake warning icon must remain OFF for temperatures > 4.0°C / 5.0°C",
            actual_result="Snowflake warning icon is illuminated next to '13.0 °C'",
            can_trace_snippet=can.export_trace_log()[-2:],
            dlt_log_snippet="[TEMP:WARN] [ERROR] Ice hazard snowflake telltale triggered at ambient temp +13.0°C",
            impact_analysis="Driver confusion and false hazard warnings leading to loss of trust in ADAS/HMI."
        )
        generated_tickets.append(ticket)

    # Generate HTML Test Execution Summary Report
    html_report = TestReportGenerator.generate_html_report("HMI_Cluster_Automated_Regression", results)
    report_path = os.path.join(os.path.dirname(__file__), "test_execution_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_report)

    # Print Summary to Console
    print("\n📊 EXECUTION RESULTS:")
    for r in results:
        status_icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {status_icon} [{r['test_id']}] {r['name']} -> {r['status']}")

    if generated_tickets:
        ticket_path = os.path.join(os.path.dirname(__file__), "generated_jira_defect.md")
        with open(ticket_path, "w", encoding="utf-8") as f:
            f.write(JiraDefectGenerator.export_markdown(generated_tickets[0]))
        print(f"\n🎫 Automated Jira Defect Ticket generated: {ticket_path}")

    print(f"📄 HTML Test Summary Report generated: {report_path}")
    print("=" * 70)


if __name__ == "__main__":
    run_full_suite()
