1. clone or download the code from Github  
```git clone https://github.com/zanut/ku-polls.git```  
2. change directory to the project root  
```cd ku-polls```
3. create a virtual environment and install dependencies)  
```python -m venv venv```
4. create .env file in the project from sample.env  
```cp sample.env .env```
5. configure the .env setting details already explaned in the .env file  
```nano .env```
6. activate the virtual environment  
```venv\Scripts\activate``` (Windows)  
```source venv/bin/activate``` (MacOS, Linux)
7. install dependencies  
```pip install -r requirements.txt```
8. run migrations  
```python manage.py migrate```
9. load data from the data/polls-v3.json and data/users-v1.json  
```python manage.py loaddata data/polls-v3.json data/users-v1.json```
