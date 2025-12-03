import { useState, useEffect } from "react";
import { ArrowLeft, Calendar, DollarSign, ShoppingCart, TrendingUp } from "lucide-react";
import { managerAppController } from "../../services/ManagerAppController";
import * as Types from "../../types/index";

interface DailySalesSummaryProps {
  onBack: () => void;
}

export default function DailySalesSummary({ onBack }: DailySalesSummaryProps) {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [summary, setSummary] = useState<Types.DailySalesSummary | null>(null);

  useEffect(() => {
    loadSummary();
  }, [selectedDate]);

  const loadSummary = async () => {
    try {
      const date = new Date(selectedDate);
      const summaryData = await managerAppController.showDailySalesSummary(date);
      setSummary(summaryData);
    } catch (error) {
      console.error("Error loading sales summary:", error);
      // If API fails, show empty summary
      setSummary({
        date: selectedDate,
        totalRevenue: 0,
        numberOfOrders: 0,
        topSellingItems: [],
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={onBack}
            className="hover:bg-gray-200 p-2 rounded-lg transition"
          >
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-4xl font-bold text-gray-800">Daily Sales Summary</h1>
        </div>

        {/* Date Selector */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <label className="block text-sm font-semibold mb-2 flex items-center gap-2">
            <Calendar size={20} />
            Select Date
          </label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-red-500"
          />
        </div>

        {/* Summary Cards */}
        {summary && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Total Revenue</p>
                    <p className="text-3xl font-bold text-gray-800">
                      ${summary.totalRevenue.toFixed(2)}
                    </p>
                  </div>
                  <DollarSign size={40} className="text-green-600" />
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Number of Orders</p>
                    <p className="text-3xl font-bold text-gray-800">
                      {summary.numberOfOrders}
                    </p>
                  </div>
                  <ShoppingCart size={40} className="text-blue-600" />
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm mb-1">Average Order Value</p>
                    <p className="text-3xl font-bold text-gray-800">
                      ${summary.numberOfOrders > 0 
                        ? (summary.totalRevenue / summary.numberOfOrders).toFixed(2)
                        : "0.00"}
                    </p>
                  </div>
                  <TrendingUp size={40} className="text-purple-600" />
                </div>
              </div>
            </div>

            {/* Top Selling Items */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Top Selling Items</h2>
              {summary.topSellingItems.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <p>No sales data for this date</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {summary.topSellingItems.map((item, index) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center gap-4">
                        <span className="text-2xl font-bold text-red-600 w-8">
                          #{index + 1}
                        </span>
                        <div>
                          <h3 className="font-bold text-gray-800">{item.name}</h3>
                          <p className="text-sm text-gray-600">{item.category}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-gray-800">${item.price.toFixed(2)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

