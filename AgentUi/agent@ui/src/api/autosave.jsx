import { apiClient } from "./client";

export const autosave = async (data) => {
    await apiClient.post("/autosave", data);
};

export const getAutosave = async () => {
    return await apiClient.get("/autosave");
}