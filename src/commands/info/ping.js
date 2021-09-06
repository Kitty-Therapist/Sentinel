const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('ping')
    .setDescription('Replies with the Discord API Latency'),
    async execute(interaction, client) {
        await interaction.reply(`Discord API: ${Math.round(client.ws.ping)}ms`)
    }
}