FROM python:3.10.11-slim AS builder
# FROM tiangolo/uvicorn-gunicorn:python3.10-slim AS builder
WORKDIR /app
COPY ./ .
RUN pip install --user --no-cache-dir -r ./docker/requirements.txt

FROM python:3.10.11-slim AS deployer
# FROM tiangolo/uvicorn-gunicorn:python3.10-slim AS deployer
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/src /app
COPY --from=builder /app/docker/entrypoint.sh /
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.sh"]