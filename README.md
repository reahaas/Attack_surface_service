# Attack_surface_service
Attack_surface_service That was fun!
Here is the architecture of my system.
![attack_surface_design_single_process](https://user-images.githubusercontent.com/35425887/126724467-eae657db-c406-465a-a03c-888948642351.png)

## My choices:
1. To reduce the response time of requests, I chose to pre-calculate all the required potential attackers for each VM, and save it as an object in the memory.
    Tradeoff: If the data is too big, this method will fail due to insufficient memory. 
    Solution: To solve this I will need to move The data to a database, and query the database per request (maybe add cache to reduce the time for popular VMs).
2. pre-calculate all the required potential attackers for each VM at server start:
    Tradeoff: If the server can't wait for a long time at startup. 
    Solution: To solve this I will need to only load the data at startup, and calculate the request "on the fly". It's also possible to start with the "on the fly" approach while calculating the final data, and after it was calculated move to the first approach (use precalculated data).
3. Tornado as an HTTP server:
    Explanation: It's a great library that allows me to easily write HTTP server and focus on the logic of my app, while it gives great async features out of the box. 



## installations:

To generate the requirements file I used:
```
python3 -m  pipreqs.pipreqs .
```

To install it:
```
python3 -m pip install -r requirements.txt
```


## Running the app:
To run the app cd to the project directory and:
```
sudo python3 runner.py -f <input_file>
# for example:
sudo python3 runner.py -f data/input-3.json
```
That will display how long it took to load the data file:
![image](https://user-images.githubusercontent.com/35425887/126723466-c587e77f-f259-4eed-b57b-11041aebeb0b.png)


## Tests:
To run the tests cd into the project directory and:
```
python3 -m pytest tests
```
![image](https://user-images.githubusercontent.com/35425887/126723654-06f36a3c-9d88-4503-8d8d-c7a61f8a401b.png)

I added a `tests/manual_load_api_requests.py` file to check the performance of the app for big amount of requests.
To run it, after the main app is already running, start the script:
```
python3 tests/manual_load_api_requests.py
```
The scrip will start to create big number of requests to the app.

## Output example:
1. Run the app with `input-3.json` as input file: `sudo python3 runner.py -f data/input-3.json`
2. Start the manual script to load on the system: `python3 tests/manual_load_api_requests.py` (first edit the `vm_id` in the `URL` variable to `vm-ab51cba10`)
3. here are the results:

api call: `http://localhost/v1/attack?vm_id=vm-ab51cba10`
![image](https://user-images.githubusercontent.com/35425887/126726509-92f1454a-1ec7-4221-bed9-d665ffca1b34.png)

api call: `http://localhost/v1/stats` (After more than 100k requests)
![image](https://user-images.githubusercontent.com/35425887/126726815-ae7f2d42-ad34-4ddf-8ab6-69046d0bfd22.png)

