from sanic import Sanic, Blueprint
from sanic.response import json
from functools import wraps

app = Sanic(__name__)

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = False

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator

bp1 = Blueprint('bp1', url_prefix='/bp1')
bp2 = Blueprint('bp2', url_prefix='/bp2')

@bp1.route('/')
@authorized()
async def bp1_route(request):
    return json({'bp1':'bp1'}, status = 200)

@bp2.route('/<param>')
async def bp2_route(request, param):
    return json({'bp2':'bp2'}, status = 200)

group = Blueprint.group(bp1, bp2)

# Register Blueprint group under the app
app.blueprint(group)

def init():
    app.run(
        host='localhost',
        port=4000,
        debug=False
    )