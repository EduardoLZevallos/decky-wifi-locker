FROM archlinux:latest

# Install required packages
RUN pacman -Syu --noconfirm --ask 4  && \
        pacman -S --noconfirm --ask 4 bash python python-pip python-pytest python-pytest-asyncio wget base-devel networkmanager iw

# Ensure NetworkManager is NOT automatically started (safety precaution)
RUN systemctl disable NetworkManager

RUN useradd -m testuser
USER testuser
WORKDIR /home/testuser/app

# Copy test files
COPY tests/test_libpath.py .
COPY defaults/assets/lock_wifi.sh .
COPY defaults/assets/unlock_wifi.sh .
COPY main.py .

# Run pytest with verbose output
CMD ["pytest", "test_libpath.py", "-v"]