import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPep8
from EVE_Gnosis.simulations.capacitor import Capacitor


def test_micro_jump_drive():
    expected_cached_run_count = 110
    expected_low_water_mark = 568.0036963311873
    expected_time = 2112000
    expected_capacitor_tick_0_percent = 0.92
    expected_capacitor_tick_0_time = 0
    expected_capacitor_tick_7_percent = 0.37
    expected_capacitor_tick_7_time = 1344000
    expected_capacitor_tick_8_percent = 0.29
    expected_capacitor_tick_8_time = 1536000
    expected_capacitor_tick_max_run_percent = 0.06
    expected_capacitor_tick_max_run_time = 2401000
    expected_failed_to_run_modules = True

    capacitor_amount = 10000
    capacitor_recharge = 9999999999999  # Can't set to 0 (divide by 0), set to a large number to kill regen
    module_list = [
        {
            'Amount': -786,
            'CycleTime': 12000,
            'ReactivationDelay': 180000,
        }
    ]  # Micro Jump Drive

    run_time = 2400000 # increase thee max run time from the default of 10 minutes
    matrix = Capacitor.capacitor_time_simulator(module_list,
                                                capacitor_amount,
                                                capacitor_recharge,
                                                run_time,
                                                )

    cached_runs_count = 0
    for _ in matrix['Cached Runs']:
        cached_runs_count += 1

    assert expected_cached_run_count == cached_runs_count
    assert expected_low_water_mark == matrix['Stability']['LowWaterMark']
    assert expected_time == matrix['Stability']['LowWaterMarkTime']

    assert expected_capacitor_tick_0_percent == matrix['Cached Runs'][0]['Capacitor Percentage']
    assert expected_capacitor_tick_0_time == matrix['Cached Runs'][0]['Current Time']
    assert expected_capacitor_tick_7_percent == matrix['Cached Runs'][7]['Capacitor Percentage']
    assert expected_capacitor_tick_7_time == matrix['Cached Runs'][7]['Current Time']
    assert expected_capacitor_tick_8_percent == matrix['Cached Runs'][8]['Capacitor Percentage']
    assert expected_capacitor_tick_8_time == matrix['Cached Runs'][8]['Current Time']
    assert expected_capacitor_tick_max_run_percent == matrix['Cached Runs'][cached_runs_count - 1][
        'Capacitor Percentage']
    assert expected_capacitor_tick_max_run_time == matrix['Cached Runs'][cached_runs_count - 1]['Current Time']
    assert expected_failed_to_run_modules == matrix['Stability']['FailedToRunModules']
