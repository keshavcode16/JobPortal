import json

from rest_framework.renderers import JSONRenderer


class ProductJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the products in a structured manner for the end user.
        """
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'product': data
                })
            return json.dumps({
                'products': data
            })
        return json.dumps({
            'product': 'No product found.'
        })


class RatingJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the ratings in a structured manner for the end user.
        """
        return json.dumps({
            'rate': data,
        })


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the products in a structured manner for the end user.
        """
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'post': data
                })
            return json.dumps({
                'products': data
            })
        return json.dumps({
            'comment': 'No post found.'
        })


class FavoriteJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    """
        Render the favorited products in a structured manner for the user.
    """

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'products': data
        })


class NotificationJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the products in a structured manner for the end user.
        """
        if data is not None:
            return json.dumps({
                'notifications': data
            })
        return json.dumps({
            'notifications': 'No notifications found.'
        })


class CommentEditHistoryJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    """
        Render the comment edit history in a structured manner for the user.
    """

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'comment_history': data
        })


class CommentLikeJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    """
        Render the favorited products in a structured manner for the user.
    """

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({
            'comment': data
        })


class BookmarkJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the ratings in a structured manner for the end user.
        """
        return json.dumps({
            'bookmark': data,
        })
