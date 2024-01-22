# runway-wfas-takehome

Hi! I'm forrest. This was actually a pretty fun little takehome. It took me about 3.5 hours e2e, but I'm pretty happy with the result. I'm not sure if I'm supposed to be doing this, but I'm going to include a little bit of a writeup of my process and some of the decisions I made.

## Running all the things

First things first, let's get everything loaded up on your end.

To get the backend started, you just need to run the python script from the root directory of the project. It's a pretty simple script, so it doesn't need any special dependencies. It will run on port 8000 by default.

```bash
cd ./backend
python3 main.py
```

Once you've got that running, you can start the react app similarly. Just `cd` into the web directory, install dependencies, and run.

```bash
cd ./web
npm install
npm run start
```
