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
1. Define a Curriculum:
```python
# Define a curriculum for the training
curriculum = Curriculum()
curriculum.add(Program({"n_units": 1000, "n_outs": 10, "batch_size": 64, "epoch": 1}, [Target.lte("loss", 0.19), Target.gte("accuracy", 0.941)]))
# ...
```
2. (Optional) Define a visualizer to get graphical results of the training:
```python
# Define figures to visualize the training
# VisualizerDefinition: x_axis = activites.key, y_axis = results.key
visualizer = Visualizer([
    VisualizerDefinition("batch_size", "loss", "Compare loss for hyperparameter: batch_size, iteration #1"),
    VisualizerDefinition("batch_size", "accuracy", "Compare accuracy for hyperparameter: accuracy, iteration #1")
])
```
3. Create the Trainer instance used to train the network:
```python
# Defines the trainer
trainer = Trainer(curriculum, visualizer)
```
4. Create the training callback that will be called at every Program (iteration):
```python
# Defines the trainer callback
# Called at each training iteration and should call the network with the parameters defined in the activity
def trainer_callback(activities):
    sum_loss, sum_accuracy = network(activities["n_units"], activities["n_outs"], activities["batch_size"], activities["epoch"])

    # Values that will be used in trainer and will be compared to the Targets
    return {"loss": sum_loss, "accuracy": sum_accuracy}
```
5. Call the training operation of the Trainer instance:
```python
trainer.train("./example/output", trainer_callback)
```
6. For this example the output patch specified above `./example/output` contain 2 files
* Example of a generated CSV:
|                                                                                                                                                                                                         | 
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| id,time_start,time_stop,time_diff,n_units_activity,epoch_activity,n_outs_activity,batch_size_activity,loss_objective,accuracy_objective,loss_result,accuracy_result,loss_evaluation,accuracy_evaluation | 
| 0,1499911851.068811,1499911873.701255,22.632444143295288,1000,1,10,64,0.19,0.941,0.18154194204012553,0.9457333333333333,True,True                                                                       | 
| 1,1499911874.298902,1499911890.028886,15.729984045028687,1000,1,10,100,0.19,0.941,0.19183134109402697,0.9421833368142446,False,True                                                                     | 
| 2,1499911890.24943,1499911904.711509,14.462079048156738,1000,1,10,128,0.19,0.941,0.19775271045764287,0.9411333333333334,False,True                                                                      | 
* Example of generated figures:
![figure](/example/output/20170713-111051.png)
