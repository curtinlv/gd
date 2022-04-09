module.exports = {
    apps: [{
        name: "jbot",
        version: "1.2.6",
        cwd: "..",
        script: "python3",
        args: "-m jbot",
        autorestart: true,
        watch: ["jbot"],
        ignore_watch: [
            "jbot/*.log",
            "jbot/*/*.log",
            "jbot/__pycache__/*",
            "jbot/bot/__pycache__/*",
            "jbot/diy/__pycache__/*",
            "jbot/requirements.txt",
            "jbot/ecosystem.config.js"
        ],
        watch_delay: 1500,
        interpreter: ""
    }]
}
