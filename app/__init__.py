from flask_restplus import Api
from flask import Blueprint, url_for

from .main.controller.sample_controller import api as sample_ns
from .main.controller.postprocess_controller import api as postprocess_ns


blueprint = Blueprint('SWIM Merge', __name__, url_prefix='/swim-merge')

class CustomAPI(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)
        This fix will force a relatve url to the specs.json instead of absolute
        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)

authorizations = {
    'Bearer Auth' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization',
        'description': 'Type in the value input box below: Bearer &lt;JWT&gt; where JWT is the token'
    }
}

api = CustomAPI(blueprint,
          title= "SWIM Merge",
          version='1.0',
          description='Postprocessing unit of SWIM workflows for final result',
          doc='/docs/',
          security='Bearer Auth',
          authorizations = authorizations
          )

#api.add_namespace(sample_ns, path='/sample')
api.add_namespace(postprocess_ns, path='/postprocess')


