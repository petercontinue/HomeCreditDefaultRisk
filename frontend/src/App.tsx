import { Navigate, Route, Routes } from "react-router-dom";
import { AppHeader } from "./components/AppHeader";
import { ApplyPage } from "./pages/ApplyPage";
import { HomePage } from "./pages/HomePage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { ResultPage } from "./pages/ResultPage";
import "./App.css";

export default function App() {
  return (
    <div className="app-shell">
      <div className="bg-layer" aria-hidden />
      <AppHeader />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/apply" element={<ApplyPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/result/:id" element={<ResultPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
