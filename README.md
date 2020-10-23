# Slicer Tutorial

This repository features a basic implementation of a slicer used in 3D printing to produce the print lines of the 3D printer to follow.

![](figs/beam_stl.png)

![](figs/final.png)

# Running the code

Use `python3 -m venv .venv` to create the virtual environment for the project.

https://docs.python.org/3/tutorial/venv.html

VSCode will default to the virtual env when you open the folder. Epic!



If you want to open and run on the command line then `cd` into the directory and run

```
source .venv/bin/activate
```

which will activate the virtual environment.


To install the packages for the slicer to run, use

```
pip install -r requirements.txt
```

To run the example, enter:

```
python src/main.py
```

# Contributing

Black-with-tabs is included as a tool to maintain a consistent code format. Please run it before you commit any code to clean up any additions you make. It's great and save you a lot of time in not having to think about the formatting.

Simply run.

```
black src/
```