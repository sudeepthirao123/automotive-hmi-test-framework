*** Settings ***
Documentation     Automotive HMI - Speedometer Digital vs Analog Needle Synchronization
...               Validates that analog needle angle aligns with the digital center readout.
...               Reference: UNECE Regulation 39 & Safety ASIL B Requirements.
Library           ../../tools/robot_hmi_library.py

Suite Setup       Initialize Cluster Test Bench
Suite Teardown    Shutdown Test Bench

*** Test Cases ***
TC_SPEED_001: Standstill Vehicle Speed Verification (0 km/h)
    [Documentation]    At 0 km/h, digital speed must read 0.0 and needle angle must be 0.0 degrees.
    [Tags]             Speedometer    Sanity    P1
    When Vehicle Speed CAN Signal Injected    0.0
    Then Displayed Digital Speed Should Be    0.0
    And Analog Needle Calculated Speed Should Match Digital Readout    Tolerance=1.0

TC_SPEED_002: City Cruise Speed Verification (50 km/h)
    [Documentation]    At 50 km/h, verify needle sync.
    [Tags]             Speedometer    P2
    When Vehicle Speed CAN Signal Injected    50.0
    Then Displayed Digital Speed Should Be    50.0
    And Analog Needle Calculated Speed Should Match Digital Readout    Tolerance=1.5

TC_SPEED_003: Highway Speed Verification (100 MPH in Imperial Mode)
    [Documentation]    Catches the Image 1 defect where needle is stuck at 72 while digital reads 100 MPH.
    [Tags]             Speedometer    Defect_Verification    Critical    P1
    Given System Units Are Set To    IMPERIAL
    When Vehicle Speed CAN Signal Injected    160.9    # 100 MPH in km/h
    Then Displayed Digital Speed Should Be    100.0
    And Analog Needle Calculated Speed Should Match Digital Readout    Tolerance=2.0
