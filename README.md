# Implementation of the MEP Metric

To evaluate the performance of a transportation system.

## Pre-requisites
+ Docker
+ Linux 

## Valhalla
Valhalla is an open-source routing engine. See the full documentation [here](https://valhalla.github.io/valhalla/). A demo server (accessed from [https://valhalla1.openstreetmap.de/isochrone](https://valhalla1.openstreetmap.de/isochrone)) is open to the public but the request rate limit is 1 call/user/sec. You need to depoly it in a running docker container in your local machine or server to bypass this limit. 

### Set up the container
...