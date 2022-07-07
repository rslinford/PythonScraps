
import wordcloud_from_webpage as wfw

dir_name = 'googlenews_202110'
print(f'Creating {dir_name}.gif')
wfw.make_gif(dir_name, f'{dir_name}.gif')
