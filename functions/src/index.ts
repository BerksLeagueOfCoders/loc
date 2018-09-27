"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const app = admin.initializeApp();
const http = require('http');
const cors = require('cors')({origin: true});


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
       
    res.status(200).send(`<!DOCTYPE html>
		<head>
		  <title>Time</title>
		</head>
		<body>      
			${x.test}
		</body>
	  </html>`);
});
});

exports.projectsGET = functions.https.onRequest((request, response) => {
   cors(request, response, () => {
      getDocument(db, "projects", "ROOT").then(x => {
       
		response.status(200).send(x);
		});
   })
})
//# sourceMappingURL=index.js.map