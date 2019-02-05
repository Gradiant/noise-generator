FROM python:3.7.2-alpine3.8

COPY noise_generator.py noise_generator_rest.py requirements.txt /opt/noise-generator/
COPY static/ /opt/noise-generator/static/
COPY templates/ /opt/noise-generator/templates/
COPY images/ /opt/noise-generator/images/

RUN python3 -m pip install -r /opt/noise-generator/requirements.txt
RUN apk add --no-cache iperf3
EXPOSE 5001

WORKDIR /opt/noise-generator
ENTRYPOINT ["python3", "noise_generator_rest.py"]
