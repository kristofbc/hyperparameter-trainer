
class Evaluator(object):
    """
        The evaluator compare the objectives of a program and the results of one training
        from the Trainer
    """
    
    def compare(self, results, targets):
        """
            Compare the results against the target from a program

            Args:
                results (dict): a dictionnary matching the key name in the targets
                targets (Target[]): a list of target to compare
            Returns:
                (dict)
        """
        data = {}
        for target in targets:
            name = target.get_objective()
            if name in results:
                value = results[name]
                res = target.compare(value)
                data[name] = res

        return data

