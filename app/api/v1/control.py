import app.services.control_service as control_service


async def command_control():
    await control_service.command_control_service()