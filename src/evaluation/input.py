
# TODO: could be merged into the evaluation script or actions
class Input:
    def __init__(self, url, input_name, input_type, task_name):
        self.url = url
        self.name = input_name
        self.task = task_name
        self.type = input_type

    def __repr__(self):
        """
        To make sure the objects are printable
        """
        return f"Input(name={self.name}, type={self.type}, task={self.task})"
