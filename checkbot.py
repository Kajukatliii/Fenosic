# Telegram bot utils
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.ext.filters import Filters
from telegram.update import Update

# Gates utils
from gates.nsbc import *
from gates.ltal import *
from gates.sole import *
from gates.onlyo import *
from gates.rzrpay import *
from gates.sashio import *
from gates.gimkit import *
from gates.cowhub import *
from gates.troablue import *
from gates.braintree import *

# System utils
from gates.util import *
import speedtest
import requests
import random
import uuid
import time
import json
import sys
import re

PM_START_TEXT = """
Hello there, I'm Fenosic a cc checker bot \n use /help or click button given below to know my cmds.
"""
buttons = [
    [
        InlineKeyboardButton(
            text="▼Help", callback_data="help_back"
        ),
    ],

HELP_STRINGS = """
🔱Bot Status - Online ✓\n Click Below buttons to know more
"""

BOT_TOKEN = 				"5459458134:AAH-Sh_nC3QJF_4d2Q-1CBIaJJyyHLSVYe0"

CC_REGEX = 					"^[\d]{16}\|[\d]{2}\|[\d]{4}\|[\d]{3}$"

HELP_COMMAND = 				"help"
IDENT_COMMAND = 			"ident"
PING_COMMAND = 				"ping"

BRAINTREE_COMMAND = 		"bt"
COWORKHUB_COMMAND = 		"ch"
GIMKIT_COMMAND = 			"gk"
LTAL_COMMAND = 				"lt"
NSBC_COMMAND = 				"ns"
ONLYONE_COMMAND = 			"oo"
RAZORPAY_COMMAND = 			"rz"
SHASHIO_COMMAND = 			"si"
SOLE_COMMAND = 				"sl"
TANGAROA_COMMAND = 			"tr"

def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )

#will do tomorrow

class TelegramBot():

	def __init__(self, token):

		self.token = token
		self.updater = Updater(BOT_TOKEN, use_context=True)
		self.updater.dispatcher.add_handler(CommandHandler(HELP_COMMAND, self.help_page))
		self.updater.dispatcher.add_handler(CommandHandler(IDENT_COMMAND, self.get_ident))
		self.updater.dispatcher.add_handler(CommandHandler(PING_COMMAND, self.ping))

		self.updater.dispatcher.add_handler(CommandHandler(BRAINTREE_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(COWORKHUB_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(GIMKIT_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(LTAL_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(NSBC_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(ONLYONE_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(RAZORPAY_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(SHASHIO_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(SOLE_COMMAND, self.check_cc))
		self.updater.dispatcher.add_handler(CommandHandler(TANGAROA_COMMAND, self.check_cc))

		self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.help_page))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.command, self.help_page)) 
		self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.help_page))


	def help_page(self, update: Update, context: CallbackContext): 
		update.message.reply_text("==================\nCC Checker\n==================\n\n/help ->\t Print this page\n/ident ->\t Get an random identity\n---\n/{} ->\t Check card on BrainTree\n/{} ->\t Check card on CoworkerHub\n/{} ->\t Check card on GimKit\n/{} ->\t Check card on LetsTalkAboutLoss\n/{} ->\t Check card on NorthStarBadCharts\n/{} ->\t Check card on OnlyOne\n/{} ->\t Check card on RazorPay\n/{} ->\t Check card on SashiOnline\n/{} ->\t Check card on Sole\n/{} ->\t Check card on Tangaroablue\n-> CC parameter format : BIN|EXPM|EXPY|CVC".format(BRAINTREE_COMMAND, COWORKHUB_COMMAND, GIMKIT_COMMAND, LTAL_COMMAND, NSBC_COMMAND, ONLYONE_COMMAND, RAZORPAY_COMMAND, SHASHIO_COMMAND, SOLE_COMMAND, TANGAROA_COMMAND))


	def ping(self, update: Update, context: CallbackContext):

		try:

			st = speedtest.Speedtest()
			servers = []

			st.get_servers(servers)
			st.get_best_server()

			update.message.reply_text("Down : {} bits/s \nUp : {} bits/s ".format(st.download(), st.upload()))

		except Exception as E: 

			update.message.reply_text("Failed to get the ping (internal error)")
			print("Error raised : " + str(E))


	def check_cc(self, update: Update, context: CallbackContext):

		try:

			splitted_command = update.message["text"].split(" ")
			result_array = ["", ""]

			message = update.message.reply_text("Verifying arguments ...")

			if len(splitted_command) == 2 and len(re.findall(CC_REGEX, splitted_command[1])) == 1:

				message.edit_text("Checking your card ...")

				random_identity = get_random_identity()

				if random_identity:

					message.edit_text("Random identity generated")

					if splitted_command[0] == '/' + BRAINTREE_COMMAND: result = check_braintree(splitted_command[1], random_identity) 
					elif splitted_command[0] == '/' + COWORKHUB_COMMAND: result = check_coworkerhub(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + GIMKIT_COMMAND: result = check_gimkit(splitted_command[1], random_identity) 
					elif splitted_command[0] == '/' + LTAL_COMMAND: result = check_letstalkaboutloss(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + NSBC_COMMAND: result = check_northstarbadcharts(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + ONLYONE_COMMAND: result = check_onlyone(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + RAZORPAY_COMMAND: result = check_razorpay(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + SHASHIO_COMMAND: result = check_shashionline(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + SOLE_COMMAND: result = check_sole(splitted_command[1], random_identity)
					elif splitted_command[0] == '/' + TANGAROA_COMMAND: result = check_tangaroablue(splitted_command[1], random_identity)
					else:
						message.edit_text("Invalid command. Type /help for help page")
						return False

					if result != False:

						message.edit_text("[{}] Result : APPROVED".format(splitted_command[0].strip("/")))

					else: message.edit_text("[{}] Result : DECLINED".format(splitted_command[0].strip("/")))

				else: message.edit_text("Failed to get a random identity")

			else: message.edit_text("Invalid command. Type /help for help page")

		except Exception as E: 

			update.message.reply_text("Failed to check card (internal error)")
			print("Error raised : " + str(E))


	def get_ident(self, update: Update, context: CallbackContext):

		try:

			random_identity = get_random_identity()

			if random_identity:

				msg = "Name : {} {}\nGender : {}\nAge : {} ({})\n---\nStreet : {}\nCity : {}\nState : {}\nPostCode : {}\nEmail : {}\nPhones : {} | {}".format(random_identity["results"][0]["name"]["first"],
					random_identity["results"][0]["name"]["last"],
					random_identity["results"][0]["gender"],
					random_identity["results"][0]["dob"]["age"],
					random_identity["results"][0]["dob"]["date"],
					random_identity["results"][0]["location"]["street"],
					random_identity["results"][0]["location"]["city"],
					random_identity["results"][0]["location"]["state"],
					random_identity["results"][0]["location"]["postcode"],
					random_identity["results"][0]["email"],
					random_identity["results"][0]["phone"],
					random_identity["results"][0]["cell"])
				msg += "Photo URL : " + random_identity["results"][0]["picture"]["large"]

				update.message.reply_text("Here's your random identity : \n\n" + msg)

			else: update.message.reply_text("Failed to get a random identity")

		except Exception as E : 

			update.message.reply_text("Failed to get a random identity (internal error)")
			print("Error raised : " + str(E))


	def start(self): 

		self.updater.start_polling()

		print("Bot is running")


def main():

	bot_process = TelegramBot(BOT_TOKEN).start()

main()
