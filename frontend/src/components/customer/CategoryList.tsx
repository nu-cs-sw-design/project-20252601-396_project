import { useEffect, useState } from "react";
import * as Types from "../../types/index";
import { customerAppController } from "../../services/CustomerAppController";

export default function CategoryList({ category, handleItemSelect }: { category: string, handleItemSelect: (itemid:Types.MenuItem)=>void }) {
  const [items, setItems] = useState<Types.MenuItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadItems() {
      try {
        const res = await customerAppController.getMenuItemsByCategory(category);
        setItems(res);
      } catch (err) {
        console.error("Error loading menu items:", err);
        alert("Failed to load menu items. Please try again.");
        setItems([]);
      } finally {
        setLoading(false);
      }
    }

    loadItems();
  }, [category]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <div className="max-w-6xl mx-auto p-8">
          <div className="text-center text-xl">Loading menu items...</div>
        </div>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-100">
        <div className="max-w-6xl mx-auto p-8">
          <div className="text-center text-xl text-gray-600">No items in this category</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-6xl mx-auto p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {items.map((item) => (
            <button
              key={item.id}
              onClick={() => handleItemSelect(item)}
              className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition text-left"
            >
              <div className="flex items-start gap-4">
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-800 mb-2">
                    {item.name}
                  </h3>
                  <p className="text-gray-600 mb-3">{item.description}</p>
                  <p className="text-2xl font-bold text-red-600">
                    ${item.price.toFixed(2)}
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
