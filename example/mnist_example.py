from trainer.trainer import Trainer

import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
from chainer.dataset import convert

from trainer.curriculum import Curriculum
from trainer.visualizer import Visualizer
from trainer.visualizer import VisualizerDefinition
from trainer.program import Program
from trainer.target import Target

def network(n_units, n_out, batch_size, epochs):
    """
        One can think of a network with multiple hyper-parameter...
        This should be in its own file: not specific for chainer-trainer
    """
    # Network definition
    class MLP(chainer.Chain):

	def __init__(self, n_units, n_out):
	    super(MLP, self).__init__(
                l1 = L.Linear(None, n_units),
                l2 = L.Linear(None, n_units),
                l3 = L.Linear(None, n_out)
            )

	def __call__(self, x):
	    h1 = F.relu(self.l1(x))
	    h2 = F.relu(self.l2(h1))
	    return self.l3(h2)

    # Instantiate the model
    model = L.Classifier(MLP(n_units, n_out))

    # Setup an optimizer
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)

    # Load the MNIST dataset
    train, test = chainer.datasets.get_mnist()
    train_count = len(train)
    test_count = len(test)

    train_iter = chainer.iterators.SerialIterator(train, batch_size)
    test_iter = chainer.iterators.SerialIterator(test, batch_size, repeat=False, shuffle=False)

    # Really basic training loop
    sum_accuracy = 0
    sum_loss = 0
    global_accuracy = 0
    global_loss = 0
    while train_iter.epoch < epochs:
        batch = train_iter.next()
        x_array, t_array = convert.concat_examples(batch, -1)
        x = chainer.Variable(x_array)
        t = chainer.Variable(t_array)

        optimizer.update(model, x, t)
        sum_loss += float(model.loss.data) * len(t.data)
        sum_accuracy += float(model.accuracy.data) * len(t.data)

	if train_iter.is_new_epoch:
            global_loss = sum_loss / train_count
            global_accuracy = sum_accuracy / train_count
	    print('epoch: ', train_iter.epoch)
            print('train mean loss: {}, accuracy: {}'.format(global_loss, global_accuracy))

	    sum_accuracy = 0
            sum_loss = 0
            for batch in test_iter:
                x_array, t_array = convert.concat_examples(batch, -1)
                x = chainer.Variable(x_array)
                t = chainer.Variable(t_array)
                loss = model(x, t)
               	sum_loss += float(loss.data) * len(t.data)
                sum_accuracy += float(model.accuracy.data) * len(t.data)

            test_iter.reset()
            print('test mean loss: {}, accuracy: {}'.format(sum_loss / test_count, sum_accuracy / test_count))
            sum_loss = 0
            sum_accuracy = 0

    # Return results
    return global_loss, global_accuracy

def main():
    # Define a curriculum for the training
    curriculum = Curriculum()
    curriculum.add(Program({"n_units": 1000, "n_outs": 10, "batch_size": 64, "epoch": 1}, [Target.lte("loss", 0.19), Target.gte("accuracy", 0.941)]))
    curriculum.add(Program({"n_units": 1000, "n_outs": 10, "batch_size": 100, "epoch": 1}, [Target.lte("loss", 0.19), Target.gte("accuracy", 0.941)]))
    curriculum.add(Program({"n_units": 1000, "n_outs": 10, "batch_size": 128, "epoch": 1}, [Target.lte("loss", 0.19), Target.gte("accuracy", 0.941)]))

    # Define figures to visualize the training
    # VisualizerDefinition: x_axis = activites.key, y_axis = results.key
    visualizer = Visualizer([
        VisualizerDefinition("batch_size", "loss", "Compare loss for hyperparameter: batch_size, iteration #1"),
        VisualizerDefinition("batch_size", "accuracy", "Compare accuracy for hyperparameter: accuracy, iteration #1")
    ])

    # Defines the trainer
    trainer = Trainer(curriculum, visualizer)

    # Defines the trainer callback
    # Called at each training iteration and should call the network with the parameters defined in the activity
    def trainer_callback(activities):
        sum_loss, sum_accuracy = network(activities["n_units"], activities["n_outs"], activities["batch_size"], activities["epoch"])

        # Values that will be used in trainer and will be compared to the Targets
        return {"loss": sum_loss, "accuracy": sum_accuracy}

    trainer.train("./example/output", trainer_callback)


if __name__ == '__main__':
    main()
