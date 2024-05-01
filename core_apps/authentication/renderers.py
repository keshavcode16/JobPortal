import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If we receive a `token` key as part of the response, it will be a
        # byte object. Byte objects don't serialize well, so we need to
        # decode it before rendering the User object.
        refresh = data.get('refresh', None)
        access = data.get('access', None)
        errors = data.get('errors', None)

        if refresh is not None and access is not None:
            # Also as mentioned above, we will decode `token` if it is of type
            # bytes.
            data['refresh'] = refresh
            data['access'] = access

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            return super(UserJSONRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'message': data
        })
