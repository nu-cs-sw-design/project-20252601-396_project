import { useEffect, useState } from "react";
import { ArrowLeft, Clock, DollarSign, User } from "lucide-react";
import * as Types from "../../types/index";
import { cashierAppController } from "../../services/CashierAppController";

interface OrderDetailsProps {
  order: Types.Order;
  onBack: () => void;
  onProceedToPayment: (order: Types.Order) => void;
}

export default function OrderDetails({ order, onBack, onProceedToPayment }: OrderDetailsProps) {
  const [orderDetails, setOrderDetails] = useState<Types.Order | null>(order);

  useEffect(() => {
    // Refresh order details
    const loadOrderDetails = async () => {
      try {
        const updatedOrder = await cashierAppController.findOrder(order.orderNumber);
        setOrderDetails(updatedOrder);
      } catch (error) {
        console.error("Error loading order details:", error);
        // Keep existing order if refresh fails
        setOrderDetails(order);
      }
    };
    loadOrderDetails();
  }, [order.id, order.orderNumber]);

  if (!orderDetails) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Order not found</div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={onBack}
              className="hover:bg-gray-100 p-2 rounded-lg transition"
            >
              <ArrowLeft size={24} />
            </button>
            <h1 className="text-3xl font-bold text-gray-800">Order Details</h1>
            <div className="w-10"></div> {/* Spacer for centering */}
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-sm text-gray-500">Order Number</p>
              <p className="text-xl font-bold">#{orderDetails.orderNumber}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Order ID</p>
              <p className="text-sm font-mono text-gray-600">{orderDetails.id}</p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex items-center gap-2 text-gray-600">
              <Clock size={16} />
              <span className="text-sm">{formatDate(orderDetails.createdAt)}</span>
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              orderDetails.status === Types.OrderStatus.CONFIRMED
                ? "bg-green-100 text-green-800"
                : orderDetails.status === Types.OrderStatus.PREPARING
                ? "bg-yellow-100 text-yellow-800"
                : "bg-gray-100 text-gray-800"
            }`}>
              {orderDetails.status}
            </span>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              orderDetails.paymentStatus === Types.PaymentStatus.PENDING
                ? "bg-red-100 text-red-800"
                : orderDetails.paymentStatus === Types.PaymentStatus.COMPLETED
                ? "bg-green-100 text-green-800"
                : "bg-gray-100 text-gray-800"
            }`}>
              Payment: {orderDetails.paymentStatus}
            </span>
          </div>
        </div>

        {/* Order Items */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Order Items</h2>
          {orderDetails.items.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No items in this order</p>
            </div>
          ) : (
            <div className="space-y-4">
              {orderDetails.items.map((item, index) => (
                <div key={index} className="border-b pb-4 last:border-b-0">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-800">
                        {item.menuItem?.name}
                      </h3>
                      {item.menuItem?.description && (
                        <p className="text-sm text-gray-600 mt-1">
                          {item.menuItem.description}
                        </p>
                      )}
                      {(item.customizations) && (
                        <p className="text-sm text-gray-500 mt-2 italic">
                          Special: {item.customizations}
                        </p>
                      )}
                      <div className="flex items-center gap-4 mt-2">
                        <span className="text-sm text-gray-600">
                          Quantity: <span className="font-bold">{item.quantity}</span>
                        </span>
                        <span className="text-sm text-gray-600">
                          Unit Price: <span className="font-bold">${item.unitPrice.toFixed(2)}</span>
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-gray-800">
                        ${(item.quantity * item.unitPrice).toFixed(2)}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Order Total */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <DollarSign size={24} className="text-red-600" />
              <span className="text-2xl font-bold text-gray-800">Total Amount</span>
            </div>
            <span className="text-3xl font-bold text-red-600">
              ${orderDetails.totalAmount.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Action Button */}
        {orderDetails.paymentStatus === Types.PaymentStatus.PENDING && (
          <button
            onClick={() => onProceedToPayment(orderDetails)}
            className="w-full bg-red-600 text-white py-4 rounded-xl text-xl font-bold hover:bg-red-700 transition"
          >
            Process Payment
          </button>
        )}
      </div>
    </div>
  );
}

