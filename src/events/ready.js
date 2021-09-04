module.exports = {
    name: "ready",
    execute(client) {
        console.log(`Successfully logged in as ${client.user.tag}`)
    }
}