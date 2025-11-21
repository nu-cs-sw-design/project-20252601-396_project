"""
Main API routes
"""
from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__, url_prefix='/api')


@main_bp.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({
        'message': 'API is working!',
        'status': 'success'
    }), 200

