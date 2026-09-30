"""
Automotive Test Report Generator
Produces HTML Test Summary Reports conforming to ISO 29119 / ASPICE test documentation standards.
Fulfills JD: "Maintain accurate test execution records and provide detailed test reports. Support release recommendations."
"""
from typing import List, Dict, Any
import time


class TestReportGenerator:
    @staticmethod
    def generate_html_report(
        suite_name: str,
        results: List[Dict[str, Any]],
        sw_version: str = "v2.4.0-RC3",
        target_hw: str = "Audi Virtual Cockpit Gen2"
    ) -> str:
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        pass_rate = (passed / total * 100) if total > 0 else 0

        release_rec = "GO FOR RELEASE" if (failed == 0 and pass_rate >= 95.0) else "NO-GO (BLOCKING DEFECTS FOUND)"
        rec_color = "#00e676" if "GO FOR" in release_rec else "#ff3366"

        rows_html = []
        for r in results:
            status_color = "#00e676" if r["status"] == "PASS" else "#ff3366"
            rows_html.append(f"""
            <tr style="border-bottom: 1px solid #202b3d;">
                <td style="padding: 12px; font-weight: bold; color: #fff;">{r['test_id']}</td>
                <td style="padding: 12px; color: #d1dcfa;">{r['name']}</td>
                <td style="padding: 12px;"><span style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color}; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 11px;">{r['status']}</span></td>
                <td style="padding: 12px; color: #8e9bb5; font-size: 12px;">{r.get('duration_ms', 15)}ms</td>
                <td style="padding: 12px; color: {'#ff7799' if r['status'] == 'FAIL' else '#8e9bb5'}; font-size: 12px;">{r.get('message', 'Passed successfully')}</td>
            </tr>
            """)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Automotive HMI Test Execution Report - {suite_name}</title>
    <style>
        body {{ background: #0a0e17; color: #f0f4fc; font-family: -apple-system, sans-serif; padding: 30px; margin: 0; }}
        .header-card {{ background: #121826; border: 1px solid #202b3d; border-radius: 12px; padding: 24px; margin-bottom: 24px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 20px 0; }}
        .metric-box {{ background: #162033; padding: 18px; border-radius: 10px; text-align: center; border: 1px solid #2b3d5c; }}
        .metric-val {{ font-size: 2rem; font-weight: bold; font-family: monospace; }}
        table {{ width: 100%; border-collapse: collapse; background: #121826; border-radius: 12px; overflow: hidden; border: 1px solid #202b3d; }}
        th {{ background: #1a2436; color: #00e5ff; text-align: left; padding: 14px; font-size: 13px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="header-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h1 style="margin:0; font-size: 1.5rem; color:#fff;">Automotive HMI Test Execution Summary</h1>
                <p style="color:#8e9bb5; margin-top:6px; font-size: 0.85rem;">Suite: {suite_name} | HW: {target_hw} | SW: {sw_version}</p>
            </div>
            <div style="text-align:right;">
                <span style="font-size: 0.8rem; color:#8e9bb5; display:block; margin-bottom:4px;">RELEASE RECOMMENDATION</span>
                <span style="background:{rec_color}22; color:{rec_color}; border:2px solid {rec_color}; padding:6px 16px; border-radius:8px; font-weight:bold; font-size:14px;">{release_rec}</span>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-box">
                <div style="font-size: 11px; color:#8e9bb5;">TOTAL TESTS</div>
                <div class="metric-val" style="color:#fff;">{total}</div>
            </div>
            <div class="metric-box">
                <div style="font-size: 11px; color:#00e676;">PASSED</div>
                <div class="metric-val" style="color:#00e676;">{passed}</div>
            </div>
            <div class="metric-box">
                <div style="font-size: 11px; color:#ff3366;">FAILED</div>
                <div class="metric-val" style="color:#ff3366;">{failed}</div>
            </div>
            <div class="metric-box">
                <div style="font-size: 11px; color:#00e5ff;">PASS RATE</div>
                <div class="metric-val" style="color:#00e5ff;">{pass_rate:.1f}%</div>
            </div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Test ID</th>
                <th>Test Case Name</th>
                <th>Status</th>
                <th>Execution Time</th>
                <th>Diagnostic Details</th>
            </tr>
        </thead>
        <tbody>
            {"".join(rows_html)}
        </tbody>
    </table>
</body>
</html>"""
        return html
