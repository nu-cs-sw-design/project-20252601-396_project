
from datetime import date, datetime
from database import db
from models.order import Order,OrderStatus
from models.order_item import OrderItem
from models.menu_item import MenuItem
from services.menu_service import MenuService


class DailySalesSummary:
    def __init__(self, date: date, total_revenue: float, number_of_orders: int, top_selling_items: list):
        self.date = date
        self.total_revenue = total_revenue
        self.number_of_orders = number_of_orders
        self.top_selling_items = top_selling_items
        
    def to_dict(self):
        return {
            'date': self.date,
            'totalRevenue': self.total_revenue,
            'numberOfOrders': self.number_of_orders,
            'topSellingItems': self.top_selling_items
        }
        

class ReportService:
    
    """Service for generating reports"""
    
    @staticmethod
    def generate_daily_sales_summary(target_date: str) -> DailySalesSummary:
        """Generate daily sales summary for a given date"""
        date_str = target_date
        start_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        end_datetime = start_datetime.replace(hour=23, minute=59, second=59)
        
        
        orders = Order.query.filter(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime,
            Order.status == OrderStatus.READY
        ).all()
        
        total_revenue = sum(order.total for order in orders)
        number_of_orders = len(orders)
        sale_per_item = {}
        for order in orders:
            for item in order.order_items:
                item_id = item.menu_item_id
                if item_id not in sale_per_item:
                    sale_per_item[item_id] = 0
                sale_per_item[item_id] += item.quantity
                
        categories = MenuService.getMenuCategories()
        menu_items = {}
        for category in categories:
            items = MenuService.getMenuItemsByCategory(category)
            for item in items:
                menu_items[item.id] = item
                
        sorted_items = sorted(sale_per_item.items(), key=lambda x: x[1], reverse=True)
        top_selling_items = []
        for item_id, quantity in sorted_items[:5]:
            top_selling_items.append(menu_items[item_id].to_dict())
        return DailySalesSummary(
            date=target_date,
            total_revenue=round(total_revenue, 2),
            number_of_orders=number_of_orders,
            top_selling_items=top_selling_items
        )