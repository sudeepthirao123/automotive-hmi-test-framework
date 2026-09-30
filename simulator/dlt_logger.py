"""
Diagnostic Log and Trace (DLT) Simulator
Emulates GENIVI / AUTOSAR DLT logging for automotive middleware debugging.
"""
import time
from typing import List, Dict


class DLTLogger:
    def __init__(self, ecu_id: str = "CLUSTER_ECU"):
        self.ecu_id = ecu_id
        self.logs: List[Dict[str, str]] = []

    def log(self, apid: str, ctid: str, level: str, message: str):
        """
        Records a DLT log line.
        apid: Application ID (e.g. 'HMI', 'TPMS', 'TELL')
        ctid: Context ID (e.g. 'WARN', 'DISP', 'COMM')
        level: 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f".{int(time.time()*1000)%1000:03d}"
        entry = {
            "timestamp": timestamp,
            "ecu": self.ecu_id,
            "apid": apid,
            "ctid": ctid,
            "level": level,
            "message": message
        }
        self.logs.append(entry)

    def export_text(self) -> str:
        lines = []
        for l in self.logs:
            lines.append(f"[{l['timestamp']}] [{l['ecu']}] [{l['apid']}:{l['ctid']}] [{l['level']}] {l['message']}")
        return "\n".join(lines)
