from flask_restplus import Namespace, fields


class SampleDto:
    api = Namespace('/sample', description='Sample API')


class PostProcessDto:
    api = Namespace('/postprocess', description='Postprocessing endpoints')
    fields = api.model('workflow', {
        'flowid': fields.String(required=True, description='swim workflow unique identifier', example='bb350d6e-0464-4b18-a3e2-ea70f8b5030b')
    })
