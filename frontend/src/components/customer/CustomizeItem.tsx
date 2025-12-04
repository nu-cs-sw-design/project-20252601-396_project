import {useState} from "react";
import {Minus,Plus} from "lucide-react"
import * as Types from "../../types/index";
import { customerAppController } from "../../services/CustomerAppController";

export default function CustomizeItem({item, orderId, goBack}:{item: Types.MenuItem, orderId:number, goBack:()=>void}) {

    const [itemQuantity, setItemQuantity] = useState<number>(1);
    const [itemCustomizations, setItemCustomizations] = useState<string>("");
    const [isAdding, setIsAdding] = useState(false);

    const handleAddToOrder = async () => {
        if (itemQuantity < 1) {
            alert("Please select at least 1 item");
            return;
        }

        setIsAdding(true);
        try {
            await customerAppController.addItemToOrder(
                orderId,
                item.id,
                itemQuantity,
                itemCustomizations
            );
            goBack();
        } catch (err) {
            console.error("API Error:", err);
            alert("Failed to add item to order. Please try again.");
        } finally {
            setIsAdding(false);
        }
    };
  
  
    return (
    <div className="min-h-screen bg-gray-100">


      <div className="max-w-4xl mx-auto p-8">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <h2 className="text-4xl font-bold text-gray-800 mb-2">
              {item.name}
            </h2>
            <p className="text-xl text-gray-600">{item.description}</p>
          </div>

          <div className="mb-8">
            <h3 className="text-2xl font-bold mb-4">Customize</h3>
            <div className="grid grid-cols-3 gap-4">
              <input
                type="text"
                placeholder="Add special instructions here!"
                value={itemCustomizations || ""}
                onChange={(e) => setItemCustomizations(e.target.value)}
                className="w-full p-4 border-2 border-gray-300 rounded-xl focus:border-red-500 focus:ring-red-500 transition"
              />
            </div>
          </div>

          <div className="mb-8">
            <h3 className="text-2xl font-bold mb-4">Quantity</h3>
            <div className="flex items-center justify-center gap-6">
              <button
                onClick={() => setItemQuantity(Math.max(1, itemQuantity - 1))}
                className="bg-gray-200 hover:bg-gray-300 p-4 rounded-full"
              >
                <Minus size={24} />
              </button>
              <span className="text-3xl font-bold w-16 text-center">
                {itemQuantity}
              </span>
              <button
                onClick={() => setItemQuantity(itemQuantity + 1)}
                className="bg-gray-200 hover:bg-gray-300 p-4 rounded-full"
              >
                <Plus size={24} />
              </button>
            </div>
          </div>

          <button
            onClick={handleAddToOrder}
            disabled={isAdding || itemQuantity < 1}
            className="w-full bg-red-600 text-white py-6 rounded-xl text-2xl font-bold hover:bg-red-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isAdding ? "Adding..." : `Add to Order - $${(itemQuantity*item.price).toFixed(2)}`}
          </button>
        </div>
      </div>
    </div>
  );
}
