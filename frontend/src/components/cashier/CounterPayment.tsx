import { useState } from "react";
import { ArrowLeft, CreditCard, Wallet, Smartphone, CheckCircle } from "lucide-react";
import * as Types from "../../types/index";
import { cashierAppController } from "../../services/CashierAppController";

interface CounterPaymentProps {
  order: Types.Order;
  onBack: () => void;
  onPaymentComplete: () => void;
}

type PaymentMethod = "cash" | "card" | "mobile" | null;

export default function CounterPayment({ order, onBack, onPaymentComplete }: CounterPaymentProps) {
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentComplete, setPaymentComplete] = useState(false);

  const handleProcessPayment = async () => {
    if (!paymentMethod) {
      alert("Please select a payment method");
      return;
    }

    setIsProcessing(true);

    try {
      // Call backend API to complete payment
      await cashierAppController.completeCounterPayment(
        order.id,
        paymentMethod
      );

      setPaymentComplete(true);
      
      // Auto redirect after 2 seconds
      setTimeout(() => {
        onPaymentComplete();
      }, 2000);
    } catch (error) {
      console.error("Payment processing error:", error);
      alert("Payment failed. Please try again.");
      setIsProcessing(false);
    }
  };

  if (paymentComplete) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-8">
        <div className="bg-white rounded-2xl shadow-xl p-12 text-center max-w-md">
          <CheckCircle size={64} className="text-green-500 mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Payment Successful!</h2>
          <p className="text-gray-600 mb-4">Order #{order.id} has been paid</p>
          <p className="text-sm text-gray-500">Redirecting...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <button
              onClick={onBack}
              className="hover:bg-gray-100 p-2 rounded-lg transition"
            >
              <ArrowLeft size={24} />
            </button>
            <h1 className="text-3xl font-bold text-gray-800">Process Payment</h1>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-500">Order Number</p>
                <p className="text-xl font-bold">#{order.id}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-500">Total Amount</p>
                <p className="text-3xl font-bold text-red-600">${order.totalAmount.toFixed(2)}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Payment Method Selection */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Select Payment Method</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => setPaymentMethod("cash")}
              className={`p-6 rounded-xl border-2 transition ${
                paymentMethod === "cash"
                  ? "border-red-600 bg-red-50"
                  : "border-gray-300 hover:border-gray-400"
              }`}
            >
              <Wallet size={32} className="mx-auto mb-2 text-gray-700" />
              <div className="font-bold text-lg">Cash</div>
            </button>
            <button
              onClick={() => setPaymentMethod("card")}
              className={`p-6 rounded-xl border-2 transition ${
                paymentMethod === "card"
                  ? "border-red-600 bg-red-50"
                  : "border-gray-300 hover:border-gray-400"
              }`}
            >
              <CreditCard size={32} className="mx-auto mb-2 text-gray-700" />
              <div className="font-bold text-lg">Card</div>
            </button>
            <button
              onClick={() => setPaymentMethod("mobile")}
              className={`p-6 rounded-xl border-2 transition ${
                paymentMethod === "mobile"
                  ? "border-red-600 bg-red-50"
                  : "border-gray-300 hover:border-gray-400"
              }`}
            >
              <Smartphone size={32} className="mx-auto mb-2 text-gray-700" />
              <div className="font-bold text-lg">Mobile</div>
            </button>
          </div>
        </div>

        {/* Payment Summary */}
        {paymentMethod && (
          <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Payment Summary</h2>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Payment Method:</span>
                <span className="font-semibold capitalize">{paymentMethod}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Amount:</span>
                <span className="font-semibold">${order.totalAmount.toFixed(2)}</span>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={onBack}
            className="flex-1 bg-gray-200 text-gray-800 py-4 rounded-xl text-xl font-bold hover:bg-gray-300 transition"
          >
            Cancel
          </button>
          <button
            onClick={handleProcessPayment}
            disabled={!paymentMethod || isProcessing}
            className="flex-1 bg-red-600 text-white py-4 rounded-xl text-xl font-bold hover:bg-red-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isProcessing ? "Processing..." : "Confirm Payment"}
          </button>
        </div>
      </div>
    </div>
  );
}

