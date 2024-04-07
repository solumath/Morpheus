from config.messages import GlobalMessages


class SystemMess(GlobalMessages):
    git_pull_brief = "Download latest changes from git"
    git_brief = "Git commands"
    shutdown_brief = "Turn off the bot"
    cogs_brief = "Print list of all cogs and their status"
    not_loaded = "Not loaded **{cogs}**"
    success_reload = "Reloaded successfully **{cogs}**"
    success_unload = "Unloaded successfully **{cogs}**"
    success_load = "Loaded successfully **{cogs}**"
    not_reloadable = "Extension(s) **{cogs}** can't be reloaded"
    cog_not_unloadable = "Extension(s) `{cogs}` can't be unloaded."
    embed_title = "Cogs information"
    embed_description = "```✅ Loaded ({loaded}) / ❌ Unloaded ({unloaded}) / 🔄 All ({all})```"
    override = "📄 Bold items are overrides of config.extension"
    morpheus_brief = "Information about Morpheus"
