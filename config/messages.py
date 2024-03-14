from .callable_string import Formatable


class GlobalMessages(metaclass=Formatable):
    Morpheus = [
        "Remember...All I'm Offering Is The Truth. Nothing More.",
        "I Have Dreamed A Dream, But Now That Dream Is Gone From Me.",
        "What Was Said Was For You, And You Alone.",
        "A Sentinel For Every Man, Woman, And Child In Zion. That Sounds Exactly Like The Thinking Of A Machine To Me.",
        "We Are Still Here!",
        "Fate, It Seems, Is Not Without A Sense Of Irony.",
        "Remember...All I'm Offering Is The Truth. Nothing More.",
        "You Have To Understand, Most People Are Not Ready To Be Unplugged...",
        "You Think That's Air You're Breathing Now?",
        "Have You Ever Had A Dream, Neo, That You Were So Sure Was Real?",
        "What You Know You Can't Explain, But You Feel It. You've Felt It Your Entire Life. ",
        "Don't THINK You Are. KNOW You Are.",
        "I Can Only Show You The Door. You're The One That Has To Walk Through It.",
        "He's Beginning To Believe!",
        "You Have To Let It All Go, Neo - Fear, Doubt, And Disbelief. Free Your Mind!",
        "You Take The Red Pill - You Stay In Wonderland, And I Show You How Deep The Rabbit Hole Goes.",
        "I Can Only Show You The Door...",
        "What is real? How do you define real?",
    ]

    not_enough_perms = "You do not have permissions to use this."
    command_on_cooldown = "This command is on cooldown. Please try again in {time}."
    member_not_found = "{user} could not be found."
    error_happened = "`Errors happen Mr. Anderson`"
    embed_not_author = "You can't interact with this embed, because you are not author."

    channel_history_brief = "Get a channel history with date, content and author."
    channel_history_success = "Accessing history successful, file `{}_history.txt` created."
    channel_history_retrieving_messages = "Retrieving messages from channel {}."

    webhook_backup_brief = "Backups whole channel with webhook."
