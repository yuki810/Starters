
view = Blueprint('index', __name__, url_prefix='/')
@view.route('/', methods=['GET'])
def show():
    return render_template('index.html', user_icon_url=user_icon_url)