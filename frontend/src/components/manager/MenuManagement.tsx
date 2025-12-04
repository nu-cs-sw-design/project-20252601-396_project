import { useEffect, useState } from "react";
import { ArrowLeft, Plus, Edit, Trash2 } from "lucide-react";
import * as Types from "../../types/index";
import { managerAppController } from "../../services/ManagerAppController";

interface MenuManagementProps {
  onBack: () => void;
}

export default function MenuManagement({ onBack }: MenuManagementProps) {
  const [menuItems, setMenuItems] = useState<Types.MenuItem[]>([]);
  const [editingItem, setEditingItem] = useState<Types.MenuItem | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    price: "",
    category: "",
    description: "",
  });

  useEffect(() => {
    loadMenuItems();
  }, []);

  const loadMenuItems = async () => {
    try {
      const items = await managerAppController.listMenuItems();
      setMenuItems(items);
    } catch (error) {
      console.error("Error loading menu items:", error);
      alert("Failed to load menu items. Please try again.");
      setMenuItems([]);
    }
  };

  const handleAddItem = () => {
    setFormData({ name: "", price: "", category: "", description: "" });
    setEditingItem(null);
    setShowAddForm(true);
  };

  const handleEditItem = (item: Types.MenuItem) => {
    setFormData({
      name: item.name,
      price: item.price.toString(),
      category: item.category,
      description: item.description,
    });
    setEditingItem(item);
    setShowAddForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" })
  };

  const handleDeleteItem = async (itemId: string) => {
    if (window.confirm("Are you sure you want to delete this menu item?")) {
      try {
        // Note: Delete endpoint not in design.puml, but we can add it
        // For now, we'll need to implement this in the backend
        // await managerAppController.deleteMenuItem(itemId);
        alert("Delete functionality isn't currently implemented for this version.");
        // loadMenuItems();
      } catch (error) {
        console.error("Error deleting menu item:", error);
        alert("Failed to delete menu item. Please try again.");
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.price || !formData.category) {
      alert("Please fill in all required fields");
      return;
    }

    try {
      if (editingItem) {
        // Update existing item
        await managerAppController.updateMenuItem(
          editingItem.id,
          parseFloat(formData.price),
          formData.description
        );
      } else {
        // Add new item
        await managerAppController.addMenuItem(
          formData.name,
          parseFloat(formData.price),
          formData.category,
          formData.description
        );
      }

      setShowAddForm(false);
      setEditingItem(null);
      setFormData({ name: "", price: "", category: "", description: "" });
      loadMenuItems();

    } catch (error) {
      console.error("Error saving menu item:", error);
      alert("Failed to save menu item. Please try again.");
    }
  };

  // Extract categories from menu items
  const categories = Array.from(new Set(menuItems.map(item => item.category)));

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="hover:bg-gray-200 p-2 rounded-lg transition"
            >
              <ArrowLeft size={24} />
            </button>
            <h1 className="text-4xl font-bold text-gray-800">Menu Management</h1>
          </div>
          <button
            onClick={handleAddItem}
            className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition flex items-center gap-2"
          >
            <Plus size={20} />
            Add Item
          </button>
        </div>

        {/* Add/Edit Form */}
        {showAddForm && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              {editingItem ? "Edit Menu Item" : "Add New Menu Item"}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-semibold mb-2">Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Price *</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                    className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Category *</label>
                  <input
                    type="text"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-red-500"
                  rows={3}
                />
              </div>
              <div className="flex gap-4">
                <button
                  type="submit"
                  className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition"
                >
                  {editingItem ? "Update" : "Add"} Item
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddForm(false);
                    setEditingItem(null);
                    setFormData({ name: "", price: "", category: "", description: "" });
                  }}
                  className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Menu Items List */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Menu Items</h2>
          {menuItems.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No menu items. Add your first item!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {categories.map((category) => {
                const categoryItems = menuItems.filter(item => item.category === category);
                return (
                  <div key={category} className="mb-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-3 capitalize">
                      {category}
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {categoryItems.map((item) => (
                        <div
                          key={item.id}
                          className="border-2 border-gray-200 rounded-lg p-4 hover:border-red-500 transition"
                        >
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex-1">
                              <h4 className="text-lg font-bold text-gray-800">{item.name}</h4>
                              <p className="text-sm text-gray-600 mt-1">{item.description}</p>
                              <p className="text-xl font-bold text-red-600 mt-2">
                                ${item.price.toFixed(2)}
                              </p>
                            </div>
                            <div className="flex gap-2">
                              <button
                                onClick={() => handleEditItem(item)}
                                className="bg-blue-100 text-blue-600 p-2 rounded hover:bg-blue-200 transition"
                              >
                                <Edit size={18} />
                              </button>
                              <button
                                onClick={() => handleDeleteItem(item.id)}
                                className="bg-red-100 text-red-600 p-2 rounded hover:bg-red-200 transition"
                              >
                                <Trash2 size={18} />
                              </button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

