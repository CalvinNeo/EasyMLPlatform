@echo off
curl -d "dropHeader=false;filePath=D:\code\golang\src\mlp\test\data_set_01.md" http://localhost/v1/data_set/upload/path
echo .
curl -d "dropHeader=false;filePath=D:\code\golang\src\mlp\test\data_set_02.json" http://localhost/v1/data_set/upload/path
echo.
