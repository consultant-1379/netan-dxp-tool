#  COPYRIGHT Ericsson 2019
#  The copyright to the computer program(s) herein is the property of
#  Ericsson Inc. The programs may be used and/or copied only with written
#  permission from Ericsson Inc. or in accordance with the terms and
#  conditions stipulated in the agreement/contract under which the
#  program(s) have been supplied.

from behave import use_step_matcher, given, when, then, step
from subprocess import Popen, PIPE
from environment import tool
from shutil import copyfile
from termcolor import colored
import os

use_step_matcher("parse")


def print_context(context):
    if context.error:
        print(colored(context.error, 'red'))


def run_tool(context, args_str):
    """Invoke the tool from the command line, passing the provided arguments."""
    os.chdir(context.scenario_dir)
    copyfile(f'{context.root_dir}/src/{tool}', f'./{tool}')
    command = ['python', f'./{tool}']
    args = args_str.split(' ') if args_str else []
    command = command + args
    with(Popen(command, stdout=PIPE, stderr=PIPE)) as p:
        out, err = p.communicate()
        context.returncode = p.returncode  # Will contain 0 if the command succeeds.
        context.output = out.decode('utf-8')
        context.error = err.decode('utf-8')


@given('a folder with files "{files_str}"')
def step_impl(context, files_str):
    files = (f.strip() for f in files_str.split(','))
    for file in files:
        copyfile(f'features/steps/data/{file}', f'{context.scenario_dir}/{file}')


@given('a folder with no dxp files')
def step_impl(context):
    # Do nothing, the folder is already empty.
    pass


@when('I run the tool with default options')
def step_impl(context):
    run_tool(context, None)


@when('I run the tool with arguments "{arguments}"')
def step_impl(context, arguments):
    run_tool(context, arguments)


@then('the tool should report the error "{text}"')
def step_impl(context, text):
    assert text in context.error, f'Error message not expected: "{context.error}".'


@then('it should create the folder "{folder}"')
def step_impl(context, folder):
    print_context(context)
    assert os.path.isdir(folder), f'It should have created the folder {folder}.'


@step('it should not create the folder "{folder}"')
def step_impl(context, folder):
    print_context(context)
    assert not os.path.isdir(folder), f'It should have not created the folder {folder}.'


@step('it should create the folder "{folder}" with the file "{file}" inside it')
def step_impl(context, folder, file):
    print_context(context)
    assert os.path.isfile(f'{folder}/{file}'), f'It should have created the file "{file}" inside "{folder}".'


@step("it should exit successfully")
def step_impl(context):
    expected_code = 0
    assert context.returncode == expected_code, \
        f'The tool should have returned {expected_code}, but have returned {context.returncode}'
