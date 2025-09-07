FROM archlinux:latest

# Install required packages
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm bash python python-pip python-pytest python-pytest-asyncio wget

# Download and install older readline
RUN wget http://archive.archlinux.org/packages/r/readline/readline-8.0.004-1-x86_64.pkg.tar.zst && \
    pacman -U --noconfirm readline-8.0.004-1-x86_64.pkg.tar.zst && \
    rm readline-8.0.004-1-x86_64.pkg.tar.zst
    
WORKDIR /app

# Copy test files
COPY tests/test_libpath.py .
COPY defaults/assets/lock_wifi.sh .
COPY defaults/assets/unlock_wifi.sh .
COPY main.py .


# Run pytest with verbose output
CMD ["pytest", "test_libpath.py"]
