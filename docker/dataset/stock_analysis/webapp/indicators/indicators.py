from flask import Blueprint
from flask import render_template
from flask import current_app as app

from ..api import get_indicators, get_patterns


# Blueprint Configuration
indicators_bp = Blueprint(
    'indicators_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
@indicators_bp.route('/', defaults={'ind': 'default'})
@indicators_bp.route('/<ind>')
def indicators(ind):
    """Indicator Page."""
    indicators = get_indicators(app)
    app.logger.info("Indicator is : {}".format(ind))
    return render_template(
        'indicators.jinja2',
        title='Indicators',
        subtitle='Indicators.',
        template='indicators-template',
        indicators=indicators,
        patterns=get_patterns(app),
        INDI=ind
    )