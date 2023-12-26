# Create a Docker image for Trusty with Python 3.6
It's a tough task just to get Python version 3.6 on Trusty. This Dockerfile help you create an Ubuntu Trusty image with Python 3.6 installed, as well as some other essential packages/libraries required for building this project.

## Build the image
To build the image, it is as simple as running the following command inside this directory:
```bash
docker build -t trusty-python3.6 .
```

It will take a long while to build the image, since the Dockerfile will install Python 3.6 from source (the official PPA for Python 3.6 is not available for Trusty anymore). Good thing is that you only need to build the image once.