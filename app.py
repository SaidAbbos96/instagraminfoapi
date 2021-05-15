from flask import Flask, request, render_template, json
from insta_get import get_data

app = Flask(__name__)


def add_info(result_sourse):
    data = {
        'API_info': {
            "api_version": "v1.0",
            "name": "infomir.uz Instagram info and download media API",
            "infoEN": "This API is provided by infomir.uz",
            "infoRU": "Этот API предоставляется от компании infomir.uz",
            "infoUZ": "Ushbu API infomir.uz tomonidan taqdim etilgan.",
            "author": {
                'name': "SaidAbbos Khudoykulov",
                'contact': "abbos.xudoyqulov@gmail.com"
            }
        }
    }
    data["result"] = result_sourse
    return data


def parse(url):
    if "/p/" in url:
        post_id = url.split(r"/p/")[1].split(r"/")[0]
        final_url = r"https://www.instagram.com/p/" + post_id + "/?__a=1"
        result = json.loads(get_data(final_url))['graphql']['shortcode_media']
    elif "/p/" not in url:
        user_id = url.split(r"https://www.instagram.com/")[1].split(r"/")[0]
        final_url = r"https://www.instagram.com/" + user_id + "/?__a=1"
        result = json.loads(get_data(final_url))

    return json.dumps(add_info(result), sort_keys=False, indent=4)


@app.route("/")
def index():
    source = get_data("https://www.instagram.com/p/B15veOxhiH9/?__a=1")
    myjson = json.loads(source)['graphql']['shortcode_media']
    res = json.dumps(add_info(myjson), sort_keys=True, indent=4)
    return render_template("index.html", data=res)


@app.route("/info", methods=['GET'])
def post():
    result = parse(request.args.get('url', default='*', type=str))
    response = app.response_class(
        response=result,
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(port=80)
