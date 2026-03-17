import { createWorkflow } from "../api/workflow";
import 

async function createWorkflowService(payload) {
    const data = await createWorkflow(payload)
    if (data["status"] == 200){
        
    }
    

}

export default createWorkflowService