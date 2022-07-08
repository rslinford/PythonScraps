
import wordcloud_from_webpage as wfw

dir_name = 'google_news_year_202001'
print(f'Creating {dir_name}.gif')
wfw.make_gif(dir_name, f'{dir_name}.gif')
