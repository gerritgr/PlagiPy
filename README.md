# MC-Epidemic
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gerritgr/DeepPlagueis.svg?token=qQ7vTmAySdBppYxywojC&branch=master)](https://travis-ci.com/gerritgr/DeepPlagueis)


## Overview
Implementation of Monte-Carlo (Gillespie) simulation for epidemic type processes on complex networks - written in Python and Rust. 
Python is used for IO/visualization/random graph generation, the simulation happens in Rust.
Each simulation is carried out by an independent Rust-thread started from `main.py`.
## Installation
If Python 3.6 and pip are installed, use
```sh
pip install -r requirements.txt
```
to download Python-dependencies.
The Rust code is precompiled in the repository; if desired, Rust can be installed with
```sh
sudo curl -sf -L https://static.rust-lang.org/rustup.sh | sh
```
and the Rust code (in the rust_ssa folder) can be build with
```sh
cd rust_ssa && cargo build --release
```
## Usage
**MC-Epidemic** can be used like this
```sh
python main.py model/SIR.yml
```
**main.py** accepts the following arguments:
```sh
positional arguments:
  model                 path to modelfile

optional arguments:
  -h, --help            show this help message and exit
  -runs [RUNS]          number of simulation runs, default is 10
  -threads [THREADS]    number of threads, default is number of cpu cores
  -plot_ind_simulations
                        plot evolution of fractions for each single simulation
                        run in separate file
```
The modelfile contains the specification of the contact process, for instance:
```sh
rule:  
  - S+I->I+I: 5.0
  - I -> R: 0.5
  - R -> S: 1.0  
horizon: 3
initial_distribution:
  S: 0.95         #automatic normalization
  I: 0.025
  R: 0.025
network:    
  kmin: 1       #optional, default is 0
  kmax: 200
  # sample degrees from this distribution (ultimate degree distribution of the network might slightly differ)
  degree_distribution: k**(-2.5)  #automatic truncation and normalization
  random_model: configuration # default in configuration, no other models supported so far
  nodes: 20000    #optional, default is 10000
```
One can also provide a fixed network
```sh
...
network: 
  file: graphfile_example.txt
```
containing a labeled graph, each line having the form `<Nodeid>;<Label>;<Neighbor1>,<Neighbor2>,...`

## Performance
Each simulation step consists of the following:
* Find a random edge: constant in number of nodes, k_max; quadradic in number of states
* Change the state of exactly one node belonging to this edge: constant in number of nodes, k_max, number of states
* Change the rate of all neighboring edges: constant in number of nodes and states (on average); linear in k_max

If we assume k_max >> number of stats, we can assue that each step is in O(k_max).
Note that typically k_max depends on the number of nodes. Furthermore, the more nodes there are, the more steps are necessary to reach a given time horizon.

The runtime of a full simulation (including graph generation and IO) of the above SIR model w.r.t. different number of nodes are reported below.

![Performance](https://i.imgur.com/pGBqkEC.jpg)

Performed on a MacBook Pro (late 2017).


## Output
**MC-Epidemic** stores the output in the output/<modelname>/ directory, including
* the generated random graph for each simulation: `graphfile_<threadid>_<randomint>.txt`
* the results file identifiying the number of nodes in each state after each reaction: `resultfile_<thradid>_<randomint>.txt`
and a seaborn visualization of this, containing 99% confidance intervals as .pdf file and one containing individual traces
* snapshots of the network at different times (TBD):  `graphsnapshot_<threadid>_<randomint>_<time>.txt** and **graphsnapshot_<threadid>_<randomint>_<time>.pdf`
* a file containing the actual degree distribution (TBD): `degreedistribution_<threadid>_<randomint>.txt`

![Example](https://i.imgur.com/guv0GJo.jpg)
Example output (traces of 10 simulation runs) for the above model with 3000 nodes.