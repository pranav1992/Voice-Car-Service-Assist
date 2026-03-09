import React from "react";

// Presentational list view for workflows. Expects handlers and data from parent.
function CreateWorkFlowPage({
  startNewWorkflow,
  isLoadingList,
  workflowList,
  handleOpenWorkflow,
  handleDeleteWorkflow,
}) {
  return (
    <div style={{ padding: 24 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2 style={{ margin: 0 }}>Workflows</h2>
        <button
          onClick={startNewWorkflow}
          style={{
            padding: "10px 14px",
            borderRadius: 8,
            border: "none",
            background: "#111",
            color: "white",
            cursor: "pointer",
          }}
        >
          + New Workflow
        </button>
      </div>

      <div style={{ marginTop: 16 }}>
        {isLoadingList ? (
          <div>Loading workflows…</div>
        ) : workflowList.length === 0 ? (
          <div>No workflows yet. Create one to get started.</div>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
              gap: 12,
            }}
          >
            {workflowList.map((wf) => (
              <div
                key={wf.id}
                style={{
                  border: "1px solid #eee",
                  borderRadius: 10,
                  padding: 12,
                  boxShadow: "0 6px 14px rgba(0,0,0,0.05)",
                  background: "white",
                }}
              >
                <div style={{ fontWeight: 600 }}>{wf.name || "Untitled"}</div>
                <div style={{ fontSize: 12, color: "#666", margin: "4px 0" }}>
                  id: {wf.id} {wf.version ? `• v${wf.version}` : ""}
                </div>
                <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
                  <button
                    onClick={() => handleOpenWorkflow(wf.id)}
                    style={{
                      flex: 1,
                      padding: "8px 10px",
                      borderRadius: 6,
                      border: "1px solid #111",
                      background: "white",
                      cursor: "pointer",
                    }}
                  >
                    Open
                  </button>
                  <button
                    onClick={() => handleDeleteWorkflow(wf.id)}
                    style={{
                      padding: "8px 10px",
                      borderRadius: 6,
                      border: "1px solid #e33",
                      background: "#ffecec",
                      color: "#c00",
                      cursor: "pointer",
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default CreateWorkFlowPage;
