Steps to Run:

1. teriminal : flask run , then install all requirements files, then do : cd .\tests\
2. Either use : locust -f locustfile.py --headless --users 10 --spawn-rate 10 --run-time 1m --csv=client_register_test_report
3. Or use : locust -f locustfile.py --loglevel=INFO --logfile=logs/locust_output.log and then View on Locust in Web Browser
4. Reports and logs are generated under logs folder