FROM python:3.12-slim

RUN pip install --no-cache-dir mitmproxy

RUN mkdir -p /proxy/logs /proxy/certs

COPY opencode-proxy/proxy_script.py /proxy/proxy_script.py
COPY opencode-proxy/entrypoint.sh /proxy/entrypoint.sh
RUN chmod +x /proxy/entrypoint.sh

WORKDIR /proxy

EXPOSE 8080

ENTRYPOINT ["/proxy/entrypoint.sh"]
