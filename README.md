# Bhoppy
A Bunny Hopper for **Counter-Strike: Global Offensive**. <br>
Working as of [07.11.2020](https://blog.counter-strike.net/index.php/2020/10/31827/). <br>
See changelogs for patch notes.

## Installation
Bhoppy uses three different python modules to complete its task. <br>
These can easily be installed using **pip**. <br>

### Pip
To make sure you have pip installed, do the following: <br> 
* Open command prompt
* Run `pip -V`
* The result should look something like this: `pip 20.2.4 from c:\users\INSERT_PATH`

If you **do not have** pip, 
the latest version can be found [here](https://pypi.org/project/pip/#files) <br>
If you do have pip, but need to **update**, simply run `py -m pip install -U pip`

### Modules
If you already have pip installed, open command prompt and do the following: <br>

`pip install keyboard` <br>
`pip install pymem` <br>
`pip install pywin32` <br>

Note: Pywin32 is a packet module containing win32gui (among others). <br>
This is updated more frequently and should be preferred.

## Run
Running bhoppy is **easy**. <br>
Open command prompt and `cd` to `bhoppy/src`. <br>
Then simply do: `py bhoppy.py`.
