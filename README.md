# PlagiPy
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gerritgr/PlagiPy.svg?branch=master)](https://travis-ci.com/gerritgr/PlagiPy)


![Screenshot](https://raw.githubusercontent.com/gerritgr/PlagiPy/master/example.png)

## Overview
Implementation of a super simple plagiarism checker in Python.
A CherryPy-based webinterface makes it easy to see which parts of a text have likely been copied. 
The score counts the number of copied words.

## Installation
If Python 3.6 and pip are installed, use
```sh
pip install -r requirements.txt
```
to download Python-dependencies.

## Usage
Via the webinterface with (the url is <http://127.0.0.1:8080>)
```sh
python start_interface.py
```
or via the command line
```sh
python compare_texts examples/text1.txt examples/text2.txt
```
