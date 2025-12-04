import * as Types from "../../types/index";
import { useEffect, useState } from "react";
import { Plus, Minus, Trash2 } from "lucide-react";
import { customerAppController } from "../../services/CustomerAppController";

export default function ReviewOrder({ 
  orderId, 
  handleReset,
  handleProceedToPayment 
}: { 
  orderId: string, 
  handleReset:()=>void,
  handleProceedToPayment?: (order: Types.Order) => void
}) {
  const [orderSummary, setOrderSummary] = useState<Types.Order | null>(null);

  const handleUpdateQuantity = async (itemId: string, quantity: number) => {
    if (quantity < 1) {
      // If quantity becomes 0, remove the item instead
      handleRemoveItem(itemId);
      return;
    }

    try {
      // Find the item to get its customizations
      const currentItem = orderSummary?.items.find(item => item.menuItem.id === itemId);
      const customizations = currentItem?.customizations || "";

      await customerAppController.editItemInOrder(
        orderId,
        itemId,
        quantity,
        customizations
      );
      
      // Reload order to get updated data
      const updatedOrder = await customerAppController.reviewCurrentOrder(orderId);
      setOrderSummary(updatedOrder);
    } catch (err) {
      console.error("API Error:", err);
      alert("Failed to update quantity. Please try again.");
    }
  };

  const handleRemoveItem = async (itemId: string) => {
    try {
      await customerAppController.removeItemFromOrder(orderId, itemId);
      
      // Reload order to get updated data
      const updatedOrder = await customerAppController.reviewCurrentOrder(orderId);
      setOrderSummary(updatedOrder);
    } catch (err) {
      console.error("API Error:", err);
      alert("Failed to remove item. Please try again.");
    }
  };

  useEffect(() => {
    async function loadOrder() {
      try {
        const order = await customerAppController.reviewCurrentOrder(orderId);
        setOrderSummary(order);
      } catch (err) {
        console.error("Error loading order:", err);
        alert("Failed to load order. Please try again.");
      }
    }

    if (orderId) {
      loadOrder();
    }
  }, [orderId]);

  if (orderSummary == null){
    return <div></div>;
  }

 
    return (
      <div className="max-w-4xl mx-auto p-8">
        {orderSummary.items.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-6xl mb-4">🛒</div>
            <p className="text-2xl text-gray-600">Your order is empty</p>
          </div>
        ) : (
          <>
            <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
              <div className="space-y-4">
                {orderSummary.items.map((item) => (
                  <div
                    key={item.menuItem.id}
                    className="border-b pb-4 last:border-b-0"
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold">
                          {item.menuItem?.name || `Item ${item.menuItem.id}`}
                        </h3>
                        {(item.customizations) && (
                          <p className="text-sm text-gray-600">
                            {item.customizations}
                          </p>
                        )}
                        {item.unitPrice > 0 && (
                          <p className="text-sm text-gray-500 mt-1">
                            ${item.unitPrice.toFixed(2)} each
                          </p>
                        )}
                        <div className="flex items-center gap-4 mt-2">
                          <button
                            onClick={() =>
                              handleUpdateQuantity(
                                item.menuItem.id,
                                item.quantity - 1
                              )
                            }
                            className="bg-gray-200 hover:bg-gray-300 p-2 rounded"
                          >
                            <Minus size={16} />
                          </button>
                          <span className="font-bold">{item.quantity}</span>
                          <button
                            onClick={() =>
                              handleUpdateQuantity(
                                item.menuItem.id,
                                item.quantity + 1
                              )
                            }
                            className="bg-gray-200 hover:bg-gray-300 p-2 rounded"
                          >
                            <Plus size={16} />
                          </button>
                          <button
                            onClick={() => handleRemoveItem(item.menuItem.id)}
                            className="ml-auto text-red-600 hover:bg-red-50 p-2 rounded"
                          >
                            <Trash2 size={20} />
                          </button>
                        </div>
                      </div>
                      <div className="text-xl font-bold">
                        ${(item.quantity * item.unitPrice).toFixed(2)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="border-t pt-4 mt-4">
                <div className="flex justify-between items-center text-3xl font-bold">
                  <span>Total:</span>
                  <span className="text-red-600">
                    ${orderSummary.totalAmount.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                    if (handleProceedToPayment && orderSummary) {
                      handleProceedToPayment(orderSummary);
                    } else {
                      alert("User payment not yet implemented!");
                      handleReset();
                    }
                }}
                className="bg-red-600 text-white py-4 rounded-xl text-xl font-bold hover:bg-red-700 transition"
              >
                Checkout
              </button>
            </div>
          </>
        )}
      </div>
    );
  
}
