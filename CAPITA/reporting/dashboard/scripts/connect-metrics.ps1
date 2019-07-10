
$metricMapping = @{
  CONTACTS_QUEUED = "CALL"
  CONTACTS_ABANDONED = "ABANDONED"
  QUEUE_ANSWER_TIME = "ASA"
  AGENTS_ONLINE = "AGENTS"
  OLDEST_CONTACT_AGE = "MAXOCW"
  CONTACTS_IN_QUEUE = "IN_QUEUE"
  AGENTS_AFTER_CONTACT_WORK = "ACW"
  AGENTS_AVAILABLE = "AVAILABLE"
}

function Get-Metrics() {
  Param(
    [PSObject]
    $QueueMetadata,
    [String]
    $ProfileName,
    [String]
    $ClientName
  )
  $startTime = Get-Date -Hour 0 -Minute 00 -Second 00
  $now = Get-Date -Second 00
  $endTime = $now.AddMinutes(- $now.Minute % 5)

  $queues = @(($QueueMetadata.queues | Get-Member -MemberType NoteProperty).Name)

  $currentMetricsToRetrieve = New-CurrentMetrics

  $callMetrics = @{}

  $currentRequestParameters = @{
    InstanceId = $QueueMetadata.instanceId
    Filters_Queue = $queues
    Grouping = @("QUEUE")
    CurrentMetric = $currentMetricsToRetrieve
    ProfileName = $ProfileName
    Region = "eu-central-1"
  }

  $currentMetricResponse = Get-CONNCurrentMetricData @currentRequestParameters
  Set-Metrics -CallMetrics $callMetrics -MetricData $currentMetricResponse.MetricResults -QueueMetadata $QueueMetadata -ClientName $ClientName

  $historicMetricsToRetrieve = New-HistoricMetrics

  $historicRequestParameters = @{
    InstanceId = $QueueMetadata.instanceId
    Filters_Queue = $queues
    Grouping = @("QUEUE")
    HistoricalMetric = $historicMetricsToRetrieve
    ProfileName = $ProfileName
    Region = "eu-central-1"
    StartTime = $startTime
    EndTime = $endTime.ToUniversalTime()
  }

  $historicMetricResponse = Get-CONNMetricData @historicRequestParameters

  Set-Metrics -CallMetrics $callMetrics -MetricData $historicMetricResponse.MetricResults -QueueMetadata $QueueMetadata -ClientName $ClientName

  return $callMetrics
}

function Find-QueueName() {
  Param(
    [PSObject]
    $Metric,
    [PSObject]
    $QueueMetadata
  )
  $arn = $Metric.Dimensions.Queue.Arn
  $queues = @{}
  $QueueMetadata.queues.PSObject.Properties | ForEach-Object { $queues[$_.Name] = $_.Value }
  if ($queues.ContainsKey($arn)) {
      return $queues[$arn]
  }
  return $arn
}

function Find-MetricName() {
  Param(
    [String]
    $MetricName
  )

  if ($metricMapping.ContainsKey($MetricName)) {
    return $metricMapping[$MetricName]
  }

  return $MetricName
}

function Set-Metrics() {
  Param(
    [HashTable]
    $CallMetrics,
    [PSObject]
    $MetricData,
    [PSObject]
    $QueueMetadata,
    [String]
    $ClientName
  )

  foreach ($metric in $MetricData) {
    $queueName = Find-QueueName -Metric $metric -QueueMetadata $QueueMetadata
    $queueMetrics = @{}
    foreach ($collection in $metric.Collections) {
      $metricName = Find-MetricName -MetricName $collection.Metric.Name
      $queueMetrics[$metricName] = $collection.Value
    }
    $CallMetrics.Add($queueName, $queueMetrics)
  }
}

function New-CurrentMetrics() {
  $currentMetrics = @(
    @{Name="AGENTS_AVAILABLE"; Unit="COUNT"},
    @{Name="AGENTS_ONLINE"; Unit="COUNT"},
    @{Name="AGENTS_ON_CALL"; Unit="COUNT"},
    @{Name="AGENTS_STAFFED"; Unit="COUNT"},
    @{Name="AGENTS_AFTER_CONTACT_WORK"; Unit="COUNT"},
    @{Name="AGENTS_NON_PRODUCTIVE"; Unit="COUNT"},
    @{Name="CONTACTS_IN_QUEUE"; Unit="COUNT"},
    @{Name="OLDEST_CONTACT_AGE"; Unit="SECONDS"}
    @{Name="CONTACTS_SCHEDULED"; Unit="COUNT"}
  )
  return $currentMetrics
}


function New-HistoricMetrics() {
  $historicMetrics = @(
    @{Name="CONTACTS_HANDLED"; Unit="COUNT"},
    @{Name="CONTACTS_QUEUED"; Unit="COUNT"},
    @{Name="ABANDON_TIME"; Unit="SECONDS"},
    @{Name="CONTACTS_ABANDONED"; Unit="COUNT"},
    @{Name="QUEUE_ANSWER_TIME"; Unit="SECONDS"}
  )
  return $historicMetrics
}


function Get-Midnight() {
  $midnight = Get-Date -Hour 0 -Minute 00 -Second 00
  return $midnight
}

function Get-MetricData() {
  Param(
    [String]
    $ClientName,
    [String]
    $ProfileName
  )
  $queue_metadata = Get-Content "$ProfileName-instance-queues.json" | Out-String | ConvertFrom-Json

  $metrics = Get-Metrics -QueueMetadata $queue_metadata -ProfileName $ProfileName -ClientName $ClientName
}

Get-MetricData -ClientName "TradeUK" -ProfileName "connect-metrics"
