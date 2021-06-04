run the init-compose.sh

the two services are connected through a docker network
it has two env variables the port it runs and the ip of the weight mircoserive 
it will stop any containers started by this script 
it will then build them anew for any updates to the code 
and finally start 

Upon running you are able to open a simple webpage to add and update trucks and providers 
if you request a providers bill that had no trucks it will return a json of an empty bill 
however 
there is a problem we regretbly failed to fix on 
recieving the respone from the weight tems api back as workable data to create the providers bill


