const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { execute } = require('./ping');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('votekick')
    .setDescription('Vote kicks someone out of a voice channel')
    .addUserOption(option => option.setName('user').setDescription('The user to kick'))
    .addStringOption(option => option.setName('reason').setDescription('The reason behind the kick')),
    async execute(interaction, client) {
        const user = interaction.options.getUser('user');
        const reason = interaction.options.getString('reason');
        const reaction = "👍";

        if (!interaction.member.voice) {
            interaction.reply({ content: `:warning: I was not able to process the vote-kick as you are not in the Voice Channel!`, ephemeral: true })
            return;
        } else {
        if (user == interaction.user) {
            interaction.reply({ content: `:warning: Sorry, You cannot vote-kick yourself. If you'd like to leave a voice channel, feel free to click the disconnect button!`, ephemeral: true})
        }
        if(!reason) {
            interaction.reply({ content: `:warning: You are required to supply a reason of why you would like to votekick`, ephemeral: true })
        }
       
        const embed = new MessageEmbed()
        .setTitle(`Pending Vote-Kick`)
        .setDescription(`${interaction.user.tag} (\`${interaction.user.id}\`) would like to kick ${user.tag} (\`${user.id}\`)`)
        .addField(`Reason`, `${reason}`)
        .setFooter(`If you agree with the kick, Please react down below!`)
        .setTimestamp();

        interaction.reply({ embeds: [embed] })
        const message = await interaction.fetchReply();
        message.react(`${reaction}`);
    }
    }
}