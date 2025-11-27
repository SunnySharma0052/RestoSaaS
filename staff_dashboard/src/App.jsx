import { useState } from "react";
import {
  ChefHat,
  LayoutDashboard,
  LogOut,
  UtensilsCrossed,
  Menu as MenuIcon,
} from "lucide-react"; // MenuIcon import kiya
import Login from "./Login";
import KitchenView from "./KitchenView";
import ManagerView from "./ManagerView";
import MenuManage from "./MenuManage"; // Import kiya

function App() {
  const [token, setToken] = useState(localStorage.getItem("staffToken"));
  // New view state: 'menu_manage'
  const [currentView, setCurrentView] = useState("kitchen");

  const handleLogout = () => {
    localStorage.removeItem("staffToken");
    setToken(null);
  };

  if (!token) {
    return <Login onLogin={(newToken) => setToken(newToken)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* SIDEBAR */}
      <div className="w-64 bg-white border-r flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-orange-600 flex items-center gap-2">
            <ChefHat /> RestoSaaS
          </h1>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <div className="text-xs font-bold text-gray-400 uppercase ml-4 mb-2">
            Operations
          </div>

          <button
            onClick={() => setCurrentView("kitchen")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition ${
              currentView === "kitchen"
                ? "bg-orange-50 text-orange-600"
                : "text-gray-600 hover:bg-gray-100"
            }`}
          >
            <UtensilsCrossed size={20} /> Kitchen View
          </button>

          <div className="text-xs font-bold text-gray-400 uppercase ml-4 mt-6 mb-2">
            Management
          </div>

          <button
            onClick={() => setCurrentView("manager")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition ${
              currentView === "manager"
                ? "bg-orange-50 text-orange-600"
                : "text-gray-600 hover:bg-gray-100"
            }`}
          >
            <LayoutDashboard size={20} /> Analytics
          </button>

          {/* New Button */}
          <button
            onClick={() => setCurrentView("menu_manage")}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition ${
              currentView === "menu_manage"
                ? "bg-orange-50 text-orange-600"
                : "text-gray-600 hover:bg-gray-100"
            }`}
          >
            <MenuIcon size={20} /> Menu Items
          </button>
        </nav>

        <div className="p-4 border-t">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-xl font-medium"
          >
            <LogOut size={20} /> Logout
          </button>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto">
        <header className="bg-white border-b p-4 px-8 flex justify-between items-center sticky top-0 z-10">
          <h2 className="text-xl font-bold text-gray-800 capitalize">
            {currentView.replace("_", " ")}
          </h2>
          <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-500 font-bold">
            M
          </div>
        </header>

        <main>
          {currentView === "kitchen" && <KitchenView token={token} />}
          {currentView === "manager" && <ManagerView token={token} />}
          {currentView === "menu_manage" && <MenuManage token={token} />}
        </main>
      </div>
    </div>
  );
}

export default App;
