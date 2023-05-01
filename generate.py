import requests
import pandas as pd

parties = {'เพื่อไทย':'ptp','ก้าวไกล':'mfp','ไทยสร้างไทย':'tstp'}

# data from https://www.vote62.com/
data = requests.get('https://vote62-general-66-site.s3.ap-southeast-1.amazonaws.com/structure.json?q=1').json()
data['candidates'] = list(filter(lambda c: c['party'] in parties.keys(), data['candidates']))
for votable in data['votables']:
    if 'candidate' not in votable:
        continue
    for candidate in data['candidates']:
        if votable['candidate'] == candidate['name']:
            votable['party'] = candidate['party']

data['votables'] = list(filter(lambda c: 'party' in c, data['votables']))

results  = []

for voting_district in data['votingDistricts']:
    row = {
        'จังหวัด': voting_district['code'].split('.')[0],
        'เขตเลือกตั้ง': int(voting_district['code'].split('.')[1]),
        'เพื่อไทย': '',
        'เพื่อไทยเบอร์': '',
        'ก้าวไกล': '',
        'ก้าวไกลเบอร์': '',
        'ไทยสร้างไทย': '',
        'ไทยสร้างไทยเบอร์': '',
        'เขต/ตำบล': []
    }
    for province in data['provinces']:
        for district in province['districts']:
            for subdistrict in district['subdistricts']:
                if voting_district['code'] == subdistrict['votingDistrict']:
                    row['เขต/ตำบล'].append(subdistrict['name'])
    row['เขต/ตำบล'] = '/n'.join(row['เขต/ตำบล'])
    for votable in data['votables']:
        if votable['resign']:
               continue
        if votable['voteingDistrict'] == voting_district['code']:
            row[votable['party']] = votable['candidate']
            row[votable['party']+'เบอร์'] = votable['no']
    results.append(row)
df = pd.DataFrame(results)
df.to_csv('result.csv', index=False)
#df.to_html('index.html', index=False)
