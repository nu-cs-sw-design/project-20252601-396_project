import { useEffect, useState } from "react";
import { DollarSign, ShoppingCart, TrendingUp, Calendar } from "lucide-react";
import { managerAppController } from "../../services/ManagerAppController";
import { kitchenAppController } from "../../services/KitchenAppController";
import * as Types from "../../types/index";

interface ManagementDashboardProps {
  onNavigateToMenu: () => void;
  onNavigateToReports: () => void;
}

export default function ManagementDashboard({ 
  onNavigateToMenu, 
  onNavigateToReports 
}: ManagementDashboardProps) {
  const [stats, setStats] = useState({
    todayRevenue: 0,
    todayOrders: 0,
    totalMenuItems: 0,
    pendingOrders: 0,
  });

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadStats = async () => {
    try {
      // Get menu items count
      const menuItems = await managerAppController.listMenuItems();
      
      // Get order queue (pending orders)
      const orderQueue = await kitchenAppController.getOrderQueue();
      
      // Get today's sales summary
      const today = new Date();
      const todaySummary = await managerAppController.showDailySalesSummary(today);

      setStats({
        todayRevenue: todaySummary.totalRevenue,
        todayOrders: todaySummary.numberOfOrders,
        totalMenuItems: menuItems.length,
        pendingOrders: orderQueue.length,
      });
    } catch (error) {
      console.error("Error loading stats:", error);
      // If API fails, show zeros
      setStats({
        todayRevenue: 0,
        todayOrders: 0,
        totalMenuItems: 0,
        pendingOrders: 0,
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8">Management Dashboard</h1>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Today's Revenue</p>
                <p className="text-3xl font-bold text-gray-800">
                  ${stats.todayRevenue.toFixed(2)}
                </p>
              </div>
              <DollarSign size={40} className="text-green-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Today's Orders</p>
                <p className="text-3xl font-bold text-gray-800">{stats.todayOrders}</p>
              </div>
              <ShoppingCart size={40} className="text-blue-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Menu Items</p>
                <p className="text-3xl font-bold text-gray-800">{stats.totalMenuItems}</p>
              </div>
              <TrendingUp size={40} className="text-purple-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Pending Orders</p>
                <p className="text-3xl font-bold text-gray-800">{stats.pendingOrders}</p>
              </div>
              <Calendar size={40} className="text-orange-600" />
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
            onClick={onNavigateToMenu}
            className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition text-left"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Menu Management</h2>
            <p className="text-gray-600">Add, edit, or remove menu items</p>
          </button>

          <button
            onClick={onNavigateToReports}
            className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition text-left"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Sales Reports</h2>
            <p className="text-gray-600">View daily sales summaries and analytics</p>
          </button>
        </div>
      </div>
    </div>
  );
}

