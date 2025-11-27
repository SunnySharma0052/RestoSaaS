import { useEffect, useState } from "react";
import axios from "axios";
import { RefreshCcw, CheckCircle, Clock } from "lucide-react";

const API_URL = "http://127.0.0.1:8000";
const RESTAURANT_ID = 1;

function KitchenView({ token }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const res = await axios.get(
        `${API_URL}/api/staff/orders/${RESTAURANT_ID}/`,
        {
          headers: { Authorization: `Token ${token}` },
        }
      );
      setOrders(res.data);
    } catch (error) {
      console.error("Error fetching orders:", error);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (orderId, newStatus) => {
    try {
      await axios.patch(
        `${API_URL}/api/staff/order/${orderId}/update/`,
        { status: newStatus },
        { headers: { Authorization: `Token ${token}` } }
      );
      fetchOrders();
    } catch (error) {
      alert("Failed to update status");
    }
  };

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case "PENDING":
        return "bg-yellow-100 border-yellow-300";
      case "ACCEPTED":
        return "bg-blue-100 border-blue-300";
      case "PREPARING":
        return "bg-orange-100 border-orange-300";
      case "READY":
        return "bg-green-100 border-green-300";
      default:
        return "bg-gray-100";
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Live Orders</h2>
        <button
          onClick={fetchOrders}
          className="p-2 rounded-full hover:bg-gray-200 text-blue-600"
        >
          <RefreshCcw className={loading ? "animate-spin" : ""} />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {orders.map((order) => (
          <div
            key={order.id}
            className={`p-4 rounded-xl border-l-8 shadow-sm ${getStatusColor(
              order.status
            )} bg-white`}
          >
            <div className="flex justify-between items-start mb-4 border-b pb-2">
              <div>
                <h2 className="text-xl font-bold">
                  Table {order.table_number || "N/A"}
                </h2>
                <span className="text-xs text-gray-500">#{order.order_id}</span>
              </div>
              <span className="px-2 py-1 rounded text-xs font-bold bg-white border">
                {order.status}
              </span>
            </div>

            <div className="space-y-2 mb-4">
              {order.items.map((item, idx) => (
                <div key={idx} className="flex justify-between text-sm">
                  <span className="font-bold">
                    {item.quantity} x {item.item_id}
                  </span>{" "}
                  {/* Note: Ideally show item name */}
                </div>
              ))}
            </div>

            <div className="flex gap-2 mt-4 pt-2 border-t">
              {order.status === "PENDING" && (
                <button
                  onClick={() => updateStatus(order.id, "ACCEPTED")}
                  className="flex-1 bg-blue-600 text-white py-2 rounded font-bold"
                >
                  Accept
                </button>
              )}
              {order.status === "ACCEPTED" && (
                <button
                  onClick={() => updateStatus(order.id, "PREPARING")}
                  className="flex-1 bg-orange-600 text-white py-2 rounded font-bold"
                >
                  Cook
                </button>
              )}
              {order.status === "PREPARING" && (
                <button
                  onClick={() => updateStatus(order.id, "READY")}
                  className="flex-1 bg-green-600 text-white py-2 rounded font-bold"
                >
                  Ready
                </button>
              )}
              {order.status === "READY" && (
                <button
                  onClick={() => updateStatus(order.id, "COMPLETED")}
                  className="flex-1 bg-gray-800 text-white py-2 rounded font-bold flex justify-center gap-2"
                >
                  <CheckCircle size={18} /> Serve
                </button>
              )}
            </div>
          </div>
        ))}
        {orders.length === 0 && (
          <p className="text-gray-400">No active orders.</p>
        )}
      </div>
    </div>
  );
}

export default KitchenView;
