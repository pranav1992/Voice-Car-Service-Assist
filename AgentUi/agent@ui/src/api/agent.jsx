import { apiClient } from "./client";

export const createAgent = async (payload) =>{
    const data = await apiClient.post("/agents/create_agent", payload)
}


export const updateAgent = async (payload) => {
    const data = await apiClient.post("/agents/update_agent", payload)
}

export const getAgent = async (agentId) => {
    const data = await apiClient.get("/agents/")
}