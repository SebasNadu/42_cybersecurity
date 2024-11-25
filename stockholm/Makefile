NAME                = stockholm.py
APP_DIR             = ./app/
TARGET_DIR          = ./infection/
FOLDERS_TO_CPY      = ~/Desktop ~/Downloads ~/Documents

# Colores
GREEN               = \033[0;32m
YELLOW              = \033[0;33m
BLUE                = \033[0;34m
NC                  = \033[0m # No Color

all: copy_folders
	@printf "${BLUE}Starting Docker containers...${NC}\n"
	@docker compose up -d

build:
	@printf "${BLUE}Building Docker containers...${NC}\n"
	@docker compose build

mkdir:
	@printf "${YELLOW}Creating target directory if it doesn't exist...${NC}\n"
	@mkdir -p $(TARGET_DIR)

copy_folders: mkdir
	@printf "${YELLOW}Copying folders to target directory...${NC}\n"
	@for folder in $(FOLDERS_TO_CPY); do \
		cp -r $${folder/#\~/$${HOME}} $(TARGET_DIR); \
	done

encrypt:
	@printf "${GREEN}Running encryption script...${NC}\n"
	@python3 $(APP_DIR)$(NAME)

decrypt:
	@printf "${GREEN}Running decryption script...${NC}\n"
	@python3 $(APP_DIR)$(NAME) -r $(KEY)

clean:
	@printf "${YELLOW}Cleaning target directory...${NC}\n"
	@rm -rf $(TARGET_DIR)*

fclean: clean
	@printf "${YELLOW}Stopping and removing Docker containers, images, volumes, and networks...${NC}\n"
	@docker compose down
	@docker network prune -f
	@yes | docker system prune -a --volumes

help:
	@printf "${GREEN}Available targets:${NC}\n"
	@printf "  ${YELLOW}all${NC}          - Build and start the Docker containers\n"
	@printf "  ${YELLOW}build${NC}        - Build the Docker containers\n"
	@printf "  ${YELLOW}mkdir${NC}        - Create the target directory\n"
	@printf "  ${YELLOW}copy_folders${NC} - Copy specified folders to the target directory\n"
	@printf "  ${YELLOW}encrypt${NC}      - Run the encryption script\n"
	@printf "  ${YELLOW}clean${NC}        - Remove files in the target directory\n"
	@printf "  ${YELLOW}fclean${NC}       - Clean Docker containers, images, volumes, and networks\n"

.PHONY: all build mkdir copy_folders encrypt clean fclean help
