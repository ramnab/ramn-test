-- CREATE VIEW
CREATE OR REPLACE VIEW contact_record_view AS 
SELECT
  rowdate, clientname,
  "json_extract_scalar"("agent", '$.routingprofile.name') "routingprofilename",
  "json_extract_scalar"("agent", '$.username') "username", 
  "json_extract_scalar"("agent", '$.connectedtoagenttimestamp') "connectedtoagenttimestamp",
  CAST("json_extract_scalar"("agent", '$.agentinteractionduration') as bigint) "agentinteractionduration",
  CAST("json_extract_scalar"("agent", '$.aftercontactworkduration') as bigint) "aftercontactworkduration",
  "json_extract_scalar"("agent", '$.aftercontactworkendtimestamp') "aftercontactworkendtimestamp",
  "json_extract_scalar"("agent", '$.aftercontactworkstarttimestamp') "aftercontactworkstarttimestamp",
  "json_extract_scalar"("agent", '$.customerholdduration') "customerholdduration",
  "json_extract_scalar"("agent", '$.hierarchygroups') "hierarchygroups",
  "json_extract_scalar"("agent", '$.longestholdduration') "longestholdduration",
  "json_extract_scalar"("agent", '$.numberofholds') "numberofholds"
  
FROM default.contact_record
WHERE ("agent" IS NOT NULL);







-- number of calls handled by agents
SELECT count(awsaccountid) AS number_of_calls_handled_by_agents 
FROM "default"."contact_record"
WHERE clientname='tradeuk' 
AND rowdate = '2019-03-04' 
AND agent IS NOT NULL;











-- number of calls per agent
SELECT username, count(username) AS num_calls 
FROM "default"."contact_record_view"
GROUP BY username;












-- average call duration
SELECT username, avg(agentinteractionduration) AS avg_duration_calls 
FROM "default"."contact_record_view" 
GROUP BY username
ORDER BY avg_duration_calls DESC;







