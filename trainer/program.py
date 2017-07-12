
class Program(object):

    def __init__(self, activities, objectives):
        """
            A single program containing the activities and objectives for a training session

            Args:
                activities (dict): a dictionary of parameters and value to use during training
                objectives (Target[]): the results to compare against
        """
        self._activities = activities
        self._objectives = objectives

    def get_activities(self):
        return self._activities
    
    def get_objectives(self):
        return self._objectives
