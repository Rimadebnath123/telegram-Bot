from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from instra_sca import login_to_instagram, scrape_profiles, extract_email

TOKEN = "7804027360:AAHCYiG6xrObAzzbt_XUub14YIkMDXZrziE"

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Influencer Scraper Bot!\n"
                                     "Send a description of the type of influencers you're looking for.")

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a description to find influencers on Instagram.\n"
                                     "Example: 'Looking for fitness influencers.'")

# Handle description input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = update.message.text
    await update.message.reply_text(f"Searching for influencers based on your description: '{description}'...\n"
                                     "This might take a few minutes.")

    # Login and scrape
    username = "yourusername"
    password = "yourpassword"
    driver = login_to_instagram(username, password)

    if driver:
        profiles = scrape_profiles(driver, description)
        result = []
        for profile in profiles:
            email = extract_email(driver, profile)
            result.append(f"Profile: {profile}\nEmail: {email or 'No email found'}")

        driver.quit()

        # Send results to the user
        await update.message.reply_text("\n\n".join(result) if result else "No profiles found.")
    else:
        await update.message.reply_text("Failed to log in to Instagram. Please try again later.")

# Set up the bot
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    application.run_polling()
