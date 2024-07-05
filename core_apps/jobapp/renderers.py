import json

from rest_framework.renderers import JSONRenderer


class JobPostJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the jobs in a structured manner for the end user.
        """
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'job': data
                })
            return json.dumps({
                'jobs': data
            })
        return json.dumps({
            'job': 'No job found.'
        })

