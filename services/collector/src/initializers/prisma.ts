import { PrismaClient } from '@birdy/data'

export const client = new PrismaClient({
  datasourceUrl: process.env.DATABASE_URL,
})
