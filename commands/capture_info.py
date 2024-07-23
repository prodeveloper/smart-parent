from data_types.uploaded import UploadedContent

class CaptureInfo:
    """
    Takes in different types of information and returns proposed dates
    """
    uploaded_content: UploadedContent
    prompt: str
    parsed_events: list[dict]
    executed: bool = False
    def __init__(self, uploaded_content):
        self.uploaded_content = uploaded_content
        self.prompt = self._get_prompt()

    def execute(self):
        self.executed = True
        pass

    def __getattr__(self, name):
        if not self.executed:
            raise RuntimeError("Command has not run. Try running the command first.")
        return self.__dict__.get(name)
    
    def _get_prompt(self):
        return """From the text below please extract the following information event and date. 
        Give response as JSON for example.
    [{
        'event': 'event name',
        'date': 'date'
    }]
    In case of multiple events, return a list of events and dates. eg
    [
        {'event': 'event name', 'date': 'date'},
        {'event': 'event name', 'date': 'date'}
    ]
    Please include nothing else in your response. If you can't find the information, return an empty list.
    """



