"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const app = admin.initializeApp();
const serviceAccount = {
    "type": "service_account",
    "project_id": "league-of-coders-e5791",
    "private_key_id": "a7b6a6f4ac0e6cf88068b2b4bd46267b3959ee26",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC72LZT0CFzL7V5\ncz0SMPEcdLmQ6p2dqJOu3k1oRqMQxI/BKrz3qbxgcwSIxbCSrpJoLXJwBDU08Nst\n9LHMoatuETmgJ1fQV4sPUHF0c2VYTweQN4JRJXAthk+eWFy61xR4Le7Rj5MUDjWF\nmn5bd9KvnogW1nu9VWJSNInVsUfjtpeB85VR9NJVrhXXyWPo2lQ4hp8vEKp0gpTu\n9kHgmdVvU5koMhWXu6WsJWNYto4+q7h0W3t5t5wenuUaTDwibNZnSh+5lT8ANPQP\ndL7Z9wA/gO3hUudU2DguqxgIAQHJ3zth6oqgLWcs0xV9jPSxh/5s+0OBOkwNUq7p\nO+CjjMcjAgMBAAECggEAGk7bFjjnfmTXoydHDdWp5wTX+lpJccuqx0peB/UgoFgP\nFAwixALTHaTuJSOeu6RUX9/Bj7ufIgd7gt+qyRB5XGRwMCRicYzZLm9jPF5u+qOy\n2PlVOH0oTU/qtbAFaKt3s+8m69WSUTQ+PbRp7vCEotDumVg3o0giiYXPKgz2lwb9\nNjPYS7kKF8d3WNXxx9BmSZWAUgzm7INEwJzmmv/UqwxtDtb7fGnI5gQHpBR0/Kbe\nYhSPPe0S7m9cKQrgopAG9QGWMUO5oeGJTAYdUzVm9lBhhYb2WrJds5vqc0Dhi3rc\ncetqCGj6EEbrNWxX8llYDD0T1TWbBpxZynSMjA+y0QKBgQD1nZl5t5tveA2alfLI\n3ROoHhRtGRnxLl77VKCTkkbvPPq9V4x7hXwj7EvV0n7dEVUdWwCyXQnR1vRw//g7\ntLSx0KcsSUiILCvI3DjpUTiMInC377JFw1Fo0Z+cxGILd/xuMv2XQmQNfzv1AySn\n4eEGmB1fbT5oX/sYMQ4SZP6p8wKBgQDDydqMEpQ97cY2/7MxxvMHz2ypce3TvsNv\n/g4+yRbJ8jjytNL/7t/YVFhM4hpD04vgkExtMl6VOwJO8MFRCTj43jC7C/L9p7nQ\nKU6RO75oLxlygyaN6iUcF9DBOYPbhS48S1Y2r9QTQm69nzjxvaPquGZ1YjFZsWdd\nL2eVFAAKEQKBgQDOPPWARPIZmV8i7MIec7RruEZCjY9A+0T6GUd0YqF5hWSt1HO7\nzIw+xc2vz76C9mjX63AcVQ9Hyg0bTXQs/kG0BZY6E5b58M0bLgADuhWXZdvsNzMk\nbStQrqQtyKDjLG8kQWC6wB6vTqUTyP3gkkSXeuc/F8YNcnqvB5HfVDqajQKBgB/z\nZfXr5kNA9VLuYYjjBbAlmn8Ad6ZRgEVbeWmnmU91dvOsrK5VhjQgd5R8ZXriH/aS\ntdYwHR1PVu4Y/gNCdQiwAdXUemAIqhsdUpQC4uzPmuCEJJuONWYjQM73mtwNHOF8\nDeK4yOwnsDjDriBNKV3Zn+bSEmmnuM2NOeMrM2JxAoGACYKe8vTinyPo5KuqSpbs\n4q8fZgQvstTPinwde75TVi815hYbKYwlAD6ZaMnrxICLI4myNHfrp7fqqGbdzupR\n87kN6RN9U8JL6sAqZuyWhVCVlQ7/6XYm4Q3rUaTxKCCQnQQxuiW943qKtttmm6Ay\nfjZDfkwWYPiNqtzHmbLhgxs=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xuvos@league-of-coders-e5791.iam.gserviceaccount.com",
    "client_id": "104112526823823715347",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xuvos%40league-of-coders-e5791.iam.gserviceaccount.com"
};
/*
const app=admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://league-of-coders-e5791.firebaseio.com'
});
*/
const db = admin.firestore(app);
// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
function getDocument(database, collectionName, docName) {
    // [START get_document]
    const ret = database.collection(collectionName).doc(docName);
    return ret.get().then(doc => {
        if (!doc.exists) {
            console.log('No such document!');
        }
        else {
            return doc.data();
        }
    })
        .catch(err => {
        console.log('Error getting document', err);
    });
    // [END get_document]
}
exports.bigben = functions.https.onRequest((req, res) => {
    getDocument(db, "projects", "ROOT").then(x => {
        res.status(200).send(`<!doctype html>
		<head>
		  <title>Time</title>
		</head>
		<body>      
			${x.test}
		</body>
	  </html>`);
    });
});
//# sourceMappingURL=index.js.map
//# sourceMappingURL=index.js.map