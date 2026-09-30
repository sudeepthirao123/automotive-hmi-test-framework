*** Settings ***
Documentation     Automotive HMI - ISO 2575 Safety Telltale Validation Suite
...               Validates Ignition KL15 lamp test (bulb check), telltale illumination, and colors.
...               Reference: ISO 2575 & ECE R121.
Library           ../../tools/robot_hmi_library.py

Suite Setup       Initialize Cluster Test Bench
Suite Teardown    Shutdown Test Bench

*** Test Cases ***
TC_TELL_001: Ignition KL15 Bulb Check (Lamp Test)
    [Documentation]    When switching from KL30 to KL15, safety telltales must illuminate for 2 seconds.
    [Tags]             Telltale    KL15    Safety    P1
    When Ignition State Changes To    KL15_ON
    Then Telltale Status Should Be    Seatbelt_Warning_Lamp    SOLID_RED
    And Telltale Status Should Be     Airbag_Warning_Lamp      SOLID_RED
    And Telltale Status Should Be     Brake_System_Lamp        SOLID_RED

TC_TELL_002: Seatbelt Reminder Warning Under Driving Conditions
    [Documentation]    When driving without seatbelt (> 20 km/h), telltale must flash red.
    [Tags]             Telltale    Seatbelt    Safety    P1
    When Vehicle Speed CAN Signal Injected    25.0
    And Seatbelt Buckle Status Set To         UNLATCHED
    Then Telltale Status Should Be            Seatbelt_Warning_Lamp    FLASHING_RED
