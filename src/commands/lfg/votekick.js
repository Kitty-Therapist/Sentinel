const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const logs = "884314964532264960";

module.exports = {
    data: new SlashCommandBuilder()
    .setName('votekick')
    .setDescription('Vote kicks someone out of a voice channel')
    .addUserOption(option => option.setName('user').setDescription('The user to kick'))
    .addStringOption(option => option.setName('reason').setDescription('The reason behind the kick'))
    .addStringOption(option => option.setName('evidence').setDescription('Evidence for the vote; ex: imgur, youtube')),
    async execute(interaction, client) {
        const user = interaction.options.getUser('user');
        const reason = interaction.options.getString('reason');
        const evidence = interaction.options.getString('evidence');
        const reaction = "👍";

        if (!interaction.member.voice.channel) {
            interaction.reply({ content: `:warning: I was not able to process the vote-kick as you are not in the Voice Channel!`, ephemeral: true })
            return;
        } else { // Checks if the user starting the vote-kick if they're in a voice channel, if not, then it will tell them they need to be in one.
        if (user == interaction.user) {
            interaction.reply({ content: `:warning: Sorry, You cannot vote-kick yourself. If you'd like to leave a voice channel, feel free to click the disconnect button!`, ephemeral: true})
            return;
        } // Checks if the user is the same as the one starting the vote-kick, If so, then it will reproduce this error
        if(!reason) {
            interaction.reply({ content: `:warning: You are required to supply a reason of why you would like to votekick.`, ephemeral: true })
            return;
        } // Checks if they supplied a reason, if not, then it will produce this error
       
        if (!user.voice || user.voice.channel !== interaction.member.voice.channel) {
            interaction.reply({ content: `:warning: I was not able to start a votekick for ${user.tag}(\`${user.id}\`). It seems they are not in a voice channel, or in the same voice channel`, ephemeral: true })
            return;
        } // Checks if user is in the same voice channel or in a voice channel at all

        const embed = new MessageEmbed()
        .setTitle(`Pending Vote-Kick`)
        .setDescription(`${interaction.user.tag} (\`${interaction.user.id}\`) would like to kick ${user.tag} (\`${user.id}\`)`)
        .addField(`Reason`, `${reason}`)
        .setFooter(`If you agree with the kick, Please react down below!`)
        .setTimestamp(); // Embed for pending vote-kick vote

        interaction.reply({ embeds: [embed] })
        const message = await interaction.fetchReply();
        message.react(`${reaction}`);

        const filter = (reaction, user) => {
            return reaction.emoji.name === '👍' && user.id === message.author.id;
        }; // Filters the reaction for what it's looking for.

        message.awaitReactions({ filter, max: 5, time: 6000, errors: ['time'] }) // Collector for collecting reactions and starting the vote
        .then(collected => console.log(collected.size))
        .catch(collected => {
            if (collected.size < interaction.member.voice.channel.members) {
                const errEmbed = new MessageEmbed()
                .setTitle(`Vote-Kick Falied`)
                .setDescription(`Not enough users voted to vote-kick ${user.tag} (\`${user.id}\`) If you'd like to report this incident, please DM our Modmail at <@711678018573303809> with the information.`)
                .setTimestamp();
                interaction.editReply({ embeds: [errEmbed] });
            } // Lets the user know the vote-kick failed due to not enough members voting after 1 minute
            if (collected.size >=  interaction.member.voice.channel.members) {
                user.voice.disconnect("voted off");
                const emb = new MessageEmbed()
                .setTitle(`Vote-Kick Successful`)
                .setDescription(`${user.tag}(\`${user.id}\`) has been successfully vote-kicked! The incident has been reported to the moderation team for review as well.`)
                .setTimestamp();

                
                interaction.editReply({ embeds: [emb] });
            } // Executes the function of passing the vote and kicking the user out of the voice channel + logging
            console.log(`This is a test, ${collected.size} out of 5 was collected.`);
        }); // This is the basic collector for reactions for messages
    }
    }
}