BACKEND_DIR=./Backend
FRONTEND_DIR=Frontend
VENV_DIR=.venv
UVICORN=$(VENV_DIR)/bin/uvicorn

APP_MODULE=main:app

back :
	@echo "Levantando Backend"
	@cd $(BACKEND_DIR) && $(UVICORN) $(APP_MODULE) --host 0.0.0.0 --reload

front:
	@echo "Levantando Frontend"
	@cd $(FRONTEND_DIR) && npm run dev

all:
	@echo "Levantando App"
	@make back & make front
