import * as fs from 'node:fs'
import * as path from 'node:path'
import { once } from 'node:events'
import { spawn, ChildProcessWithoutNullStreams } from 'node:child_process'
import dayjs from 'dayjs'
import { backOff } from 'exponential-backoff'
import { nanoid } from 'nanoid'

import type { Recording } from '../../types/index.js'
import { EventEmitter } from '../../utils/index.js'

let ffmpeg: ChildProcessWithoutNullStreams = null

export const events = new EventEmitter<{
  recording: [Recording]
}>()

export const capture = async (options: { duration: number }): Promise<void> => {
  if (ffmpeg != null) {
    await stop()
  }

  ffmpeg = spawn(
    'ffmpeg',
    [
      '-hide_banner',
      '-loglevel',
      'info',
      '-f',
      'pulse',
      '-server',
      'host.docker.internal',
      '-i',
      'default',
      '-ac',
      '2',
      '-f',
      'segment',
      '-segment_time',
      `${options.duration}`,
      '-segment_list',
      'pipe:3',
      '-segment_list_type',
      'csv',
      '-strftime',
      '1',
      '%Y-%m-%dT%H-%M-%S.wav',
    ],
    {
      cwd: '/birdy/services/recorder/data/',
      stdio: [
        'pipe', // stdin
        'pipe', // stdout
        'pipe', // stderr
        'pipe', // pipe:3
      ],
      detached: true,
    },
  )

  ffmpeg.stdout.on('data', data => console.log(data.toString('utf-8')))
  ffmpeg.stderr.on('data', data => console.error(data.toString('utf-8')))

  ffmpeg.on('exit', async (code, signal) => {
    console.log(`ffmpeg exited with code ${code}, signal ${signal}`)
  })

  // this is called whenever the segment list is updated
  ffmpeg.stdio[3].on('data', async data => {
    console.log(data.toString('utf-8'))
    const [fileName, startOffset, endOffset] = data.toString('utf-8').trim().split(',')
    const filePath = path.join('/birdy/services/recorder/data/', fileName)
    const startTime = dayjs(fileName.replace('.wav', ''), 'YYYY-MM-DD[T]HH-MM-SS')
    const buffer = fs.readFileSync(filePath)

    events.emit('recording', {
      id: nanoid(),
      startTime: startTime.toDate(),
      endTime: startTime.add(parseFloat(endOffset) - parseFloat(startOffset), 'second').toDate(),
      buffer,
    })

    // delete the temporary recording file
    await backOff(async () => fs.unlinkSync(filePath), {
      delayFirstAttempt: false,
      numOfAttempts: 5,
      retry: async (error: Error & { code?: string }): Promise<boolean> => {
        return error?.code !== 'ENOENT'
      },
    })
  })

  await once(ffmpeg, 'spawn')
}

export const stop = async (): Promise<void> => {
  if (ffmpeg) {
    process.kill(-ffmpeg.pid)
  }
}
