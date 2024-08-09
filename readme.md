Python selenium demo which creates todos with todo-mvc app

Create venv and install dependencies:
```
python3 -m venv venv
source ./venv/bin/activate
pip3 install -Ur requirements.txt
```

Possible parameters:
```
browser name, firefox and chrome are supported:
	--browser=firefox  
run browser in headless mode:
	--headless
connect to remote driver with given URL:
	--remote_driver=http://127.0.0.1:4444/wd/hub
run pytest in 2 processes, see pytest-xdist for more info on params:
	-n 2
dir to save allure report:
	--alluredir=./allure-results
rerun failed test 2 times, see pytest-rerunfailures for more params:
	--reruns 2 
```

Run tests in selenium docker with dynamic grid:
``` 
./run_in_docker.sh
```

Examples:
### Run all tests with default browser (chrome) and save allure report to ./allure-results
```
 pytest  --alluredir=./allure-results
```

### Specify browser and run test in headless mode
```
 pytest  --browser=firefox --headless
 pytest  --browser=chrome --headless
```

### Connect to remote driver and request chrome in headless mode, rerun failed tests twice
```
pytest --reruns 2 --browser=chrome --headless  --remote_driver=http://127.0.0.1:4444/wd/hub
```

### Run tests in 2 parallel processes
```
 pytest -n 2 --alluredir=./allure-results 
```

### Show allure report in browser
```
 allure serve ./allure-results 
```
