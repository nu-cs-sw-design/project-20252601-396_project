import { useEffect, useState } from "react";
import { Clock, CheckCircle, XCircle, ChefHat } from "lucide-react";
import * as Types from "../../types/index";
import { kitchenAppController } from "../../services/KitchenAppController";

interface OrderQueueProps {
  onOrderSelect?: (order: Types.Order) => void;
}

export default function OrderQueue({ onOrderSelect }: OrderQueueProps) {
  const [orders, setOrders] = useState<Types.Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | Types.OrderStatus>("all");

  useEffect(() => {
    loadOrders();
    // Refresh orders every 3 seconds
    const interval = setInterval(loadOrders, 3000);
    return () => clearInterval(interval);
  }, [filter]);

  const loadOrders = async () => {
    try {
      let allOrders: Types.Order[] = [];
      
      if (filter === "all") {
        // Get all orders in queue (confirmed and preparing)
        allOrders = await kitchenAppController.getOrderQueue();
      } else {
        // Get orders by specific status
        const queue = await kitchenAppController.getOrderQueue();
        allOrders = queue.filter(order => order.status === filter);
      }

      // Filter out cancelled and completed orders
      allOrders = allOrders.filter(
        order => 
          order.status !== Types.OrderStatus.CANCELLED &&
          order.status !== Types.OrderStatus.COMPLETED
      );

      // Sort by creation time (oldest first for kitchen)
      allOrders.sort((a, b) => 
        new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      );

      setOrders(allOrders);
      setLoading(false);
    } catch (error) {
      console.error("Error loading orders:", error);
      setLoading(false);
      // If API fails, show empty list
      setOrders([]);
    }
  };

  const handleMarkInPreparation = async (orderId: string) => {
    try {
      await kitchenAppController.markInPreparation(orderId);
      loadOrders();
    } catch (error) {
      console.error("Error marking order in preparation:", error);
      alert("Failed to update order status. Please try again.");
    }
  };

  const handleMarkReady = async (orderId: string) => {
    try {
      await kitchenAppController.markReady(orderId);
      loadOrders();
    } catch (error) {
      console.error("Error marking order as ready:", error);
      alert("Failed to update order status. Please try again.");
    }
  };

  const handleCancelOrder = async (orderId: string) => {
    if (window.confirm("Are you sure you want to cancel this order?")) {
      try {
        await kitchenAppController.cancelOrder(orderId);
        loadOrders();
      } catch (error) {
        console.error("Error cancelling order:", error);
        alert("Failed to cancel order. Please try again.");
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getStatusColor = (status: Types.OrderStatus) => {
    switch (status) {
      case Types.OrderStatus.CONFIRMED:
        return "bg-blue-100 text-blue-800";
      case Types.OrderStatus.PREPARING:
        return "bg-yellow-100 text-yellow-800";
      case Types.OrderStatus.READY:
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
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
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-4xl font-bold text-gray-800 flex items-center gap-3">
              <ChefHat size={40} className="text-red-600" />
              Kitchen Order Queue
            </h1>
            <button
              onClick={loadOrders}
              className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
            >
              Refresh
            </button>
          </div>

          {/* Filter Buttons */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setFilter("all")}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                filter === "all"
                  ? "bg-red-600 text-white"
                  : "bg-white text-gray-800 hover:bg-gray-100"
              }`}
            >
              All Orders
            </button>
            <button
              onClick={() => setFilter(Types.OrderStatus.CONFIRMED)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                filter === Types.OrderStatus.CONFIRMED
                  ? "bg-red-600 text-white"
                  : "bg-white text-gray-800 hover:bg-gray-100"
              }`}
            >
              Confirmed
            </button>
            <button
              onClick={() => setFilter(Types.OrderStatus.PREPARING)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                filter === Types.OrderStatus.PREPARING
                  ? "bg-red-600 text-white"
                  : "bg-white text-gray-800 hover:bg-gray-100"
              }`}
            >
              Preparing
            </button>
            <button
              onClick={() => setFilter(Types.OrderStatus.READY)}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                filter === Types.OrderStatus.READY
                  ? "bg-red-600 text-white"
                  : "bg-white text-gray-800 hover:bg-gray-100"
              }`}
            >
              Ready
            </button>
          </div>
        </div>

        {/* Orders List */}
        {orders.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-6xl mb-4">🍳</div>
            <p className="text-2xl text-gray-600">No orders in queue</p>
            <p className="text-gray-500 mt-2">All orders have been processed</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {orders.map((order) => (
              <div
                key={order.id}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800">Order #{order.orderNumber}</h3>
                    <p className="text-sm text-gray-500 mt-1">ID: {order.id}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(order.status)}`}>
                    {order.status}
                  </span>
                </div>

                <div className="flex items-center gap-2 text-gray-600 mb-4">
                  <Clock size={16} />
                  <span className="text-sm">{formatDate(order.createdAt)}</span>
                </div>

                {/* Order Items */}
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-800 mb-2">Items:</h4>
                  <div className="space-y-1">
                    {order.items.map((item, index) => (
                      <div key={index} className="text-sm text-gray-600">
                        <span className="font-semibold">{item.quantity}x</span>{" "}
                        {item.menuItem?.name || `Item ${item.menuItem.id}`}
                        {(item.customizations) && (
                          <span className="text-gray-500 italic">
                            {" "}({item.customizations})
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-2 mt-4">
                  {order.status === Types.OrderStatus.CONFIRMED && (
                    <button
                      onClick={() => handleMarkInPreparation(order.id)}
                      className="flex-1 bg-yellow-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-yellow-700 transition flex items-center justify-center gap-2"
                    >
                      <ChefHat size={18} />
                      Start Preparing
                    </button>
                  )}
                  {order.status === Types.OrderStatus.PREPARING && (
                    <button
                      onClick={() => handleMarkReady(order.id)}
                      className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-700 transition flex items-center justify-center gap-2"
                    >
                      <CheckCircle size={18} />
                      Mark Ready
                    </button>
                  )}
                  {order.status !== Types.OrderStatus.READY && (
                    <button
                      onClick={() => handleCancelOrder(order.id)}
                      className="bg-red-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-700 transition flex items-center justify-center gap-2"
                    >
                      <XCircle size={18} />
                      Cancel
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

