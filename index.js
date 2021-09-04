const { Client, Intents, Message } = require('discord.js');
const { token } = require('./config.json');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_PRESENCES], commandPrefix:">>" });

client.once('ready', () => {
    client.user.setStatus('online')
    client.user.setActivity('VALORANT', {type:'WATCHING'})
    console.log('Sentinel is ready to go!');
});

client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;

    const { commandName } = interaction;

    if (commandName === 'ping') {
        await interaction.reply("I'm still alive! :heart:");
    }
});

client.login(token);
