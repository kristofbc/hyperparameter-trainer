
class Target(object):
    @staticmethod
    def lt(objective, value):
        """
            Implementation of lower-than <
            
            Args:
                objective (str): name of the objective
                value (str): the target value
        """
        return Target(objective, "<", value)
    
    @staticmethod
    def lte(objective, value):
        """
            Implementation of lower-than-equal <=
            
            Args:
                objective (str): name of the objective
                value (str): the target value
        """
        return Target(objective, "<=", value)

    @staticmethod
    def eq(objective, value):
        """
            Implementation of equal =
            
            Args:
                objective (str): name of the objective
                value (str): the target value
        """
        return Target(objective, "=", value)

    @staticmethod
    def gt(objective, value):
        """
            Implementation of greater-than >
            
            Args:
                objective (str): name of the objective
                value (str): the target value
        """
        return Target(objective, ">", value)

    @staticmethod
    def gte(objective, value):
        """
            Implementation of greater-than-equal >=
            
            Args:
                objective (str): name of the objective
                value (str): the target value
        """
        return Target(objective, ">=", value)
    
    @staticmethod
    def ne(objective, value):
        """
            Implementation of not-equal !=
            
            Args:
                objective (str): name of the objective
                value (str): the target value
        """
        return Target(objective, "!=", value)

    def __init__(self, objective, operator, value):
        """
            A target is an objective, operator, value container
        
            Args:
                objective (str): name of the objective
                operator (str): comparison operator between the objective and value
                value (str|int): the target value
        """
        self._objective = objective
        self._operator = operator
        self._value = value

    def compare(self, value):
        """
            Compare the value to this Target

            Args:
                value (str|int): the value to compare
            Returns:
                (boolean)
        """
        if self._operator == ">":
            return value > self._value
        elif self._operator == ">=":
            return value >= self._value
        elif self._operator == "=":
            return value == self._value
        elif self._operator == "<":
            return value < self._value
        elif self._operator == "<=":
            return value <= self._value
        elif self._operator == "!=":
            return value != self._value
        
        raise ValueError("Operator not found for {}".format(self._operator))

    def get_objective(self):
        return self._objective

    def get_operator(self):
        return self._operator

    def get_value(self):
        return self._value


