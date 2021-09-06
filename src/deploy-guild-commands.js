const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const { clientID, guildID, token } = require('../config.json');
const fs = require('fs');

const commands = [];

const rest = new REST({ version: '9' }).setToken(token); // Puts through a route using the v9 of the gateway with the token

// const cmds = fs.readdirSync('./commands').filter(file => file.endsWith('.js')); 

// // for (const file of cmds) {
// //     const command = require(`./commands/${file}`);
// //     commands.push(command.data.toJSON());
// // } // Reading Command Files

fs.readdirSync('./commands/').forEach(dir => {
    const cmds = fs.readdirSync(`./commands/${dir}/`).filter(file => file.endsWith(".js"));
    for (let file of cmds) {
        const cmd = require(`./commands/${dir}/${file}`)
        commands.push(cmd.data.toJSON());
    }
})

(async () => {
    try {
        await rest.put(
            Routes.applicationGuildCommands(clientID, guildID),
            { body: commands },
        );

        console.log(`Successfully deployed slash commands to guild.`);
    } catch (err) {
        console.error(err);
    }
})(); // Updating Commands to a specific server ID 

// Explanation: If you're pushing slash commands publically, it will take at least an hour for it to update to all the guilds it's in or just that specific guild, setting it to 1 guild ID and pushing to it will update it on the fly, best to use for testing servers before pushing it to the main
