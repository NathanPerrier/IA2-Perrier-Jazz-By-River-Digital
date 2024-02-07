from ..__init__ import *

class RetrieveWarnings():
    def __init__(self, request):
        self.request = request
        self.warnings = self.request.warning()
       
    def get_warnings(self):
        return self.request.api('warnings')   
        
    def get_warning_title(self):
        for warning in self.warnings:
            return warning['title']
    
    def get_warning_description(self):
        for warning in self.warnings:
            return warning['short_title']
    
    def get_warning_id(self):
        for warning in self.warnings:
            return warning['id']