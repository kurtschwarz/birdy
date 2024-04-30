from enum import Enum

class AnalyzerTopic(str, Enum):
    ANALYZER_SERVICE_ONLINE = "birdy/analyzer/status/online"
    ANALYZER_SERVICE_OFFLINE = "birdy/analyzer/status/offline"

class CollectorTopic(str, Enum):
    COLLECTOR_SERVICE_ONLINE = "birdy/collector/:collectorId/status/online"
    COLLECTOR_SERVICE_OFFLINE = "birdy/collector/:collectorId/status/offline"

class RecorderTopic(str, Enum):
    RECORDER_SERVICE_ONLINE = "birdy/recorder/:recorderId/status/online"
    RECORDER_SERVICE_OFFLINE = "birdy/recorder/:recorderId/status/offline"
    RECORDER_SERVICE_RECORDING_CAPTURED = "birdy/recorder/:recorderId/recording/:recordingId/captured"
    RECORDER_SERVICE_RECORDING_COLLECTED = "birdy/recorder/:recorderId/recording/:recordingId/collected"

class Topic(str, Enum):
    ANALYZER_SERVICE_ONLINE = "birdy/analyzer/status/online"
    ANALYZER_SERVICE_OFFLINE = "birdy/analyzer/status/offline"
    COLLECTOR_SERVICE_ONLINE = "birdy/collector/:collectorId/status/online"
    COLLECTOR_SERVICE_OFFLINE = "birdy/collector/:collectorId/status/offline"
    RECORDER_SERVICE_ONLINE = "birdy/recorder/:recorderId/status/online"
    RECORDER_SERVICE_OFFLINE = "birdy/recorder/:recorderId/status/offline"
    RECORDER_SERVICE_RECORDING_CAPTURED = "birdy/recorder/:recorderId/recording/:recordingId/captured"
    RECORDER_SERVICE_RECORDING_COLLECTED = "birdy/recorder/:recorderId/recording/:recordingId/collected"

