# FROM balenalib/raspberrypi3-python:3
FROM balenalib/raspberrypi3-debian:stretch-run-20190612


RUN apt-get update && \
  apt-get install -y --no-install-recommends libjpeg-dev \
  libopenjp2-7 \
  zlib1g \
  python3-dev \
  git \
  python-imaging python-smbus i2c-tools \
  python3-pil \
  python3-pip \
  python3-setuptools \
  python3-rpi.gpio && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

ENV DBUS_SYSTEM_BUS_ADDRESS unix:path=/host/run/dbus/system_bus_socket

# --------------------

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

# --------------------

WORKDIR /usr/src/app

COPY /device_rpi/requirements.txt ./device_rpi/

RUN pip3 install --upgrade setuptools

RUN pip3 install --no-cache-dir -r ./device_rpi/requirements.txt

COPY . .

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

CMD [ "python3","-u", "./device.py" ]