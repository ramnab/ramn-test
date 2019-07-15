CREATE OR REPLACE VIEW queue_interval_view AS
SELECT
  "rowdate",
  "clientname",
  "queue",
  "date_format"("startinterval"  AT TIME ZONE 'Europe/London', '%Y-%m-%d %H:%i:%S') "startinterval",
  "date_format"("endinterval" AT TIME ZONE 'Europe/London', '%Y-%m-%d %H:%i:%S') "endinterval",
  "aftercontactworktime",
  "agentoncontacttime",
  "agentidletime",
  "averagequeueabandontime",
  "averageaftercontactworktime",
  "averagequeueanswertime",
  "averagehandletime",
  "averagecustomerholdtime",
  "averageagentinteractionandcustomerholdtime",
  "averageagentinteractiontime",
  "contactsabandoned",
  "contactsabandonedin15seconds",
  "contactsabandonedin20seconds",
  "contactsabandonedin25seconds",
  "contactsabandonedin30seconds",
  "contactsabandonedin45seconds",
  "contactsabandonedin60seconds",
  "contactsabandonedin90seconds",
  "contactsabandonedin120seconds",
  "contactsabandonedin180seconds",
  "contactsabandonedin240seconds",
  "contactsabandonedin300seconds",
  "contactsabandonedin600seconds",
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
  "contactsansweredin15seconds",
  "contactsansweredin20seconds",
  "contactsansweredin25seconds",
  "contactsansweredin30seconds",
  "contactsansweredin45seconds",
  "contactsansweredin60seconds",
  "contactsansweredin90seconds",
  "contactsansweredin120seconds",
  "contactsansweredin180seconds",
  "contactsansweredin240seconds",
  "contactsansweredin300seconds",
  "contactsansweredin600seconds",
  "contactsqueued",
  "contactstransferredin",
  "contactstransferredout",
  "contactstransferredoutinternal",
  "contactstransferredoutexternal",
  "contactstransferredinfromqueue",
  "contactstransferredoutfromqueue",
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
  "agentinteractionandholdtime",
  "agentinteractiontime",
  "averageoutboundagentinteractiontime",
  "averageoutboundaftercontactworktime"
FROM
  ccm_connect_reporting_test.queue_interval
