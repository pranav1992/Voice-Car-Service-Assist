import { apiClient } from "./client";

export const getWorkflow = async (workflowId) => {
    const { data } = await apiClient.get(`/workflows/${workflowId}`);
    return data;
};

export const createWorkflow = async (payload) => {
    const { data } = await apiClient.post("/workflows/create_workflow", payload);
    return data;
};

export const updateWorkflow = async (workflowId, payload) => {
    const { data } = await apiClient.put(`/workflows/${workflowId}`, payload);
    return data;
};

export const deleteWorkflow = async (workflowId) => {
    const { data } = await apiClient.delete(`/workflows/${workflowId}`);
    return data;
};

export const getWorkflows = async () => {
    console.log("getWorkflows");
    const { data } = await apiClient.get("/workflows/all_workflows");
    console.log(data);
    return data;
};