# gamedaydemo

Instructions 

- git clone https://github.com/zked/gamedaydemo.git
- Open gamedaydemo in your IDE
- pip install newrelic (Check other options if necessary https://docs.newrelic.com/install/python/#pip)
- change ingest license in newrelic.ini
- python3 adice.py or python adice.py
- attach the value of each dice(result) to the transactions and add the sum of it to your pathpoint KPI's
newrelic.agent.add_custom_parameter('roll_result', result)
