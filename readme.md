# run the server
uvicorn main:app --reload


docker exec -i postgres psql -U postgres -d event-booker < ./migrations/0002_token.sql 
