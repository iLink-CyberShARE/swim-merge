from flask import request
from flask_restplus import Resource
from ..util.dto import PostProcessDto
from ..service.merge_service import MergeService
from flask_jwt import jwt_required, current_identity

api = PostProcessDto.api
_fields = PostProcessDto.fields

@api.route('')
class PostProcess(Resource):
    @api.doc('Workflow result merge')
    @jwt_required()
    @api.response(200, 'The request was received succesfully')
    @api.response(500, 'Internal error occured')
    @api.response(401, 'Not Authorized')
    @api.expect(_fields, validate=True)
    def post(self):
        """Merge output results from specified workflow"""
        if(current_identity == None):
            return 'Not Authorized', 401
        data = request.json
        ms = MergeService(data, 1)
        return ms.merge_scenarios()