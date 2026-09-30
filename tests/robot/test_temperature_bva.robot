*** Settings ***
Documentation     Automotive HMI - Outside Temperature & Snowflake Ice Warning BVA Test Suite
...               Validates boundary value analysis, hysteresis behavior, and freeze warning telltales.
...               Reference: ISO 2575 & Functional Specification REQ-HMI-TEMP-042
Library           ../../tools/robot_hmi_library.py

Suite Setup       Initialize Cluster Test Bench
Suite Teardown    Shutdown Test Bench

*** Test Cases ***
TC_TEMP_BVA_001: Baseline Warm Temperature - Snowflake Must Be OFF
    [Documentation]    Verifies that normal ambient temperature (6.0°C) does NOT activate the snowflake warning.
    [Tags]             Functional    Baseline    P3
    Given Vehicle CAN Simulation Is Active
    When Outside Temperature Signal Is Injected    6.0
    Then Snowflake Telltale Status Should Be       OFF
    And Displayed Outside Temperature Should Be    6.0

TC_TEMP_BVA_002: Just Above Trigger Boundary (5.1°C) - Snowflake Must Be OFF
    [Documentation]    Boundary test immediately above the 5.0°C freeze threshold.
    [Tags]             BVA    Safety    P2
    When Outside Temperature Signal Is Injected    5.1
    Then Snowflake Telltale Status Should Be       OFF

TC_TEMP_BVA_003: Exact Boundary Value (5.0°C) - Strictly Below Requirement
    [Documentation]    Requirement specifies 'below 5.0°C' (< 5.0). 5.0°C must remain OFF.
    [Tags]             BVA    Critical    P1
    When Outside Temperature Signal Is Injected    5.0
    Then Snowflake Telltale Status Should Be       OFF

TC_TEMP_BVA_004: Just Below Boundary Value (4.9°C) - Snowflake MUST Turn ON
    [Documentation]    First value strictly below 5.0°C. Must illuminate snowflake telltale and chime.
    [Tags]             BVA    Safety    P1
    When Outside Temperature Signal Is Injected    4.9
    Then Snowflake Telltale Status Should Be       ON

TC_TEMP_BVA_005: Deep Freezing Temperature (3.0°C) - Continuous Illumination
    [Documentation]    Verifies steady ON state under freezing conditions.
    [Tags]             Functional    P2
    When Outside Temperature Signal Is Injected    3.0
    Then Snowflake Telltale Status Should Be       ON

TC_TEMP_BVA_006: Rising Temperature Hysteresis (4.5°C to 5.5°C) - Must Remain ON
    [Documentation]    Tests hysteresis memory: When warming up from cold, warning must stay ON below 6.0°C.
    [Tags]             Hysteresis    Stability    P1
    When Outside Temperature Signal Is Injected    3.0
    Then Snowflake Telltale Status Should Be       ON
    When Outside Temperature Signal Is Injected    5.5
    Then Snowflake Telltale Status Should Be       ON    # Hysteresis prevents flickering

TC_TEMP_BVA_007: Rising Temperature Past Hysteresis Threshold (6.0°C) - Extinguish Warning
    [Documentation]    Verifies snowflake turns OFF once temperature reliably rises to 6.0°C.
    [Tags]             Hysteresis    P2
    When Outside Temperature Signal Is Injected    6.0
    Then Snowflake Telltale Status Should Be       OFF

TC_TEMP_DEFECT_008: Defect Verification - Snowflake Must NOT Be Active at 13.0°C
    [Documentation]    Catches the Audi Cockpit Image 1 defect where snowflake was active at 13.0°C!
    [Tags]             Regression    Defect_Verification    P1
    When Outside Temperature Signal Is Injected    13.0
    Then Snowflake Telltale Status Should Be       OFF
