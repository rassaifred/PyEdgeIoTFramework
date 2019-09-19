FROM rassaifred/balena_rpi3_base_image

# --------------------

WORKDIR /usr/src/app

COPY /device_rpi/requirements.txt ./device_rpi/

RUN pip3 install --upgrade setuptools

RUN pip3 install --no-cache-dir -r ./device_rpi/requirements.txt

COPY . .

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

CMD [ "python3","-u", "./device.py" ]