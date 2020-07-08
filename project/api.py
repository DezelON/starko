import json

def get_body(request):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode) if body_unicode != "" else {}