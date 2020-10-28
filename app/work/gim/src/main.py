from src.GIMESQueryTool.src import gim_es_query_tool

# The PA_ID for backfill
pa_id = 'amzn1.pa.o.A3690GOO3ZBMR4'
# local aws configure profile name
local_profile_name = 'gim-beta-na'

gim_es_query_tool.backfill_es_to_sqs(local_profile_name, pa_id)
