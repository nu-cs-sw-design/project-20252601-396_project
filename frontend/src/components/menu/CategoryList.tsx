import { useEffect, useState } from "react";
import * as Types from "../../types/index";
const MENU_ITEMS: Types.MenuItem[] = [
  {
    id: "b1",
    name: "Classic Burger",
    description: "Beef patty with lettuce, tomato, and special sauce",
    price: 8.99,
    category: "burgers",
  },
  {
    id: "b2",
    name: "Cheese Burger",
    description: "Classic burger with melted cheddar cheese",
    price: 9.99,
    category: "burgers",
  },
  {
    id: "b3",
    name: "Deluxe Burger",
    description: "Double patty with bacon, cheese, and premium toppings",
    price: 12.99,
    category: "burgers",
  },

  {
    id: "s1",
    name: "French Fries",
    description: "Crispy golden fries",
    price: 3.99,
    category: "sides",
  },
  {
    id: "s2",
    name: "Onion Rings",
    description: "Crispy battered onion rings",
    price: 4.99,
    category: "sides",
  },
  {
    id: "s3",
    name: "Chicken Nuggets",
    description: "6-piece crispy chicken nuggets",
    price: 5.99,
    category: "sides",
  },

  {
    id: "d1",
    name: "Coca Cola",
    description: "Refreshing cola drink",
    price: 2.49,
    category: "drinks",
  },
  {
    id: "d2",
    name: "Lemonade",
    description: "Fresh squeezed lemonade",
    price: 2.99,
    category: "drinks",
  },
  {
    id: "d3",
    name: "Milkshake",
    description: "Creamy vanilla milkshake",
    price: 4.99,
    category: "drinks",
  },
];

export default function CategoryList({ category, handleItemSelect }: { category: string, handleItemSelect: (itemid:Types.MenuItem)=>void }) {
  const [items, setItems] = useState<Types.MenuItem[]>([]);

  useEffect(() => {
    async function loadItems() {
      const res = await new Promise<Types.MenuItem[]>((resolve) => {
        setTimeout(() => {
          resolve(MENU_ITEMS.filter((i) => i.category === category));
        }, 600);
      });

      setItems(res);
    }

    loadItems();
  }, [category]);

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
