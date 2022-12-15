
import os
import json
from flask import json as flask_json
from app.main.config import config_by_name
from mongoengine import connect, disconnect_all
from ..model.composer_request import ComposerRequest
from ..model.flowmap import FlowMap
from ..model.run import Run
from ..model.public_scenario import PublicScenario
from ..model.src import SRC
from ..model.provenance import Provenance
from datetime import datetime
from flask import Response

class MergeService:

    def __init__(self, data=None, userid=None):
        """
        Service for workflow result merge.
        Receives flowid in data payload and extracted user id from auth token.
        """

        print('Found workflow identifier:')
        print(data['flowid'])

        self.data = data
        self.dbConnected = False
        self.userid = userid

        self.connect_db()


    def merge_scenarios(self):
        """
        Merges the results of workflow model executions according to reequest specification from user.
        Returns a SWIM resource container with user requested outputs and provenance trace.
        """

        try:
            if(not self.dbConnected):
                raise Exception("MongoDB not connected")

            # get the flow request by id
            flowrequest = ComposerRequest.objects(flowid=self.data['flowid']).only('outputs').first()

            # extract requested output composer ids
            cataloglist = []
            for catalogid in flowrequest.outputs:
                cataloglist.append(catalogid['id'])

            # get the flow mappings for those ids
            flowmappings = FlowMap.objects(catalogID__in=cataloglist)
            
            # get the list of model executions on this flow
            runs = Run.objects(flowid=self.data['flowid'])
            runlist = []
            for run in runs:
                runlist.append(run['runid'])
            print(runlist)

            # initialize SRC
            response = SRC(self.data['flowid'])

            # declare list of extracted model outputs
            modeloutputs = []

            # TODO: this code could be optimized with some mongo pipeline magic, check if worth it
            # for each model scenario search for outputs and extract 
            for userscenario in PublicScenario.objects(_id__in=runlist).exclude('modelInputs'):
                for flowmapping in flowmappings:
                    for output in userscenario.modelOutputs:
                        if(output.varName == flowmapping.swimID):
                            raw_output = output.to_json(use_db_field=False).lstrip("\"").rstrip("\"")
                            obj_output = json.loads(raw_output)
                            modeloutputs.append(obj_output)
                            prov = {
                                "id" : output.varName,
                                "entity" : "Model Output",
                                "wasGeneratedBy" : userscenario._id,
                                "generatedAtTime" : userscenario.endedAtTime
                            }
                            response.provenance.append(prov)

            # build metadata portion of the response
            response.metadata['status'] = 'success'
            response.metadata['type'] = 'Workflow Result'
            
            # build resource portion of the response with model outputs
            response.resource = modeloutputs

            # build provenance portion of the response
            # wfprov = Provenance(self.data['flowid'], "SWIM Workflow", "SWIM Model Broker", None )
            now = datetime.now()
            wfprov = {
                "id" : self.data['flowid'],
                "entity" : "SWIM Workflow",
                "wasGeneratedBy" : "SWIM Model Broker",
                "generatedAtTime" :  now.strftime("%d/%m/%Y %H:%M:%S")
            }
            response.provenance.append(wfprov)

            # TODO: save workflow result to database?

            # for debug only export to file
            # self.export_json(response, 'response.json')

            resp = Response(flask_json.dumps(response.__dict__),
                    mimetype='application/json')

            return resp

        except Exception as e:
            resp = {
                'status': 'fail',
                'message': str(e)
            }
            return resp, 500


    def export_json(self, src, path):
        """
        Export an assembled scenario specification to a JSON file to a target path.
        """
        print('Exporting to file...')      

        # convert spec to json string for file save
        json_spec = json.dumps(src.__dict__, ensure_ascii=False)

        # save scenario spec to file
        with open(path, 'w') as f:
            f.write(json_spec)

    def connect_db(self):
        """
        Retrieve database connection settings and open connections to swim and
        and workflow database instances.
        """
        print("Connecting mongo databases...")

        # get config setings
        environment = (os.getenv('BOILERPLATE_ENV') or 'dev')
        settings = config_by_name[environment]
        swimURL = settings.MODEL_DATABASE_URL
        workflowURL = settings.WORKFLOW_DATABASE_URL
        
        # connect to mongo database instances
        connect(host=swimURL, alias='swim-db-alias')
        connect(host=workflowURL, alias='workflow-db-alias')

        self.dbConnected = True

    def disconnect_db(self):
        """
        Disconnect all database instances.
        """
        print("Disconnecting mongo databases...")
        disconnect_all()
        self.dbConnected = False