from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

app = App.get_running_app()


class SpeakerDetails(Factory.BoxLayout):

    speaker = ObjectProperty(None)

    Builder.load_string('''
<SpeakerDetails>
    spacing: dp(13)
    orientation: 'vertical'
    padding: dp(4)
    AsyncImage:
        source: root.speaker['photo']
        allow_stretch: True
        keep_ratio: True
    Label
        text: root.speaker['name']
    Label
        text: root.speaker['info']
        valign: 'middle'
        size: self.texture_size
        text_size: self.width, None
        ''')

class ScreenTalks(Screen):
    '''
    Screen to display the talk schedule as per talks.json generated by
    pydelhiconf.network every time the app is started. A default
    talk schedule is provided.

    Screen looks like:

    -----------------------------------------
   |              ------------               |
   |              |          |               |
   |              |          |               |
   |              |          |               |
   |              |          |               |
   |              |          |               |
   |              ------------               |
   |              Speaker name               |
   |                                         |
   |About talk                               |
   |                                         |
   |About speaker                            |
   |Social links                             |
   |                                         | 
    -----------------------------------------

    '''

    talkid = StringProperty('')

    Builder.load_string('''
<ScreenTalks>
    size_hint_y: None
    height: dp(45)
    spacing: dp(9)
    name: 'ScreenTalks'
    BoxLayout
        orientation: 'vertical'
        padding: dp(4)
        Label:
            id: talk_title
            valign: 'middle'
            size: self.texture_size
            text_size: self.width, None
        Label:
            id: talk_desc
            valign: 'middle'
            size: self.texture_size
            text_size: self.width, None
    
<ImBut@ButtonBehavior+Image>
    text_size: self.size
    size_hint_y: None
        ''')

    def on_enter(self):
        from network import get_data
        talks = get_data('tracks', onsuccess=False)
        talk_info = talks['0.0.1'][0][self.talkid]
        self.ids.talk_title.text = talk_info['title']
        self.ids.talk_desc.text = talk_info['description']
        if 'speaker' in talk_info.keys():
            speaker = SpeakerDetails(speaker=talk_info['speaker'])
            speaker_social = talk_info['speaker']['social'][0]
            social_len = len(speaker_social)
            gl = GridLayout(cols=social_len,
                            size_hint_y=None,
                            padding='2dp',
                            spacing='2dp')
            import webbrowser
            for social_acc, social_link in speaker_social.items():
                imbt = Factory.ImBut()
                imbt.source = app.script_path + '/data/' + social_acc + '.png'
                imbt.on_release = lambda *x: webbrowser.open(social_link)
                gl.add_widget(imbt)

            self.add_widget(speaker)
            speaker.add_widget(gl)
      