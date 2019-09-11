ARG CACHEBUST=1

FROM rassaifred/balena_rpi3_base_image

# --------------------

WORKDIR /usr/src/app

COPY /device_rpi/requirements.txt ./device_rpi/

RUN pip3 install --no-cache-dir -r ./device_rpi/requirements.txt

COPY . .

CMD [ "python3","-u", "./device.py" ]