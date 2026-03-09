import { useState } from "react";
import NodePalette from "../panels/NodePalette";
import ToolConfigPanel from "../panels/ToolConfigPanel";
import AgentConfigPanel from "../panels/AgentConfigPanel";
import HandoffPanel from "../panels/HandoffPanel";
import { ReactFlow, Controls } from "@xyflow/react";

function WorkflowBuilderPage({
  workflowName,
  setWorkflowName,
  workflowDescription,
  setWorkflowDescription,
  reactFlow,
  setView,
  workflowId,
  updateExistingWorkflow,
  saveNewWorkflow,
  isSaving,
  addAgentNode,
  nodesWithHandlers,
  edges,
  nodeTypes,
  onNodesChange,
  onEdgesChange,
  onConnect,
  onReconnect,
  onEdgeClick,
  onNodeClick,
  sidebarOpen,
  selectedTool,
  selectedAgent,
  selectedEdge,
  updateToolData,
  updateAgentData,
  updateEdgeData,
  deleteAgent,
  deleteEdge,
  initialAgentIdRef,
  statusMessage,
  onCloseSidebar,
  onSavePanel,
}) {
  const [paletteOpen, setPaletteOpen] = useState(true);
  const showSidebar =
    sidebarOpen && (selectedTool || selectedAgent || selectedEdge);
  const leftColWidth = paletteOpen ? "240px" : "40px";
  const gridTemplateColumns = `${leftColWidth} 1fr${
    showSidebar ? " 320px" : ""
  }`;

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "12px 16px",
          borderBottom: "1px solid #eee",
          background: "#fafafa",
        }}
      >
        <input
          value={workflowName}
          onChange={(e) => setWorkflowName(e.target.value)}
          placeholder="Workflow name"
          style={{
            flex: 1,
            padding: "10px 12px",
            borderRadius: 8,
            border: "1px solid #ddd",
          }}
        />
        <textarea
          value={workflowDescription}
          onChange={(e) => setWorkflowDescription(e.target.value)}
          placeholder="Short description"
          rows={1}
          style={{
            flex: 1,
            padding: "10px 12px",
            borderRadius: 8,
            border: "1px solid #ddd",
            resize: "vertical",
            minHeight: 42,
          }}
        />
        <button
          onClick={() => reactFlow.fitView()}
          style={{
            padding: "10px 12px",
            borderRadius: 8,
            border: "1px solid #ddd",
            background: "white",
            cursor: "pointer",
          }}
        >
          Fit View
        </button>
        <button
          onClick={() => setView("list")}
          style={{
            padding: "10px 12px",
            borderRadius: 8,
            border: "1px solid #ddd",
            background: "white",
            cursor: "pointer",
          }}
        >
          Back to List
        </button>
        <button
          onClick={workflowId ? updateExistingWorkflow : saveNewWorkflow}
          disabled={isSaving}
          style={{
            padding: "10px 14px",
            borderRadius: 8,
            border: "none",
            background: "#111",
            color: "white",
            cursor: "pointer",
            opacity: isSaving ? 0.7 : 1,
          }}
        >
          {workflowId ? "Update Workflow" : "Save Workflow"}
        </button>
      </div>

      <div
        style={{
          flex: 1,
          display: "grid",
          gridTemplateColumns,
          gap: 0,
          minHeight: 0,
        }}
      >
        <div
          style={{
            padding: paletteOpen ? 16 : 8,
            borderRight: "1px solid #eee",
            overflowY: "auto",
            position: "relative",
          }}
        >
          <button
            onClick={() => setPaletteOpen((v) => !v)}
            title={paletteOpen ? "Hide palette" : "Show palette"}
            style={{
              position: "absolute",
              top: 8,
              right: 8,
              width: 24,
              height: 24,
              borderRadius: 6,
              border: "1px solid #ddd",
              background: "white",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {paletteOpen ? "◀" : "▶"}
          </button>
          {paletteOpen ? (
            <NodePalette onAddAgent={addAgentNode} />
          ) : (
            <div style={{ width: 8 }} />
          )}
        </div>

        <div style={{ position: "relative" }}>
          <ReactFlow
            nodes={nodesWithHandlers}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onReconnect={onReconnect}
            onEdgeClick={onEdgeClick}
            onNodeClick={onNodeClick}
            fitView
            style={{ width: "100%", height: "100%" }}
          >
            <Controls />
          </ReactFlow>
        </div>

        {showSidebar ? (
          <div
            style={{
              padding: 16,
              marginRight: 16,
              borderLeft: "1px solid #eee",
              overflowY: "auto",
            }}
          >
            {selectedTool ? (
              <ToolConfigPanel
                tool={selectedTool}
                onChange={updateToolData}
                onSave={onSavePanel}
                onClose={onCloseSidebar}
              />
            ) : selectedAgent ? (
              <AgentConfigPanel
                agent={selectedAgent}
                onChange={updateAgentData}
                onDelete={deleteAgent}
                canDelete={selectedAgent.id !== initialAgentIdRef.current}
                onSave={onSavePanel}
                onClose={onCloseSidebar}
              />
            ) : selectedEdge ? (
              <HandoffPanel
                edge={selectedEdge}
                onChange={updateEdgeData}
                onDelete={deleteEdge}
                onSave={onSavePanel}
                onClose={onCloseSidebar}
              />
            ) : null}
          </div>
        ) : null}
      </div>

      {statusMessage && (
        <div
          style={{
            padding: "8px 16px",
            borderTop: "1px solid #eee",
            background: "#fafafa",
          }}
        >
          {statusMessage}
        </div>
      )}
    </div>
  );
}

export default WorkflowBuilderPage;
