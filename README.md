# NetAn DXP Tool (dxp)

## Description

This project creates a tool for extracting the source files from the `dxp` file. The objective is to allow the source
code developed in Spotfire to be version controlled and have the proper code review process. 

The following code will be extracted to the default locations:
- `src/IronPython`: IronPython files
- `src/JavaScript`: JavaScript files

## Installing the Python libraries

This project has a `requirements.txt` with all the libraries needed for running this project. 
In order to install all the Python libraries, run:

```bash
 pip install -r requirements.txt
```

## Running the tests

This project contains automated tests using `behave`, a BDD tool. All the tests assets are organized as follows:

- `features/steps/data`: directory, contains files and data used by tests.
- `features/steps/*.py`: all the `behave` steps definitions.
- `features/environment.py`: contains code to prepare the tests execution.
- `features/*.feature`: files with `Gherkin` syntax for defining features and scenarios for testing.

In order to run the tests, execute from the root of the project:

```bash
behave
```

## Building the distributable 

The script `install.sh` will build and install the tool in the same location as the `git` executable file.

**IMPORTANT**: The script must be run with administrator privileges because it will copy the executable file to the 
same directory as the git binary is located.


In order to build and install the tool:
```bash
./install.sh
```

Verify the help section of the tool to see how to use it:
```bash
dxp -h
```
