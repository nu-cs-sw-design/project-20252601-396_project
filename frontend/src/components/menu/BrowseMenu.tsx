import { useEffect, useState } from "react";
import CategoryList from "./CategoryList";
import * as Types from "../../types/index"

export default function BrowseMenu({handleItemSelect}:{handleItemSelect:(item:Types.MenuItem)=>void}) {
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string|null>(null);

  useEffect(() => {
    async function loadCategories() {
      const res = await new Promise<string[]>((resolve) => {
        setTimeout(() => {
          resolve(["burgers", "sides", "drinks"]);
        }, 600);
      });

      setCategories(res);
    }

    loadCategories();
  }, []);


  return (
  <div className="max-w-6xl mx-auto p-8">
    {selectedCategory === null ? (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className="bg-white p-12 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
          >
            <h2 className="text-3xl font-bold text-gray-800">{category}</h2>
          </button>
        ))}
      </div>
    ) : (
    
      <CategoryList category={selectedCategory} handleItemSelect={handleItemSelect} />
    )}
  </div>
);

}
