import { Client } from 'minio'

import { config } from '../../config.js'

const minio =
  config.storage === 's3'
    ? new Client({
        endPoint: new URL(config.storageS3Endpoint).hostname,
        port: parseInt(new URL(config.storageS3Endpoint)?.port || '0') || undefined,
        useSSL: new URL(config.storageS3Endpoint).protocol === 'https:',
        accessKey: config.storageS3AccessKey,
        secretKey: config.storageS3SecretKey,
      })
    : null

export const storeRecording = async (id: string, buffer: Buffer): Promise<void> => {
  await minio.putObject(config.storageS3Bucket, `${id}.wav`, buffer)
}
