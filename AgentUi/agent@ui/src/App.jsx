import { useCallback, useEffect, useRef, useState } from "react";
import {
  useReactFlow,
  applyEdgeChanges,
  applyNodeChanges,
  addEdge,
  reconnectEdge,
  ReactFlowProvider,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

import AgentNode from "./components/AgentNode";
import ToolNode from "./components/ToolNode";
import {
  DEFAULT_AGENT_DATA,
  DEFAULT_HANDOFF_DATA,
  DEFAULT_TOOL_DATA,
} from "./constants";
import {
  createWorkflow,
  updateWorkflow,
  getWorkflows,
  deleteWorkflow,
  getWorkflow,
} from "./api/workflow";
import CreateWorkflowDialog from "./components/createWorkflowDialog";
import CreateWorkFlowPage from "./pages/createWorkFlowPage";
import WorkflowBuilderPage from "./pages/workflowBuilderPage";

const nodeTypes = { agent: AgentNode, tool: ToolNode };

function FlowCanvas() {
  const reactFlow = useReactFlow();

  // keep track of the first agent so it can't be deleted
  const initialAgentIdRef = useRef(crypto.randomUUID());

  const [nodes, setNodes] = useState([
    {
      id: initialAgentIdRef.current,
      position: { x: 0, y: 0 },
      type: "agent",
      data: { ...DEFAULT_AGENT_DATA },
    },
  ]);
  const [edges, setEdges] = useState([]);

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedToolId, setSelectedToolId] = useState(null);
  const [selectedAgentId, setSelectedAgentId] = useState(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState(null);
  const [workflowName, setWorkflowName] = useState("My workflow");
  const [workflowId, setWorkflowId] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [view, setView] = useState("list"); // "list" | "builder"
  const [workflowList, setWorkflowList] = useState([]);
  const [isLoadingList, setIsLoadingList] = useState(false);
  const [workflowDescription, setWorkflowDescription] = useState("");
  const [showNewDialog, setShowNewDialog] = useState(false);
  const [newNameInput, setNewNameInput] = useState("");
  const [newDescInput, setNewDescInput] = useState("");

  const clearSelection = useCallback(() => {
    setSelectedToolId(null);
    setSelectedAgentId(null);
    setSelectedEdgeId(null);
  }, []);

  const closeSidebar = useCallback(() => {
    clearSelection();
    setSidebarOpen(false);
  }, [clearSelection]);

  const saveAndCloseSidebar = useCallback(() => {
    setSidebarOpen(false);
    clearSelection();
  }, [clearSelection]);

  const openAgentConfig = useCallback((agentId) => {
    setSelectedAgentId(agentId);
    setSelectedToolId(null);
    setSelectedEdgeId(null);
    setSidebarOpen(true);
  }, []);

  const nodesWithHandlers = nodes.map((n) => ({
    ...n,
    data: {
      ...n.data,
      addNode,
      addToolNode,
      openAgentConfig,
      isInitial: n.id === initialAgentIdRef.current,
    },
  }));

  const selectedTool = nodes.find((n) => n.id === selectedToolId);
  const selectedAgent = nodes.find((n) => n.id === selectedAgentId);
  const selectedEdge = edges.find((e) => e.id === selectedEdgeId);

  const onNodesChange = useCallback(
    (changes) =>
      setNodes((nds) =>
        applyNodeChanges(
          changes.filter(
            (change) =>
              !(
                change.type === "remove" &&
                change.id === initialAgentIdRef.current
              ),
          ),
          nds,
        ),
      ),
    [],
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [],
  );

  const isValidConnection = useCallback(
    (connection) => {
      const sourceNode = nodes.find((n) => n.id === connection.source);
      const targetNode = nodes.find((n) => n.id === connection.target);
      return sourceNode?.type === "agent" && targetNode?.type === "agent";
    },
    [nodes],
  );

  const onConnect = useCallback(
    (params) => {
      if (!isValidConnection(params)) return;
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            data: { ...DEFAULT_HANDOFF_DATA },
          },
          eds,
        ),
      );
    },
    [isValidConnection],
  );

  const onReconnect = useCallback((oldEdge, newConnection) => {
    setEdges((eds) => {
      const updated = reconnectEdge(oldEdge, newConnection, eds);
      return updated.map((e) =>
        e.id === oldEdge.id
          ? { ...e, data: oldEdge.data ?? DEFAULT_HANDOFF_DATA }
          : e,
      );
    });
  }, []);

  const onEdgeClick = useCallback(
    (_, edge) => {
      const sourceNode = nodes.find((n) => n.id === edge.source);
      const targetNode = nodes.find((n) => n.id === edge.target);
      if (sourceNode?.type === "agent" && targetNode?.type === "agent") {
        setSelectedEdgeId(edge.id);
        setSelectedToolId(null);
        setSelectedAgentId(null);
        setSidebarOpen(true);
      }
    },
    [nodes],
  );

  const onNodeClick = useCallback((_, node) => {
    if (node.type === "tool") {
      setSelectedToolId(node.id);
      setSelectedAgentId(null);
      setSelectedEdgeId(null);
      setSidebarOpen(true);
    }
  }, []);

  function addAgentNode() {
    const newNode = {
      id: crypto.randomUUID(),
      type: "agent",
      position: {
        x: 200 + Math.random() * 200,
        y: 200 + Math.random() * 200,
      },
      data: { ...DEFAULT_AGENT_DATA },
    };
    setNodes((nds) => [...nds, newNode]);
    setSidebarOpen(false);
  }

  function addToolNode(agentId) {
    const agent = nodes.find((n) => n.id === agentId);
    if (!agent) return;

    const toolId = crypto.randomUUID();
    const toolNode = {
      id: toolId,
      type: "tool",
      position: { x: agent.position.x, y: agent.position.y + 150 },
      data: { ...DEFAULT_TOOL_DATA },
    };
    const edge = {
      id: `${toolId}-${agentId}`,
      source: toolId,
      target: agentId,
      targetHandle: "tools",
    };

    setNodes((nds) => [...nds, toolNode]);
    setEdges((eds) => [...eds, edge]);
  }

  function addNode(sourceId) {
    const newId = crypto.randomUUID();
    const newAgent = {
      id: newId,
      type: "agent",
      position: { x: 400, y: 200 },
      data: { ...DEFAULT_AGENT_DATA },
    };

    const newEdge = {
      id: `${sourceId}-${newId}`,
      source: sourceId,
      target: newId,
      sourceHandle: "next",
      targetHandle: "prev",
      data: { ...DEFAULT_HANDOFF_DATA },
    };

    setNodes((nds) => [...nds, newAgent]);
    setEdges((eds) => [...eds, newEdge]);
  }

  const updateToolData = useCallback((toolId, updates) => {
    setNodes((nds) =>
      nds.map((n) =>
        n.id === toolId ? { ...n, data: { ...n.data, ...updates } } : n,
      ),
    );
  }, []);

  const updateAgentData = useCallback((agentId, updates) => {
    setNodes((nds) =>
      nds.map((n) =>
        n.id === agentId ? { ...n, data: { ...n.data, ...updates } } : n,
      ),
    );
  }, []);

  const updateEdgeData = useCallback((edgeId, updates) => {
    setEdges((eds) =>
      eds.map((e) =>
        e.id === edgeId ? { ...e, data: { ...e.data, ...updates } } : e,
      ),
    );
  }, []);

  const deleteEdge = useCallback((edgeId) => {
    setEdges((eds) => eds.filter((e) => e.id !== edgeId));
    setSelectedEdgeId(null);
    setSidebarOpen(false);
  }, []);

  const deleteAgent = useCallback((agentId) => {
    if (agentId === initialAgentIdRef.current) return;

    setNodes((nds) => nds.filter((n) => n.id !== agentId));
    setEdges((eds) =>
      eds.filter((e) => e.source !== agentId && e.target !== agentId),
    );
    setSelectedAgentId(null);
    setSidebarOpen(false);
  }, []);

  const serializeWorkflow = useCallback(() => {
    const nodeById = Object.fromEntries(nodes.map((n) => [n.id, n]));

    // helper to strip functions from data
    const cleanData = (data = {}) =>
      Object.fromEntries(
        Object.entries(data).filter(([, value]) => typeof value !== "function"),
      );

    // group tool nodes that are connected to an agent via the "tools" handle
    const agentToolsMap = {};
    edges.forEach((e) => {
      const sourceNode = nodeById[e.source];
      const targetNode = nodeById[e.target];
      if (sourceNode?.type === "tool" && targetNode?.type === "agent") {
        if (!agentToolsMap[targetNode.id]) agentToolsMap[targetNode.id] = [];
        agentToolsMap[targetNode.id].push({
          id: sourceNode.id,
          type: sourceNode.type,
          data: cleanData(sourceNode.data),
        });
      }
    });

    // build serialized nodes: agents with embedded tools, plus any non-tool nodes
    const serializedNodes = nodes
      .filter((n) => n.type !== "tool") // tools are nested under their agent
      .map(({ data, ...rest }) => ({
        ...rest,
        data: {
          ...cleanData(data),
          type: rest.type,
          tools: agentToolsMap[rest.id] || [],
        },
      }));

    // keep edges that do not involve nested tool nodes and add type + cleaned data
    const serializedEdges = edges
      .filter((e) => {
        const sourceNode = nodeById[e.source];
        const targetNode = nodeById[e.target];
        return sourceNode?.type !== "tool" && targetNode?.type !== "tool";
      })
      .map((e) => ({
        ...e,
        type: e.type || "default",
        data: cleanData(e.data),
      }));

    const meta = {};
    if (workflowDescription.trim())
      meta.description = workflowDescription.trim();

    return {
      ...(Object.keys(meta).length ? { meta } : {}),
      nodes: serializedNodes,
      edges: serializedEdges,
    };
  }, [nodes, edges, workflowDescription]);

  const loadWorkflowIntoCanvas = useCallback((payload) => {
    if (!payload?.nodes) return;
    // reconstruct agents and tools
    const agentNodes = [];
    const toolNodes = [];
    const edgesFromTools = [];

    payload.nodes.forEach((n) => {
      const { tools = [], ...restData } = n.data || {};
      agentNodes.push({
        ...n,
        data: {
          ...restData,
          type: "agent",
        },
      });
      tools.forEach((t) => {
        const toolId = t.id || crypto.randomUUID();
        toolNodes.push({
          id: toolId,
          type: "tool",
          position: { x: n.position?.x || 0, y: (n.position?.y || 0) + 150 },
          data: t.data || {},
        });
        edgesFromTools.push({
          id: `${toolId}-${n.id}`,
          source: toolId,
          target: n.id,
          targetHandle: "tools",
        });
      });
    });

    const filteredEdges =
      payload.edges?.filter(
        (e) =>
          agentNodes.find((a) => a.id === e.source) &&
          agentNodes.find((a) => a.id === e.target),
      ) || [];

    setNodes([...agentNodes, ...toolNodes]);
    setEdges([...filteredEdges, ...edgesFromTools]);
  }, []);

  const saveNewWorkflow = useCallback(async () => {
    const name = workflowName.trim();
    if (!name) {
      setStatusMessage("Please enter a workflow name before saving.");
      return;
    }
    const taken = workflowList.some(
      (wf) => wf.name?.toLowerCase() === name.toLowerCase(),
    );
    if (taken) {
      setStatusMessage(
        "Workflow name already exists. Choose a different name.",
      );
      return;
    }
    setIsSaving(true);
    try {
      const payload = serializeWorkflow();
      const res = await createWorkflow({ name, payload });
      setWorkflowId(res.id);
      setStatusMessage(`Saved new workflow "${name}" (id: ${res.id}).`);
      setView("list");
      fetchWorkflowList();
    } catch (err) {
      console.error(err);
      setStatusMessage(
        err.response?.data?.detail || err.message || "Failed to save.",
      );
    } finally {
      setIsSaving(false);
    }
  }, [serializeWorkflow, workflowName]);

  const updateExistingWorkflow = useCallback(async () => {
    const name = workflowName.trim();
    if (!name) {
      setStatusMessage("Please enter a workflow name before updating.");
      return;
    }
    if (!workflowId) {
      setStatusMessage("Provide a workflow ID to update.");
      return;
    }
    const taken = workflowList.some(
      (wf) =>
        String(wf.id) !== String(workflowId) &&
        wf.name?.toLowerCase() === name.toLowerCase(),
    );
    if (taken) {
      setStatusMessage("Another workflow already uses this name.");
      return;
    }
    setIsSaving(true);
    try {
      const payload = serializeWorkflow();
      const res = await updateWorkflow(workflowId, { name, payload });
      setStatusMessage(`Updated workflow "${res.name}" (id: ${res.id}).`);
      setView("list");
      fetchWorkflowList();
    } catch (err) {
      console.error(err);
      setStatusMessage(
        err.response?.data?.detail || err.message || "Failed to update.",
      );
    } finally {
      setIsSaving(false);
    }
  }, [serializeWorkflow, workflowId, workflowName]);

  const fetchWorkflowList = useCallback(async () => {
    setIsLoadingList(true);
    try {
      const data = await getWorkflows();
      const list = Array.isArray(data)
        ? data
        : Array.isArray(data?.data)
          ? data.data
          : [];
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

  const handleOpenWorkflow = useCallback(
    async (id) => {
      try {
        const wf = await getWorkflow(id);
        setWorkflowId(String(wf.id));
        setWorkflowName(wf.name || "Untitled");
        setWorkflowDescription(wf.payload?.meta?.description || "");
        loadWorkflowIntoCanvas(wf.payload);
        setView("builder");
        setStatusMessage(`Opened workflow "${wf.name}"`);
      } catch (err) {
        console.error(err);
        setStatusMessage(
          err.response?.data?.detail ||
            err.message ||
            "Failed to open workflow.",
        );
      }
    },
    [loadWorkflowIntoCanvas],
  );

  const handleDeleteWorkflow = useCallback(
    async (id) => {
      if (!confirm("Delete this workflow permanently?")) return;
      try {
        await deleteWorkflow(id);
        setStatusMessage("Workflow deleted.");
        fetchWorkflowList();
      } catch (err) {
        console.error(err);
        setStatusMessage(
          err.response?.data?.detail || err.message || "Failed to delete.",
        );
      }
    },
    [fetchWorkflowList],
  );

  const startNewWorkflow = useCallback(() => {
    setNewNameInput("");
    setNewDescInput("");
    setShowNewDialog(true);
  }, []);

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

  const renderBuilder = () => (
    <WorkflowBuilderPage 
      workflowName={workflowName}
      setWorkflowName={setWorkflowName}
      workflowDescription={workflowDescription}
      setWorkflowDescription={setWorkflowDescription}
      reactFlow={reactFlow}
      setView={setView}
      workflowId={workflowId}
      updateExistingWorkflow={updateExistingWorkflow}
      saveNewWorkflow={saveNewWorkflow}
      isSaving={isSaving}
      addAgentNode={addAgentNode}
      nodesWithHandlers={nodesWithHandlers}
      edges={edges}
      nodeTypes={nodeTypes}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      onReconnect={onReconnect}
      onEdgeClick={onEdgeClick}
      onNodeClick={onNodeClick}
      sidebarOpen={sidebarOpen}
      selectedTool={selectedTool}
      selectedAgent={selectedAgent}
      selectedEdge={selectedEdge}
      updateToolData={updateToolData}
      updateAgentData={updateAgentData}
      updateEdgeData={updateEdgeData}
      deleteAgent={deleteAgent}
      deleteEdge={deleteEdge}
      initialAgentIdRef={initialAgentIdRef}
      statusMessage={statusMessage}
      onCloseSidebar={closeSidebar}
      onSavePanel={saveAndCloseSidebar}
    />
  );

  const renderList = () => (
    <CreateWorkFlowPage
      startNewWorkflow={startNewWorkflow}
      isLoadingList={isLoadingList}
      workflowList={workflowList}
      handleOpenWorkflow={handleOpenWorkflow}
      handleDeleteWorkflow={handleDeleteWorkflow}
    />
  );

  const renderNewDialog = () =>
    showNewDialog ? (
      <CreateWorkflowDialog
        newNameInput={newNameInput}
        setNewNameInput={setNewNameInput}
        newDescInput={newDescInput}
        setNewDescInput={setNewDescInput}
        setShowNewDialog={setShowNewDialog}
        confirmNewWorkflow={confirmNewWorkflow}
      />
    ) : null;

  return (
    <>
      {view === "builder" ? renderBuilder() : renderList()}
      {renderNewDialog()}
    </>
  );
}

export default function App() {
  return (
    <ReactFlowProvider>
      <FlowCanvas />
    </ReactFlowProvider>
  );
}
