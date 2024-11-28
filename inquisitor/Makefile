SERVER		= ftp-server
CLIENT		= client
ATTACKER	= inquisitor

# Colors
CYAN			="\033[1;36m"
RED				="\033[31m"
GREEN			="\033[32m"
YELLOW		="\033[33m"
RESET			="\033[m"
BLUE			= \033[0;34m

FOLDERS_TO_CPY      = ~/Downloads
TARGET_DIR          = ./volumes/server/

all: copy_folders
	@printf "${BLUE}Starting Docker containers...${NC}\n"
	docker-compose up -d

copy_folders:
	@printf "${YELLOW}Copying Download folder to server directory...${NC}\n"
	@for folder in $(FOLDERS_TO_CPY); do \
		cp -r $${folder/#\~/$${HOME}} $(TARGET_DIR); \
	done

re: fclean all

build:
	@printf "${BLUE}Building Docker containers...${NC}\n"
	docker-compose up --build -d

down:
	@printf "${YELLOW}Stopping Docker containers${NC}\n"
	docker-compose down

clean: down
	@printf "${YELLOW}removing Docker containers, images, volumes, and networks stopped...${NC}\n"
	 docker system prune -f -a

fclean: down
	@printf "${YELLOW}Cleaning volumes/server directory...${NC}\n"
	@rm -rf $(TARGET_DIR)*
	@touch ./volumes/server/.gitkeep
	@printf "${YELLOW}removing All Docker containers, images, volumes, and networks...${NC}\n"
	docker system prune -f -a --volumes

server:
	docker exec -it ftp-server /bin/bash

client:
	docker exec -it client /bin/sh

inquisitor:
	docker exec -it inquisitor /bin/bash

info:
	@printf "[docker informations]\n"

	@echo $(CYAN)$(SERVER)$(RESET)
	@printf " - IPAddress	: "
	@docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(SERVER)
	@printf " - MacAddress	: "
	@docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(SERVER)

	@echo $(CYAN)$(CLIENT)$(RESET)
	@printf " - IPAddress	: "
	@docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(CLIENT)
	@printf " - MacAddress	: "
	@docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(CLIENT)

	@echo $(CYAN)$(ATTACKER)$(RESET)
	@printf " - IPAddress	: "
	@docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(ATTACKER)
	@printf " - MacAddress	: "
	@docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $(ATTACKER)
