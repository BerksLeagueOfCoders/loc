"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const functions = require("firebase-functions");
// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
exports.bigben = functions.https.onRequest((req, res) => {
    const hours = (new Date().getHours() % 12) + 1; // London is UTC + 1hr;
    res.status(200).send(`<!doctype html>
    <head>
      <title>Time</title>
    </head>
    <body>
      ${'BA '.repeat(hours)}
    </body>
  </html>`);
});
//# sourceMappingURL=index.js.map
//# sourceMappingURL=index.js.map