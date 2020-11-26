from flask import Blueprint
from flask import render_template


# Blueprint Configuration
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@admin_bp.route('/', methods=['GET'])
def admin():
    """Homepage."""
    return render_template(
        'admin.jinja2',
        title='Administration',
        subtitle='Stock Analysis Administrator.',
        template='admin-template'
    )