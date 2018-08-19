from flask import Blueprint, render_template, request, current_app
from simpledu.models import Live

live = Blueprint('live', __name__, url_prefix='/live')


@live.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    lives = Live.query.paginate(page=page,
                                    per_page=current_app.config['INDEX_PER_PAGE'],
                                    error_out=False)
    return render_template('live/index.html', pagination=lives)


@live.route('/<int:live_id>')
def detail(live_id):
    live = Live.query.get_or_404(live_id)
    return render_template('live/detail.html', live=live)
