*** Settings ***
Documentation     Automotive HMI - Tire Pressure Monitoring System (TPMS) Validation
...               Validates unit consistency across all 4 wheels (bar vs kPa), nominal ranges, and UI errors.
...               Reference: ECE R64 & Functional Specification REQ-HMI-TPMS-108
Library           ../../tools/robot_hmi_library.py

Suite Setup       Initialize Cluster Test Bench
Suite Teardown    Shutdown Test Bench

*** Test Cases ***
TC_TPMS_001: Nominal Pressure Display in Metric Mode (kPa)
    [Documentation]    All 4 wheels must display equal units ('kPa') and nominal pressure (230 kPa).
    [Tags]             TPMS    Metric    P2
    Given System Units Are Set To    METRIC
    When TPMS CAN Signals Injected    FL=230    FR=230    RL=230    RR=230
    Then All Four Wheels Should Display Unit    kPa
    And All Four Wheels Pressure Should Match Injected Values

TC_TPMS_002: Defect Catch - Front Right Must NOT Display 'bar' In Metric Mode
    [Documentation]    Direct regression test catching the Audi Cockpit Image 1 defect (FR displaying 444 bar).
    [Tags]             TPMS    Defect_Verification    Critical    P1
    Given System Units Are Set To    METRIC
    When TPMS CAN Signals Injected    FL=230    FR=230    RL=230    RR=230
    Then Wheel Unit Should Be    FR    kPa    # Must never be 'bar' in Metric mode!
    And Wheel Pressure Should Not Exceed Maximum Physical Limit    FR    500

TC_TPMS_003: Low Pressure Warning Threshold
    [Documentation]    Tire dropping below 180 kPa must trigger TPMS Amber Telltale.
    [Tags]             TPMS    Safety    P1
    When TPMS CAN Signals Injected    FL=165    FR=230    RL=230    RR=230
    Then Telltale Status Should Be    TPMS_Warning_Lamp    SOLID_AMBER
