import { useEffect, useState } from "react";
import axios from "axios";
import { Search, Edit2, Check, X } from "lucide-react";

const API_URL = "http://127.0.0.1:8000";
const RESTAURANT_ID = 1;

function MenuManage({ token }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  // Items Fetch karna
  const fetchItems = async () => {
    try {
      const res = await axios.get(
        `${API_URL}/api/manager/menu/${RESTAURANT_ID}/`,
        {
          headers: { Authorization: `Token ${token}` },
        }
      );
      setItems(res.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching menu:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [token]);

  // Stock Toggle karna (Available <-> Out of Stock)
  const toggleStock = async (id, currentStatus) => {
    try {
      // Optimistic UI Update (Turant screen par change dikhao)
      const updatedItems = items.map((item) =>
        item.id === id ? { ...item, is_available: !currentStatus } : item
      );
      setItems(updatedItems);

      // Backend Update
      await axios.patch(
        `${API_URL}/api/manager/item/${id}/update/`,
        { is_available: !currentStatus },
        { headers: { Authorization: `Token ${token}` } }
      );
    } catch (error) {
      alert("Failed to update stock");
      fetchItems(); // Error aaye to wapas purana data lao
    }
  };

  // Filter Items based on search
  const filteredItems = items.filter((item) =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <div className="p-10">Loading Menu...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Menu Management</h2>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search food..."
            className="pl-10 pr-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 text-gray-500 text-sm uppercase">
            <tr>
              <th className="p-4">Item Name</th>
              <th className="p-4">Price</th>
              <th className="p-4">Status</th>
              <th className="p-4 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredItems.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50 transition">
                <td className="p-4 font-medium text-gray-800">{item.name}</td>
                <td className="p-4 text-gray-600">₹{item.price}</td>
                <td className="p-4">
                  {item.is_available ? (
                    <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold">
                      In Stock
                    </span>
                  ) : (
                    <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-bold">
                      Out of Stock
                    </span>
                  )}
                </td>
                <td className="p-4 text-center">
                  <button
                    onClick={() => toggleStock(item.id, item.is_available)}
                    className={`px-4 py-2 rounded-lg text-sm font-bold transition ${
                      item.is_available
                        ? "bg-red-50 text-red-600 hover:bg-red-100"
                        : "bg-green-50 text-green-600 hover:bg-green-100"
                    }`}
                  >
                    {item.is_available ? "Mark Out of Stock" : "Mark In Stock"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredItems.length === 0 && (
          <div className="p-8 text-center text-gray-400">No items found</div>
        )}
      </div>
    </div>
  );
}

export default MenuManage;
