from ..__init__ import *

class RetrieveSummary():
    def __init__(self, request):
        self.request = request
        try:
            self.model = summary.Summary(search=self.request.zip, debug=0)
        except:
            self.model = summary.Summary(search=self.request.location, debug=0)
        
    def get_summary(self):
        summarydict = {}
        for item in self.model.summary().values():
            summarydict[item.label] = (f'{item.value}{item.unit}' if item.unit != '°' else f'{item.value}{item.unit}C')
        return summarydict
        
    def get_summary_text(self):
        result = ''

        for item in self.get_summary().values():
            result += f"{item.label:20s}{item.value}{item.unit}\n"
            
        return result