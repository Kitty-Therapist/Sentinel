module.exports = {
    name: "ready",
    execute(client) {
        console.log(`Successfully logged in as ${client.user.tag}`)
        client.user.setPresence({
            status: "online",
            activities: [{
                name: "Valorant",
                type: "WATCHING"
            }]
        })
    }
}