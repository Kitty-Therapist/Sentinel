const { Client, Intents } = require('discord.js');
const { token } = require('./config.json');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_PRESENCES] });

client.once('ready', () => {
    client.user.setStatus('online')
    client.user.setActivity('VALORANT', {type:'WATCHING'})
    console.log('Sentinel is ready to go!');
});

client.login(token);
