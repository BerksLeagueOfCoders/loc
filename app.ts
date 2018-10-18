'use strict';

const express = require('express');
const path = require('path');
const fs = require('fs');
const passport=require('passport');
const app = express();
const api =  require('./api/index.js'); 
const cors = require('cors');
const GitHubStrategy = require('passport-github').Strategy;
const Users=require('./Userlib');
app.use(passport.initialize());
app.use(passport.session());
	
passport.use(new GitHubStrategy({
    clientID: "d0ac056a3928c7310baf",
    clientSecret: "4e1c897332b930a34723b6fa9437d885b64262a0",
    callbackURL: "https://leagueofcoders.net/auth/github/callback"
  },
  function(accessToken, refreshToken, profile, cb) {
    Users.findOrCreate({ githubId: profile.id }, function (err, user) {
      return cb(err, user);
    });
  }
));



app.get('/auth/github', 
  passport.authenticate('github'));

app.get('/auth/github/callback', 
  passport.authenticate('github', { failureRedirect: 'leagueofcoders.net/auth/' }),
  function(req, res) {
    // Successful authentication, redirect home.
    res.redirect('/');
  });

app.get("/crab", (req, res) =>{
  res.send("fdasfdsa dsa ");
});

app.use("/api", cors(), (req, res)=>{
	api.projectsGET().then((x)=> {
		res.json(x)
	});
});

app.post("/loginTest", (req, res)=>{
	console.log(req);
	res.status(200);
	res.send("OK");
});
// Use the built-in express middleware for serving static files from './www'
app.use("/", (req, res) =>{
	const p=path.join(__dirname, path.join("/www", req.path));
	console.log(p);
	fs.lstat(p, (err, stats) => {
		if(err!==null){
			res.status(404);
			res.send();
		} else{	
			if(stats.isDirectory()){
				res.sendFile(path.join(p, 'index.html'));
			} else if(stats.isFile()){
				res.sendFile(p);
			}
		}
	});
});






// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');	
});