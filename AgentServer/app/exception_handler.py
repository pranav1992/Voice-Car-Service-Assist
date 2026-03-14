from app.application.exceptions.workflow_exceptions import\
                                            workflow_exception_handler
from app.application.exceptions.agent_exceptions import\
                                            agent_exception_handler
from app.application.exceptions.exceptions import exception_handler


def register_exception_handlers(app):
    workflow_exception_handler(app)
    agent_exception_handler(app)
    exception_handler(app)
