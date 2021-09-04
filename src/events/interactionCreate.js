module.exports = {
    name: "interactionCreate",
    async execute(interaction, client, message) {
        if (!interaction.isCommand()) return;

        const command = client.commands.get(interaction.commandName);

        if (!command) return;

        try {
            await command.execute(interaction, client, message);
        } catch (err) {
            console.error(err)
        }
    }
}