import { Client } from 'minio'

const minio = new Client({
  endPoint: process.env.MINIO_ENDPOINT,
  port: parseInt(process.env.MINIO_PORT),
  useSSL: false,
  accessKey: process.env.MINIO_ROOT_USER,
  secretKey: process.env.MINIO_ROOT_PASSWORD,
})

export const storeRecording = async (
  id: string,
  buffer: Buffer
): Promise<void> => {
  await minio.putObject(
    'birdy-recordings-unprocessed',
    `${id}.wav`,
    buffer
  )
}
