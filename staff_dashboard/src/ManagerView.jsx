import { useEffect, useState } from "react";
import axios from "axios";
import {
  TrendingUp,
  DollarSign,
  ShoppingBag,
  AlertTriangle,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";
// Note: Agar aapka restaurant ID 2 hai to ise 2 karein
const RESTAURANT_ID = 1;

function ManagerView({ token }) {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios
      .get(`${API_URL}/api/manager/stats/${RESTAURANT_ID}/`, {
        headers: { Authorization: `Token ${token}` },
      })
      .then((res) => {
        setStats(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("API Error:", err);
        // Error message set karein
        setError(err.response?.data?.error || err.message);
        setLoading(false);
      });
  }, [token]);

  if (loading)
    return (
      <div className="p-10 text-gray-500">
        Loading Stats... (Check Backend Terminal)
      </div>
    );

  // Error Screen
  if (error)
    return (
      <div className="p-10 text-red-500 flex flex-col items-center">
        <AlertTriangle size={48} className="mb-2" />
        <h3 className="font-bold text-xl">Error Loading Dashboard</h3>
        <p className="font-mono bg-red-50 p-2 mt-2 rounded">{error}</p>
      </div>
    );

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Business Overview
      </h2>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 text-green-600 rounded-full">
              <DollarSign />
            </div>
            <div>
              <p className="text-sm text-gray-500">Today's Revenue</p>
              <h3 className="text-2xl font-bold">₹{stats.today_revenue}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 text-blue-600 rounded-full">
              <ShoppingBag />
            </div>
            <div>
              <p className="text-sm text-gray-500">Total Orders</p>
              <h3 className="text-2xl font-bold">{stats.total_orders}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-orange-100 text-orange-600 rounded-full">
              <TrendingUp />
            </div>
            <div>
              <p className="text-sm text-gray-500">Best Seller</p>
              <h3 className="text-xl font-bold truncate w-32">
                {stats.top_items.length > 0
                  ? stats.top_items[0].item__name
                  : "N/A"}
              </h3>
            </div>
          </div>
        </div>
      </div>

      {/* Top Items Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="font-bold text-gray-700 mb-4">Top Selling Items</h3>
        <table className="w-full text-left">
          <thead>
            <tr className="border-b text-gray-400 text-sm">
              <th className="py-2">Item Name</th>
              <th className="py-2">Orders Count</th>
            </tr>
          </thead>
          <tbody>
            {stats.top_items.length > 0 ? (
              stats.top_items.map((item, idx) => (
                <tr key={idx} className="border-b last:border-0">
                  <td className="py-3 font-medium text-gray-700">
                    {item.item__name}
                  </td>
                  <td className="py-3 text-gray-500">{item.count} orders</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2" className="py-4 text-center text-gray-400">
                  No sales yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ManagerView;
