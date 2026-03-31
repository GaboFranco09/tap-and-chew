const admin = require('firebase-admin')
const path  = require('path')
require('dotenv').config()

const serviceAccount = require(
  path.resolve(process.env.FIREBASE_CREDENTIALS_PATH)
)

admin.initializeApp({
  credential:  admin.credential.cert(serviceAccount),
  databaseURL: process.env.FIREBASE_DATABASE_URL,
})

const db = admin.database()

module.exports = db