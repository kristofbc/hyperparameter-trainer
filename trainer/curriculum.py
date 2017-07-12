from program import Program

class Curriculum(object):
    """
        The Curriculum is the intended results for the network.
        Contain different hyperparameters and their expected results

        Args:
            
    """
    def __init__(self):
        self._programs = []
        self._cursor = 0

    """
        Add a new set of "activities" (parameters) and their objectives (targets)

        Args:
            program (Program): the program to add to this curriculum
    """
    def add(self, program):
        self._programs.append(program)

    """
        Update the currentn program

        Args:
            program (Program): the program to replace the current one
    """
    def update(self, program):
        self._programs[self._cursor] = program

    """
        Iterate to the next program

        Returns:
            (Program)
    """
    def next(self):
        self._cursor += 1

    """
        Check if there's other programs

        Returns:
            (boolean)
    """
    def has_next(self):
        return self._cursor < len(self._programs)

    """
        Get the current program

        Returns:
            (Program)
    """
    def current(self):
        return self._programs[self._cursor]
    
    """
        Return to previous position

        Returns:
            (Program)
    """
    def previous(self):
        self._cursor += -1

    """
        Check if there's previous program

        Returns:
            (boolean)
    """
    def has_previous(self):
        return self._cursor > 0 

    """
        Rewind the cursor to the beginning of the programs
    """
    def rewind(self):
        self._cursor = 0


