# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * In the virtualenv: Update pip setuputils and wheel to support building new packages
FROM debian:11-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv=3.9.2-3 gcc=4:10.2.1-1 libpython3-dev=3.9.2-3 && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Build the virtualenv as a separate step: Only re-execute this step when 
# requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r requirements.txt


# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11:nonroot
COPY --from=build-venv /venv /venv
WORKDIR /venv
USER nonroot
ENTRYPOINT [ "/venv/bin/aws-energy-labeler" ]
CMD [ "--help" ]