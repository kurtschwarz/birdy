export interface Location {
  id: string
  latitude: number
  longitude: number
}

export interface Recording {
  id: string
  startTime: Date
  endTime: Date
  buffer: Buffer
  location: Location
}
