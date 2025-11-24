import * as Types from "../../types/index";
import { useEffect, useState } from "react";
import { Plus, Minus, Trash2 } from "lucide-react";

export default function ReviewOrder({ orderId, handleReset }: { orderId: string, handleReset:()=>void}) {
  const [orderSummary, setOrderSummary] = useState<Types.Order | null>(null);

  const handleUpdateQuantity = async (itemId: string, quantity: number) => {
    try {
      const res = await new Promise<string>((resolve) => {
        setTimeout(() => {
          resolve(
            "order" +
              orderId +
              "updated item " +
              itemId +
              " updated quantity to" +
              quantity
          );
        }, 600);
      });
      alert(res);
    } catch (err) {
      console.error("API Error:", err);
    }
  };

  const handleRemoveItem = async (itemId: string) => {
    try {
      const res = await new Promise<string>((resolve) => {
        setTimeout(() => {
          resolve("order" + orderId + "removed item " + itemId);
        }, 600);
      });
      alert(res);
    } catch (err) {
      console.error("API Error:", err);
    }
  };

  useEffect(() => {
    async function loadOrder() {
      const res = await new Promise<Types.Order>((resolve) => {
        setTimeout(() => {
          resolve({
            id: "order1",
            items: [],
            total: 12,
            status: Types.OrderStatus.PENDING,
            createdAt: "11/23/2025",
            customerName: "Robert",
            customerEmail: "blahblah@blahblah.com",
          });
        }, 600);
      });

      setOrderSummary(res);
    }

    loadOrder();
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
                    key={item.menuItemId}
                    className="border-b pb-4 last:border-b-0"
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold">{item.menuItemId}</h3>
                        <p className="text-sm text-gray-600">
                          {item.specialInstructions}
                        </p>
                        <div className="flex items-center gap-4 mt-2">
                          <button
                            onClick={() =>
                              handleUpdateQuantity(
                                item.menuItemId,
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
                                item.menuItemId,
                                item.quantity + 1
                              )
                            }
                            className="bg-gray-200 hover:bg-gray-300 p-2 rounded"
                          >
                            <Plus size={16} />
                          </button>
                          <button
                            onClick={() => handleRemoveItem(item.menuItemId)}
                            className="ml-auto text-red-600 hover:bg-red-50 p-2 rounded"
                          >
                            <Trash2 size={20} />
                          </button>
                        </div>
                      </div>
                      {/* <div className="text-xl font-bold">
                        ${item.price.toFixed(2)}
                      </div> */}
                    </div>
                  </div>
                ))}
              </div>

              {/* <div className="border-t pt-4 mt-4">
                <div className="flex justify-between items-center text-3xl font-bold">
                  <span>Total:</span>
                  <span className="text-red-600">
                    ${calculateTotal().toFixed(2)}
                  </span>
                </div>
              </div> */}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                    alert("User payment not yet implemented!");
                    handleReset();
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
