import * as events from 'node:events'

export class EventEmitter<Events extends Record<string, any>> {
  private _emitter = new events.EventEmitter()

  emit<EventName extends keyof Events & string>(
    eventName: EventName,
    ...eventArg: Events[EventName]
  ) {
    this._emitter.emit(eventName, ...(eventArg as []))
  }

  on<EventName extends keyof Events & string>(
    eventName: EventName,
    handler: (...eventArg: Events[EventName]) => void
  ) {
    this._emitter.on(eventName, handler as any)
  }

  off<EventName extends keyof Events & string>(
    eventName: EventName,
    handler: (...eventArg: Events[EventName]) => void
  ) {
    this._emitter.off(eventName, handler as any)
  }
}
