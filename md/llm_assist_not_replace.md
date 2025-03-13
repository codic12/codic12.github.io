---
title: Using LLMs to assist, not replace
date: 03/12/2025
summary: With examples.
---
In the modern tech world, many rising CS majors are scared they're going to be out of a job. As someone in high school surrounded by prospecting CS majors, I understand the sentiment. AI is scary good; if you're a junior developer, realistically in most scenarios a LLM can write better, more organized code than you for a fraction of the cost.

However, what a lot of people don't understand is that LLMs are just large mathematical functions; while they're perfectly capable of doing the menial grudge work of programming, they're not able to take a step back and architect a large project from scratch. 

Being a professional in a software field isn't nessecarily about being able to memorize every tidbit of syntax or know how to implement every specific algorithm; it's about understanding how things tie together at a larger level. And that's where human involvement is still very much needed. AI will never be able to replace the people making executive decisions; the risk of it blowing up is just far too high and doesn't make sense at all from a financial perspective.

And understanding how to use LLMs effectively isn't just a good skill to have in today's market; it's absolutely *essential* to have a future as a high-level junior software developer. (Obviously, if you're going into high-risk fields like finance or operating systems development, your job is a lot more secure because of how important that code functioning is to society).

<p style='text-align:center'><img src='https://victorzhou.com/media/neural-network-post/network3.png' width='500'></p>
<p style='text-align:center'>how a basic neural network works; it's just math!</p>

## Prompt engineering
A buzzword you've probably heard is **prompt engineering**. But what exactly is prompt engineering? Well, as [OpenAI defines it](https://platform.openai.com/docs/guides/prompt-engineering):

> The process of crafting prompts to get the right output from a model is called prompt engineering. You can improve output by giving the model precise instructions, examples, and necessary context information - like private or specialized information not included in the model's training data.

Basically - your goal is to provide the LLM enough input about the task and word your prompt in such a way that you get exactly what you want. In the case of producing code, this is especially important; you want to be *as specific as possible* with both technical and overall architectural choices. If you leave these choices up to the model, chances are you won't get what you wanted. Technical choices could include things like:

- languages
- frameworks
- algorithms

while architectural choices you might want to specify could be, for example:

- the general structure of a REST API (which endpoints do what and with which method).
- how authentication is handled
- how you want things to be stored in a database

Here's some examples we can try on ChatGPT:

### Bad prompt &#x274C

> Write me a chat application using rest apis and a web frontend.

```js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: '*',
        methods: ['GET', 'POST']
    }
});

app.use(cors());
app.use(express.json());

let messages = [];

app.get('/messages', (req, res) => {
    res.json(messages);
});

app.post('/messages', (req, res) => {
    const { user, text } = req.body;
    const message = { user, text, timestamp: new Date() };
    messages.push(message);
    io.emit('message', message);
    res.status(201).json(message);
});

io.on('connection', (socket) => {
    console.log('A user connected');
    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

server.listen(3000, () => {
    console.log('Server running on port 3000');
});

// Frontend code ommitted for brevity

module.exports = { app, server, frontend };
```

### Good prompt &#x2705
Prompt 1:

> Write me a server in JavaScript & Node.js, using the `express` framework.
> 
> Make tables in a SQLite database for `users` (containing username, password, ID, email, registration date), `channels` (containing IDs, and users joined) and `messages` (containing user IDs and channel IDs and the actual message text)
> with the following endpoints for a REST API:
> 
> * `GET /` => render index template (don't make this template itself yet)
> * `POST /login` => compare credentials with those in database `users` table, give one-time token if correct.
> * `POST /signup` => insert into `users` table, make sure those credentials don't exist already. remember to hash and salt the password.
> for the below also remember to check the authentication token in the header:
> * `PUT /channels/create` => create a new channel, it'll give you the ID as a result
> * `GET /channels` => get list of all channels
> * `GET /messages/{channel_id}` => return all messages from that channel ID
> * `PUT /channels/{id}` => send a message at that channel

Prompt 2:
> Now using the above API (input it again if you lost the model's context), write me a web application for chatting which lets you log in, sign up, and have different channels. You can use CSS frameworks but refrain from using anything that would be too heavy. Make it look modern, using material design, modern typography, smooth animations and blur effects, etc. I'd like it to also have a generally pastel colorscheme. The design aspect is very important; in addition to functionality make sure it seamlessly integrates with a user's day to day web experience. Also show me how to tie this back to the / endpoint in my original server.

