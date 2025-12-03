import { useState, useEffect } from "react";
import OrderList from "../components/cashier/OrderList";
import OrderDetails from "../components/cashier/OrderDetails";
import CounterPayment from "../components/cashier/CounterPayment";
import * as Types from "../types/index";

type ViewMode = "list" | "details" | "payment";

export default function CashierUI() {
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [selectedOrder, setSelectedOrder] = useState<Types.Order | null>(null);

  const handleOrderSelect = (order: Types.Order) => {
    setSelectedOrder(order);
    setViewMode("details");
  };

  const handleBackToList = () => {
    setSelectedOrder(null);
    setViewMode("list");
  };

  const handleProceedToPayment = (order: Types.Order) => {
    setSelectedOrder(order);
    setViewMode("payment");
  };

  const handlePaymentComplete = () => {
    setSelectedOrder(null);
    setViewMode("list");
  };

  const handleBackFromPayment = () => {
    if (selectedOrder) {
      setViewMode("details");
    } else {
      setViewMode("list");
    }
  };

  function renderView() {
    switch (viewMode) {
      case "list":
        return (
          <OrderList
            onOrderSelect={handleOrderSelect}
          />
        );
      case "details":
        if (!selectedOrder) {
          setViewMode("list");
          return null;
        }
        return (
          <OrderDetails
            order={selectedOrder}
            onBack={handleBackToList}
            onProceedToPayment={handleProceedToPayment}
          />
        );
      case "payment":
        if (!selectedOrder) {
          setViewMode("list");
          return null;
        }
        return (
          <CounterPayment
            order={selectedOrder}
            onBack={handleBackFromPayment}
            onPaymentComplete={handlePaymentComplete}
          />
        );
      default:
        return null;
    }
  }

  return <div>{renderView()}</div>;
}
