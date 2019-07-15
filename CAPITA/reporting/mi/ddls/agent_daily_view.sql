CREATE OR REPLACE VIEW agent_daily_view AS
SELECT
  "rowdate",
  "clientname",
  "agent",
  "date_format"("startinterval"  AT TIME ZONE 'Europe/London', '%Y-%m-%d %H:%i:%S') "startinterval",
  "date_format"("endinterval" AT TIME ZONE 'Europe/London', '%Y-%m-%d %H:%i:%S') "endinterval",
  "agentname",
  "agentfirstname",
  "agentlastname",
  "aftercontactworktime",
  "agentoncontacttime",
  "agentidletime",
  "nonproductivetime",
  "averageaftercontactworktime",
  "contactsagenthungupfirst",
  "contactsconsulted",
  "contactshandled",
  "contactshandledincoming",
  "contactshandledoutbound",
  "callbackcontactshandled",
  "contactsputonhold",
  "contactsholddisconnect",
  "contactsholdagentdisconnect",
  "contactsholdcustomerdisconnect",
  "contactsincoming",
  "callbackcontacts",
  "contactsqueued",
  "contactstransferredin",
  "contactstransferredout",
  "contactstransferredoutinternal",
  "contactstransferredoutexternal",
  "contactstransferredinfromqueue",
  "contactstransferredoutfromqueue",
  "errorstatustime",
  "customerholdtime",
  "agentanswerrate",
  "maximumqueuedtime",
  "contactsmissed",
  "contacthandletime",
  "contactflowtime",
  "occupancy",
  "servicelevel15seconds",
  "servicelevel20seconds",
  "servicelevel25seconds",
  "servicelevel30seconds",
  "servicelevel45seconds",
  "servicelevel60seconds",
  "servicelevel90seconds",
  "servicelevel120seconds",
  "servicelevel180seconds",
  "servicelevel240seconds",
  "servicelevel300seconds",
  "servicelevel600seconds",
  "onlinetime",
  "agentinteractionandholdtime",
  "agentinteractiontime",
  "averageoutboundagentinteractiontime",
  "averageoutboundaftercontactworktime",
  "breaktime",
  "lunchtime",
  "mentortime",
  "admintime",
  "trainingtime",
  "meetingtime",
  "onetoonetime",
  "outboundtime",
  "special1time",
  "outboundagentinteractiontime",
  "outboundagentaftercontactworktime"
FROM
  ccm_connect_reporting_[env].agent_daily
