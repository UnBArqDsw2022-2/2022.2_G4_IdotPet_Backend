from fastapi import FastAPI

from controllers.user_controller import router as user_router
from controllers.pet_controller import router as pet_router


app = FastAPI(title='IdotPet')
app.include_router(user_router)
app.include_router(pet_router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
