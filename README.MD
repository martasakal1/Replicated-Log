## Replicated Log
Client-Server application that includes Master and two secondaries 

### Instruction 
To run application use the following commands:

    docker-compose build
    docker-compose up
 
 To test application use:
    
    curl -X POST http://127.0.0.1:8080/messages/new -H 'Content-Type: application/json' 
    -d '{"email":"dhdh1@gmail.com"}'
    
    curl -X GET http://127.0.0.1:8080/get_message
