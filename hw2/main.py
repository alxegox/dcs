from aiohttp import web
import redis
import json
from settings import config
from aiohttp_validate import validate

REDIS_SET_NAME = 'inc'


r = redis.Redis(host=config.db_host, port=config.db_port, db=0)

routes = web.RouteTableDef()

class Storage:

    pass

with open('jsonschema/increment/request.json') as json_file:
    increment_validatior = json.load(json_file)

@validate(increment_validatior)
@routes.post('/increment')
async def handle(request: web.Request):
    number = await request.text()
    number_json = json.loads(number)
    parsed_number = number_json['number']

    if r.sismember(REDIS_SET_NAME, number):
        return web.Response(body='number already exists', status=400)

    inc = f'{parsed_number + 1}'
    if r.sismember(REDIS_SET_NAME, inc):
        return web.Response(body='inc number already exists', status=400)

    r.sadd(REDIS_SET_NAME, parsed_number)

    return web.Response(body=inc)

def main():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=config.app_host, port=config.app_port)

if __name__ == '__main__':
    main()