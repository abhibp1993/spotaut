FROM debian:bullseye
LABEL maintainer="Abhishek N. Kulkarni" \
        email="abhi.bp1993@gmail.com" \
        version="0.0.1"


# Install python
RUN apt-get update && \
    RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
    python3-dev && \
    apt-get clean

# Install spot
# Reference: https://gitlab.lrde.epita.fr/spot/spot-web/-/blob/master/docker/Dockerfile
RUN echo 'deb [trusted=true] http://www.lrde.epita.fr/repo/debian/ stable/' >> /etc/apt/sources.list && \
    apt-get update && \
    RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
    spot libspot-dev spot-doc python3-spot && \
    apt-get clean

# Server configuration
RUN mkdir /home/spotservice
ENV SRC_DIR /home/spotservice
COPY src/* ${SRC_DIR}
WORKDIR ${SRC_DIR}
ENV PYTHONUNBUFFERED=1
CMD ["python3", "server.py"]
