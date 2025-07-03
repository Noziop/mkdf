CC = gcc
CFLAGS = -Wall -Wextra -g -pthread
LDFLAGS = -pthread

# Chemins
SRC_DIR = src
BUILD_DIR = build
INCLUDE_DIR = include

# Modules (structure SOLID)
MODULES = utils fs config templates cli web main

# Sources générées dynamiquement
SRC_FILES = $(foreach mod,$(MODULES),$(wildcard $(SRC_DIR)/$(mod)/*.c))
OBJ_FILES = $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRC_FILES))

# Cible principale
TARGET = mkdf_refactored

.PHONY: all clean check-deps

all: dirs $(TARGET)

# Création des répertoires de build
dirs:
	@mkdir -p $(BUILD_DIR)
	@$(foreach mod,$(MODULES),mkdir -p $(BUILD_DIR)/$(mod);)

# Règle de compilation
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

# Création de l'exécutable
$(TARGET): $(OBJ_FILES)
	$(CC) $(OBJ_FILES) $(LDFLAGS) -o $@

# Vérification des dépendances (amélioration)
check-deps:
	@echo "Vérification des dépendances..."
	@which $(CC) > /dev/null || (echo "$(CC) non trouvé" && exit 1)
	@echo "#include <pthread.h>" > /tmp/pthread_test.c
	@echo "int main() { pthread_t t; return 0; }" >> /tmp/pthread_test.c
	@$(CC) -pthread /tmp/pthread_test.c -o /tmp/pthread_test > /dev/null 2>&1 || \
		(echo "pthread non disponible" && exit 1)
	@rm -f /tmp/pthread_test.c /tmp/pthread_test
	@echo "Toutes les dépendances sont satisfaites"

# Nettoyage
clean:
	rm -rf $(BUILD_DIR) $(TARGET)
