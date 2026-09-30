# Automotive HMI & IVI Senior Test Engineer Interview Master Guide

> **Prepared for:** Client Interview (Senior Manual Test Engineer – Automotive HMI & Test Automation)  
> **Target Role:** Senior Test Engineer validating In-Vehicle Infotainment (IVI), Digital Instrument Cluster (HMI), Signal Simulation, and Test Automation Execution  
> **Key Principle:** Explained in **simple, easy-to-remember words** first, followed by the **exact professional phrases** to use in the interview.

---

## Table of Contents
1. [Core Mindset & How Interviewers Evaluate You](#1-core-mindset--how-interviewers-evaluate-you)
2. [Automotive Concepts Explained in Plain English](#2-automotive-concepts-explained-in-plain-english)
3. [The 10 Most Important Interview Questions (With Easy & Professional Answers)](#3-the-10-most-important-interview-questions)
   - Q1: Complete End-to-End Testing Lifecycle (Requirements to Release)
   - Q2: Elements of a Perfect Defect Report (Jira Ticket)
   - Q3: Post-Fix Workflow (Retesting vs. Regression Testing)
   - Q4: Regression Testing Strategy & Test Case Selection
   - Q5: Should Every Fixed Defect Be Added to Regression?
   - Q6: Handling 1-Day Regression Crunches & Urgent Releases
   - Q7: Defect Duplication & Multi-Tester Coordination
   - Q8: When NOT to Create a Defect Ticket
   - Q9: Boundary Value Analysis (BVA) & The Snowflake Warning (Deep Dive)
   - Q10: Automotive HMI Testing Specifics (Telltales, Sensor Disconnect, Log Analysis)
4. [Defect Spotting Mastery: Complete Analysis of Provided Images](#4-defect-spotting-mastery-complete-analysis-of-provided-images)
   - Screen 1: Audi Digital Cockpit (12 Defects Dissected)
   - Screen 2: IVI Media Player (7 Defects Dissected)
5. [Additional IVI Defect Practice Scenarios (Interview Drills)](#5-additional-ivi-defect-practice-scenarios)
   - Scenario 3: HVAC Dual-Zone Climate Display
   - Scenario 4: ADAS & Cluster Navigation Display
   - Scenario 5: Bluetooth / Handsfree Call Screen
   - Scenario 6: EV Battery Management & Charging Cluster
6. [Sample Automotive Jira Defect Tickets](#6-sample-automotive-jira-defect-tickets)
7. [Automotive Acronyms Cheat Sheet](#7-automotive-acronyms-cheat-sheet)

---

## 1. Core Mindset & How Interviewers Evaluate You

The interviewers are assessing **three critical pillars**:

1. **Defect Acumen (Eagle Eye):**  
   Can you look at a car screen (Cluster or Infotainment) and immediately spot layout flaws, unit mismatches, localization bugs, logic contradictions, and timing errors?
2. **Testing Rigor (ISTQB & Methodology):**  
   Do you blindly run test cases, or do you understand *why* you use Boundary Value Analysis (BVA), Equivalence Partitioning (EP), and State Transition Testing? Do you understand the difference between *retesting* and *regression*?
3. **Automotive Domain Wisdom:**  
   Do you know how vehicle hardware works? Do you understand CAN signals, sensor timeouts, DTCs (Diagnostic Trouble Codes), telltale safety priorities (Red = Stop immediately, Amber = Caution/Take action, Green/Blue = Active system), and log analysis (DLT, Android logcat, QNX slog2)?

---

## 2. Automotive Concepts Explained in Plain English

| Term | What it is in Simple Words | Real Car Example |
| :--- | :--- | :--- |
| **HMI (Human-Machine Interface)** | Everything the driver looks at or touches to interact with the car. | The digital speed screen (Cluster), the middle touchscreen (IVI), and the windshield projection (HUD). |
| **Cluster (Instrument Cluster)** | The screen behind the steering wheel displaying critical driving data. | Speedometer, tachometer (RPM), fuel/battery level, warning lights. Must NEVER crash or freeze. |
| **IVI (In-Vehicle Infotainment)** | The center dashboard display for entertainment and comfort. | Radio, Spotify/Media, Bluetooth calls, Navigation maps, HVAC climate controls, Vehicle settings. |
| **Telltale** | An internationally standardized warning or status symbol on the dashboard. | Check Engine icon, Seatbelt light, Low Tyre Pressure, High Beam blue light, Snowflake ice warning. |
| **CAN Bus (Controller Area Network)** | The internal nervous system/wires of the car allowing different microcomputers (ECUs) to talk to each other without a central server. | When the outside temperature sensor reads 3°C, it broadcasts a CAN message; the Cluster ECU reads it and lights up the snowflake telltale. |
| **HIL (Hardware-in-the-Loop) Bench** | A lab testing setup where the actual car screens and computers are connected to simulated car sensors on a desk. | You don't need a real car driving in freezing snow to test the snowflake icon; you use a simulation tool (like Vector CANoe) to send a fake temperature signal to the screen. |
| **DTC (Diagnostic Trouble Code)** | A 5-character error code saved by the car when something breaks. | If you unplug the temperature sensor, the ECU logs a DTC (e.g., `U0100` or `B1045`) indicating "Sensor signal open circuit". |
| **DLT (Diagnostic Log and Trace)** | The standard automotive logging format used to see what the software was doing when an issue occurred. | Like a flight black box recording software events, CAN message exchanges, and internal error codes. |
| **Hysteresis** | An intentional delay or gap between the ON threshold and OFF threshold to prevent a display from flickering rapidly. | If warning turns ON at 4.9°C, it shouldn't flicker off at 5.0°C and on at 4.9°C while driving. It turns ON at 4.9°C and stays ON until temp rises steadily past 6.0°C. |

---

## 3. The 10 Most Important Interview Questions

### Q1: Explain your complete testing process from requirement analysis to customer release.

#### In Easy Words:
> "Testing is not just clicking buttons. First, I study the requirement document to make sure it's clear and not missing details. Then I write the test plan and test cases. Next, I verify my test bench and simulator are ready. Then I execute the tests, log bugs with logs/traces, verify bug fixes, run regression tests, and finally provide a test report showing pass/fail percentages and my release recommendation."

#### Professional Interview Answer:
> "I follow the V-Model / ASPICE testing lifecycle:
> 1. **Requirement Analysis:** Review functional specifications and HMI UX guidelines. I check for ambiguities, contradictory acceptance criteria, and ensure requirements are testable.
> 2. **Test Planning & Test Design:** Determine scope, test types (Functional, Boundary, Regression, Negative), and write test cases linked to requirements for 100% traceability (e.g., in Jira / Polarion / DOORS).
> 3. **Environment Setup & Sanity Check:** Verify the HIL test bench, flashing the correct target SW/HW version, and configuring simulation tools (e.g., Vector CANoe/CANalyzer).
> 4. **Execution & Defect Logging:** Execute manual test cases and automated suites. For every failure, collect evidence (screenshots, videos, CAN traces `.blf`/`.asc`, DLT logs) and log clear Jira tickets.
> 5. **Bug Retesting & Regression:** Retest fixed tickets and execute a focused regression suite to ensure no side effects.
> 6. **Test Reporting & Release Support:** Deliver the final Test Summary Report with execution metrics, defect density by severity, and a clear Go/No-Go release recommendation based on exit criteria."

---

### Q2: What are the typical elements of a good defect report (Jira ticket)?

#### In Easy Words:
> "A developer should never have to call me to ask 'how do I reproduce this?' A good defect report tells them exactly what happened, where it happened, how to recreate it step-by-step, proof (screenshot/log), and why it matters."

#### Professional Checklist for Jira Defect:
1. **Summary / Title:** Concise, formatted: `[Component][Function] Short description of problem` (e.g., `[Cluster][TPMS] Inconsistent pressure units (bar vs kPa) displayed on front right tire`).
2. **Environment & Build Details:** Software version, Hardware variant, Target display (Cluster/IVI), Test bench ID.
3. **Severity & Priority:** 
   - Severity = Technical/safety impact (Critical, Major, Minor).
   - Priority = Urgency of fix for this release (P1, P2, P3).
4. **Preconditions:** Initial car state (e.g., Ignition ON, Vehicle speed = 0 km/h, Language = German).
5. **Step-by-Step Reproduction:** Numbered steps starting from the home screen.
6. **Expected Result:** What the specification says should happen.
7. **Actual Result:** What actually happened on the screen.
8. **Test Evidence:** Clear screenshot/video showing the defect highlighted.
9. **Logs & Traces:** Attached DLT logs, system logcat/slog2, and synchronized CAN bus traces (`.blf` or `.asc`).
10. **Impact Analysis & Component Owner:** Which module is affected (e.g., HMI Middleware, TPMS ECU, Rendering engine).

---

### Q3: Once a developer fixes a defect, what testing do you perform? What is the difference between Retesting and Regression Testing?

#### In Easy Words:
> - **Retesting:** Checking the EXACT bug that was broken to see if it is now fixed. (Did the doctor fix the broken arm?)
> - **Regression Testing:** Checking the REST of the system to make sure the fix didn't accidentally break something else. (Did fixing the arm hurt the shoulder or leg?)

#### Detailed Comparison Table:

| Aspect | Retesting (Confirmation Testing) | Regression Testing |
| :--- | :--- | :--- |
| **Definition** | Testing specifically to verify that the reported defect has been resolved. | Testing other unchanged parts of the application to ensure the fix didn't introduce new bugs. |
| **Trigger** | Triggered immediately when a developer marks a defect as "Resolved / Ready for Test". | Triggered after a build contains one or more bug fixes, new features, or code changes. |
| **Scope** | Very narrow: Only the exact failed test case and specific steps from the Jira ticket. | Broader: Dependent modules, related workflows, and critical path test cases. |
| **Automation** | Usually done manually first with exact parameters. | High priority for automation execution (e.g., Robot Framework / PyTest). |

---

### Q4: If you have thousands of test cases and limited time, how do you decide which tests to include in Regression Testing?

#### In Easy Words:
> "You cannot run everything when time is short. You use Risk-Based Testing: First test safety-critical features (speed, brakes, airbags, telltales), then test features directly connected to the code that changed (impact analysis), then high-frequency customer features (navigation, radio, climate). You skip low-risk edge cases."

#### Professional 4-Tier Selection Strategy:
1. **Safety-Critical & Legal Requirements (Highest Priority - ASIL/ISO):**
   - Speedometer display accuracy, warning lamps (Brake, Airbag, Engine, Seatbelt), gear selection status.
2. **Impact-Based Test Cases (Ripple Effect):**
   - Analyze developer release notes and Git commits. If the developer touched the Media Player Bluetooth stack, execute all Bluetooth, phonebook, and audio routing test cases.
3. **Core / Happy Path User Workflows:**
   - Ignition ON/OFF cycles, cluster sleep/wake modes, language switching, volume adjustment.
4. **Historical Failure Prone Areas:**
   - Modules with frequent regression bugs in previous builds.

---

### Q5: Should EVERY fixed defect be added to the regression suite? Give one scenario where you would add it and one where you would not.

#### In Easy Words:
> "No! If you add every bug to the regression suite, your suite will become gigantic and impossible to finish. Only add bugs that represent high risk, core functionality, or common user paths."

#### Concrete Examples to Give in the Interview:
- **Scenario WHERE YOU WOULD ADD IT (YES):**
  > *"A defect where the digital speedometer freezes when shifting from Drive to Reverse while navigating. This is a critical safety issue and an important customer path. We must automate/add this to our regression suite to ensure it never happens again."*
- **Scenario WHERE YOU WOULD NOT ADD IT (NO):**
  > *"A cosmetic spelling typo in the Finnish language sub-menu under 'Ambient Lighting - Custom Color 3' that only occurred when transitioning from Swedish to Finnish in engineering test mode. This is an ultra-rare edge case with zero safety impact; retesting once is sufficient, adding it to regression wastes precious execution time."*

---

### Q6: If regression testing must be completed within ONE DAY due to an urgent customer release deadline, what do you do?

#### In Easy Words:
> "1. Don't panic.  
> 2. Run our automated sanity/smoke suite first.  
> 3. Focus manual testing strictly on the changes made for this release and safety-critical functions.  
> 4. Divide tests among team members.  
> 5. Communicate risks clearly to management: 'We validated critical paths; non-critical areas have residual risk'."

#### Professional Answer:
> 1. **Execute Automated Smoke/Sanity Suite:** Immediately trigger automated Robot Framework/Python test suites covering basic sanity checks across all ECUs and displays.
> 2. **Apply Impact & Risk-Based Selection:** Consult with the software leads to identify exact modules touched in the hotfix. Select only tests directly related to the fix plus P1 safety telltales and cluster displays.
> 3. **Parallel Execution:** Distribute test cases across available test benches and team members (e.g., Tester A on Cluster, Tester B on IVI).
> 4. **Blocker First Policy:** Log blockers immediately and communicate directly with the customer proxy team without waiting for end-of-day reports.
> 5. **Transparent Release Documentation:** Clearly document which test suites were executed, which were omitted due to time constraints, and provide a calculated Risk Assessment for customer sign-off.

---

### Q7: If two testers discover the same defect, should they create two Jira tickets? How do you prevent duplicates?

#### In Easy Words:
> "No, never create duplicate tickets! It wastes developers' time and clutters the system. Before logging a bug, you search Jira. If another tester found it first, you add your logs or extra findings as a comment on their ticket instead."

#### Professional Answer:
> "They should **not** create two separate tickets. Creating duplicates artificially inflates defect metrics and leads to duplicate triage and developer investigation.
> 
> **How to prevent and handle duplicates:**
> 1. **Search Before Logging:** Always query Jira by component, keyword, or error symptom (e.g., `component = Cluster AND text ~ "tire pressure"`).
> 2. **Collaborate & Comment:** If another tester already logged the issue, the second tester should add any additional evidence (such as reproduction on another HW variant or an alternative CAN trace) as a comment on the existing ticket.
> 3. **If a Duplicate is Accidentally Created:** Mark the newer ticket as `Closed - Duplicate` and link it using Jira's `Duplicates` relation to the primary ticket."

---

### Q8: When would you NOT create a defect ticket even when you observe unexpected behavior?

#### Interview Traps Solved Simply:
1. **Test Environment / Setup Issue:** A loose OBD/CAN cable, incorrect power supply voltage (e.g., 9V instead of 12V), or corrupted flashing environment. *Action: Fix the bench setup and rerun.*
2. **Expected Behavior per Updated Specification:** A feature change was agreed upon in a Change Request (CR) but the tester was reading an outdated specification document. *Action: Verify with requirements engineer.*
3. **Known Issue Already Documented:** The defect is already open and acknowledged in the current sprint/release backlog. *Action: Link/reference existing ticket.*
4. **Third-Party / Customer Proxy Known Limitation:** A planned mock or stub in early development stages (e.g., navigation maps not loaded because GPS simulator is offline). *Action: Document in test execution log, do not log a SW defect.*
5. **Non-Reproducible Single Glitch without Logs:** If an anomaly happens once but cannot be reproduced after 10 attempts and no logs/traces were captured. *Action: Note as an observation in testing notes, continue monitoring with debug logging enabled.*

---

### Q9: Boundary Value Analysis (BVA) & The Snowflake Warning (Deep Dive)

#### The Exact Interview Question:
> **Requirement:** An automotive HMI displays a snowflake symbol based on outside temperature:
> - Snowflake should appear when temperature goes **below 5°C**.
> - Snowflake should remain displayed while temperature is low.
> - Snowflake should disappear when temperature rises **above 4°C** (or 6°C depending on hysteresis spec).

#### 1. What is Boundary Value Analysis (BVA)?
> **Easy Words:** "Software almost always breaks at the edges of ranges—at the exact border where the rules change. BVA tests the exact boundary, one step below, and one step above."

#### 2. Exact Test Values Selection Table:
Assuming standard 2-point / 3-point BVA with 0.1°C resolution:

| Test Temp (°C) | Direction / Action | Expected Snowflake Status | Rationale |
| :--- | :--- | :--- | :--- |
| **6.0°C** | Normal high temp | **OFF** | Well above boundary. |
| **5.1°C** | Just above boundary | **OFF** | Above 5°C threshold. |
| **5.0°C** | Exactly ON boundary | **OFF** (if req says `< 5°C`) | Critical boundary test! "Below 5" means 5.0 is still OFF. |
| **4.9°C** | Just below boundary | **ON** | First value strictly below 5.0°C. Snowflake MUST turn ON. |
| **3.0°C** | Low temperature | **ON** | Stays ON while freezing. |
| **3.9°C** | Rising temperature | **ON** | Low temp state maintained. |
| **4.0°C** | Disappearance boundary | **ON/OFF** (Check spec!) | Critical boundary for rising temperature. |
| **4.1°C** | Just above disappearance | **OFF** | If threshold is `> 4°C`, must turn OFF. |

#### 3. What is Hysteresis and Why is it Essential in Cars?
> **Say this in the interview to impress them:**
> *"Outside temperature sensors oscillate rapidly due to wind, engine heat, and sensor noise. If the threshold were strictly 5.0°C for both ON and OFF, a car driving at 4.9°C - 5.0°C would cause the snowflake icon and warning chime to toggle on and off every two seconds, distracting the driver!  
> Therefore, automotive systems use **hysteresis**: turning ON when dropping below 5.0°C (at 4.9°C), and remaining ON until the temperature safely rises above 6.0°C or 7.0°C."*

---

### Q10: Automotive HMI Testing Specifics (Telltales, Sensor Disconnect, Log Analysis)

1. **Telltale Testing Rules:**
   - **Lamp Test on Ignition ON (KL15):** When key turns to ignition, all safety telltales must illuminate for 2–3 seconds (bulb check), then turn off if no errors exist.
   - **Color Standardization (ISO 2575):**
     - **RED:** Immediate danger (Brake failure, engine overheat, battery charging defect, airbag fault).
     - **AMBER / YELLOW:** Attention required / degraded mode (Check engine, low fuel, TPMS, ABS fault).
     - **GREEN / BLUE:** System operational status (Turn signals, low beam, high beam).
2. **Sensor Disconnection / Bus Timeout Testing:**
   - What happens if the outside temperature sensor is disconnected?
   - The ECU stops receiving CAN messages. After a timeout period (e.g., 500ms), the Cluster must:
     1. NOT freeze or crash.
     2. Display fallback symbols (e.g., `--.- °C` or invalid indicator).
     3. Log a CAN timeout DTC (e.g., `U0100`).
     4. Deactivate unreliable telltales.
3. **Log Analysis Tools:**
   - **DLT (Diagnostic Log and Trace):** Filter by ECU Application ID (APID) and Context ID (CTID) to see infotainment and cluster middleware events.
   - **Vector CANoe/CANalyzer:** Open `.blf` / `.asc` traces, filter by CAN ID or Signal name (e.g., `AmbientTemp_Raw`).
   - **Android Automotive OS (AAOS):** `adb logcat -b main -b system` filtered by tag or package name.
   - **QNX:** `slog2info` for real-time OS logs.

---

## 4. Defect Spotting Mastery: Complete Analysis of Provided Images

### Screen 1: Audi Digital Cockpit (`cd2cf8d5-fa25-4311-949c-eb79230194b5.jpg`)

Here are the **12 defects** present in the instrument cluster image:

```
+-----------------------------------------------------------------------------------+
| [1] Fuel: "Hello"         [2] Media: 450 km              Status Bar               |
|                                                                                   |
|    ( 4 )            TYRE PRESSURE (Reifendruck)                 ( 100 )           |
|  ( 3   5 )          [3] FL: 444 kPa  |  [4] FR: 444 bar       ( 80    120 )       |
| ( 2     7 )             44.4°C [5]   |      44°C             ( 60      140 )      |
| ( 1  Datum )                                                 ( 40  [7]  160 )     |
| (  30.02.21) [6]    [8] German typo: "Zurücksezten"          ( 20 [8]   180 )     |
|    ( D4 )                                                        ( 100 MPH ) [9]  |
|                                                                                   |
| [12] Telltale Overlap   [10] Snowflake at 13.0°C     [11] 21:30 AM & Units (km)   |
+-----------------------------------------------------------------------------------+
```

1. **Impossible Date (Fatal Calendar Logic Bug):**
   - Left dial displays `Datum: 30.02.2021`. February never has 30 days.
2. **Top Bar Fuel Indicator String Bug:**
   - Fuel pump icon displays text string `"Hello"` instead of fuel range or level.
3. **Top Bar Media Icon String Mismatch:**
   - Music note icon displays distance string `"450 km"` instead of track/audio metadata.
4. **TPMS Unit Inconsistency & Dangerous Pressure Value:**
   - Front Left reads `444 kPa`, while Front Right reads `444 bar`! 
   - 444 bar is physically impossible (~440 atmospheres). Front right unit should be kPa, not bar.
5. **TPMS Temperature Decimal Inconsistency:**
   - Front Left shows `44.4°C` (one decimal point), whereas all other three tires show integer `44°C`.
6. **German Spelling Error (L10n):**
   - Reset button prompt reads `"Zurücksezten mit OK"`. Correct German spelling is `"Zurücksetzen"` (extra 'z').
7. **Analog Needle vs. Digital Speed Mismatch:**
   - Digital readout in the center of the right dial displays `100 MPH`.
   - The white analog needle points to approximately `70 - 75 MPH`.
8. **Navigation Turn Indicator Conflict:**
   - The large blue 3D navigation guidance arrow directs a **LEFT TURN**.
   - The lane assist indicator directly below it displays a highlighted **RIGHT TURN** arrow.
9. **Unit System Conflict (Metric vs Imperial):**
   - Speedometer center shows `100 MPH` (Imperial).
   - Speed limiter on bottom right shows `LIM 63 km/h` (Metric).
   - Odometer displays `223450 km` (Metric) and trip shows `1009,0 km` (Metric).
   - Units must be globally uniform based on vehicle region settings.
10. **Telltale Violation: Snowflake Active at 13°C:**
    - Ice hazard snowflake icon `*` is displayed next to `13.0 °C`. Freeze warnings should only appear below 4°C/5°C.
11. **Time Format Invalid String:**
    - Clock displays `21:30 AM`. 24-hour military time cannot have an `AM` suffix.
12. **UI Visual Collision / Text Overlap:**
    - The red seatbelt warning icon and amber ESP OFF icon are overlapping directly over the odometer mileage digits `223450 km` and clock `21:30 AM`.

---

### Screen 2: IVI Media Player (`e0aaf2ff-5c37-4132-9674-dae3cf68d97a.jpg`)

Here are the **7 defects** present in the Infotainment screen:

1. **Album Artwork Rotation & Severe Cropping:**
   - The album art for "A Beautiful Lie" (30 Seconds To Mars) is rotated 90° counter-clockwise and cropped horizontally.
2. **Severe Multilingual / Localization Collision:**
   - Top Header: `"Wiedergabe"` (German for Playback).
   - Source dropdown: `"Source"` (English).
   - Bottom Left Button: `"Список"` (Russian for Tracklist/List).
   - Bottom Right Button: `"More"` (English).
   - Three distinct languages displayed simultaneously on a single screen!
3. **Redundant Duplicate Metadata:**
   - Song title `"A Beautiful Lie"` is displayed as the main title header, and then repeated directly below the artist name:
     `30 Seconds To Mars`
     `A Beautiful Lie`
4. **Playback Scrubber Bar Desynchronization:**
   - Elapsed Time: `1:06` (66s).
   - Remaining Time: `-2:03` (123s).
   - Total Track Length: 189s.
   - 66s / 189s = **34.9% complete**.
   - However, the yellow scrubber handle is positioned at approximately **12%** of the bar.
5. **UI Bounding Box Clipping on Playback Controls:**
   - The playback control frame surrounding `|<`, `||`, `>|` has a misaligned bottom border that clips unevenly into the bottom menu divider.
6. **Inconsistent Naming & Capitalization:**
   - USB source label displays lowercase `"newstick"`. System style guidelines require title case (e.g., `"USB Stick 2"` or `"Newstick"`).
7. **Clock Format Discrepancy:**
   - Top right status bar displays `"0:31"`. Lacks AM/PM notation or two-digit 24h leading zero (`00:31`).

---

## 5. Additional IVI Defect Practice Scenarios

To ensure you can tackle any screen the interviewer presents, master these 4 additional automotive scenarios:

### Scenario 3: HVAC Dual-Zone Climate Control Display
- **Typical Defects to Look For:**
  1. *Temperature Conflict in SYNC Mode:* When `SYNC` button is illuminated, driver temp is set to 22.0°C, but passenger side displays 18.5°C.
  2. *Air Distribution Impossibility:* Defrost windshield icon, face vents, and footwell vents are all highlighted simultaneously in maximum fan speed without Auto mode.
  3. *Unit Mismatch:* Driver displays `21°C`, passenger displays `72°F`.
  4. *Fan Speed Indicator Bar Overflow:* Fan graphic has 7 segment bars, but 8 segments are filled.
  5. *Truncated Text in German/French:* `"Frontscheibenenteisung"` (Windshield defroster) truncated as `"Frontscheiben..."` with text overlapping the heated seat button.

### Scenario 4: ADAS & Cluster Navigation Display
- **Typical Defects to Look For:**
  1. *Speed Limit Mismatch:* Road sign recognition (TSR) camera shows `120 km/h`, but cluster digital display enforces a red warning ring at `90 km/h`.
  2. *Adaptive Cruise Control (ACC) Contradiction:* ACC icon is GREEN (active control), but brake pedal warning telltale is also RED (manual braking required).
  3. *Distance to Empty (Range) Calculation Error:* Fuel tank gauge shows 100% full, but Range shows `15 km`.
  4. *Lane Keep Assist Graphic Bug:* Car icon displayed driving outside the painted road borders while status reads "Lane Centered".

### Scenario 5: Bluetooth / Phone Handsfree Screen
- **Typical Defects to Look For:**
  1. *Timer Running in Disconnected State:* Call status says `"Call Ended / Disconnected"`, but the call duration timer continues incrementing `04:12... 04:13...`
  2. *Character Encoding (Mojibake):* Contact name with accents/umlauts displayed as `"Jrgen Mller"` or `"\u00e4"`.
  3. *Conflicting Audio Routing:* Bluetooth audio icon shows handset active, but speakerphone icon is also highlighted.
  4. *Mute Button Inversion:* Microphone icon shows slash through it (Muted), but status text reads `"Microphone Active"`.

### Scenario 6: EV Battery Management & Charging Screen
- **Typical Defects to Look For:**
  1. *Negative Charging Time:* Displays `"Time to 80%: -15 min"`.
  2. *State of Charge (SOC) Mismatch:* Battery graphic shows 50% fill, but text readout displays `92%`.
  3. *Power Flow Contradiction:* Vehicle is plugged into DC Fast Charger, but energy flow animation shows arrows moving from the battery out into the wall.
  4. *Charging Speed Calculation Bug:* Voltage = 400V, Current = 200A, but power displayed reads `8 kW` instead of `80 kW` (math conversion bug).

---

## 6. Sample Automotive Jira Defect Tickets

### Ticket 1: The Audi Cluster Tire Pressure Defect
* **Issue Type:** Bug
* **Summary:** `[Cluster][TPMS] Unit mismatch (bar instead of kPa) displayed for Front Right tire on Reifendruck screen`
* **Component:** Cluster_HMI / TPMS_Display
* **Affects Version:** `v2.4.0-RC3`
* **Hardware:** Audi Virtual Cockpit Gen2 HIL Bench #04
* **Severity:** Major (Incorrect unit display can lead to critical tire inflation errors)
* **Priority:** P2
* **Preconditions:**
  1. Ignition state = KL15 (Ignition ON).
  2. Cluster language set to German (`Deutsch`).
  3. Pressure units configured to Metric (`kPa`).
  4. CANoe simulation running `TPMS_Simulation_Pack.cfg`.
* **Steps to Reproduce:**
  1. Boot cluster to home screen.
  2. Use steering wheel left toggle to navigate to Vehicle Functions menu (`Fahrzeug`).
  3. Select Tire Pressure Monitor (`Reifendruck`).
  4. Observe tire pressure readings and units for all four wheels.
* **Expected Result:**
  - Front Right tire pressure displays in `kPa` (e.g., `444 kPa`), matching the other three wheels and system settings.
* **Actual Result:**
  - Front Right tire pressure displays unit `bar` (`444 bar`), creating an extreme unit discrepancy and displaying an impossible physical pressure.
* **Attachments:**
  - `cluster_tpms_unit_error.png` (Annotated screenshot)
  - `tpms_canoe_can_trace_2026-09-30.blf`
  - `dlt_cluster_hmi_trace.dlt`
* **Impact Analysis:**
  - Driver confusion regarding tire pressure safety. Potential compliance failure against ECE automotive cluster display requirements.

---

## 7. Automotive Acronyms Cheat Sheet

- **HMI:** Human-Machine Interface (Screens & visual controls).
- **IVI:** In-Vehicle Infotainment (Central multimedia screen).
- **HUD:** Head-Up Display (Windshield projection).
- **CAN:** Controller Area Network (Automotive message protocol).
- **ECU:** Electronic Control Unit (Car computer module).
- **HIL:** Hardware-in-the-Loop (Testing real ECU hardware with simulated vehicle signals).
- **SIL:** Software-in-the-Loop (Testing code in a PC virtual environment without real ECUs).
- **DTC:** Diagnostic Trouble Code (Vehicle error codes like `U0100`).
- **DLT:** Diagnostic Log and Trace (Automotive logging standard).
- **KL15:** Ignition switch ON (terminal 15).
- **KL30:** Permanent battery power (terminal 30).
- **KL31:** Ground (terminal 31).
- **ASIL:** Automotive Safety Integrity Level (A = lowest risk, D = highest safety risk like steering/braking).
- **ASPICE:** Automotive Software Process Improvement and Capability Determination.
