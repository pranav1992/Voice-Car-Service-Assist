import { Routes, Route } from "react-router";
import WorkflowBuilderPage from "./pages/workflowBuilderPage";
import CreateWorkFlowPage from "./pages/createWorkFlowPage";
import PageNotFound from "./pages/pageNotFound";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<CreateWorkFlowPage/>} />
      <Route path="/workflows/:workflowId" element={<WorkflowBuilderPage />} />
      <Route path="*" element={<PageNotFound />} />
    </Routes>
  );
}



