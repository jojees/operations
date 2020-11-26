from flask import Blueprint
from flask import render_template


# Blueprint Configuration
dashboard_bp = Blueprint(
    'dashboard_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    """Homepage."""
    return render_template(
        'dashboard.jinja2',
        title='Dashboard',
        subtitle='Stock Analysis Dashboard.',
        template='dashboard-template'
    )