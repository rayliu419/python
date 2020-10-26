
import sys
import json

pa1 = sys.argv[1]
pa2 = sys.argv[2]
pa3 = sys.argv[3]

with open('data/old_merge_event.json', 'r') as f:
    mergeEvent = json.load(f)

mergeEvent["Message"]["CreatedFrom"][0]["PartnerAccountId"] = pa1
mergeEvent["Message"]["CreatedFrom"][1]["PartnerAccountId"] = pa2
mergeEvent["Message"]["MergedTo"]["PartnerAccountId"] = pa3
mergeEvent["MessageAttributes"]["PartnerAccountId"] = pa3
mergeEvent["MessageAttributes"]["TombstonedPartnerAccountIds"]["value"][0] = pa1
mergeEvent["MessageAttributes"]["TombstonedPartnerAccountIds"]["value"][2] = pa2
with open('mergeEvent.json', 'w') as f:
    json.dump(mergeEvent, f)

