	$env:GOOGLE_APPLICATION_CREDENTIALS="keys\website-7d5de3f05db5.json"

Start-Process -FilePath "tsc" -ArgumentList "-w"

Start-Process -FilePath "nodemon" -ArgumentList "app.js"



