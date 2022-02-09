# instrument_control
python control of santec, new focus, yokogawa, optilab for optical measurements

enter into terminal:
'conda env create --file research01.yml'

this is to create an environment that will allow you to work with the python_control programs

use:
'conda activate research'
to activate the "research" environment that is the default name for the environment created by research01.yml

if you are using a new computer, you could try:
'conda env create --file research.yml'

this will try to install all new dependencies, but may not work and you might have to remove the environment
and redo the process by:
'conda remove --name research --all'


# to run the program:

1. open anaconda prompt (mini) as an admin, you can search it from start menu.
2. enter 'conda activate research' into the terminal, this will activate an environment
2a. navigate to the correct folder.  If you need to change from C: to something like X:, 
	just type and enter "X:", then navigate to correct directory by typing in "cd XXXXXXXXXX",
	XXXXXXXXXX is the location of the file.
3. enter the name of the file.  E.g. 'python tlb6700_1um_main.py' to run
