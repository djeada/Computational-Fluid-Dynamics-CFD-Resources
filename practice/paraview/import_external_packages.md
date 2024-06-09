# How to Import External Python Packages in ParaView Console

## Introduction

ParaView comes with its own Python interpreter, allowing easy access to ParaView's Python package. However, using external Python packages (e.g., `pandas`, `matplotlib`) within `PvPython` can be challenging. This guide explains how to overcome this issue by leveraging Python virtual environments.

## Steps to Import External Packages

### 1. Install `virtualenv`

First, you need to install `virtualenv` to manage your virtual environments.

```sh
$ python -m pip install --user virtualenv
```

2. Create a Virtual Environment

Create a virtual environment in the directory of your choice (e.g., venv).

sh

$ python -m virtualenv venv

3. Activate the Virtual Environment

Activate the virtual environment and install the required packages inside it.

    Linux/macOS:

```sh
$ source ./venv/bin/activate
```

Windows:

```sh
> .\venv\Scripts\activate
```

4. Install Required Packages

While the virtual environment is activated, install the packages you need (e.g., pandas).

sh

(venv) $ pip install pandas

5. Deactivate the Virtual Environment

After installing the required packages, deactivate the virtual environment.

```sh
(venv) $ deactivate
```

6. Modify the Script to Activate the Environment

Modify your script to activate the virtual environment during execution. This can be done by adding the following code at the beginning of your script:

```python
import sys
if '--virtual-env' in sys.argv:
  virtualEnvPath = sys.argv[sys.argv.index('--virtual-env') + 1]
  # Linux/macOS
  virtualEnv = virtualEnvPath + '/bin/activate_this.py'
  # Windows
  # virtualEnv = virtualEnvPath + '/Scripts/activate_this.py'
  if sys.version_info.major < 3:
    execfile(virtualEnv, dict(__file__=virtualEnv))
  else:
    exec(open(virtualEnv).read(), {'__file__': virtualEnv})

# The main script starts from here
import pandas as pd
from paraview.simple import *
```

7. Execute the Script with PvPython

Run your script using PvPython and specify the path to the virtual environment.

```sh
$ pvpython my_script.py --virtual-env venv
```

Example Script

Assuming the script is named my_script.py and the virtual environment is located in a directory called venv, your script might look like this:

```python
import sys
if '--virtual-env' in sys.argv:
  virtualEnvPath = sys.argv[sys.argv.index('--virtual-env') + 1]
  # Linux/macOS
  virtualEnv = virtualEnvPath + '/bin/activate_this.py'
  # Windows
  # virtualEnv = virtualEnvPath + '/Scripts/activate_this.py'
  if sys.version_info.major < 3:
    execfile(virtualEnv, dict(__file__=virtualEnv))
  else:
    exec(open(virtualEnv).read(), {'__file__': virtualEnv})

# The main script starts from here
import pandas as pd
from paraview.simple import *

# Your ParaView automation code goes here
```
