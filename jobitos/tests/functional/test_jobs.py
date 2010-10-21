from jobitos.tests import *

class TestJobsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='jobs', action='index'))
        # Test response...
