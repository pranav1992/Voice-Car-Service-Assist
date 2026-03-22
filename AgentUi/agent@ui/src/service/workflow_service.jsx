import { createWorkflow } from "../api/workflow";


async function createWorkflowService(payload) {
    const data = await createWorkflow(payload)
    return data

}

export default createWorkflowService