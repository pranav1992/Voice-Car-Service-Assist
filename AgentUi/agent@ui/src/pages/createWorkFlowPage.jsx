import CreateWorkflowDialog from "../components/createWorkflowDialog";

import {
  createWorkflow,
  updateWorkflow,
  getWorkflows,
  deleteWorkflow,
  getWorkflow,
} from "../api/workflow";
import { useState, useCallback, useEffect } from "react";
// Presentational list view for workflows. Expects handlers and data from parent.
function CreateWorkFlowPage() {
  const [showNewDialog, setShowNewDialog] = useState(false);
  const [newNameInput, setNewNameInput] = useState("");
  const [newDescInput, setNewDescInput] = useState("");
  const [isLoadingList, setIsLoadingList] = useState(false);
  const [workflowList, setWorkflowList] = useState([]);
  const [workflowId, setWorkflowId] = useState("");
  const [workflowName, setWorkflowName] = useState("My workflow");
  const [workflowDescription, setWorkflowDescription] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  const fetchWorkflowList = useCallback(async () => {
    setIsLoadingList(true);
    try {
      console.log("fetchWorkflowList")
      const data = await getWorkflows();
      const list = Array.isArray(data)
        ? data
        : Array.isArray(data?.data)
          ? data.data
          : [];
      console.log(list)
      setWorkflowList(list);
    } catch (err) {
      console.error(err);
      setStatusMessage(
        err.response?.data?.detail ||
          err.message ||
          "Failed to load workflows.",
      );
    } finally {
      setIsLoadingList(false);
    }
  }, []);

  useEffect(() => {
    fetchWorkflowList();
  }, [fetchWorkflowList]);


  // const loadWorkflowIntoCanvas = useCallback((payload) => {
  //   if (!payload?.nodes) return;
  //   // reconstruct agents and tools
  //   const agentNodes = [];
  //   const toolNodes = [];
  //   const edgesFromTools = [];

  //   payload.nodes.forEach((n) => {
  //     const { tools = [], ...restData } = n.data || {};
  //     agentNodes.push({
  //       ...n,
  //       data: {
  //         ...restData,
  //         type: "agent",
  //       },
  //     });
  //     tools.forEach((t) => {
  //       const toolId = t.id || crypto.randomUUID();
  //       toolNodes.push({
  //         id: toolId,
  //         type: "tool",
  //         position: { x: n.position?.x || 0, y: (n.position?.y || 0) + 150 },
  //         data: t.data || {},
  //       });
  //       edgesFromTools.push({
  //         id: `${toolId}-${n.id}`,
  //         source: toolId,
  //         target: n.id,
  //         targetHandle: "tools",
  //       });
  //     });
  //   });

  //   const filteredEdges =
  //     payload.edges?.filter(
  //       (e) =>
  //         agentNodes.find((a) => a.id === e.source) &&
  //         agentNodes.find((a) => a.id === e.target),
  //     ) || [];

  //   setNodes([...agentNodes, ...toolNodes]);
  //   setEdges([...filteredEdges, ...edgesFromTools]);
  // }, []);

  // const handleOpenWorkflow = useCallback(
  //   async (id) => {
  //     try {
  //       const wf = await getWorkflow(id);
  //       setWorkflowId(String(wf.id));
  //       setWorkflowName(wf.name || "Untitled");
  //       setWorkflowDescription(wf.payload?.meta?.description || "");
  //       loadWorkflowIntoCanvas(wf.payload);
  //       setView("builder");
  //       setStatusMessage(`Opened workflow "${wf.name}"`);
  //     } catch (err) {
  //       console.error(err);
  //       setStatusMessage(
  //         err.response?.data?.detail ||
  //           err.message ||
  //           "Failed to open workflow.",
  //       );
  //     }
  //   },
  //   [loadWorkflowIntoCanvas],
  // );

  // const handleDeleteWorkflow = useCallback(
  //   async (id) => {
  //     if (!confirm("Delete this workflow permanently?")) return;
  //     try {
  //       await deleteWorkflow(id);
  //       setStatusMessage("Workflow deleted.");
  //       fetchWorkflowList();
  //     } catch (err) {
  //       console.error(err);
  //       setStatusMessage(
  //         err.response?.data?.detail || err.message || "Failed to delete.",
  //       );
  //     }
  //   },
  //   [fetchWorkflowList],
  // );


  // const saveNewWorkflow = useCallback(async () => {
  //   const name = workflowName.trim();
  //   if (!name) {
  //     setStatusMessage("Please enter a workflow name before saving.");
  //     return;
  //   }
  //   const taken = workflowList.some(
  //     (wf) => wf.name?.toLowerCase() === name.toLowerCase(),
  //   );
  //   if (taken) {
  //     setStatusMessage(
  //       "Workflow name already exists. Choose a different name.",
  //     );
  //     return;
  //   }
  //   setIsSaving(true);
  //   try {
  //     const payload = serializeWorkflow();
  //     const res = await createWorkflow({ name, payload });
  //     setWorkflowId(res.id);
  //     setStatusMessage(`Saved new workflow "${name}" (id: ${res.id}).`);
  //     setView("list");
  //     fetchWorkflowList();
  //   } catch (err) {
  //     console.error(err);
  //     setStatusMessage(
  //       err.response?.data?.detail || err.message || "Failed to save.",
  //     );
  //   } finally {
  //     setIsSaving(false);
  //   }
  // }, [serializeWorkflow, workflowName]);

  // const updateExistingWorkflow = useCallback(async () => {
  //   const name = workflowName.trim();
  //   if (!name) {
  //     setStatusMessage("Please enter a workflow name before updating.");
  //     return;
  //   }
  //   if (!workflowId) {
  //     setStatusMessage("Provide a workflow ID to update.");
  //     return;
  //   }
  //   const taken = workflowList.some(
  //     (wf) =>
  //       String(wf.id) !== String(workflowId) &&
  //       wf.name?.toLowerCase() === name.toLowerCase(),
  //   );
  //   if (taken) {
  //     setStatusMessage("Another workflow already uses this name.");
  //     return;
  //   }
  //   setIsSaving(true);
  //   try {
  //     const payload = serializeWorkflow();
  //     const res = await updateWorkflow(workflowId, { name, payload });
  //     setStatusMessage(`Updated workflow "${res.name}" (id: ${res.id}).`);
  //     setView("list");
  //     fetchWorkflowList();
  //   } catch (err) {
  //     console.error(err);
  //     setStatusMessage(
  //       err.response?.data?.detail || err.message || "Failed to update.",
  //     );
  //   } finally {
  //     setIsSaving(false);
  //   }
  // }, [serializeWorkflow, workflowId, workflowName]);

  const startNewWorkflow = useCallback(() => {
    setNewNameInput("");
    setNewDescInput("");
    setShowNewDialog(true);
  }, []);

  // const confirmNewWorkflow = ()=>{showNewDialog(false)}

  const confirmNewWorkflow = useCallback(() => {
    const name = (newNameInput || "").trim();
    if (!name) {
      setStatusMessage("Workflow name is required.");
      return;
    }
    const taken = workflowList.some(
      (wf) => wf.name?.toLowerCase() === name.toLowerCase(),
    );
    if (taken) {
      setStatusMessage("Workflow name already exists. Pick a different name.");
      return;
    }
    console.log(name)
    setStatusMessage("");
    setWorkflowName(name);
    setWorkflowDescription(newDescInput.trim());
    setNodes([
      {
        id: initialAgentIdRef.current,
        position: { x: 0, y: 0 },
        type: "agent",
        data: { ...DEFAULT_AGENT_DATA },
      },
    ]);
    setEdges([]);
    setWorkflowId("");
    setSidebarOpen(false);
    setView("builder");
    setStatusMessage(`Started new workflow "${name}".`);
    setShowNewDialog(false);
  }, [newDescInput, newNameInput, workflowName]);

  const renderNewDialog = () =>
    showNewDialog ? (
      <CreateWorkflowDialog
        setShowNewDialog={setShowNewDialog}
        newNameInput={newNameInput}
        setNewNameInput={setNewNameInput}
        newDescInput={newDescInput}
        setNewDescInput={setNewDescInput}
        confirmNewWorkflow={confirmNewWorkflow}
      />
    ) : null;

  return (
    <>
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
            onClick={
              ()=> startNewWorkflow()
            }
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
                      onClick={() => {}
                        // handleOpenWorkflow(wf.id)
                      }
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
                      onClick={() =>{}
                        //  handleDeleteWorkflow(wf.id)
                        }
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
      {renderNewDialog()}
    </>
  );
}

export default CreateWorkFlowPage;
