import { useState } from "react";
import * as Types from "../../types/index";
import { customerAppController } from "../../services/CustomerAppController";

export default function OrderPayment({
  order,
  handleReset,
  goBack
}: {
  order: Types.Order;
  handleReset: () => void;
  goBack: () => void;
}) {
  const [paymentOption, setPaymentOption] = useState<"system" | "counter" | null>(null);
  const [cardInfo, setCardInfo] = useState({
    cardNumber: "",
    expiryDate: "",
    cvv: "",
    cardholderName: ""
  });
  const [isProcessing, setIsProcessing] = useState(false);

  const handleConfirmOrder = async () => {
    if (!paymentOption) {
      alert("Please select a payment method");
      return;
    }

    setIsProcessing(true);

    try {
      if (paymentOption === "system") {
        // Validate card info
        if (!cardInfo.cardNumber || !cardInfo.expiryDate || !cardInfo.cvv || !cardInfo.cardholderName) {
          alert("Please fill in all card information");
          setIsProcessing(false);
          return;
        }

        // First confirm the order
        await customerAppController.confirmOrder(order.id, "system");
        
        // Then process payment
        const cardInfoString = JSON.stringify(cardInfo);
        await customerAppController.payOnSystem(order.id, cardInfoString);
        
        alert("Payment processed successfully!");
      } else {
        // Mark as pay at counter
        await customerAppController.confirmOrder(order.id, "counter");
        alert("Order confirmed. Please pay at the counter when picking up.");
      }

      // Reset and go back to welcome screen
      handleReset();
    } catch (err) {
      console.error("Payment Error:", err);
      alert("Payment failed. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto p-8">
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <h2 className="text-3xl font-bold mb-6 text-center">Payment</h2>
          
          {/* Order Summary */}
          <div className="mb-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-xl font-bold mb-4">Order Summary</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Order ID:</span>
                <span className="font-semibold">{order.id}</span>
              </div>
              <div className="flex justify-between">
                <span>Items:</span>
                <span className="font-semibold">{order.items.length}</span>
              </div>
              <div className="flex justify-between text-2xl font-bold pt-2 border-t">
                <span>Total:</span>
                <span className="text-red-600">${order.total.toFixed(2)}</span>
              </div>
            </div>
          </div>

          {/* Payment Method Selection */}
          <div className="mb-8">
            <h3 className="text-xl font-bold mb-4">Select Payment Method</h3>
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => setPaymentOption("system")}
                className={`p-6 rounded-xl border-2 transition ${
                  paymentOption === "system"
                    ? "border-red-600 bg-red-50"
                    : "border-gray-300 hover:border-gray-400"
                }`}
              >
                <div className="text-2xl mb-2">💳</div>
                <div className="font-bold text-lg">Pay on System</div>
                <div className="text-sm text-gray-600 mt-1">Card payment</div>
              </button>
              <button
                onClick={() => setPaymentOption("counter")}
                className={`p-6 rounded-xl border-2 transition ${
                  paymentOption === "counter"
                    ? "border-red-600 bg-red-50"
                    : "border-gray-300 hover:border-gray-400"
                }`}
              >
                <div className="text-2xl mb-2">🏪</div>
                <div className="font-bold text-lg">Pay at Counter</div>
                <div className="text-sm text-gray-600 mt-1">Pay when picking up</div>
              </button>
            </div>
          </div>

          {/* Card Information Form (only show if system payment selected) */}
          {paymentOption === "system" && (
            <div className="mb-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="text-xl font-bold mb-4">Card Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Cardholder Name</label>
                  <input
                    type="text"
                    value={cardInfo.cardholderName}
                    onChange={(e) => setCardInfo({ ...cardInfo, cardholderName: e.target.value })}
                    placeholder="John Doe"
                    className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Card Number</label>
                  <input
                    type="text"
                    value={cardInfo.cardNumber}
                    onChange={(e) => setCardInfo({ ...cardInfo, cardNumber: e.target.value })}
                    placeholder="1234 5678 9012 3456"
                    maxLength={19}
                    className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Expiry Date</label>
                    <input
                      type="text"
                      value={cardInfo.expiryDate}
                      onChange={(e) => setCardInfo({ ...cardInfo, expiryDate: e.target.value })}
                      placeholder="MM/YY"
                      maxLength={5}
                      className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2">CVV</label>
                    <input
                      type="text"
                      value={cardInfo.cvv}
                      onChange={(e) => setCardInfo({ ...cardInfo, cvv: e.target.value })}
                      placeholder="123"
                      maxLength={4}
                      className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={goBack}
              className="flex-1 bg-gray-200 text-gray-800 py-4 rounded-xl text-xl font-bold hover:bg-gray-300 transition"
            >
              Back
            </button>
            <button
              onClick={handleConfirmOrder}
              disabled={isProcessing || !paymentOption}
              className="flex-1 bg-red-600 text-white py-4 rounded-xl text-xl font-bold hover:bg-red-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isProcessing ? "Processing..." : "Confirm Payment"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}