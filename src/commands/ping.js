const { SlashCommandBuilder } = require('@discordjs/builders');
const { execute } = require('../events/ready');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('ping')
    .setDescription('Replies with the Discord API Latency'),
    async execute(interaction, client, message) {
        await interaction.reply(`Discord API: ${Math.round(client.ws.ping)}ms`)
    }
}