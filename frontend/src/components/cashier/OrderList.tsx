import { useEffect, useState } from "react";
import { Search, Clock, DollarSign } from "lucide-react";
import * as Types from "../../types/index";
import { cashierAppController } from "../../services/CashierAppController";

interface OrderListProps {
  onOrderSelect: (order: Types.Order) => void;
}

export default function OrderList({ onOrderSelect }: OrderListProps) {
  const [orders, setOrders] = useState<Types.Order[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrders();
    // Refresh orders every 5 seconds
    const interval = setInterval(loadOrders, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadOrders = async () => {
    try {
      const pendingOrders = await cashierAppController.listPendingCounterPayments();
      // Sort by creation time (newest first)
      pendingOrders.sort((a, b) => 
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      );
      setOrders(pendingOrders);
      setLoading(false);
    } catch (error) {
      console.error("Error loading orders:", error);
      setLoading(false);
      // If API fails, show empty list
      setOrders([]);
    }
  };

  const handleSearch = async () => {
    if (searchTerm.trim()) {
      try {
        const order = await cashierAppController.findOrder(Number(searchTerm.trim()));
        onOrderSelect(order);
        setSearchTerm("");
      } catch (error) {
        alert(`Order #${searchTerm} not found`);
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading orders...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Pending Payments</h1>
          
          {/* Search Bar */}
          <div className="flex gap-4 mb-6">
            <div className="flex-1 flex gap-2">
              <input
                type="text"
                placeholder="Search by order number..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500"
              />
              <button
                onClick={handleSearch}
                className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition flex items-center gap-2"
              >
                <Search size={20} />
                Search
              </button>
            </div>
            <button
              onClick={loadOrders}
              className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
            >
              Refresh
            </button>
          </div>
        </div>

        {/* Orders List */}
        {orders.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-6xl mb-4">📋</div>
            <p className="text-2xl text-gray-600">No pending payments</p>
            <p className="text-gray-500 mt-2">All orders have been processed</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {orders.map((order) => (
              <button
                key={order.id}
                onClick={() => onOrderSelect(order)}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition text-left w-full"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800">Order #{order.id}</h3>
                    <p className="text-sm text-gray-500 mt-1">ID: {order.id}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    order.status === Types.OrderStatus.CONFIRMED
                      ? "bg-green-100 text-green-800"
                      : order.status === Types.OrderStatus.PREPARING
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-gray-100 text-gray-800"
                  }`}>
                    {order.status}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Clock size={16} />
                    <span className="text-sm">{formatDate(order.createdAt)}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-600">
                    <span className="text-sm">Items: {order.items.length}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="flex items-center gap-2">
                    <DollarSign size={20} className="text-red-600" />
                    <span className="text-2xl font-bold text-red-600">
                      ${order.totalAmount.toFixed(2)}
                    </span>
                  </div>
                  <span className="text-sm text-gray-500">Click to view</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

