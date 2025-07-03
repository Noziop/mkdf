CC = gcc
CFLAGS = -Wall -Wextra -g -pthread
LDFLAGS = -pthread
SRC_DIR = src
BUILD_DIR = build
INCLUDE_DIR = include
PREFIX ?= /usr/local
MANDIR = $(PREFIX)/share/man
MAN_FILE ?= mkdf.1

# Source files
SRCS = $(SRC_DIR)/main.c $(SRC_DIR)/directory_handler.c $(SRC_DIR)/cli_handler.c $(SRC_DIR)/web_handler.c $(SRC_DIR)/config_handler.c
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Main target
TARGET = mkdf

.PHONY: all clean install install-man

all: $(BUILD_DIR) $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $@

install: $(TARGET) install-man
	mkdir -p $(PREFIX)/bin
	install -m 755 $(TARGET) $(PREFIX)/bin/

install-man:
	mkdir -p $(MANDIR)/man1
	mkdir -p $(MANDIR)/fr/man1
ifeq ($(MAN_FILE),mkdf.en.1)
	# Installation en anglais (par défaut)
	install -m 644 mkdf.en.1 $(MANDIR)/man1/mkdf.1
else
	# Installation en français
	install -m 644 mkdf.1 $(MANDIR)/man1/mkdf.1
	install -m 644 mkdf.en.1 $(MANDIR)/man1/mkdf.en.1
endif

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

# Run the program
run: $(TARGET)
	./$(TARGET)

# Web interface
web: $(TARGET)
	./$(TARGET) --web