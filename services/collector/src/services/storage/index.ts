import { Client } from 'minio'

import { config } from '../../config.js'

const minio = new Client({
  endPoint: config.minioEndpoint,
  port: config.minioPort,
  useSSL: false,
  accessKey: config.minioUser,
  secretKey: config.minioPassword,
})

export const storeRecording = async (
  id: string,
  buffer: Buffer
): Promise<void> => {
  await minio.putObject(
    config.storageBucketName,
    `${id}.wav`,
    buffer
  )
}
