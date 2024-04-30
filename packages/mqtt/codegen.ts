import * as fs from 'node:fs'

import * as topics from './src/topics.js'

export default (async () => {
  let python = 'from enum import Enum\n\n'

  for (const [topic, enums] of Object.entries(topics)) {
    python += `class ${topic}(str, Enum):\n`
    for (const [key, value] of Object.entries(enums)) {
      python += `    ${key} = "${value}"\n`
    }
    python += `\n`
  }

  fs.writeFileSync('./gen/py/birdy_mqtt/__init__.py', python)
})()
