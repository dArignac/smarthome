FROM balenalib/raspberrypi3-python:3.7.4-build

# build on a non arm device, see # https://www.balena.io/docs/reference/base-images/base-images/#building-arm-containers-on-x86-machines
RUN [ "cross-build-start" ]
RUN apt-get update && apt-get install -y libglib2.0-dev
COPY requirements.txt /requirements.txt
RUN sudo pip install --user -r requirements.txt
RUN [ "cross-build-end" ]

COPY demo.py /demo.py
CMD ["python", "/demo.py"]

# FIXME build image is ca. 740 MB while the run is 270 MB
# FIXME either copy the right paths from the build image or install the required prerequisites in the run image
# FIMXE you can analyse the image layers withh "dive"
#FROM balenalib/raspberrypi3-python:3.7.4-run
#COPY --from=build /root/.local /root/.local
#ENV PATH=/root/.local/bin:$PATH
