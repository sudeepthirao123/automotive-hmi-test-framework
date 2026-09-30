"""
Automated Automotive Jira Defect Exporter
Automatically formats test failure results, CAN traces, and DLT logs into enterprise Jira defect tickets.
Fulfills JD: "Create detailed defect tickets for failed test executions: clear description, reproduction steps, logs, traces, evidence, impact analysis."
"""
from typing import Dict, Any, Optional
import json


class JiraDefectGenerator:
    @staticmethod
    def generate_ticket(
        test_name: str,
        component: str,
        error_message: str,
        severity: str = "Major",
        priority: str = "P2",
        reproduction_steps: Optional[list] = None,
        expected_result: str = "",
        actual_result: str = "",
        can_trace_snippet: Optional[list] = None,
        dlt_log_snippet: Optional[str] = None,
        impact_analysis: str = ""
    ) -> Dict[str, Any]:
        """Creates a standardized Jira ticket structure."""

        steps_formatted = "\n".join([f"{i+1}. {step}" for i, step in enumerate(reproduction_steps or [])])
        can_formatted = json.dumps(can_trace_snippet, indent=2) if can_trace_snippet else "None attached"

        ticket = {
            "fields": {
                "project": {"key": "HMI"},
                "issuetype": {"name": "Bug"},
                "summary": f"[{component}] {test_name}: {error_message.splitlines()[0]}",
                "environment": "Audi Virtual Cockpit HIL Bench #01 (SW: v2.4.0-RC3, CANoe 16.0)",
                "priority": {"name": priority},
                "customfield_severity": severity,
                "description": f"""
*PRECONDITIONS:*
- Ignition state = KL15 (Ignition ON)
- CAN Simulation active on Channel 1
- Target firmware build v2.4.0-RC3

*STEPS TO REPRODUCE:*
{steps_formatted}

*EXPECTED RESULT:*
{expected_result}

*ACTUAL RESULT:*
{actual_result}

*DIAGNOSTIC EVIDENCE & CAN TRACE:*
{{code:json}}
{can_formatted}
{{code}}

*DLT MIDDLEWARE LOG:*
{{code}}
{dlt_log_snippet or "No fatal DLT assertions"}
{{code}}

*IMPACT ANALYSIS:*
{impact_analysis or "Functional non-compliance against automotive UX and safety specifications."}
                """.strip()
            }
        }
        return ticket

    @staticmethod
    def export_markdown(ticket_dict: Dict[str, Any]) -> str:
        f = ticket_dict["fields"]
        return f"""
# 🐛 JIRA DEFECT REPORT: {f['summary']}

| Field | Value |
| :--- | :--- |
| **Issue Type** | {f['issuetype']['name']} |
| **Component** | HMI Cluster |
| **Environment** | {f['environment']} |
| **Severity** | {f.get('customfield_severity', 'Major')} |
| **Priority** | {f['priority']['name']} |

### Description
{f['description']}
        """.strip()
