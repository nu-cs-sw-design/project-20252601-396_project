import { useState } from "react";
import ManagementDashboard from "../components/manager/ManagementDashboard";
import MenuManagement from "../components/manager/MenuManagement";
import DailySalesSummary from "../components/manager/DailySalesSummary";

type ViewMode = "dashboard" | "menu" | "reports";

export default function ManagerUI() {
  const [viewMode, setViewMode] = useState<ViewMode>("dashboard");

  const handleNavigateToMenu = () => {
    setViewMode("menu");
  };

  const handleNavigateToReports = () => {
    setViewMode("reports");
  };

  const handleBackToDashboard = () => {
    setViewMode("dashboard");
  };

  function renderView() {
    switch (viewMode) {
      case "dashboard":
        return (
          <ManagementDashboard
            onNavigateToMenu={handleNavigateToMenu}
            onNavigateToReports={handleNavigateToReports}
          />
        );
      case "menu":
        return <MenuManagement onBack={handleBackToDashboard} />;
      case "reports":
        return <DailySalesSummary onBack={handleBackToDashboard} />;
      default:
        return null;
    }
  }

  return <div>{renderView()}</div>;
}
