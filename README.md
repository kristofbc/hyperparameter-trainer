# Chainer training wrapper
Easily tune hyperparameters and compare the performance of a network.

This package provide the ability to run multiple training of the same Network with different parameters and compare the performances.
By changing the hyperparameters (called "activities") and defining targets (called "objective"), the Trainer will compare each iterations and provide the best combination of parameters.

## Philosophy
Think of chainer-trainer like a gym curriculum:
* Trainer: what will train the neural network
* Curriculum: what the Trainer used to guide the training
* Program: multiple program constitute a Curriculum and are the iteration to execute by the Trainer
* "activities": are what defines a Program
* "objectives": are the target of a Program. They're defined by Target: {objective} {operator} {result}. i.e: loss < 0.2

## Examples
A simple MNIST network example is provided in `example/mnist_example.py` and can be run by:
```bash
$ python example.py
```
