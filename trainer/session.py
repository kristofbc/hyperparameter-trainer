import time

class Session(object):
    _sessions = {}

    @staticmethod
    def attach(session_name="default"):
        """
            Attach to an existing running Session

            Args:
                session_name (str): name of the session to attach
            Returns:
                (Session)
        """
        if Session.exists(session_name):
            return Session(session_name)

        return None

    @staticmethod
    def exists(session_name):
        """
            Check if a Session exists

            Args:
                session_name (str): name of the session to check
            Returns:
                (bool)
        """
        return session_name in Session._sessions
        

    def __init__(self, session_name="default"):
        """
            The session is started by a Trainer.
            Controls the state of the Curriculum.
            Unlike a basic training where a whole Program should be completed,
            the session gives the possibility to interupt a Program, rewind or forward a Curriculum from anywhere

            Properties are stored in a static dict because they can be retrieved later in an other scripts
            
            Args:
                session_name (str): name of the new session
        """
        if not Session.exists(session_name):
            Session._sessions[session_name] = {
                "name": session_name,
                "started": False,
                "paused": False,
                "ended": False,
                "training_callback": None,
                "results_callback": None,
                "start_time": 0,
                "stop_time": 0,
                "pause_time": 0,
                "index": 0,
                "curriculum": None
            }

        self._name = session_name

    def get(self, name):
        """
            Attribute name to retrieve

            Attr:
                name (str): name of the attribute to get
            Returns:
                (mixed)
        """
        if name not in Session._sessions[self._name]:
            raise AttributeError("Property does not exists for {}".format(name))

        return Session._sessions[self._name][name]

    def set(self, name, value):
        """
            Attribute to store

            Attr:
                name (str): name of the attribute to store
                value (mixed): value of the attribute to store
        """
        Session._sessions[self._name][name] = value
    
    def start(self, curriculum, training_callback, results_callback):
        """
            Start the training Session
            
            Args:
                curriculum (Curriculum): the curriculum containing the Program
                training_callback (function(activities):dict): called for each iteration
                results_callback (function(results, program, time_start, time_stop)): When data is yield by the network
        """
        if self.get("started"):
            raise RuntimeError("Unable to start a Session that is already started")

        self.set("started", True)
        self.set("curriculum", curriculum)
        self.set("training_callback", training_callback)
        self.set("results_callback", results_callback)

        while self.get("curriculum").has_next() and not self.get("ended"):
            self.current()
            self.next()


    def next(self):
        """
            Forward to the next Program
        """
        if self.get("curriculum").has_next():
            self.get("curriculum").next()
            self.set("index", self.get("index")+1)
        else:
            self.set("ended", True)

    def previous(self):
        """
            Backward on the previous Program
        """
        if self.get("curriculum").has_previous():
            self.get("curriculum").previous()
            self.set("index", self.get("index")-1)
            self.set("ended", False)

    def current(self):
        """
            Execute the current program
        """
        if self.get("paused"):
            return

        program = self.get("curriculum").current()
        activities = program.get_activities()
        objectives = program.get_objectives()

        print("Training curriculum #{}".format(self.get("index")+1))
        print(activities)
        self.set("start_time", time.time())
        results = self.get("training_callback")(activities)
        self.set("stop_time", time.time())
        self.get("results_callback")(results, program, self.get("start_time"), self.get("stop_time")-self.get("pause_time"))

    def pause(self):
        """
            Pause the current Curriculum
        """
        if not self.get("paused"):
            self.set("paused", True)
            self.set("pause_time", time.time())

    def resume(self):
        """
            Resume the current Curriculum
        """
        if self.get("paused"):
            self.set("paused", False)
            self.set("pause_time", time.time()-self.get("pause_time"))

    def results(self, results):
        """ 
            Produce results for the current Program in the curriculum

            Args:
                results (dict): results to evaluate
        """
        self.get("results_callback")(results, self.get("curriculum").current(), self.get("start_time"), time.time()-self.get("pause_time"))
        

