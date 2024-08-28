#  COPYRIGHT Ericsson 2019
#  The copyright to the computer program(s) herein is the property of
#  Ericsson Inc. The programs may be used and/or copied only with written
#  permission from Ericsson Inc. or in accordance with the terms and
#  conditions stipulated in the agreement/contract under which the
#  program(s) have been supplied.

import os
import re
from shutil import rmtree

root_dir = os.getcwd()

tool = 'dxp.py'
input_data_dir = 'features/steps/data'
output_data_dir = 'out/test/data'


def before_all(context):
    rmtree('out', ignore_errors=True)


def before_scenario(context, scenario):
    # Always set the actual directory to be the root dir.
    # Test steps can modify the current directory with no side effects.
    os.chdir(root_dir)

    scenario_name = re.sub(r'[ ,\']+', '_', scenario.name)
    # The directory for storing test data for the scenario.
    scenario_dir = f'{output_data_dir}/{scenario_name}'
    # Remove the scenario directory, if exists.
    rmtree(scenario_dir, ignore_errors=True)
    # Create the scenario directory again, empty.
    os.makedirs(scenario_dir, exist_ok=True)
    # Save the scenario directory path to be used in scenarios.
    context.scenario_dir = scenario_dir
    # Save the root directory to be used in scenarios.
    context.root_dir = root_dir
