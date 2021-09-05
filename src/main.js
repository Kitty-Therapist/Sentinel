const { Client, Intents, Collection, Message } = require('discord.js');
const client  = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES ]});
const fs = require('fs');
const config = require('../config.json');

client.commands = new Collection();
const cmds = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
const events = fs.readdirSync('./events').filter(file => file.endsWith('.js'));

for (const file of cmds) {
    const command =  require(`./commands/${file}`);
    client.commands.set(command.data.name, command);
} // Command handler

for (const file of events) {
    const event = require(`./events/${file}`);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args, client));
    } else {
        client.on(event.name, (...args) => event.execute(...args, client));
    }
} // Event handler



client.login(config.token);