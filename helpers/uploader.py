import time
from pyrogram import Client
from pyrogram.types import CallbackQuery
from helpers.display_progress import progress_for_pyrogram
import os
import re
from helpers.fs_utils import  get_media_info, get_cover


async def uploadAudio(c: Client,cb: CallbackQuery,merged_Audio_path,title,artist,duration,file_size,upload_mode:bool):
	try:
		sent_ = None

		# Temporary hack for uploading everything as audio irrespective
		# of the user settings.
		# TODO: Remove the setting completely from the bot.
		upload_mode = False

		audio_file_name = os.path.basename(merged_Audio_path)
		audio_file_name = re.sub(r"\s\s*", ".", audio_file_name)
		audio_file_name = re.sub(r"__*", ".", audio_file_name)

		file_caption = ".".join(audio_file_name.split(".")[:-1])

		if upload_mode is False:
			duration , artist, title = get_media_info(merged_Audio_path)
			thumb = get_cover(merged_Audio_path)
			c_time = time.time()
			if thumb:
				sent_ = await c.send_audio(
					chat_id=cb.message.chat.id,
					audio=merged_Audio_path,
					duration=duration,
					performer=artist,
					thumb=thumb,
					title= re.sub(r"\s*-\s*[pP]art.*", " ", title),
					caption=f"**{file_caption}**",
					file_name=audio_file_name,
					progress=progress_for_pyrogram,
					progress_args=(
						"Uploading file as audio",
						cb.message,
						c_time
					)
				)
			else:
				sent_ = await c.send_audio(
					chat_id=cb.message.chat.id,
					audio=merged_Audio_path,
					duration=duration,
					performer=artist,
					title= re.sub(r"\s*-\s*[pP]art.*", " ", title),
					caption=f"**{file_caption}**",
					file_name=audio_file_name,
					progress=progress_for_pyrogram,
					progress_args=(
						"Uploading file as audio",
						cb.message,
						c_time
					)
				)
		else:
			c_time = time.time()
			sent_ = await c.send_document(
				chat_id=cb.message.chat.id,
				document=merged_Audio_path,
				caption=f"** {merged_Audio_path.rsplit('/',1)[-1]}**",
				progress=progress_for_pyrogram,
				progress_args=(
					"Uploading file as document",
					cb.message,
					c_time
				)
			)
	except Exception as err:
		print(err)
		await cb.message.edit("Failed to upload")
