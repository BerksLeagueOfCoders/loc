'use strict';
import * as utils from '/js/apiUtils.js';

// Copyright 2016, Google, Inc.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.



window.addEventListener("load", function(){
  // This is the host for the backend.
  // TODO: When running Firenotes locally, set to http://localhost:8081. Before
  // deploying the application to a live production environment, change to
  // https://backend-dot-<PROJECT_ID>.appspot.com as specified in the
  // backend's app.yaml file.

  // Obtain the following from the "Add Firebase to your web app" dialogue
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyDVOAFHSl4IE0eGGkW3kDtGFGpkvWlO-vs",
    authDomain: "website-218316.firebaseapp.com",
    databaseURL: "https://website-218316.firebaseio.com",
    projectId: "website-218316",
    storageBucket: "website-218316.appspot.com",
    messagingSenderId: "991927885446"
  };

  // This is passed into the backend to authenticate the user.
  var userIdToken = null;

  // Firebase log-in
  function configureFirebaseLogin() {

    firebase.initializeApp(config);


    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        var name = user.displayName;
        /* If the provider gives a display name, use the name for the
        personal welcome message. Otherwise, use the user's email. */
        var welcomeName = name ? name : user.email;

        user.getToken().then(function(idToken) {
          userIdToken = idToken;
			utils.setCookie("__session", idToken);
			window.location.replace("/");
        });

      }


    });

  }

  // Firebase log-in widget
  function configureFirebaseLoginWidget() {
    var uiConfig = {
      'signInSuccessUrl': '/',
      'signInOptions': [
        // Leave the lines as is for the providers you want to offer your users.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.GithubAuthProvider.PROVIDER_ID,

      ],
      // Terms of service url
      'tosUrl': '<your-tos-url>',
    };

    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start('#firebaseui-auth-container', uiConfig);
  }


  // [END gae_python_fetch_notes]

  // Sign out a user
function signOut(event) {
    event.preventDefault();
	utils.deleteCookie("__session");
    firebase.auth().signOut().then(function() {
      console.log("Sign out successful");
    }, function(error) {
      console.log(error);
    });
  }

  
  configureFirebaseLogin();
  configureFirebaseLoginWidget();

});
