# Dockerfile.r
FROM r-base:4.3.1

# Avoid interactive prompts and speed up R
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system libs only if you need more packages later
# (kept minimal here; readr & dplyr need no extras on Debian slim)

# Install CRAN packages declared in install_packages.R
COPY install_packages.R .
RUN Rscript install_packages.R

# Copy your source tree
COPY src/ ./src/

# Default command runs your R pipeline
CMD ["Rscript", "src/r-app/main.R"]
