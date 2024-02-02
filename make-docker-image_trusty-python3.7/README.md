# Create a Docker image for Trusty with Python 3.7
It's a tough task just to get Python version 3.7 on Trusty (Ubuntu 14.04). This Dockerfile help you create an Ubuntu Trusty image with Python 3.7 installed, as well as some other essential packages/libraries required for building this project.

## Build the image
To build the image, it is as simple as running the following command inside this directory:
```bash
docker build -t trusty-python3.7 .
```

It will take a long while to build the image, since the Dockerfile will install Python 3.7 from source. All PPA seems to have dropped support for Trusty, so this is probably the only way to get Python 3.7 on Trusty. Good thing is, you only need to build the image once.