elect-data
==========

Data processing of the AEC's EML feed for the Australian Federal Election

## Input data
The input data can be found in the [AEC's media feed](http://www.aec.gov.au/media/mediafeed/).
The AEC site lists the specification for their media format in [this pdf](http://www.aec.gov.au/media/mediafeed/).

## Fetching the data
The Python2.7 `fetchdata.py` script fetches data from the AEC's FTP server and polls it every 90 seconds.
The script downloads the zip data and extracts the relevant xml files and converts them into JSON files.

All of the files are downloaded, extracted and converted inside of the folder that the script is run.
Therefore it is recommended that you run the script in the `data/<year>` directory, i.e., `python ../../scripts/fetchdata.py`.

By default the data is fetched from the 2010 directory on the AEC's servers.
To fetch a different year change the `FEED_ID` in the `fetchdata.py` script to match the url for that year.
For a list of feeds see http://results.aec.gov.au/.

## Live output data
The aim of this project is to produce some simple sets of JSON data from the complex EML format.
This will hopefully encourage developers with small project ideas to jump in a play with the data.

### electorates.json
The electorates json file is a map of electorate IDs to electorate objects.
```javascript
{
  179: {
    "id": 179,          // The electorate's ID
    "name": "Adelaide", // The electorate's name
    "state": "SA"       // The electorate's state location
  },
  ...
}
```

### parties.json
The parties json file is a map of party IDs to party objects.
```javascript
{
  198: {
    "id": 198,                        // The party's ID
    "shortname": "ALP",               // The party's 2-4 letter abbreviation/acronym
    "name": "Australian Labor Party", // The party's registered name
  },
  ...
}
```

### candidates.json
The candidates json file maps candidate IDs to candidate objects.
```javascript
{
  23971: {
    "id": 23971,           // The candidate's ID
    "party_id": 198,       // The candidate's party's ID
    "electorate_id": 179,  // The candidate's electorate
    "name": "ELLIS, Kate", // The candidate's ballot paper name
    "firstname": "Kate",   // The candidate's first name
    "lastname": "ELLIS",   // The candidate's surname
    "gender": "female"     // The candidate's gender
  }
  ...
}
```

### firstpreferences.json
The firstpreferences json file maps electorates to the tallies of first preferences for each candidate.
```javascript
{
  179: {
    "electorate_id": 179, // The ID of the electorate
    "votes": {            // Tallies of first preferences
      23971: 45678        // Candidate ID is the key
                          // and the value is the number of first preferences
    }
  }
}
```

### twocandidate.json
The twocandidate json file maps electorates to the two preferred candidates and the number associated of votes for each.
```javascript
{
  179: {
    "candidates": [       // List of two preferred candidates
      {
        "id": 23971,      // ID of the candidate
        "votes": 46810,   // The number of votes the candidate has
                          // over the other candidate
      },
      ...
    ]
  },
  ...
}
```

## Historical data

### preferences.json
The preferences json file is a map of electorate ids to preference flow objects.
The preference flow objects consist of a list of preference flow round objects.
The preference flow round objects consists of vote tallies for each candidate and
the ID of the candidate whose votes were transferred.
```javascript
{
  179: {
    "electorate_id": 179,        // The electorate of the preference flows
    "rounds": [                  // The list of rounds of preference flows
      {
        23971: {
          "candidate_id": 23971, // The id of the candidate for this preference flow data
          "round": 0,            // A zero indexed number for which round of preference flow it is
          "eliminated": false,   // Has the candidate been eliminated from the running yet?
          "votes": 45678,        // The total number of votes the candidate has
                                 // for this round of preferences (0 for eliminated candidates)
        },
        "transferrer": null      // The id of the vote transferrer
                                 // for this round (null for the first round)
      },
      ...
    ]
  },
  ...
}
```
