import json
import xmltodict

def value(eml):
    return int(eml['#text'])

def candidate_id(candidate_eml):
    return int(candidate_eml['eml:CandidateIdentifier']['@Id'])


def eml_to_JSON(eml_file, type="media feed"):
    elect_data = xmltodict.parse(open(eml_file))
    
    if type == "media feed":
      firstprefs_json = {}
      twocandidate_json = {}

      for election in elect_data['MediaFeed']['Results']['Election']:
          # House of Representative contests
          if 'House' in election:
              for contest in election['House']['Contests']['Contest']:
                  electorate_id = int(contest['eml:ContestIdentifier']['@Id'])

                  # First preference data
                  firstprefs = contest['FirstPreferences']
                  candidates = firstprefs['Candidate']
                  
                  firstprefs_json[electorate_id] = {
                      'electorate_id': electorate_id,
                      'total': value(firstprefs['Total']['Votes']),
                      'formal': value(firstprefs['Formal']['Votes']),
                      'informal': value(firstprefs['Informal']['Votes']),
                      'votes': {
                          candidate_id(candidate):
                              value(candidate['Votes'])
                          for candidate in candidates
                      }
                  }

                  # Two Candidate Preferred data
                  twocand = contest['TwoCandidatePreferred']
                  restricted = '@Restricted' in twocand
                  maverick = '@Maverick' in twocand
                  
                  if not(restricted) and not(maverick):
                      candidates = twocand['Candidate']
                  else:
                      candidates = []
                  
                  twocandidate_json[electorate_id] = {
                      'electorate_id': electorate_id,
                      'available': not(restricted) and not(maverick),
                      'candidates': {
                          candidate_id(candidate): {
                              'candidate_id': candidate_id(candidate),
                              'votes': value(candidate['Votes']),
                          }
                          for candidate in candidates
                      }
                  }
                  
      # Write JSON files
      json.dump(firstprefs_json, open('firstpreferences.json', 'w'))
      json.dump(twocandidate_json, open('twocandidate.json', 'w'))
      
    elif type == "candidates":
      candidates_json = {}

      for election in elect_data['EML']['CandidateList']['Election']:
        category = election['ElectionIdentifier']['ElectionCategory']

        # House of Representatives candidates
        if category == 'House':
          for electorate in election['Contest']:
            electorate_id = int(electorate['ContestIdentifier']['@Id'])
            
            for candidate in electorate['Candidate']:
              cand_id = int(candidate['CandidateIdentifier']['@Id'])

              candidates_json[cand_id] = {
                'candidate_id': cand_id,
                'electorate_id': electorate_id,
                'party_id': int(candidate['Affiliation']['AffiliationIdentifier']['@Id']) if 'Affiliation' in candidate else None,
                'party': candidate['Affiliation'] if 'Affiliation' in candidate else None,
                'name': candidate['CandidateIdentifier']['CandidateName'],
                'firstname': candidate['CandidateFullName']['xnl:PersonName']['xnl:FirstName'][1],
                'lastname': candidate['CandidateFullName']['xnl:PersonName']['xnl:LastName'][1],
                'gender': candidate['Gender'],
              }

      json.dump(candidates_json, open('candidates.json', 'w'))

    elif type == "electorates":
      pass
