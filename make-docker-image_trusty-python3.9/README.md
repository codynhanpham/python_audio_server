# Create a Docker image for Trusty with Python 3.9
This Dockerfile help you create an Ubuntu Trusty image with Python 3.9 installed, as well as some other essential packages/libraries required for building this project.

## Build the image
To build the image, it is as simple as running the following command inside this directory:
```bash
docker build -t trusty-python3.9 .
```

It will take a long while to build the image, since the Dockerfile will install Python 3.9 from source. All PPA seems to have dropped support for Trusty, so this is probably the only way to get Python 3.9 on Trusty. Good thing is, you only need to build the image once.