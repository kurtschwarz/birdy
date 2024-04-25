import fs from 'node:fs'

for (const path of fs.readdirSync('.', { recursive: true })) {
  if (/service_pb2_grpc.py$/.test(path)) {
    fs.writeFileSync(
      path,
      fs
        .readFileSync(path, 'utf-8')
        .replace(/^from\s(?!birdy_protos\.)(.*)\simport/gm, 'from birdy_protos.$1 import'),
      'utf-8',
    )
  }
}
