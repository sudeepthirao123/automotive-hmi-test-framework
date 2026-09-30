"""
Automotive Log & CAN Trace Analyzer
Parses CAN bus trace files and DLT logs to support failure root-cause analysis.
Fulfills JD: "Support debugging activities by providing detailed failure analysis and traces."
"""
from typing import List, Dict, Any


class LogTraceAnalyzer:
    def __init__(self):
        self.anomalies: List[Dict[str, Any]] = []

    def analyze_can_trace(self, trace_frames: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes a sequence of CAN frames for:
        1. Cycle time violations (Message timeouts > 500ms)
        2. Signal value spikes or out-of-range bounds
        3. Unit / Physical range violations (e.g. TPMS 444 bar)
        """
        self.anomalies.clear()
        last_timestamps: Dict[str, float] = {}

        for idx, frame in enumerate(trace_frames):
            can_id = frame.get("can_id")
            timestamp = frame.get("timestamp", 0.0)
            signals = frame.get("signals", {})

            # 1. Timeout Check
            if can_id in last_timestamps:
                delta_ms = (timestamp - last_timestamps[can_id]) * 1000
                if delta_ms > 500.0:
                    self.anomalies.append({
                        "frame_index": idx,
                        "type": "CAN_TIMEOUT_ERROR",
                        "can_id": can_id,
                        "severity": "CRITICAL",
                        "details": f"Message {can_id} delayed by {delta_ms:.1f}ms (Limit: 500ms)"
                    })
            last_timestamps[can_id] = timestamp

            # 2. Value Bounds Check (TPMS)
            for sig_name, val in signals.items():
                if "Pressure" in sig_name and isinstance(val, (int, float)):
                    if val > 500.0:
                        self.anomalies.append({
                            "frame_index": idx,
                            "type": "OUT_OF_BOUNDS_VALUE",
                            "signal": sig_name,
                            "value": val,
                            "severity": "MAJOR",
                            "details": f"Signal {sig_name} value {val} exceeds physical sensor range (0-500 kPa)"
                        })

                # Temperature Freeze Warning Anomaly
                if sig_name == "Outside_Temp_Raw" and isinstance(val, (int, float)):
                    ice_req = signals.get("Ice_Warning_Request", False)
                    if val >= 10.0 and ice_req is True:
                        self.anomalies.append({
                            "frame_index": idx,
                            "type": "LOGICAL_CONTRADICTION",
                            "signal": sig_name,
                            "severity": "MAJOR",
                            "details": f"Ice warning active at warm ambient temperature ({val}°C)"
                        })

        return self.anomalies

    def parse_dlt_log(self, raw_dlt_text: str) -> List[Dict[str, str]]:
        """Parses DLT text and extracts ERROR and FATAL events."""
        error_lines = []
        for line in raw_dlt_text.splitlines():
            if "[ERROR]" in line or "[FATAL]" in line:
                error_lines.append({
                    "raw": line,
                    "level": "FATAL" if "[FATAL]" in line else "ERROR"
                })
        return error_lines
