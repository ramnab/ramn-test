# republish historical events

Republish historical events from one account into the common
reporting bucket.

Republishes a given day's events
    Usage:

```bash
python republish.py [-r REGION] SOURCE SOURCE_ENV DEST DEST_ENV DAY
    
# For example: 
python republish.py -r eu-central-1 tradeuk-prod prod tradeuk-nonprod test 2019/06/03
        
#  Will republish the agent events from 2019/06/03 from tradeuk-prod to common test account
#  using tradeuk-nonprod account
```

Note that the script currently only handles agent events but can be
readily adapted for CTRs, for instance.
