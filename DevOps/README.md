welcome to team DevOps!
please note:
if you want to run our CI
use the following commands in order to build and run it:

docker build -t image .
docker run -it -v /var/run/docker.sock:/var/run/docker.sock -p 8080:8080 image
