from flask import Flask
from api import api as api_blueprint
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/aweme/v1/web')
# 精选页面使用/aweme/v2/web
app.register_blueprint(api_blueprint, url_prefix='/aweme/v2/web', name='api_v2')

CORS(app, origins='*', supports_credentials=True)  # 解决跨域问题


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3010)
