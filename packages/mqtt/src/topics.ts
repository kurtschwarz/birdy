// @birdy/collector topics
export enum CollectorTopic {
  COLLECTOR_SERVICE_ONLINE = 'birdy/collector/:collectorId/status/online',
  COLLECTOR_SERVICE_OFFLINE = 'birdy/collector/:collectorId/status/offline',
}

export type CollectorTopicDefinitions = {
  [CollectorTopic.COLLECTOR_SERVICE_ONLINE]: { collectorId: string, now: Date },
  [CollectorTopic.COLLECTOR_SERVICE_OFFLINE]: { collectorId: string, now: Date },
}

// @birdy/recorder topics
export enum RecorderTopic {
  RECORDER_SERVICE_ONLINE = 'birdy/recorder/:recorderId/status/online',
  RECORDER_SERVICE_OFFLINE = 'birdy/recorder/:recorderId/status/offline'
}

export type RecorderTopicDefinitions = {
  [RecorderTopic.RECORDER_SERVICE_ONLINE]: { recorderId: string, now: Date },
  [RecorderTopic.RECORDER_SERVICE_OFFLINE]: { recorderId: string, now: Date },
}

// combined topics
export const Topic = { ...CollectorTopic, ...RecorderTopic }
export type Topic = typeof Topic
export type Topics = keyof TopicDefinitions
export type TopicDefinitions = CollectorTopicDefinitions & RecorderTopicDefinitions
