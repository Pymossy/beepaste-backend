import datetime
import json
from sanic import response
from mongoengine.errors import ValidationError, FieldDoesNotExist
from beepaste.modules.v1.models.paste import PasteModel as Paste  # TODO fix
from sanic.views import HTTPMethodView


class PasteView(HTTPMethodView):

    async def get(self, request, **kwargs):
        ''' fetching paste by pasteid from database '''
        userid = request['userid']
        if userid is None:
            return response.json(
                {'status': 'fail', 'details': 'user is not authenticated'},
                status=401)
        else:
            try:
                paste_id = kwargs.get('pasteid')
                paste = await Paste.objects(uri=paste_id).first()
                if paste.expiryDate < datetime.datetime.now():
                    return response.json(
                        {'status': 'success', 'paste': paste},
                        status=200)
                else:
                    paste.delete()
                    return response.json(
                        {'status': 'fail', 'details': "This paste has been expired"},
                        status=410)
                    # TOOD: Delete this from database
            except:
                return response.json({'status': 'fail', 'details': "Paste Not found"}, status=404)

    async def post(self, request):
        ''' saves a sent JSON object into database and returns a link to it '''
        input_json = request.json
        # TODO validation with some lib like marshmallow
        # https://github.com/marshmallow-code/marshmallow
        # not use try catch if validate faild return error from marshmallow
        # else pass to the model
        try:
            # TODO: set ownerID using the token used to authorize api!
            new_paste = Paste(**input_json)
            new_paste.views = 0
            await new_paste.generate_url()
            new_paste.validate()
            new_paste.save()
            new_paste_obj = json.loads(new_paste.to_json())
            ret_data = {
                'status': 'success',
                'paste': new_paste_obj
            }
            return response.json(
                {'status': 'success', 'paste': new_paste_obj},
                status=201)
        except ValidationError as e:
            return response.json(
                {'status': 'fail', 'details': 'invalid data',
                    'errors': e.to_dict()},
                status=400)
        except FieldDoesNotExist as e:
            return response.json(
                {'status': 'fail', 'details': 'invalid data'},
                status=400)

        # TODO: handle other exceptions!

    async def put(self, request):
        return response.json(
            {'status': 'fail', 'details': 'Method Not Allowed'},
            status=405)

    async def patch(self, request):
        return response.json(
            {'status': 'fail', 'details': 'Method Not Allowed'},
            status=405)

    async def delete(self, request):
        return response.json(
            {'status': 'fail', 'details': 'Method Not Allowed'},
            status=405)