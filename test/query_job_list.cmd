@echo off
curl -d "" http://localhost/v1/job/query/list
echo .
curl -d "id=1" http://localhost/v1/job/query