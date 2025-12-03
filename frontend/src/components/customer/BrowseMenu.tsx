import { useEffect, useState } from "react";
import CategoryList from "./CategoryList";
import * as Types from "../../types/index";
import { customerAppController } from "../../services/CustomerAppController";

export default function BrowseMenu({handleItemSelect}:{handleItemSelect:(item:Types.MenuItem)=>void}) {
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string|null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCategories() {
      try {
        const res = await customerAppController.browseMenu();
        setCategories(res);
      } catch (err) {
        console.error("Error loading categories:", err);
        alert("Failed to load menu categories. Please try again.");
        // Fallback to default categories
        setCategories(["burgers", "sides", "drinks"]);
      } finally {
        setLoading(false);
      }
    }

    loadCategories();
  }, []);


  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-8">
        <div className="text-center text-xl">Loading categories...</div>
      </div>
    );
  }

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
              <h2 className="text-3xl font-bold text-gray-800 capitalize">{category}</h2>
            </button>
          ))}
        </div>
      ) : (
        <CategoryList category={selectedCategory} handleItemSelect={handleItemSelect} />
      )}
    </div>
  );

}
