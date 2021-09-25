
class Templates:
	def __init__(self):
		self.regexExpressions()
		self.baseLinks()

	def regexExpressions(self):
		self.channel_id_on_searchpage = r'"browseId":"([a-zA-z0-9_-]+)"'
		self.channel_title_on_videospage = r'"channelId":"[a-zA-Z0-9_-]+","title":"(.*)","navigation'
		self.channel_subs = r'"subscriberCountText"[a-zA-Z:{".\s}]+([\d.]+)\s?([a-zA-Z]+)'
		self.video_id_on_videospage = r'"videoId":"([a-zA-Z0-9_-]+)","thumbnail"'
		self.decription_time_on_playing = r'"description":{"simpleText":"(.*)"},"lengthSeconds":"([\d,]+)"'
		self.email_on_aboutpage = r'"([a-zA-Z0-9_.+- ]+@[a-zA-Z0-9- ]+\.[a-zA-Z0-9.- ]+)"'

	def baseLinks(self):
		self.black_list = "FEwhat_to_watch"
		self.search_base = "https://www.youtube.com/results?search_query="
		self.channel_base = "https://www.youtube.com/channel/"
		self.video_base = "https://www.youtube.com/watch?v="