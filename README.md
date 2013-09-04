elect-data
==========

Data processing of the AEC's EML feed for the Australian Federal Election

## Input data
The input data can be found in the [AEC's media feed](http://www.aec.gov.au/media/mediafeed/).
The AEC site lists the specification for their media format in [this pdf](http://www.aec.gov.au/media/mediafeed/).

## Output data
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

### preferences.json
The preferences json file is a map of electorate ids to preference flow objects.
The preference flow objects consist of a list of preference flow round objects.
The preference flow round objects consists of vote tallies for each candidate and
the ID of the candidate whose votes were transferred.
```javascript
{
  198: {
    "electorate_id": 198,        // The electorate of the preference flows
    "rounds": [                  // The list of rounds of preference flows
      {
        23971: {
          "candidate_id": 23971, // The id of the candidate for this preference flow data
          "votes": 45678,        // The total number of votes the candidate has
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
