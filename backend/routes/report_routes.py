from flask import Blueprint, request, jsonify
from services.report_service import ReportService

report_bp = Blueprint('report', __name__, url_prefix='/api/reports')
@report_bp.route('sales-summary/<string:date>', methods=['GET'])
def get_sales_summary(date: str):
    """
    UC15: Generate Sales Summary Report
    Get sales summary report for a given date range
    Query params:
        - date: the date for which to generate the report (YYYY-MM-DD)
    """
    try:
        # For simplicity, assume date is a single day; in practice, could be a range
        report = ReportService.generate_daily_sales_summary(date)
        return jsonify({
            'data': report.to_dict(),
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
    
    