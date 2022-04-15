IDIR =-I ~/.mujoco/mujoco210/include
LDIR =-L ~/.mujoco/mujoco210/bin
CC=gcc
TARGET=test

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(IDIR) $(LDIR) -pthread -o $(TARGET) $(TARGET).cpp -lmujoco210nogl
