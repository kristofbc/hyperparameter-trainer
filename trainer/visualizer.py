import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

class Visualizer(object):
    """
        Visualize the impact of a Curriculum

        Args:
            definitions (VisualizerDefinition[]): contain the definitions for each graphs to output
    """
    def __init__(self, definitions):
        print("init")
        self._definitions = definitions
        self._results = []

    def add_results(self, activities, objectives, results, evaluations):
        """
            Visualize the impact of each activities considering the objectives, results and evaluations for each Program

            Args:
                activities (dict): a dictionary of parameters and value to use during training
                objectives (Target[]): the targets of the programs
                results (dict): the results of the training
                evaluations (dict): the evaluations of the results against the objective
        """
        self._results.append([activities, objectives, results, evaluations])

    def visualize(self):
        """
            Create the visualization graphs from the results

            Returns:
                (pyplot)
        """
        # For all the definitions, generate the corresponding plot
        gs = gridspec.GridSpec(len(self._definitions), len(self._definitions))
        for i in xrange(len(self._definitions)):
            definition = self._definitions[i]
            title = definition.get_title()
            axis_x_key = definition.get_axis_x()
            axis_y_key = definition.get_axis_y()
            
            # Loop through all the results obtained from a Program
            min_x, max_x, min_y, max_y = 0, 0, 0, 0
            data_x, data_y, prog_eval, index_annotation = [], [], [], 0
            for j in xrange(len(self._results)):
                activities, objectives, results, evaluations = self._results[j]

                if axis_x_key not in activities:
                    raise ValueError("Unable to construct the figure: the axis_x_key is not in the activities list")
                data_x.append(activities[axis_x_key])

                if axis_y_key not in results:
                    raise ValueError("Unable to construct the figure: the axis_y_key is not in the results list")
                data_y.append(results[axis_y_key])
                
                index_annotation += 1
                prog_eval.append("blue" if evaluations[axis_y_key] is True else "red")

            # Build the figure
            plt.figure(1)
            # If there's a creation callback, let the user code handle that
            creation_callback = definition.get_creation_callback()
            if creation_callback is not None:
                creation_callback(plt, definition)
            else:
                plt.subplot("{0}{1}{2}".format(len(self._definitions), 1, i+1))
                plt.scatter(data_x, data_y, color=prog_eval)
                # Add the index on the plot
                for j in xrange(index_annotation):
                    plt.annotate(j, (data_x[j], data_y[j]))
                plt.xlabel(axis_x_key)
                plt.ylabel(axis_y_key)
                plt.title(title, y=1.08)

        plt.tight_layout()
        return plt


class VisualizerDefinition(object):

    def __init__(self, axis_x, axis_y, title, creation_callback=None):
        self._axis_x = axis_x
        self._axis_y = axis_y
        self._title = title
        self._creation_callback = creation_callback

    def get_axis_x(self):
        return self._axis_x
    
    def get_axis_y(self):
        return self._axis_y

    def get_title(self):
        return self._title

    def get_creation_callback(self):
        return self._creation_callback


