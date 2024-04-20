// @birdy/collector topics
export enum CollectorTopic {
  // status topics
  COLLECTOR_SERVICE_ONLINE = 'birdy/collector/:collectorId/status/online',
  COLLECTOR_SERVICE_OFFLINE = 'birdy/collector/:collectorId/status/offline',
}

export type CollectorTopicDefinitions = {
  // status topic definitions
  [CollectorTopic.COLLECTOR_SERVICE_ONLINE]: { collectorId: string; now: Date }
  [CollectorTopic.COLLECTOR_SERVICE_OFFLINE]: { collectorId: string; now: Date }
}

// @birdy/recorder topics
export enum RecorderTopic {
  // status topic definitions
  RECORDER_SERVICE_ONLINE = 'birdy/recorder/:recorderId/status/online',
  RECORDER_SERVICE_OFFLINE = 'birdy/recorder/:recorderId/status/offline',

  // recording topic definitions
  RECORDER_SERVICE_RECORDING_CAPTURED = 'birdy/recorder/:recorderId/recording/:recordingId/captured',
  RECORDER_SERVICE_RECORDING_COLLECTED = 'birdy/recorder/:recorderId/recording/:recordingId/collected',
}

export type RecorderTopicDefinitions = {
  // status topics
  [RecorderTopic.RECORDER_SERVICE_ONLINE]: { recorderId: string; now: Date }
  [RecorderTopic.RECORDER_SERVICE_OFFLINE]: { recorderId: string; now: Date }

  // recording topics
  [RecorderTopic.RECORDER_SERVICE_RECORDING_CAPTURED]: {
    recorderId: string
    recordingId: string
    duration: number
  }
  [RecorderTopic.RECORDER_SERVICE_RECORDING_COLLECTED]: {
    recorderId: string
    recordingId: string
    duration: number
  }
}

// combined topics
export const Topic = { ...CollectorTopic, ...RecorderTopic }
export type Topic = typeof Topic
export type Topics = keyof TopicDefinitions
export type TopicDefinitions = CollectorTopicDefinitions & RecorderTopicDefinitions
